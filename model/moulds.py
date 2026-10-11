"""Printed mould parts for the epoxy-granite castings, how they fix to the mould boards, and STL
export split for a small printer.

The mould boxes are melamine board (mouldbox.py): flat, cheap, and the reference for the castings'
important faces. Everything with shape is printed:
  core    pocket cores: thin closed-top shells, left in the casting; a post on each bolts to a bridge
  former  recesses in a cast face (gutters, trough, motor relief, gasket grooves): pulled after curing
  filler  rounded corners and the upright toe: pulled after curing, reused
  plug    removable pocket formers and locators (tie-rod nut pockets, tube ends)
  liner   stays in the casting (drain liner)
  kit     brackets, saddles, holders, bushings: they hold the boards and the steel, reused

How the pieces join, so they only go together one way and need no glue:
  - A piece bolts to its board from the board's far side: an M4 bolt (M3 on thin pieces) through a
    hole in the board into a captive nut. The nut drops into a pocket in the face against the board
    and slides sideways to the bolt ("bayonet"), so no opening shows on a cast face.
  - Pieces too thin for a nut (gasket-groove beads, shallow formers) have 3 mm pins that push into
    1/8 in holes; the casting's own pressure holds them on the board.
  - Pieces cut to fit the bed have a peg and socket on the cut face. Cores have a bulkhead either
    side of the cut, bolted with two M3.
  - Slip fits are 0.15 mm a side.
"""

import csv
import math
import os

import Part
from FreeCAD import Rotation, Vector

BED = 170.0       # Bambu A1 mini: 180 mm cube, less a margin
WALL = 1.6        # core shell wall: four 0.4 mm lines (the sand inside holds the shape)
BULKHEAD = 2.4    # core walls either side of a cut, bolted together
PETG = 1.27       # g/cm^3
FIT = 0.15        # slip fit, a side
MIN_WALL = 1.2    # least plastic around a nut, a hole or a peg
BOARD = 18.0      # melamine thickness (build_cnc sets it from P['mould_board'])
BOARD_MAX = 19.0  # bolt lengths still go through the nut on a board this thick
# clearance hole, nut across flats, nut thickness, plastic between the board and the nut
HW = {'M3': dict(hole=3.4, af=5.5, t=2.4, skin=2.0),
      'M4': dict(hole=4.5, af=7.0, t=3.2, skin=2.5)}
LENGTHS = (6, 8, 10, 12, 16, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80)
PIN_D, PIN_L = 3.0, 6.0     # pins into 1/8 in (3.2 mm) holes
PEG_D, PEG_H = 5.0, 4.0
POST = 12.0       # core posts, square
LIP = 8.0         # core bulkheads: a frame this wide
DRILL = {'M3': 3.4, 'M4': 4.5, 'pin': 3.2}


def bolt_length(grip):
    """Shortest stock length at least `grip` long."""
    return next(n for n in LENGTHS if n >= grip - 1e-6)


def nut_bolt(size):
    """Bolt length through a board into a captive nut, and how deep its hole goes into the piece."""
    hw = HW[size]
    n = bolt_length(BOARD_MAX + hw['skin'] + hw['t'] + 2 * FIT + 0.5)
    return n, n - BOARD + 1.0


class Fix:
    """Something through a mould board. kind: 'bolt' (into a captive nut in a printed piece, or a
    bracket), 'pin', or 'hole' (insert screws, core rods, bolts into cast-in nuts, hole-saw holes).
    p is on the board face the thing sits against; n points into the board."""

    def __init__(self, kind, p, n, d, what, size=None, length=None, qty=1):
        self.kind, self.p, self.n, self.d, self.what = kind, Vector(p), Vector(n), d, what
        self.size, self.length, self.qty = size, length, qty


# --------------------------------------------------------------------------
# Geometry helpers
# --------------------------------------------------------------------------
def unit(v):
    v = Vector(v)
    v.normalize()
    return v


def perp(n):
    """Some unit vector square to n."""
    a = min((Vector(1, 0, 0), Vector(0, 1, 0), Vector(0, 0, 1)), key=lambda e: abs(e.dot(n)))
    return unit(a - n * a.dot(n))


def frame(n, s):
    n = unit(n)
    s = Vector(s)
    s = unit(s - n * s.dot(n))
    return n, s, n.cross(s)


def poly(pts):
    return Part.Face(Part.makePolygon(list(pts) + [pts[0]]))


def hexagon(c, w, s, b, af, h):
    """Hex prism from c along w (length h), flats parallel to s."""
    r = af / math.sqrt(3)
    return poly([c + s * (r * math.cos(math.pi / 3 * k)) + b * (r * math.sin(math.pi / 3 * k)) for k in range(6)]).extrude(w * h)


def bar(c, w, s, b, length, width, h):
    """Box from c: `length` along s, `width` centred across b, `h` along w."""
    o = c - b * (width / 2)
    return poly([o, o + s * length, o + s * length + b * width, o + b * width]).extrude(w * h)


def block(c, a, b, n, la, lb, ln):
    """Box with a corner at c and edges la, lb, ln along the unit vectors a, b, n."""
    return poly([c, c + a * la, c + a * la + b * lb, c + b * lb]).extrude(n * ln)


def halfspace(p, n, size=4000.0):
    n = unit(n)
    s = perp(n)
    return bar(p - s * (size / 2), n, s, n.cross(s), size, size, size)


def prism(poly_xy, z0, z1):
    face = Part.Face(Part.makePolygon([Vector(x, y, z0) for x, y in poly_xy + poly_xy[:1]]))
    return face.extrude(Vector(0, 0, z1 - z0))


def plane_faces(shape, p0, n):
    """The planar faces of shape lying in the plane through p0 with normal n."""
    out = []
    for f in shape.Faces:
        if not isinstance(f.Surface, Part.Plane) or abs(abs(f.Surface.Axis.dot(n)) - 1) > 1e-6:
            continue
        if abs((f.Vertexes[0].Point - p0).dot(n)) < 0.05:
            out.append(f)
    return out


# --------------------------------------------------------------------------
# Fixings
# --------------------------------------------------------------------------
def nut_trap(p, n, s, size, mode='bayonet', grow=0.0, run=14.0, depth=None):
    """Cutter for a bolt that comes through the board into a captive nut. p is on the face against
    the board, n points out of the piece into the board, s is the way the nut slides.
    mode 'bayonet': the nut drops into a pocket in that face and slides along s to the bolt;
    'side': the slot runs out along s through a side face (into air, a core's inside or a board).
    grow > 0 gives the keep-out (the cutter plus the plastic it needs around it)."""
    hw = HW[size]
    n, s, b = frame(n, s)
    w = -n
    af, t = hw['af'] + 2 * (FIT + grow), hw['t'] + 2 * (FIT + grow)
    z0 = hw['skin'] - grow
    depth = nut_bolt(size)[1] if depth is None else depth
    c = p + w * z0
    out = [Part.makeCylinder(hw['hole'] / 2 + grow, depth + grow + 0.5, p + n * 0.5, w), hexagon(c, w, s, b, af, t)]
    if mode == 'bayonet':
        reach = hw['af'] + 3.0
        out += [bar(c, w, s, b, reach, af, t), hexagon(p + s * reach + n * 0.5, w, s, b, af, z0 + t + 0.5)]
    elif mode == 'side':
        out.append(bar(c, w, s, b, run, af, t))
    return out[0].multiFuse(out[1:])


def nut_recess(p, w, size, depth=None):
    """Hex pocket for a nut, from the outside face p inward along w (the bolt pulls it in)."""
    hw = HW[size]
    s = perp(w)
    return hexagon(p - w * 0.5, w, s, w.cross(s), hw['af'] + 2 * FIT, (depth or hw['t'] + 0.3) + 0.5)


def pin(p, n):
    n = unit(n)
    body = Part.makeCylinder(PIN_D / 2, PIN_L - 0.6 + 0.4, p - n * 0.4, n)
    return body.fuse(Part.makeCone(PIN_D / 2, PIN_D / 2 - 0.6, 0.6, p + n * (PIN_L - 0.6), n))


def fits(piece, keep, p, n):
    """True if the keep-out lies inside the piece, or beyond its face against the board."""
    return keep.cut(piece).cut(halfspace(p, n)).Volume < 0.5


def fasten(piece, p0, n, count=1, sizes=('M4', 'M3', 'pin'), what='', avoid=()):
    """Fix a printed piece to the board it sits against (the plane through p0, n out of the piece):
    `count` bolts into captive nuts, or pins where it is too thin. avoid: [(point, radius)] other
    holes in that board to keep clear of. Returns (piece, [Fix])."""
    n = unit(n)
    faces = plane_faces(piece, p0, n)
    if not faces:
        return piece, []
    area = sum(f.Area for f in faces)
    c = sum((f.CenterOfMass * f.Area for f in faces), Vector()) * (1.0 / area)
    pts = [v.Point for f in faces for v in f.Vertexes]
    e1 = perp(n)
    best = max((math.radians(a) for a in range(0, 180, 15)),
               key=lambda a: _spread(pts, n, e1, a))
    e1 = unit(e1 * math.cos(best) + n.cross(e1) * math.sin(best))
    e2 = n.cross(e1)
    us = [(q - c).dot(e1) for q in pts]
    vs = [(q - c).dot(e2) for q in pts]
    bb = piece.BoundBox
    thick = max((Vector(x, y, z) - c).dot(-n) for x in (bb.XMin, bb.XMax) for y in (bb.YMin, bb.YMax)
                for z in (bb.ZMin, bb.ZMax))
    sizes = [z for z in sizes if z == 'pin' or thick >= nut_bolt(z)[1] + MIN_WALL]
    fixes, used = [], []
    want = count
    for size in sizes:
        k = want if size != 'pin' else max(want, 2)
        span = max(us) - min(us)
        targets = [min(us) + span * (i + 0.5) / k for i in range(k)]
        found = []
        for u in targets:
            q = _place(piece, c, e1, e2, n, u, (min(vs) + max(vs)) / 2, size, used, faces, max(vs) - min(vs), avoid)
            if q is not None:
                found.append(q)
                used.append(q[0])
        if len(found) == k or (found and size == 'pin'):
            for q, s in found:
                if size == 'pin':
                    piece = piece.fuse(pin(q, n))
                    fixes.append(Fix('pin', q, n, DRILL['pin'], what or 'pin'))
                else:
                    piece = piece.cut(nut_trap(q, n, s, size))
                    fixes.append(Fix('bolt', q, n, DRILL[size], what, size, nut_bolt(size)[0]))
            return piece.removeSplitter(), fixes
        for q, _ in found:
            used.remove(q)
    return piece, fixes


def _spread(pts, n, e1, a):
    e = e1 * math.cos(a) + n.cross(e1) * math.sin(a)
    d = [q.dot(e) for q in pts]
    return max(d) - min(d)


def _place(piece, c, e1, e2, n, u, v, size, used, faces, width, avoid=()):
    """Nearest spot to (u, v) on the face where the fixing fits. Quick checks first (its footprint
    is on the face, the plastic is deep enough under it); the solid check only runs when they pass."""
    w = -n
    for q in _candidates(faces, c, e1, e2, u, v):
        if any((q - o).Length < 16.0 for o in used) or any((q - a).Length < r + 6.0 for a, r in avoid):
            continue
        if size == 'pin':
            r = PIN_D / 2 + 0.2               # a pin stands on the face: it needs only its own footprint
            if not _on(faces, [q + d * r for d in (e1, -e1, e2, -e2)] + [q]):
                continue
            if not piece.isInside(q + w * 1.5, 0.01, True):
                continue
            keep = Part.makeCylinder(r, 1.5 + 0.5, q + n * 0.5, -n)
            if fits(piece, keep, q, n):
                return q, None
            continue
        hw = HW[size]
        af = hw['af'] + 2 * (FIT + MIN_WALL)
        rr = af / math.sqrt(3)
        reach = hw['af'] + 3.0
        deep = hw['skin'] + hw['t'] + 2 * FIT + MIN_WALL
        if not piece.isInside(q + w * (nut_bolt(size)[1] + MIN_WALL), 0.01, True):
            continue
        toward = c - q
        for s in sorted((e1, -e1, e2, -e2), key=lambda s_: -s_.dot(toward)):
            b = n.cross(s)
            foot = [q, q - s * rr, q + s * (reach + rr)] + [q + s * t + b * (e * af / 2) for t in (0, reach) for e in (-1, 1)]
            if not _on(faces, foot) or not all(piece.isInside(f + w * deep, 0.01, True) for f in foot):
                continue
            if fits(piece, nut_trap(q, n, s, size, grow=MIN_WALL), q, n):
                return q, s
    return None


def _candidates(faces, c, e1, e2, u, v, step=2.5, reach=24.0):
    """Points on the faces near (u, v), nearest first (along the face before across it)."""
    pts = []
    for i in range(-int(reach / step), int(reach / step) + 1):
        for j in range(-int(reach / step), int(reach / step) + 1):
            q = c + e1 * (u + i * step) + e2 * (v + j * step)
            if _on(faces, [q]):
                pts.append((abs(i) + 1.5 * abs(j), q))
    return [q for _, q in sorted(pts, key=lambda t: t[0])]


def _on(faces, pts):
    """All the points lie on one of the faces."""
    for p in pts:
        if not any(f.isPartOfDomain(*f.Surface.parameter(p)) for f in faces):
            return False
    return True


# --------------------------------------------------------------------------
# Cutting to the bed
# --------------------------------------------------------------------------
def split(shape, lim=BED):
    """Cut a solid into equal slabs along its longest axes until every piece fits the bed.
    Returns [(piece, [(axis, coordinate), ...])] with the cut faces each piece has."""
    bb = shape.BoundBox
    lens = (bb.XLength, bb.YLength, bb.ZLength)
    ax = max(range(3), key=lambda i: lens[i])
    if lens[ax] <= lim:
        return [(shape, [])]
    n = math.ceil(lens[ax] / lim)
    lo = (bb.XMin, bb.YMin, bb.ZMin)[ax]
    step = lens[ax] / n
    out = []
    for k in range(n):
        o = [bb.XMin - 1, bb.YMin - 1, bb.ZMin - 1]
        size = [bb.XLength + 2, bb.YLength + 2, bb.ZLength + 2]
        o[ax], size[ax] = lo + k * step, step
        cuts = ([(ax, lo + k * step)] if k else []) + ([(ax, lo + (k + 1) * step)] if k < n - 1 else [])
        for s in shape.common(Part.makeBox(*size, Vector(*o))).Solids:
            if s.Volume > 1.0:
                out += [(p, cuts + c) for p, c in split(s, lim)]
    return out


def split_bed(shape, lim=BED):
    return [p for p, _ in split(shape, lim)]


def keyed(pieces):
    """A peg on one side of each cut face and a socket on the other, where the section has room.
    pieces: [(piece, cuts)] from split(). Returns the pieces."""
    shapes = [p for p, _ in pieces]
    axes = (Vector(1, 0, 0), Vector(0, 1, 0), Vector(0, 0, 1))
    for i, (_, ci) in enumerate(pieces):
        for ax, coord in ci:
            a = axes[ax]
            lo = shapes[i].BoundBox
            if abs((lo.XMax, lo.YMax, lo.ZMax)[ax] - coord) > 0.05:
                continue                                  # i is above this cut; its partner pegs into it
            for j, (_, cj) in enumerate(pieces):
                if j == i or (ax, coord) not in cj:
                    continue
                p0 = a * coord
                faces = plane_faces(shapes[i], p0, a)
                partner = shapes[j]
                both = shapes[i].fuse(partner)
                spot = None
                for f in faces:
                    fb = f.BoundBox
                    cands = [f.CenterOfMass] + [Vector(x, y, z) for x in _steps(fb.XMin, fb.XMax)
                                                for y in _steps(fb.YMin, fb.YMax) for z in _steps(fb.ZMin, fb.ZMax)]
                    cands.sort(key=lambda q: (q - f.CenterOfMass).Length)
                    for q in cands[:40]:
                        q = q + a * (coord - q.dot(a))
                        keep = Part.makeCylinder(PEG_D / 2 + FIT + MIN_WALL, PEG_H + 0.5 + MIN_WALL + 2.0, q - a * 2.0, a)
                        if keep.cut(both).Volume < 0.5:
                            spot = q
                            break
                    if spot:
                        break
                if spot is None:
                    continue
                shapes[i] = shapes[i].fuse(Part.makeCylinder(PEG_D / 2, PEG_H + 0.5, spot - a * 0.5, a)).removeSplitter()
                shapes[j] = shapes[j].cut(Part.makeCylinder(PEG_D / 2 + FIT, PEG_H + 0.5, spot - a * 0.1, a)).removeSplitter()
    return shapes


def _steps(a, b, step=3.0):
    n = max(1, int((b - a) / step))
    return [a + (b - a) * (k + 0.5) / n for k in range(n)]


# --------------------------------------------------------------------------
# Cores
# --------------------------------------------------------------------------
def shell_core(poly_xy, z_top, wall=WALL):
    """Pocket core: closed at the pocket's top (z_top), open at the casting's underside (z = 0)."""
    face = Part.Face(Part.makePolygon([Vector(x, y, -1.0) for x, y in poly_xy + poly_xy[:1]]))
    inner = face.makeOffset2D(-wall, join=2).extrude(Vector(0, 0, z_top - wall + 1.0))
    return prism(poly_xy, 0.0, z_top).cut(inner)


def core(poly_xy, z_top, posts=(), lim=BED):
    """Pocket core in bed-sized parts: a shell closed at the pocket's top (z_top) and open at the
    casting's underside (z = 0), with a bolted bulkhead either side of each cut.
    posts: [(x, y, f, z_bolt, z_end)]: a 12 mm post rising past the rim to the side of a bridge,
    f the unit (x, y) vector toward the bridge face (6 mm from the post's centre), bolted to it by an
    M4 at height z_bolt into a nut that slides in from the post's end (z_end).
    Returns ([parts], [Fix]) with the bridge bolts."""
    full = prism(poly_xy, 0.0, z_top)
    face = Part.Face(Part.makePolygon([Vector(x, y, -1.0) for x, y in poly_xy + poly_xy[:1]]))
    void = face.makeOffset2D(-WALL, join=2).extrude(Vector(0, 0, z_top - WALL + 1.0))
    bb = full.BoundBox
    ax = 0 if bb.XLength >= bb.YLength else 1
    lo, length = (bb.XMin, bb.YMin)[ax], (bb.XLength, bb.YLength)[ax]
    n = max(1, math.ceil(length / lim))
    cuts = []
    for k in range(1, n):
        cpos = lo + length * k / n
        for x, y, *_ in posts:
            pc = (x, y)[ax]
            if abs(cpos - pc) < 13.0:
                cpos = pc + (13.0 if cpos > pc else -13.0)
        cuts.append(cpos)
    edges = [lo - 1.0] + cuts + [lo + length + 1.0]
    out, fixes = [], []
    for k in range(len(edges) - 1):
        a, b = edges[k], edges[k + 1]
        ia = a + (BULKHEAD if k else -1.0)
        ib = b - (BULKHEAD if k < len(edges) - 2 else -1.0)
        piece = full.common(_slab(ax, a, b)).cut(void.common(_slab(ax, ia, ib)))
        out.append(piece)
    # the bulkheads are frames: an 8 mm lip round the inside, bolted through the lip by the closed face
    window = face.makeOffset2D(-WALL - LIP, join=2).extrude(Vector(0, 0, z_top - WALL - LIP + 1.0))
    for k, cpos in enumerate(cuts):
        win = window.common(_slab(ax, cpos - BULKHEAD - 1.0, cpos + BULKHEAD + 1.0))
        out[k], out[k + 1] = out[k].cut(win), out[k + 1].cut(win)
        sec = void.common(_slab(ax, cpos - 0.5, cpos + 0.5)).BoundBox
        o0, o1 = (sec.YMin, sec.YMax) if ax == 0 else (sec.XMin, sec.XMax)
        a = Vector(1, 0, 0) if ax == 0 else Vector(0, 1, 0)
        zb = z_top - WALL - LIP / 2
        for t in (0.27, 0.73):
            ov = o0 + (o1 - o0) * t
            q = (Vector(cpos, ov, zb) if ax == 0 else Vector(ov, cpos, zb))
            hole = Part.makeCylinder(HW['M3']['hole'] / 2, 2 * BULKHEAD + 2.0, q - a * (BULKHEAD + 1.0), a)
            out[k] = out[k].cut(hole)
            out[k + 1] = out[k + 1].cut(hole)
    for x, y, f, z_bolt, z_end in posts:
        f = unit(Vector(f[0], f[1], 0))
        post = Part.makeBox(POST, POST, z_top - WALL + 0.5 - z_end, Vector(x - POST / 2, y - POST / 2, z_end))
        k = next(i for i in range(len(out)) if edges[i] <= (x, y)[ax] <= edges[i + 1])
        q = Vector(x, y, z_bolt) + f * (POST / 2)
        post = post.cut(nut_trap(q, f, Vector(0, 0, -1), 'M4', mode='side', run=40.0))
        out[k] = out[k].fuse(post).removeSplitter()
        fixes.append(Fix('bolt', q, f, DRILL['M4'], 'core post', 'M4', nut_bolt('M4')[0]))
    return out, fixes


def _slab(ax, a, b, big=2000.0):
    o = [-big, -big, -big]
    size = [2 * big, 2 * big, 2 * big]
    o[ax], size[ax] = a, b - a
    return Part.makeBox(*size, Vector(*o))


def fillers(envelope, min_dim=15.0, min_vol=5e3):
    """What the casting's rounded corners and sloped faces leave empty in a square mould box.
    Thin edge-fillet slivers are left out (quarter-round moulding does those)."""
    bb = envelope.BoundBox
    box = Part.makeBox(bb.XLength, bb.YLength, bb.ZLength, Vector(bb.XMin, bb.YMin, bb.ZMin))
    rest = box.cut(envelope)
    return [s for s in rest.Solids
            if min(s.BoundBox.XLength, s.BoundBox.YLength, s.BoundBox.ZLength) >= min_dim and s.Volume > min_vol]


# --------------------------------------------------------------------------
# Export
# --------------------------------------------------------------------------
def print_pose(shape, up=None, flip=False):
    """Turn `up` (or z, upside down if flip) to +z and move to the origin."""
    s = shape.copy()
    if up is not None:
        s.rotate(Vector(0, 0, 0), *_axis_angle(unit(up), Vector(0, 0, 1)))
    elif flip:
        s.rotate(Vector(0, 0, 0), Vector(1, 0, 0), 180)
    bb = s.BoundBox
    s.translate(Vector(-bb.XMin, -bb.YMin, -bb.ZMin))
    return s


def _axis_angle(a, b):
    r = Rotation(a, b)
    return r.Axis, math.degrees(r.Angle)


def grams(shape, kind):
    """Rough filament use: walls about 1.2 mm deep all round, and infill inside them (15 %, or
    40 % for liners and cast-in parts). Thin shells come out solid."""
    v = shape.Volume / 1000.0
    walls = min(v, shape.Area / 100.0 * 0.12)
    return (walls + (0.4 if kind in ('liner', 'cast-in') else 0.15) * (v - walls)) * PETG


def export(rows, root):
    """rows: dicts (folder, name, shape or [parts], kind, qty, note, up). Writes STLs under root,
    returns manifest rows. A single shape is cut to the bed here (no keys); lists go as they are."""
    import MeshPart
    out = []
    for r in rows:
        d = os.path.join(root, r['folder'])
        os.makedirs(d, exist_ok=True)
        parts = r['shape'] if isinstance(r['shape'], list) else split_bed(r['shape'])
        for k, p in enumerate(parts):
            stem = f"{r['kind']}-{r['name']}" + (f'-part{k + 1}of{len(parts)}' if len(parts) > 1 else '')
            pose = print_pose(p, r.get('up'), r['kind'] == 'core')
            mesh = MeshPart.meshFromShape(Shape=pose, LinearDeflection=0.05, AngularDeflection=0.25, Relative=False)
            mesh.write(os.path.join(d, stem + '.stl'))
            bb = pose.BoundBox
            out.append(dict(folder=r['folder'], file=stem + '.stl', kind=r['kind'], qty=r['qty'],
                            size=f'{bb.XLength:.0f} x {bb.YLength:.0f} x {bb.ZLength:.0f}',
                            grams=grams(p, r['kind']) * r['qty'], note=r['note'] if k == 0 else ''))
    with open(os.path.join(root, 'manifest.csv'), 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=['folder', 'file', 'kind', 'qty', 'size', 'grams', 'note'])
        w.writeheader()
        for r in out:
            w.writerow({**r, 'grams': f"{r['grams']:.0f}"})
    return out
