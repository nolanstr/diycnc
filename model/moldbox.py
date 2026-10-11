"""Mold boxes: melamine boards cut to a list and held together by printed brackets with M4 bolts,
plus the hole map for every board.

Every wall is 25 mm taller than the casting (the freeboard), so the brackets, saddles and leg
holders bolt through the walls above the pour line and nothing goes through a cast face:
  - corner brackets hold each outside corner along that band,
  - floor brackets hold each wall's foot from outside and bolt down through the floor,
  - saddles hook over the wall tops and carry the bridges that hold the cores down,
  - the boards are drilled from the cast side (clean holes on the cast faces), using the
    printed brackets as drill guides where there is one.
Each bracket has a hex pocket that holds its nut, so assembly is one bolt from the outside.
"""

import math

import Part
from FreeCAD import Vector

import molds
from molds import FIT, HW, Fix, block, bolt_length, nut_recess, unit

SLOT = 0.4        # board thickness + this = slot width in printed parts that go over a board edge
TH = 6.0          # bracket legs


def board_t():
    return molds.BOARD


class Board:
    """A melamine board: its inside (cast) face is the plane through `origin` with normal -N, so N
    points away from the cavity. Seen from inside, U is right and V is up; the outline is in (u, v)."""

    def __init__(self, name, mold, origin, N, V, outline, qty=1, note='', view='inside', show=()):
        self.name, self.mold, self.qty, self.note, self.view, self.show = name, mold, qty, note, view, list(show)
        self.N, self.V = unit(N), unit(V)
        self.U = self.N.cross(self.V)
        self.o = Vector(origin)
        self.outline = list(outline)
        self.t = board_t()
        self.holes = []          # (u, v, d, what)

    def uv(self, p):
        d = p - self.o
        return d.dot(self.U), d.dot(self.V)

    def at(self, u, v, w=0.0):
        return self.o + self.U * u + self.V * v + self.N * w

    def contains(self, p, n):
        if abs(Vector(n).dot(self.N)) < 0.99:
            return False
        w = (p - self.o).dot(self.N)
        if abs(w) > 0.6 and abs(w - self.t) > 0.6:
            return False
        return inside(self.uv(p), self.outline)

    def solid(self):
        face = molds.poly([self.at(u, v) for u, v in self.outline])
        s = face.extrude(self.N * self.t)
        cuts = [Part.makeCylinder(d / 2, self.t + 2, self.at(u, v, -1.0), self.N) for u, v, d, _ in self.holes]
        return s.cut(cuts) if cuts else s

    def size(self):
        us = [u for u, _ in self.outline]
        vs = [v for _, v in self.outline]
        return max(us) - min(us), max(vs) - min(vs)

    def rect(self):
        us = [u for u, _ in self.outline]
        vs = [v for _, v in self.outline]
        return len(self.outline) == 4 and len(set(round(u, 2) for u in us)) == 2 and len(set(round(v, 2) for v in vs)) == 2


def inside(q, outline):
    """Point in polygon (edges count as inside)."""
    x, y = q
    n = len(outline)
    hit = False
    for i in range(n):
        (x0, y0), (x1, y1) = outline[i], outline[(i + 1) % n]
        if min(x0, x1) - 0.6 <= x <= max(x0, x1) + 0.6 and min(y0, y1) - 0.6 <= y <= max(y0, y1) + 0.6:
            dx, dy = x1 - x0, y1 - y0
            ln = math.hypot(dx, dy)
            if ln > 0 and abs((x - x0) * dy - (y - y0) * dx) / ln < 0.6:
                return True
        if (y0 > y) != (y1 > y) and x < x0 + (y - y0) * (x1 - x0) / (y1 - y0):
            hit = not hit
    return hit


def box_board(name, mold, lo, hi, N, V, **kw):
    """Rectangular board filling the box between corners lo and hi."""
    N, V = unit(N), unit(V)
    U = N.cross(V)
    cs = [Vector(x, y, z) for x in (lo[0], hi[0]) for y in (lo[1], hi[1]) for z in (lo[2], hi[2])]
    us, vs, ws = [c.dot(U) for c in cs], [c.dot(V) for c in cs], [c.dot(N) for c in cs]
    o = U * min(us) + V * min(vs) + N * min(ws)
    du, dv = max(us) - min(us), max(vs) - min(vs)
    return Board(name, mold, o, N, V, [(0, 0), (du, 0), (du, dv), (0, dv)], **kw)


# --------------------------------------------------------------------------
# Printed kit pieces. Each returns (solid, [Fix]).
# --------------------------------------------------------------------------
def angle_bracket(c, a1, m1, a2, m2, up, h, leg=44.0, hole_at=33.0, bolts=(True, True)):
    """L bracket on two board faces that meet along an edge running along `up`, its top at c.
    Leg k lies on face k (mk: the face normal on the bracket's side) and runs along ak from the edge.
    Works for outside corners (ak = -m of the other face) and inside ones (ak = m of the other)."""
    down = -unit(up)
    s = block(c, a1, m1, down, leg, TH, h).multiFuse([block(c, a2, m2, down, leg, TH, h),
                                                     block(c, m1, m2, down, TH, TH, h)]).removeSplitter()
    fixes = []
    for (a, m), bolt in zip(((a1, m1), (a2, m2)), bolts):
        if not bolt:
            continue
        p = c + a * hole_at + down * (h / 2)
        s = s.cut(Part.makeCylinder(HW['M4']['hole'] / 2, TH + 2, p - m, m)).cut(nut_recess(p + m * TH, -m, 'M4'))
        fixes.append(Fix('bolt', p, -m, HW['M4']['hole'], 'corner bracket', 'M4', bolt_length(molds.BOARD_MAX + TH + 0.5)))
    return s, fixes


def floor_bracket(c, n_out, up, along, w=24.0, h=25.0, reach=32.0):
    """Outside a wall's foot: one leg up the wall's outer face, one on the floor, bolted down through
    the floor. c is on the wall's outer face where it meets the floor."""
    n_out, up, along = unit(n_out), unit(up), unit(along)
    o = c - along * (w / 2)
    s = block(o, along, n_out, up, w, TH, h).fuse(block(o, along, n_out, up, w, reach, TH))
    for e in (0.0, w - 3.0):
        q = o + along * e
        tri = molds.poly([q + n_out * TH + up * TH, q + n_out * (reach - 2) + up * TH, q + n_out * TH + up * (h - 2)])
        s = s.fuse(tri.extrude(along * 3.0))
    p = c + n_out * ((TH + reach) / 2)
    s = s.cut(Part.makeCylinder(HW['M4']['hole'] / 2, TH + 2, p - up, up)).cut(nut_recess(p + up * TH, -up, 'M4'))
    return s.removeSplitter(), [Fix('bolt', p, -up, HW['M4']['hole'], 'floor bracket', 'M4',
                                    bolt_length(molds.BOARD_MAX + TH + 0.5))]


def saddle(c, n_out, up, along, width=None, depth=12.0, cheeks=True):
    """Cap over a wall's top edge that carries a bridge end: the cap, a leg down the wall's outside,
    and two cheeks. c: on the wall's inner face at its top, mid-saddle; n_out: the wall's outward
    normal (the bridge crosses the wall along -n_out). width=None: the bridge stands on edge between
    the cheeks and is bolted through them; width=w: a flat bridge w wide rests between them.
    One bolt through the leg and the wall, above the pour line, holds it (nut and washer inside).
    Prints on the leg's outer face. Returns (solid, [Fix on the wall], bridge Fix or None)."""
    n_out, up, along = unit(n_out), unit(up), unit(along)
    slot = board_t() + SLOT
    gap = slot if width is None else width + 4 * FIT
    half = gap / 2 + TH if cheeks else gap / 2
    o = c - along * half
    s = block(o, along, n_out, up, 2 * half, slot + TH, TH)                                 # cap
    s = s.fuse(block(o + n_out * slot, along, n_out, -up, 2 * half, TH, 25.0))              # leg
    ch = 22.0 if width is None else 10.0
    for e in ((0.0, 2 * half - TH) if cheeks else ()):
        s = s.fuse(block(o + along * e + up * TH, along, n_out, up, TH, slot + TH, ch))
    p = c - up * depth
    s = s.cut(Part.makeCylinder(HW['M4']['hole'] / 2, TH + 2, p + n_out * (slot - 1), n_out))
    wall_fix = Fix('bolt', p, n_out, HW['M4']['hole'], 'saddle', 'M4', bolt_length(molds.BOARD_MAX + TH + SLOT + 5.0))
    bridge_fix = None
    if width is None:
        q = c + n_out * (slot / 2) + up * (TH + 11.0)
        s = s.cut(Part.makeCylinder(HW['M4']['hole'] / 2, 2 * half + 2, q - along * (half + 1), along))
        s = s.cut(nut_recess(q + along * half, -along, 'M4'))
        bridge_fix = Fix('bolt', q - along * (board_t() / 2), along, HW['M4']['hole'], 'saddle', 'M4',
                         bolt_length(molds.BOARD_MAX + 2 * TH + SLOT + 0.5))
    return s.removeSplitter(), [wall_fix], bridge_fix


def bushing(c, n, side, sq, hole=63.5):
    """Push fit in a hole-saw hole, flush with the cast face at c, flange on the far side
    (n points through the board, away from the cavity); a square hole `sq` for a tube."""
    n, side = unit(n), unit(side)
    t = board_t()
    q = sq + 2 * FIT
    b = n.cross(side)
    body = Part.makeCylinder((hole - 0.1) / 2, t, c, n)
    for d in (side, -side, b, -b):                 # four tabs on the far side hold it in
        body = body.fuse(block(c + n * t + d * (hole / 2 - 4.0) - d.cross(n) * 6.0, d, d.cross(n), n, 12.0, 12.0, 3.0))
    return body.cut(block(c - n - side * (q / 2) - b * (q / 2), side, b, n, q, q, t + 5)), \
        [Fix('hole', c, n, hole, 'hole saw')]


def tube_hanger(c, up, side, sq, length, cap=3.0, strap=(20.0, 2.4)):
    """Cap on a tube end with two straps down to a holder: the tube hangs at the right height.
    c: where the straps' feet stand (on the holder top), length from there to the tube end."""
    up, side = unit(up), unit(side)
    b = up.cross(side)
    q = sq + 2 * FIT
    o = q + 2 * strap[1]
    s = block(c + up * length - side * (o / 2) - b * (o / 2), side, b, up, o, o, cap)
    for start in (q / 2, -q / 2 - strap[1]):
        s = s.fuse(block(c + side * start - b * (strap[0] / 2), side, b, up, strap[1], strap[0], length + 0.5))
    return s.removeSplitter(), []


# --------------------------------------------------------------------------
# The kit
# --------------------------------------------------------------------------
class Kit:
    def __init__(self):
        self.boards = []
        self.rows = []           # printed pieces (dicts, see molds.export)
        self.hardware = {}       # description -> count
        self.by_mold = {}        # mold -> {description: count}
        self.loose = []          # Fixes that land on no board (reported)

    def board(self, b):
        self.boards.append(b)
        return b

    def fix(self, fixes, mold, mult=1):
        """Put fixings on the boards of `mold` and count their hardware (x mult)."""
        for f in fixes:
            hits = [b for b in self.boards if b.mold == mold and b.contains(f.p, f.n)]
            if not hits:
                self.loose.append((mold, f))
                continue
            for b in hits:                         # a bolt through a cleat and the floor: both get the hole
                u, v = b.uv(f.p)
                if not any(abs(u - h[0]) < 0.5 and abs(v - h[1]) < 0.5 for h in b.holes):
                    b.holes.append((u, v, f.d, f.what))
            if f.kind == 'bolt':
                self.count(f'{f.size} x {f.length} bolt', f.qty * mult, mold)
                self.count(f'{f.size} nut', f.qty * mult, mold)
                self.count(f'{f.size} washer', f.qty * mult, mold)

    def count(self, what, n, mold=None):
        self.hardware[what] = self.hardware.get(what, 0) + n
        if mold:
            d = self.by_mold.setdefault(mold, {})
            d[what] = d.get(what, 0) + n

    def add(self, folder, name, kind, shape, qty=1, note='', up=None, placed=None, show=None):
        """A printed piece: shape (or [parts]) to print; placed = [world shapes] shown in the `show` groups."""
        shapes = placed if placed is not None else (list(shape) if isinstance(shape, list) else [shape])
        row = dict(folder=folder, name=name, kind=kind, shape=shape, qty=qty, note=note, up=up,
                   placed=[(s, list(show or [])) for s in shapes])
        self.rows.append(row)
        return row

    def add_many(self, folder, name, kind, pieces, note='', up=None, mold=None, per=1, show=None, merge=False, mult=1,
                 reuse=False):
        """Identical pieces at several places: pieces = [(solid, fixes)], printed once with a quantity.
        merge: add to an earlier row with the same folder and name (reuse: the same prints, moved)."""
        if not pieces:
            return None
        for _, fx in pieces:
            self.fix(fx, mold, mult)
        old = next((r for r in self.rows if merge and r['folder'] == folder and r['name'] == name), None)
        if old:
            old['qty'] = max(old['qty'], len(pieces) * per) if reuse else old['qty'] + len(pieces) * per
            old['placed'] += [(s, list(show or [])) for s, _ in pieces]
            return old
        return self.add(folder, name, kind, pieces[0][0], len(pieces) * per, note, up, [s for s, _ in pieces], show)
