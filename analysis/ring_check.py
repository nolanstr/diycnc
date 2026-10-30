"""Does any of the steel ring? Local vibration modes of the steel members and the parts bolted to them,
with fine 10-node tetrahedra (cad-rust-app's FEA through cadrust), each mode's loss factor and how much of its
strain energy is in steel or aluminum.

    python ring_check.py                    # every group (about 20 min)
    python ring_check.py legs table         # some of them

The voxel model (damping.py) smears the 1/8 in tube walls and thin plates over 5-10 mm voxels, so their own
modes, the tuning-fork ones, aren't in it. Here each group is meshed with its walls a few elements thick, with
a chunk of the casting it's cast into (clamped where the chunk is cut out of the casting) or with the rail
blocks it rides on (held where they run on the rails). Parts that touch are tied (bonded): bolted joints are
stiffer than that in practice only in the sense of not slipping, and they add damping this leaves out, so the
loss factors here are the pessimistic ones.

A mode rings when its loss factor is low: under RING_ETA (0.005: an amplification over 200 at resonance)
inside the band cutting can excite (below F_MAX, 2 kHz: 24,000 rpm with 3 flutes is 1.2 kHz, and its
harmonics). For a ringing hollow tube it also tries filling it, with epoxy granite (the same mix, bonded) and
with dry sand (soft and lossy: E 50 MPa, eta 0.15, a rough figure; sand's damping comes from friction and
depends on how hard it's packed).
"""

import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
CAD = os.path.join(os.path.dirname(HERE), 'model')
sys.path.insert(0, CAD)

F_MAX = 2000.0
RING_ETA = 0.005
COUNT = 16
# material: E (MPa), nu, density (g/cm3), loss factor
MAT = dict(eg=(30e3, 0.25, 2.35, 0.02), steel=(200e3, 0.29, 7.85, 0.0005), alu=(69e3, 0.33, 2.70, 0.0003),
           sand=(50.0, 0.30, 1.60, 0.15), petg=(2.0e3, 0.38, 1.27, 0.02))
LOOK_MAT = dict(granite='eg', steeltube='steel', steel='steel', black='steel', alu='alu', spindle='alu', motor='steel',
                brass='steel', seal='petg', printed='petg', tin='steel')
SPINDLE_KG = 4.5


def load():
    src = open(os.path.join(CAD, 'build_cnc.py')).read()
    src = src[:src.rstrip().rfind('\nmain()')]
    ns = {'__file__': os.path.join(CAD, 'build_cnc.py'), '__name__': 'build_cnc'}
    exec(compile(src, 'build_cnc.py', 'exec'), ns)
    return ns


def inflate(bb, d):
    return (bb.XMin - d, bb.YMin - d, bb.ZMin - d, bb.XMax + d, bb.YMax + d, bb.ZMax + d)


def box_of(b):
    from cadrust.freecad import Part, Vector
    return Part.makeBox(b[3] - b[0], b[4] - b[1], b[5] - b[2], Vector(b[0], b[1], b[2]))


def tube_core(shape, wall):
    """The hollow inside a straight tube: its box shrunk by the wall across the two short directions."""
    from cadrust.freecad import Part, Vector
    bb = shape.BoundBox
    lo, hi = [bb.XMin, bb.YMin, bb.ZMin], [bb.XMax, bb.YMax, bb.ZMax]
    ax = max(range(3), key=lambda k: hi[k] - lo[k])
    for k in range(3):
        if k != ax:
            lo[k] += wall + 0.05
            hi[k] -= wall + 0.05
    return Part.makeBox(hi[0] - lo[0], hi[1] - lo[1], hi[2] - lo[2], Vector(*lo)).cut(shape)


class Case:
    """One group: bodies (name, shape, material, element size) and how it's held."""

    def __init__(self, name, note):
        self.name, self.note = name, note
        self.bodies, self.holds, self.fills = [], [], []

    def add(self, name, shape, mat, size):
        if shape is None or shape.isNull() or shape.Volume < 1.0:
            return
        self.bodies.append((name, shape, mat, size))

    def hold_cut_faces(self, body, box, skip=()):
        """Clamp a casting chunk where the box cut it out (the box's faces, but not those in `skip`, e.g. '-z')."""
        x0, y0, z0, x1, y1, z1 = box
        for tag, b, n in (('-x', (x0 - .5, y0 - 1, z0 - 1, x0 + .5, y1 + 1, z1 + 1), (-1, 0, 0)),
                          ('+x', (x1 - .5, y0 - 1, z0 - 1, x1 + .5, y1 + 1, z1 + 1), (1, 0, 0)),
                          ('-y', (x0 - 1, y0 - .5, z0 - 1, x1 + 1, y0 + .5, z1 + 1), (0, -1, 0)),
                          ('+y', (x0 - 1, y1 - .5, z0 - 1, x1 + 1, y1 + .5, z1 + 1), (0, 1, 0)),
                          ('-z', (x0 - 1, y0 - 1, z0 - .5, x1 + 1, y1 + 1, z0 + .5), (0, 0, -1)),
                          ('+z', (x0 - 1, y0 - 1, z1 - .5, x1 + 1, y1 + 1, z1 + .5), (0, 0, 1))):
            if tag not in skip:
                self.holds.append((body, b, n))

    def hold_face(self, body, shape, side):
        """Hold a body's face on one side of its box ('-z': its bottom)."""
        bb = shape.BoundBox
        lo, hi = [bb.XMin, bb.YMin, bb.ZMin], [bb.XMax, bb.YMax, bb.ZMax]
        k = 'xyz'.index(side[1])
        v = lo[k] if side[0] == '-' else hi[k]
        b = [c - 1 for c in lo] + [c + 1 for c in hi]
        b[k], b[k + 3] = v - 0.5, v + 0.5
        n = [0, 0, 0]
        n[k] = -1 if side[0] == '-' else 1
        self.holds.append((body, tuple(b), tuple(n)))


def solve(case, extra=()):
    """Modes of the group (plus `extra` bodies). Returns [(Hz, loss, metal share, part with the most strain)]."""
    from cadrust import _core as C
    fm = C.FeModel()
    names = []
    bodies = list(case.bodies) + list(extra)
    for name, shape, mat, size in bodies:
        e, nu, rho, eta = MAT[mat]
        if name == 'SpindleBody':
            rho = SPINDLE_KG * 1e6 / shape.Volume
        fm.add_body(shape._s, e, nu, rho, size, name, eta=eta)
        names.append(name)
    fm.mesh(tol=0.3)
    for body, b, n in case.holds:
        i = names.index(body)
        try:
            fm.fix(fm.patch(b, [i], n))
        except ValueError:
            pass                                    # that face of the box doesn't cut the part
    fr = fm.modal(COUNT)
    loss = fm.mode_losses()
    out = []
    metal = [i for i, (_, _, m, _) in enumerate(bodies) if m in ('steel', 'alu')]
    for j, f in enumerate(fr):
        if f > F_MAX:
            break
        sh = fm.strain_shares(j)
        top = max(range(len(sh)), key=lambda i: sh[i])
        out.append((f, loss[j], sum(sh[i] for i in metal), names[top], sh[top]))
    return out, fm.size()


def show(label, rows, size):
    print(f'  {label} ({size[1]:,} elements)', flush=True)
    ring = []
    for f, eta, metal, top, share in rows:
        flag = 'RINGS' if eta < RING_ETA else ''
        print(f'    {f:7.0f} Hz  loss {eta:.4f} (x{1 / max(eta, 1e-9):5.0f} at resonance)  metal {metal:4.0%}  '
              f'most in {top} ({share:.0%})  {flag}', flush=True)
        if flag:
            ring.append(f)
    if not rows:
        print(f'    nothing below {F_MAX:.0f} Hz', flush=True)
    return ring


def cases(ns, m):
    by = {p['name']: p for p in m.parts}
    P = ns['P']
    out = {}

    def part(n):
        return by[n]['shape'] if n in by else None

    def mat(n):
        return LOOK_MAT.get(by[n]['look'], 'steel')

    # legs: a 1-1/2 in tube, 35 mm cast into the base corner, a leveling foot screwed into its end
    c = Case('legs', 'front left leg: tube and foot insert, its top 35 mm cast into the base corner, standing on its foot')
    leg = part('LegFrontL')
    box = inflate(leg.BoundBox, 60.0)
    box = (box[0], box[1], leg.BoundBox.ZMax - P['leg_embed'] - 5, box[3], box[4], leg.BoundBox.ZMax + 60)
    c.add('LegFrontL', leg, 'steel', 3.0)
    c.add('BaseChunk', part('BaseFrontCasting').common(box_of(box)), 'eg', 12.0)
    c.add('LegFrontLInsert', part('LegFrontLInsert'), 'steel', 4.0)
    c.hold_cut_faces('BaseChunk', box, skip=('-z',))
    c.hold_face('LegFrontL', leg, '-z')               # on its leveling foot
    c.fills = ['LegFrontL']
    out['legs'] = c

    # an upright column: 2x2x1/8 tube in the upright casting
    c = Case('columns', 'upright column L1 in its casting (the tie rod inside is unbonded, left out)')
    col = part('UprightColumnL1')
    box = inflate(col.BoundBox, 50.0)
    c.add('UprightColumnL1', col, 'steel', 3.0)
    c.add('UprightChunk', part('UprightLCasting').common(box_of(box)), 'eg', 14.0)
    c.hold_cut_faces('UprightChunk', box)
    c.fills = ['UprightColumnL1']
    out['columns'] = c

    # a base girder: 2x3x1/8 tube under a table rail
    c = Case('girders', 'base girder front L (2x3x1/8 tube) with its rail bar, in the front base casting')
    gd = part('BaseGirderFrontL')
    box = inflate(gd.BoundBox, 45.0)
    c.add('BaseGirderFrontL', gd, 'steel', 3.0)
    c.add('BaseRailBarFrontL', part('BaseRailBarFrontL'), 'steel', 4.0)
    c.add('BaseChunk', part('BaseFrontCasting').common(box_of(box)), 'eg', 14.0)
    c.hold_cut_faces('BaseChunk', box)
    c.fills = ['BaseGirderFrontL']
    out['girders'] = c

    # the table on its four blocks
    c = Case('table', 'the 6061 table (10 x 3/4 in) on its four Y blocks, held where the blocks run on the rails')
    c.add('Table', part('Table'), 'alu', 5.0)
    for s in 'LR':
        for i in '12':
            n = f'Y_Block{s}{i}'
            c.add(n, part(n), 'steel', 6.0)
            c.hold_face(n, part(n), '-z')
    out['table'] = c

    # the X carriage with the Z axis and spindle on it
    c = Case('carriage', 'X carriage plate and angles, Z blocks, rails, risers and plate, clamp and spindle; held at the X blocks')
    for n in ('XCarriagePlate', 'XCarriageAngleL', 'XCarriageAngleR', 'Z_RiserL', 'Z_RiserR', 'Z_RailL', 'Z_RailR',
              'ZPlate', 'SpindleClamp', 'SpindleBody'):
        if n in by:
            c.add(n, part(n), mat(n), 5.0 if n != 'SpindleBody' else 8.0)
    for s in 'LR':
        for i in '12':
            for n, side in ((f'X_Block{s}{i}', '+y'), (f'Z_Block{s}{i}', None)):
                if n in by:
                    c.add(n, part(n), 'steel', 6.0)
                    if side:
                        c.hold_face(n, part(n), side)
    out['carriage'] = c

    # the X rails on their risers on the beam's face bar
    c = Case('x rails', 'X risers and rails on the beam face bar, in a chunk of the beam casting')
    fb = part('BeamFacePlate')
    box = inflate(fb.BoundBox, 25.0)
    c.add('BeamFacePlate', fb, 'steel', 5.0)
    for n in ('X_RiserL', 'X_RiserR', 'X_RailL', 'X_RailR'):
        c.add(n, part(n), 'steel', 5.0)
    c.add('BeamChunk', part('BeamCasting').common(box_of(box)), 'eg', 14.0)
    c.hold_cut_faces('BeamChunk', box)
    out['x rails'] = c
    return out


def main():
    want = [a for a in sys.argv[1:] if not a.startswith('-')]
    t = time.time()
    ns = load()
    m = ns['build']()
    print(f'model built ({time.time() - t:.0f} s); modes below {F_MAX:.0f} Hz, ringing under eta {RING_ETA}', flush=True)
    summary = []
    for key, case in cases(ns, m).items():
        if want and key not in want:
            continue
        t = time.time()
        print(f'{key}: {case.note}', flush=True)
        rows, size = solve(case)
        ring = show('as drawn', rows, size)
        summary.append((key, 'as drawn', rows))
        if ring and case.fills:
            for fill in ('eg', 'sand'):
                extra = [(f'{n}Fill', tube_core(s, 3.175), fill, 6.0) for n, s, _, _ in case.bodies if n in case.fills]
                rows2, size2 = solve(case, extra)
                show(f'filled with {"epoxy granite" if fill == "eg" else "dry sand"}', rows2, size2)
                summary.append((key, f'filled with {fill}', rows2))
        print(f'  ({time.time() - t:.0f} s)', flush=True)
    print('\nlowest loss factor below 2 kHz per group:')
    for key, label, rows in summary:
        if rows:
            f, eta = min(((r[0], r[1]) for r in rows), key=lambda x: x[1])
            print(f'  {key:10s} {label:24s} {eta:.4f} at {f:.0f} Hz')
        else:
            print(f'  {key:10s} {label:24s} no modes below {F_MAX:.0f} Hz')


if __name__ == '__main__':
    main()
