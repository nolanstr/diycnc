"""Steel skeletons from stock: flat bar and tube cut to length, drilled from printed templates, and
clamped by threaded rod and bolts. (Plates can also be custom laser-cut outlines with slots, but the
frame no longer uses any.)

Every plate lies in a plane square to x, y or z. Its outline is a polygon in that plane (in
x, y, z order of the two in-plane axes), extruded through its thickness. Two kinds of joint,
both cut from the plates as they are placed, so a slot always matches its tab:

- through(a, b): a tab on plate a passes through plate b; b gets the slot.
- lap(a, b, axis): plates a and b cross along `axis`; each gets a slot half way, a from the
  +axis end and b from the -axis end (an egg-crate joint).

Holes, tapped holes (cut at the tap drill size) and lightening windows are cut in global
coordinates. write_dxf() slices each finished plate through its middle and writes its outline
for a laser-cutting service.
"""

import math

import Part
from FreeCAD import Vector

CLR = 0.25                     # slot clearance a side
T38, T14, T12 = 9.525, 6.35, 12.7
TAP = {'M5': (5.0, 4.2), 'M6': (6.0, 5.0), '3/8-16': (9.525, 7.94), '1/4-20': (6.35, 5.1), '1/2-13': (12.7, 10.7)}  # major, drill
AXES = {'x': 0, 'y': 1, 'z': 2}


def _vec(normal, c, p, q):
    if normal == 'z':
        return Vector(p, q, c)
    if normal == 'y':
        return Vector(p, c, q)
    return Vector(c, p, q)


def _unit(normal):
    return {'x': Vector(1, 0, 0), 'y': Vector(0, 1, 0), 'z': Vector(0, 0, 1)}[normal]


def tabbed(p0, q0, p1, q1, tabs=()):
    """Rectangle p0..p1 x q0..q1 with tabs: (side, a0, a1, depth), side 'q0' (the p-edge at q0),
    'p1', 'q1' or 'p0'; a0..a1 along that edge; depth outward."""
    by = {s: sorted([t for t in tabs if t[0] == s], key=lambda t: t[1]) for s in ('q0', 'p1', 'q1', 'p0')}
    pts = [(p0, q0)]
    for _, a0, a1, d in by['q0']:
        pts += [(a0, q0), (a0, q0 - d), (a1, q0 - d), (a1, q0)]
    pts.append((p1, q0))
    for _, a0, a1, d in by['p1']:
        pts += [(p1, a0), (p1 + d, a0), (p1 + d, a1), (p1, a1)]
    pts.append((p1, q1))
    for _, a0, a1, d in reversed(by['q1']):
        pts += [(a1, q1), (a1, q1 + d), (a0, q1 + d), (a0, q1)]
    pts.append((p0, q1))
    for _, a0, a1, d in reversed(by['p0']):
        pts += [(p0, a1), (p0 - d, a1), (p0 - d, a0), (p0, a0)]
    return pts


class Plate:
    def __init__(self, name, normal, c0, t, outline, note='', qty=1):
        self.name, self.normal, self.c0, self.t, self.note, self.qty = name, normal, c0, t, note, qty
        self.outline = outline
        self.taps = {}
        self.drills = []          # (p, q, major, drill): tapped holes, modeled at the major diameter
        self.holes = []           # (p, q, finished d, tap or None): for the drilling templates
        self.stock = None         # ('flat', t, width, length, length axis 'p' or 'q') for a flat bar
        pts = [_vec(normal, c0, p, q) for p, q in outline]
        face = Part.Face(Part.makePolygon(pts + pts[:1]))
        self.slab = face.extrude(_unit(normal) * t)          # outline only: what slots are cut against
        self.shape = self.slab.copy()

    # ---- cutting -------------------------------------------------------------
    def cut(self, shape):
        self.shape = self.shape.cut(shape)
        return self

    def hole(self, p, q, d, tap=None):
        """A hole square to the plate at in-plane (p, q); tap names a thread (modeled at its major
        diameter, drawn in the DXF at its tap drill)."""
        if tap:
            d, drill = TAP[tap]
            self.taps[tap] = self.taps.get(tap, 0) + 1
            self.drills.append((p, q, d, drill))
        self.holes.append((p, q, d, tap))
        n = _unit(self.normal)
        self.cut(Part.makeCylinder(d / 2, self.t + 2, _vec(self.normal, self.c0 - 1, p, q), n))
        return self

    def hexhole(self, p, q, af):
        """Hex hole (flats af) square to the plate, flats parallel to the p axis."""
        r = af / math.sqrt(3)
        pts = [_vec(self.normal, self.c0 - 1, p + r * math.cos(math.radians(60 * k)), q + r * math.sin(math.radians(60 * k)))
               for k in range(6)]
        self.cut(Part.Face(Part.makePolygon(pts + pts[:1])).extrude(_unit(self.normal) * (self.t + 2)))
        return self

    def window(self, p0, q0, p1, q1, r=6.0):
        """Rounded rectangular lightening window."""
        n = _unit(self.normal)
        a, b = _vec(self.normal, self.c0 - 1, p0, q0), _vec(self.normal, self.c0 + self.t + 1, p1, q1)
        box = Part.makeBox(abs(b.x - a.x), abs(b.y - a.y), abs(b.z - a.z),
                           Vector(min(a.x, b.x), min(a.y, b.y), min(a.z, b.z)))
        edges = [e for e in box.Edges if abs(abs((e.Vertexes[1].Point - e.Vertexes[0].Point).normalize().dot(n)) - 1) < 1e-6]
        try:
            box = box.makeFillet(r, edges)
        except Exception:
            pass
        self.cut(box)
        return self

    def truss(self, p0, p1, q0, q1, keep=(), post=20.0, bay=110.0, r=8.0):
        """Lighten a web: windows between p0..p1 and q0..q1 (in-plane), split into bays no longer than
        `bay` by posts `post` wide, with a post wherever the plate crosses another (at p in `keep`)."""
        stops = sorted([p0 - post / 2] + [k for k in keep if p0 < k < p1] + [p1 + post / 2])
        for a, b in zip(stops, stops[1:]):
            n = max(1, math.ceil((b - a - post) / bay))
            w = (b - a) / n
            for i in range(n):
                lo, hi = a + i * w + post / 2, a + (i + 1) * w - post / 2
                if hi - lo > 2 * r + 4 and q1 - q0 > 2 * r + 4:
                    self.window(lo, q0, hi, q1, r)
        return self

    def to_cut(self):
        """The plate as it is to be cut: tapped holes at their tap drill size."""
        shape = self.shape
        n = _unit(self.normal)
        for p, q, major, drill in self.drills:
            base = _vec(self.normal, self.c0 - 1, p, q)
            shape = shape.fuse(Part.makeCylinder(major / 2 + 0.01, self.t, base + n, n).common(self.slab))
            shape = shape.cut(Part.makeCylinder(drill / 2, self.t + 2, base, n))
        return shape.removeSplitter() if self.drills else shape

    @property
    def mass(self):
        return self.shape.Volume * 7.85e-6


def flat_bar(name, normal, c0, t, p0, q0, p1, q1, note=''):
    """A piece of stock flat bar (thickness t) lying in a plane square to `normal`, p0..p1 x q0..q1."""
    pl = Plate(name, normal, c0, t, tabbed(p0, q0, p1, q1), note=note)
    w, ln = sorted((p1 - p0, q1 - q0))
    pl.stock = ('flat', t, w, ln, 'p' if p1 - p0 >= q1 - q0 else 'q')
    return pl


class Tube:
    """A piece of stock rectangular tube along `axis` from a0 to a1, centered on (c1, c2) in the other two
    axes (in x, y, z order), outside w1 x w2 (same order), wall `wall`."""
    def __init__(self, name, axis, c1, c2, w1, w2, wall, a0, a1, note=''):
        self.name, self.axis, self.c1, self.c2, self.w1, self.w2, self.wall = name, axis, c1, c2, w1, w2, wall
        self.a0, self.a1, self.note = min(a0, a1), max(a0, a1), note
        self.env = self._box(w1, w2, 0.0, 1.5 * wall)
        self.shape = self.env.cut(self._box(w1 - 2 * wall, w2 - 2 * wall, 1.0, 0.5 * wall))
        self.holes = []           # (face axis, position along, position across, d, what)
        self.stock = ('tube', w1, w2, wall, self.a1 - self.a0)

    def _box(self, w1, w2, ext, r):
        o = [0.0, 0.0, 0.0]
        sz = [0.0, 0.0, 0.0]
        i = AXES[self.axis]
        others = [k for k in range(3) if k != i]
        o[i], sz[i] = self.a0 - ext, self.a1 - self.a0 + 2 * ext
        for k, c, w in zip(others, (self.c1, self.c2), (w1, w2)):
            o[k], sz[k] = c - w / 2, w
        b = Part.makeBox(*sz, Vector(*o))
        n = Vector(*[1.0 if k == i else 0.0 for k in range(3)])
        edges = [e for e in b.Edges if abs(abs((e.Vertexes[1].Point - e.Vertexes[0].Point).normalize().dot(n)) - 1) < 1e-6]
        try:
            return b.makeFillet(r, edges)
        except Exception:
            return b

    def drill(self, face, along, across, d, what='', both=True):
        """A hole through the wall(s) square to `face` ('x', 'y' or 'z', one of the two across the tube) at
        `along` (on the tube's axis) and `across` (on the remaining axis), through both walls or the near one."""
        i, f = AXES[self.axis], AXES[face]
        k = 3 - i - f
        p0 = [0.0, 0.0, 0.0]
        p0[i], p0[k] = along, across
        c_f = self.c1 if f == [m for m in range(3) if m != i][0] else self.c2
        half = (self.w1 if f == [m for m in range(3) if m != i][0] else self.w2) / 2
        p0[f] = c_f - half - 1
        n = Vector(*[1.0 if m == f else 0.0 for m in range(3)])
        length = 2 * half + 2 if both else self.wall + 2
        self.shape = self.shape.cut(Part.makeCylinder(d / 2, length, Vector(*p0), n))
        others = [m for m in range(3) if m != i]
        lo = (self.c2 - self.w2 / 2) if f == others[0] else (self.c1 - self.w1 / 2)   # the face's edge, across
        self.holes.append((face, along - self.a0, across - lo, d, what, both))
        return self

    @property
    def mass(self):
        return self.shape.Volume * 7.85e-6


def _inflate(bb, d, keep=None):
    """Box from a BoundBox grown by d a side (not along axis index `keep`, which grows by 1)."""
    lo = [bb.XMin, bb.YMin, bb.ZMin]
    hi = [bb.XMax, bb.YMax, bb.ZMax]
    for i in range(3):
        g = 1.0 if i == keep else d
        lo[i] -= g
        hi[i] += g
    return Part.makeBox(hi[0] - lo[0], hi[1] - lo[1], hi[2] - lo[2], Vector(*lo))


def through(a, b, clr=CLR):
    """Plate a's tabs pass through plate b: cut matching slots in b."""
    r = a.shape.common(b.slab)
    if r.Volume < 1.0:
        raise ValueError(f'{a.name} does not pass through {b.name}')
    for s in r.Solids:
        b.cut(_inflate(s.BoundBox, clr, keep=AXES[b.normal]))


def lap(a, b, axis, clr=CLR):
    """Plates a and b cross along axis ('x', 'y' or 'z'): half-depth slots, a from the +axis end."""
    r = a.slab.common(b.slab)
    if r.Volume < 1.0:
        raise ValueError(f'{a.name} does not cross {b.name}')
    i = AXES[axis]
    bb = r.BoundBox
    lo, hi = [bb.XMin, bb.YMin, bb.ZMin], [bb.XMax, bb.YMax, bb.ZMax]
    mid = (lo[i] + hi[i]) / 2
    for plate, (s0, s1) in ((a, (mid, hi[i] + 50.0)), (b, (lo[i] - 50.0, mid))):
        l2, h2 = list(lo), list(hi)
        for j in range(3):
            if j != i:
                l2[j] -= clr
                h2[j] += clr
        l2[i], h2[i] = s0, s1
        plate.cut(Part.makeBox(h2[0] - l2[0], h2[1] - l2[1], h2[2] - l2[2], Vector(*l2)))


# ---- DXF ---------------------------------------------------------------------
def _ents(shape, normal, c, drills=()):
    """DXF entities of the plate's section at depth c, in its in-plane (p, q) coordinates."""
    n = _unit(normal)
    pq = (lambda v: (v.y, v.z)) if normal == 'x' else (lambda v: (v.x, v.z)) if normal == 'y' else (lambda v: (v.x, v.y))
    wires = shape.slice(n, c)
    allp = [pq(v.Point) for w in wires for v in w.Vertexes]
    op, oq = min(p for p, _ in allp), min(q for _, q in allp)
    ents = []
    for w in wires:
        for e in w.Edges:
            cv = e.Curve
            if isinstance(cv, Part.Circle):
                cp, cq = pq(cv.Center)
                cp, cq = cp - op, cq - oq
                if e.isClosed():
                    r = cv.Radius
                    for dp, dq, major, drill in drills:
                        if abs(dp - op - cp) < 0.05 and abs(dq - oq - cq) < 0.05 and abs(2 * r - major) < 0.05:
                            r = drill / 2
                    ents.append(f'0\nCIRCLE\n8\n0\n10\n{cp:.4f}\n20\n{cq:.4f}\n30\n0\n40\n{r:.4f}')
                    continue
                a0, a1 = (math.degrees(math.atan2(pq(v.Point)[1] - oq - cq, pq(v.Point)[0] - op - cp)) for v in e.Vertexes[:2])
                # the (p, q) frame is right-handed about +n for z and x, left-handed for y
                ccw = cv.Axis.dot(n) > 0
                if normal == 'y':
                    ccw = not ccw
                if not ccw:
                    a0, a1 = a1, a0
                ents.append(f'0\nARC\n8\n0\n10\n{cp:.4f}\n20\n{cq:.4f}\n30\n0\n40\n{cv.Radius:.4f}\n50\n{a0:.4f}\n51\n{a1:.4f}')
                continue
            pts = [v.Point for v in e.Vertexes] if isinstance(cv, (Part.Line, Part.LineSegment)) else e.discretize(24)
            for a, b in zip(pts, pts[1:]):
                (ap, aq), (bp, bq) = pq(a), pq(b)
                ents.append(f'0\nLINE\n8\n0\n10\n{ap - op:.4f}\n20\n{aq - oq:.4f}\n30\n0\n'
                            f'11\n{bp - op:.4f}\n21\n{bq - oq:.4f}\n31\n0')
    size = (max(p for p, _ in allp) - op, max(q for _, q in allp) - oq)
    return ents, size


def write_dxf(plate, path):
    """Write the plate's outline (R12, mm). Returns its size (mm)."""
    ents, size = _ents(plate.shape, plate.normal, plate.c0 + plate.t / 2, plate.drills)
    with open(path, 'w') as fh:
        fh.write('0\nSECTION\n2\nHEADER\n9\n$INSUNITS\n70\n4\n0\nENDSEC\n0\nSECTION\n2\nENTITIES\n'
                 + '\n'.join(ents) + '\n0\nENDSEC\n0\nEOF\n')
    return size


DRILL = {4.2: 'M5 tap drill (4.2 mm), tap M5', 5.0: 'M6 tap drill (5 mm), tap M6',
         7.94: '5/16 in, tap 3/8-16', 10.7: '27/64 in, tap 1/2-13', 6.5: '1/4 in', 6.6: '17/64 in',
         7.0: '9/32 in', 9.6: '3/8 in', 10.5: '13/32 in', 12.7: '1/2 in', 13.5: '17/32 in', 14.0: '9/16 in',
         14.3: '9/16 in'}


def drill_name(d, tap=None):
    if tap:
        d = TAP[tap][1]
    return DRILL.get(round(d, 2), f'{d:.1f} mm')


def thickness_name(t):
    return {T38: '3/8 in', T14: '1/4 in', T12: '1/2 in'}.get(t, f'{t:.2f} mm')


def inch(mm):
    """A stock size in inches: 50.8 -> '2', 63.5 -> '2-1/2', 9.525 -> '3/8'."""
    v = mm / 25.4
    whole = int(v + 1e-6)
    frac = round((v - whole) * 16)
    if frac == 16:
        whole, frac = whole + 1, 0
    if not frac:
        return f'{whole}'
    num, den = frac, 16
    while num % 2 == 0:
        num, den = num // 2, den // 2
    return f'{whole}-{num}/{den}' if whole else f'{num}/{den}'
