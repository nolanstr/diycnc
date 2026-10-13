"""Detailed component geometry for the CNC layout model.

Linear-motion parts are built in a local frame: x = u (along the axis),
y = v (across it), z = w (away from the mounting face). build_cnc.Frame
places them. Spindle and clamp are built directly in machine coordinates.
"""

import math

import Part
from FreeCAD import Vector as V


# --------------------------------------------------------------------------
# Primitives
# --------------------------------------------------------------------------
def box(u0, u1, v0, v1, w0, w1):
    return Part.makeBox(u1 - u0, v1 - v0, w1 - w0, V(u0, v0, w0))


def cyl_u(r, u0, u1, v=0.0, w=0.0):
    return Part.makeCylinder(r, u1 - u0, V(u0, v, w), V(1, 0, 0))


def cyl_v(r, v0, v1, u=0.0, w=0.0):
    return Part.makeCylinder(r, v1 - v0, V(u, v0, w), V(0, 1, 0))


def cyl_w(r, w0, w1, u=0.0, v=0.0):
    return Part.makeCylinder(r, w1 - w0, V(u, v, w0), V(0, 0, 1))


def ring_u(r_out, r_in, u0, u1, v=0.0, w=0.0):
    return cyl_u(r_out, u0, u1, v, w).cut(cyl_u(r_in, u0 - 1, u1 + 1, v, w))


def prism_u(pts, u0, u1):
    """Extrude a closed (v, w) outline along u."""
    wire = Part.makePolygon([V(u0, v, w) for v, w in pts] + [V(u0, *pts[0])])
    return Part.Face(wire).extrude(V(u1 - u0, 0, 0))


def chamfered_square(half, c, w0=0.0):
    """(v, w) outline of a square centered on (0, w0) with chamfered corners."""
    h = half
    return [(-h + c, w0 - h), (h - c, w0 - h), (h, w0 - h + c), (h, w0 + h - c),
            (h - c, w0 + h), (-h + c, w0 + h), (-h, w0 + h - c), (-h, w0 - h + c)]


def _direction(edge):
    if not isinstance(edge.Curve, Part.Line):
        return None
    d = edge.Vertexes[-1].Point - edge.Vertexes[0].Point
    if d.Length < 1e-9:
        return None
    d.normalize()
    return d


def parallel(axis):
    a = V(*axis)
    a.normalize()

    def pred(edge):
        d = _direction(edge)
        return d is not None and abs(abs(d.dot(a)) - 1.0) < 1e-6
    return pred


def soften(shape, r, pred=None, chamfer=False):
    """Fillet (or chamfer) the edges matching pred; returns the input if OCC refuses."""
    edges = [e for e in shape.Edges if pred is None or pred(e)]
    if not edges:
        return shape
    try:
        out = shape.makeChamfer(r, edges) if chamfer else shape.makeFillet(r, edges)
        return out if out.isValid() else shape
    except Exception:
        return shape


def plate(x0, x1, y0, y1, z0, z1, c=1.0):
    return soften(box(x0, x1, y0, y1, z0, z1), c, chamfer=True)


def square_tube(axis, c1, c2, size, wall, a0, a1):
    """Steel square tube along 'x', 'y' or 'z' from a0 to a1, section centerd on (c1, c2) in the
    other two axes (in x, y, z order). Returns (outer envelope, tube wall)."""
    def section(s, ext):
        h = s / 2
        if axis == 'x':
            return box(a0 - ext, a1 + ext, c1 - h, c1 + h, c2 - h, c2 + h)
        if axis == 'y':
            return box(c1 - h, c1 + h, a0 - ext, a1 + ext, c2 - h, c2 + h)
        return box(c1 - h, c1 + h, c2 - h, c2 + h, a0 - ext, a1 + ext)
    along = parallel({'x': (1, 0, 0), 'y': (0, 1, 0), 'z': (0, 0, 1)}[axis])
    outer = soften(section(size, 0), 1.5 * wall, along)
    inner = soften(section(size - 2 * wall, 1), 0.5 * wall, along)
    return outer, outer.cut(inner)


# --------------------------------------------------------------------------
# HGR15 rail / HGH15CA block (rail bottom at w = 0, centered on v = 0)
# Ref: HIWIN Linear Guideway catalog G99TE23-2203, HG series, HGH-CA table (p.38)
#   rail WR 15, HR 15, bolt holes d 4.5 / D 7.5 / h 5.3, P 60, E 20, M4x16
#   block H 28, H1 4.3, W 34, N 9.5, B 26, C 26, L1 39.4, L 61.4, M4 x 5,
#   grease nipple M4 on the end cap, axis 7.95 below the block top, G 5.3 proud.
# HIWIN does not dimension the ball grooves (4-row, 45 deg contact); the notch
# positions below are estimates: top-corner grooves ~2.5 mm and flank grooves
# ~7.5 mm below the rail top.
# --------------------------------------------------------------------------
RAIL_HALF = [(7.5, 0.0), (7.5, 6.3), (6.3, 7.5), (6.3, 8.3), (7.5, 9.5), (7.5, 11.6),
             (6.7, 12.4), (6.7, 13.6), (7.1, 14.0), (7.1, 14.5), (6.6, 15.0)]
RAIL_PROFILE = [(-v, w) for v, w in RAIL_HALF[:1]] + RAIL_HALF + [(-v, w) for v, w in reversed(RAIL_HALF[1:])]


def hgr15_rail(length, pitch=60.0, end=20.0):
    rail = prism_u(RAIL_PROFILE, -length / 2, length / 2)
    n = int((length - 2 * end) // pitch) + 1
    first = -(n - 1) * pitch / 2
    holes = []
    for i in range(n):
        u = first + i * pitch
        holes += [cyl_w(2.25, -1, 16, u), cyl_w(3.75, 15 - 5.3, 16, u)]
    return rail.cut(holes)


# End view of the block: N 9.5 from rail side to block side, body from H1 4.3 to H 28,
# with the lower outside corners relieved.
BLOCK_BODY = [(-17, 6.3), (-15, 4.3), (-7.6, 4.3), (-7.6, 15), (7.6, 15), (7.6, 4.3),
              (15, 4.3), (17, 6.3), (17, 28), (-17, 28)]
BLOCK_CAP = [(-16.5, 6.6), (-14.8, 5.0), (-7.8, 5.0), (-7.8, 15.2), (7.8, 15.2), (7.8, 5.0),
             (14.8, 5.0), (16.5, 6.6), (16.5, 27.2), (-16.5, 27.2)]


def hgh15_block():
    """HGH15CA carriage centered on u = 0: [(suffix, shape, look)]."""
    body = prism_u(BLOCK_BODY, -19.7, 19.7)
    body = body.cut([cyl_w(1.7, 28 - 5, 29, u, v) for u in (-13, 13) for v in (-13, 13)])
    caps = prism_u(BLOCK_CAP, 19.7, 30.7).fuse(prism_u(BLOCK_CAP, -30.7, -19.7))
    nz = 28 - 7.95
    hexnut = prism_u([(3.5 * math.cos(math.radians(a)), nz + 3.5 * math.sin(math.radians(a))) for a in range(30, 390, 60)],
                     -30.7 - 3.3, -30.7)
    nipple = hexnut.fuse(cyl_u(2.0, -30.7 - 5.3, -30.7 - 3.3, 0, nz))
    return [('', body, 'steel'), ('Seals', caps, 'seal'), ('Nipple', nipple, 'brass')]


# --------------------------------------------------------------------------
# Ballscrew hardware (screw axis at (v = 0, w = a))
# Ref: TBI Motion catalog sheets, hosted by Anaheim Automation:
#   L010974 SFU ball screw, L011175 BK support units, L011178 BF support units.
# Nut housings: DSG16H drawing (makerstore.cc TR-BS-DSG16-00); DSG12H overall size
# from zyltech / vxb listings (center height and holes not published: estimated).
# --------------------------------------------------------------------------
SFU = {
    # body D, flange D1 x T, across flats F, overall L, bolt circle bcd, 6 holes
    'SFU1204': dict(d=12.0, lead=4.0, D=24.0, D1=40.0, T=10.0, F=30.0, L=40.0, bcd=32.0, hole=4.5),
    'SFU1605': dict(d=16.0, lead=5.0, D=28.0, D1=48.0, T=10.0, F=40.0, L=50.0, bcd=38.0, hole=5.5),
}
# TBI recommended end machining: BK side journal (bearing seat + locknut thread) of
# diameter bk_a for length bk_e from the BK inner face, then the motor stub; BF journal.
ENDS = {
    'SFU1204': dict(bk_a=10.0, bk_e=36.0, stub=8.0, stub_l=15.0, bf_a=8.0),
    'SFU1605': dict(bk_a=12.0, bk_e=36.0, stub=10.0, stub_l=15.0, bf_a=10.0),
}
SUPPORT = {
    # L, width B, height H, center height h, flange height H1, raised center B1, bolt spacing P,
    # vertical bolt holes X thru / Y counterbore x Z deep at C from the end, axial holes d2 on E.
    # lock = BK locknut (radius, width): not published, estimated.
    'BK10': dict(L=25.0, B=60.0, H=39.0, h=22.0, H1=32.5, B1=34.0, P=46.0, X=6.6, Y=10.8, Z=5.0,
                 C=(6.0, 19.0), d2=5.5, E=15.0, lock=(10.0, 8.0)),
    'BK12': dict(L=25.0, B=60.0, H=43.0, h=25.0, H1=32.5, B1=34.0, P=46.0, X=6.6, Y=10.8, Z=1.5,
                 C=(6.0, 19.0), d2=5.5, E=18.0, lock=(11.0, 8.0)),
    'BF10': dict(L=20.0, B=60.0, H=39.0, h=22.0, H1=32.5, B1=34.0, P=46.0, X=6.6, Y=10.8, Z=5.0,
                 C=(10.0,), d2=5.5, E=15.0, lock=None),
    'BF12': dict(L=20.0, B=60.0, H=43.0, h=25.0, H1=32.5, B1=34.0, P=46.0, X=6.6, Y=10.8, Z=1.5,
                 C=(10.0,), d2=5.5, E=18.0, lock=None),
}
HOUSING = {
    # W across, H base-to-far-face, L along the axis (= nut body length), ch base-to-axis, bore
    'SFU1605': dict(name='DSG16H', W=52.0, H=40.0, L=40.0, ch=20.0, bore=28.0, chamfer=12.0, holes=(40.0, 24.0), face_bcd=38.0),
    'SFU1204': dict(name='DSG12H (24 mm bore)', W=50.0, H=36.0, L=30.0, ch=15.0, bore=24.0, chamfer=8.0, holes=(38.0, 18.0),
                    face_bcd=32.0),
}


def ballscrew(kind, u0, length, bf, bk, a):
    """Machined screw from the BF outer face (u0). Returns (shape, BK outer face u1, stub start, stub end)."""
    s, e = SFU[kind], ENDS[kind]
    lbf, lbk = SUPPORT[bf]['L'], SUPPORT[bk]['L']
    tail = e['bk_e'] - lbk + e['stub_l']
    u1 = u0 + length - tail
    s0 = u1 + e['bk_e'] - lbk
    screw = cyl_u(e['bf_a'] / 2, u0, u0 + lbf, 0, a).fuse([
        cyl_u(s['d'] / 2, u0 + lbf, u1 - lbk, 0, a),
        cyl_u(e['bk_a'] / 2, u1 - lbk, s0, 0, a),
        cyl_u(e['stub'] / 2, s0, s0 + e['stub_l'], 0, a)])
    return screw.removeSplitter(), u1, s0, s0 + e['stub_l']


def sfu_nut(kind, uc, a):
    """Flanged ballnut centerd on uc, flange toward -u, flats facing +/-w."""
    s = SFU[kind]
    u0 = uc - s['L'] / 2
    flange = cyl_u(s['D1'] / 2, u0, u0 + s['T'], 0, a)
    flange = flange.common(box(u0 - 1, u0 + s['T'] + 1, -s['D1'], s['D1'], a - s['F'] / 2, a + s['F'] / 2))
    rb = s['bcd'] / 2
    flange = flange.cut([cyl_u(s['hole'] / 2, u0 - 1, u0 + s['T'] + 1, rb * math.cos(t), a + rb * math.sin(t))
                         for t in (math.radians(x) for x in (0, 45, -45, 180, 135, 225))])
    body = cyl_u(s['D'] / 2, u0 + s['T'], u0 + s['L'], 0, a)
    wiper = ring_u(s['D'] / 2 + 0.5, s['D'] / 2 - 1.0, u0 + s['L'] - 4.0, u0 + s['L'] - 3.4, 0, a)
    nut = flange.fuse(body).cut(wiper)
    return nut.cut(cyl_u(s['d'] / 2, u0 - 1, u0 + s['L'] + 1, 0, a)).removeSplitter()


def nut_housing(kind, uc, a, carrier):
    """DSG housing bolted under the moving part (w = carrier), with a shim to make up the height."""
    s, h = SFU[kind], HOUSING[kind]
    u0, u1 = uc - s['L'] / 2 + s['T'], uc - s['L'] / 2 + s['T'] + h['L']
    wb = a + h['ch']
    blk = box(u0, u1, -h['W'] / 2, h['W'] / 2, wb - h['H'], wb)
    blk = soften(blk, h['chamfer'], lambda e: parallel((1, 0, 0))(e)
                 and all(abs(v.Point.z - (wb - h['H'])) < 1e-6 for v in e.Vertexes), chamfer=True)
    rb = h['face_bcd'] / 2
    taps = [cyl_u(2.1, u0 - 0.01, u0 + 10, rb * math.cos(t), a + rb * math.sin(t))
            for t in (math.radians(x) for x in (0, 45, -45, 180, 135, 225))]
    blk = blk.cut(taps + [cyl_u(h['bore'] / 2, u0 - 1, u1 + 1, 0, a)])
    out = [('', blk, 'black')]
    if carrier - wb > 0.3:
        out.append(('Shim', box(u0, u1, -h['W'] / 2, h['W'] / 2, wb, carrier), 'alu'))
    return out


def support(kind, u0, a, journal_r, lock_r=None):
    """TBI BK/BF support (inverted T: B x H1 flange, B1 x H center) from u0 to u0 + L."""
    s = SUPPORT[kind]
    u1 = u0 + s['L']
    body = box(u0, u1, -s['B'] / 2, s['B'] / 2, 0, s['H1']).fuse(box(u0, u1, -s['B1'] / 2, s['B1'] / 2, 0, s['H']))
    body = soften(body.removeSplitter(), 0.8, chamfer=True)
    cuts = [cyl_u(journal_r, u0 - 1, u1 + 1, 0, a)]
    for v in (-s['P'] / 2, s['P'] / 2):
        for c in s['C']:
            cuts += [cyl_w(s['X'] / 2, -1, s['H1'] + 1, u0 + c, v), cyl_w(s['Y'] / 2, s['H1'] - s['Z'], s['H1'] + 1, u0 + c, v)]
        wb = (s['H1'] - s['E']) / 2
        cuts += [cyl_u(s['d2'] / 2, u0 - 1, u1 + 1, v, w) for w in (wb, wb + s['E'])]
    out = [('', body.cut(cuts), 'black')]
    if s['lock'] and lock_r:
        r, t = s['lock']
        out.append(('LockNut', ring_u(r, lock_r, u1, u1 + t, 0, a), 'black'))
    return out


def coupler(u0, u1, a, bore0, bore1, hub=15.0, r=12.5):
    """D25 L30 beam coupler with blind bores (radius bore0 from u0, bore1 from u1)."""
    c = cyl_u(r, u0, u1, 0, a)
    span = u1 - u0
    grooves = [ring_u(r + 1, r - 4, u0 + span * f - 0.6, u0 + span * f + 0.6, 0, a) for f in (0.38, 0.5, 0.62)]
    screws = [cyl_w(2.2, a + r - 2, a + r + 0.01, u, 0) for u in (u0 + 5, u1 - 5)]
    bores = [cyl_u(bore0, u0 - 1, u0 + hub, 0, a), cyl_u(bore1, u1 - hub, u1 + 1, 0, a)]
    return c.cut(grooves + screws + bores)


def motor_bracket(u0, f, a, half=31.5, plate=8.0):
    """Hollow NEMA 23 bracket from the BK outer face (u0) to the motor face (f).

    Kit brackets bolt to the BK's axial holes; motor face to BK ~45-55 mm (estimated, no
    published drawing).
    """
    b = box(u0, f, -half, half, 0, a + half)
    b = soften(b, 2.0, parallel((1, 0, 0)))
    holes = [cyl_u(2.75, f - plate - 1, f + 1, v, a + w) for v in (-23.57, 23.57) for w in (-23.57, 23.57)]
    b = b.cut([box(u0 - 1, f - plate, -half + 6, half - 6, -1, a + half - 6),
               cyl_u(19.5, f - plate - 1, f + 1, 0, a),
               box(u0 + 6, f - plate - 4, -half - 1, half + 1, a - 11, a + 11)] + holes)
    return b


# StepperOnline factory drawings (omc-stepperonline.com/download/<model>.pdf):
#   flange 57.3 max, holes 47.14 apart, 4x 5.1, pilot 38.1 x 1.6, shaft 21 +/-1 from
#   the mounting face with a D-flat 15 long. Closed-loop models add a 25 mm encoder
#   cover with a cable block on one side at the rear (~35 x 12 proud).
MOTORS = {
    '23HS45-4204D-E1000': dict(sq=57.3, body=113.0, encoder=25.0, shaft_d=8.0, flat=7.5),     # 3.0 Nm closed loop
    '23HS30-5004D-E1000': dict(sq=56.4, body=76.0, encoder=25.0, shaft_d=8.0, flat=7.5),      # 2.0 Nm closed loop
    '23HS30-3004S': dict(sq=57.3, body=76.5, encoder=0.0, shaft_d=6.35, flat=5.85),           # 1.9 Nm open loop
}
SHAFT_LEN = 21.0
PILOT = (19.05, 1.6)


def nema23(f, a, model):
    """NEMA 23 with its mounting face at u = f, shaft toward -u: [(suffix, shape, look)]."""
    s = MOTORS[model]
    h = s['sq'] / 2
    body, enc = s['body'], s['encoder']
    sq = chamfered_square(h, 4.5, a)
    holes = [cyl_u(2.55, f - 1, f + 11, v, a + w) for v in (-23.57, 23.57) for w in (-23.57, 23.57)]
    front = prism_u(sq, f, f + 10).cut(holes)
    stack = prism_u(chamfered_square(h - 0.8, 4.5, a), f + 10, f + body - 10)
    rear = prism_u(sq, f + body - 10, f + body)
    out = [('Caps', front.fuse(rear), 'alu'), ('Body', stack, 'motor')]
    end = f + body
    if enc:
        cover = prism_u(chamfered_square(h, 5.5, a), end, end + enc - 3)
        cap = prism_u(chamfered_square(h - 3, 4.0, a), end + enc - 3, end + enc)
        block = box(end + enc - 35, end + enc - 2, -10, 10, a + h, a + h + 12)
        out.append(('Encoder', cover.fuse([cap, block]), 'motor'))
    else:
        out.append(('Leads', cyl_w(4.0, a + h - 0.01, a + h + 10, end - 20, 0), 'motor'))
    r = s['shaft_d'] / 2
    shaft = cyl_u(r, f - SHAFT_LEN, f - PILOT[1], 0, a)
    shaft = shaft.cut(box(f - SHAFT_LEN - 1, f - SHAFT_LEN + 15, -r - 1, r + 1, a + s['flat'] - r, a + r + 1))
    out += [('Pilot', cyl_u(PILOT[0], f - PILOT[1], f, 0, a), 'alu'), ('Shaft', shaft, 'steel')]
    return out


# --------------------------------------------------------------------------
# Spindle (machine coordinates, axis on Z through x = y = 0)
# --------------------------------------------------------------------------
# GDZ80-2.2 water-cooled spindle (StepperOnline drawings GDZ80-2.2A/B):
#   body 80 x 213; nose stack 20.5 (59 cap x 15 + chamfered 47 dust disc); shaft
#   with 22 AF flats; ER20 nut 30 AF hex, nut tip 60.5 below the body front; rear
#   boss ~43 x 4 with 4 cap screws on a 48 square; 4-pin aviation socket on the
#   axis (plug + clamp ~48 proud); two 13 AF water fittings at +/-12, 32 off axis,
#   ~26 proud, for 4 x 6 hose. Scaled values are +/-1 mm. Measure your own: sellers
#   list 213 / 230 / 240 body lengths.
SPINDLE = dict(d=80.0, body=213.0, nose=20.5, nut_tip=60.5, nut_af=30.0, nut_len=22.0)


def hexagon(af, z0, h, x=0.0, y=0.0):
    r = af / math.sqrt(3)
    pts = [V(x + r * math.cos(math.radians(a)), y + r * math.sin(math.radians(a)), z0) for a in range(0, 420, 60)]
    return Part.Face(Part.makePolygon(pts)).extrude(V(0, 0, h))


def spindle(front, stickout=30.0, flute=18.0):
    """Spindle with its Ø80 body front face at z = front, axis on Z: [(suffix, shape, look)]."""
    S = SPINDLE
    top = front + S['body']
    tip = front - S['nut_tip']
    nut0 = tip
    nut1 = tip + S['nut_len']
    out = [('Flutes', Part.makeCylinder(3.0, flute, V(0, 0, tip - stickout)), 'tin'),
           ('Shank', Part.makeCylinder(3.0, stickout - flute, V(0, 0, tip - stickout + flute)), 'steel')]
    nut = hexagon(S['nut_af'], nut0, S['nut_len'])
    nut = nut.common(Part.makeCylinder(S['nut_af'] / math.sqrt(3) - 0.6, S['nut_len'], V(0, 0, nut0)))
    out.append(('ER20Nut', nut.cut(Part.makeCylinder(3.0, S['nut_len'] + 2, V(0, 0, nut0 - 1))), 'steel'))
    shaft = Part.makeCylinder(12.5, front - S['nose'] - nut1, V(0, 0, nut1))
    shaft = shaft.common(Part.makeBox(22, 40, front, V(-11, -20, nut1)))
    out.append(('Shaft', shaft, 'steel'))
    disc = Part.makeCone(21.0, 23.5, 5.5, V(0, 0, front - S['nose']))
    cap = Part.makeCylinder(29.5, 15.0, V(0, 0, front - 15.0))
    out.append(('Nose', disc.fuse(cap), 'steel'))
    body = Part.makeCylinder(S['d'] / 2, S['body'], V(0, 0, front))
    body = soften(body, 2.0, lambda e: abs(e.Vertexes[0].Point.z - top) < 1e-6, chamfer=True)
    out.append(('Body', body, 'spindle'))
    rear = Part.makeCylinder(21.5, 4.0, V(0, 0, top))
    rear = rear.fuse([Part.makeCylinder(3.5, 4.0, V(x, y, top)) for x in (-24, 24) for y in (-24, 24)])
    out.append(('RearCap', rear, 'steel'))
    conn = Part.makeBox(30, 30, 3, V(-15, -15, top + 4))
    conn = conn.fuse([Part.makeCylinder(10.0, 10, V(0, 0, top + 7)), Part.makeCylinder(13.0, 14, V(0, 0, top + 17)),
                      Part.makeCone(11.0, 6.0, 17, V(0, 0, top + 31))])
    out.append(('Connector', conn, 'motor'))
    for x in (-12, 12):
        fit = hexagon(13, top, 7, x, -32).fuse(Part.makeCylinder(3.0, 19, V(x, -32, top + 7)))
        out.append((f'Water{"L" if x < 0 else "R"}', fit, 'brass'))
    return out


def spindle_clamp(z0, back_y, bore=40.0, wall=10.0, foot_w=148.0, foot_t=14.0, depth=80.0):
    """Cast 80 mm foot clamp (148 W x 80 D, 14 foot, bore center 50 off the foot).

    Foot bolts to the Z plate at y = back_y; the split and 3x M8 clamp bolts face front.
    Ref: 80 mm cast spindle bracket drawing, cnconline.co.za/products/80mm-spindle-bracket.
    """
    r = bore + wall
    foot = soften(Part.makeBox(foot_w, foot_t, depth, V(-foot_w / 2, back_y - foot_t, z0)), 3.0, parallel((0, 0, 1)))
    webs = Part.makeBox(2 * r, r, depth, V(-r, back_y - r, z0))
    lug = Part.makeBox(32, 20, depth, V(-16, -r - 18, z0))
    c = foot.fuse([Part.makeCylinder(r, depth, V(0, 0, z0)), webs, lug])
    bolts_z = (z0 + 15, z0 + depth / 2, z0 + depth - 15)
    cuts = [Part.makeCylinder(bore, depth + 2, V(0, 0, z0 - 1)),
            Part.makeBox(3, r + 2, depth + 2, V(-1.5, -r - 20, z0 - 1))]
    cuts += [Part.makeCylinder(4.25, 40, V(-20, -r - 8, z), V(1, 0, 0)) for z in bolts_z]
    for x in (-foot_w / 2 + 12, foot_w / 2 - 12):
        for z in (z0 + 18, z0 + depth - 18):
            cuts += [Part.makeCylinder(3.4, foot_t + 2, V(x, back_y - foot_t - 1, z), V(0, 1, 0)),
                     Part.makeCylinder(5.5, 6, V(x, back_y - foot_t - 1, z), V(0, 1, 0))]
    c = c.cut(cuts).removeSplitter()
    heads = Part.makeCompound([Part.makeCylinder(6.5, 8.0, V(16, -r - 8, z), V(1, 0, 0)) for z in bolts_z])
    return [('', c, 'black'), ('Bolts', heads, 'steel')]


# --------------------------------------------------------------------------
# Enclosure hardware
# --------------------------------------------------------------------------
def tslot20(length):
    """2020 T-slot (Misumi HFS5-2020: 6 slot, 2 lip, 4 deep cavity 12 wide, 4.2 bore, R1) along u."""
    s = soften(box(0, length, -10, 10, -10, 10), 1.0, parallel((1, 0, 0)))
    cuts = [cyl_u(2.1, -1, length + 1)]
    for ang in (0, 90, 180, 270):
        for c in (box(-1, length + 1, -3.0, 3.0, 7.9, 10.5),
                  prism_u([(-6.0, 8.0), (6.0, 8.0), (2.0, 4.0), (-2.0, 4.0)], -1, length + 1)):
            c.rotate(V(0, 0, 0), V(1, 0, 0), ang)
            cuts.append(c)
    return s.cut(cuts)


def leveling_foot(x, y, z_top, h=20.0):
    pad = Part.makeCylinder(20.0, 6.0, V(x, y, z_top - h))
    hexnut = Part.makeCylinder(9.5, 6.0, V(x, y, z_top - h + 8), V(0, 0, 1), 360)
    stud = Part.makeCylinder(6.0, h - 6.0, V(x, y, z_top - h + 6))
    return [('Pad', pad, 'rubber'), ('Stud', stud.fuse(hexnut), 'steel')]


# --------------------------------------------------------------------------
# Coolant, covers and cable chain
# --------------------------------------------------------------------------
def _scaled(v, f):
    return V(v.x * f, v.y * f, v.z * f)


def hose(points, r):
    """Hose along a polyline, with rounded bends."""
    pts = [V(*p) for p in points]
    solids = [Part.makeSphere(r, p) for p in pts[1:-1]]
    for a, b in zip(pts, pts[1:]):
        d = b - a
        if d.Length > 1e-6:
            solids.append(Part.makeCylinder(r, d.Length, a, d))
    return solids[0].multiFuse(solids[1:]).removeSplitter() if len(solids) > 1 else solids[0]


def loc_line(points, r=5.5, step=8.5):
    """Segmented ball-joint coolant hose (Loc-Line style) ending in a round nozzle."""
    pts = [V(*p) for p in points]
    balls = []
    for a, b in zip(pts, pts[1:]):
        d = b - a
        n = max(1, int(d.Length // step))
        balls += [Part.makeSphere(r, a + _scaled(d, i / n)) for i in range(n)]
    tip = pts[-1] - pts[-2]
    tip.normalize()
    nozzle = Part.makeCone(r * 0.8, 1.6, 12.0, pts[-1], tip)
    return balls[0].multiFuse(balls[1:] + [nozzle])


def roll_cover(x0, x1, y, z, floor, r=18.0, feet=()):
    """Spring roller for a roll-up way cover, axis along x, with end brackets down to the floor.
    feet: (x, y, wx, wy) 5 mm tabs on the floor, each with an M5 clearance hole at (x, y)."""
    drum = cyl_u(r, x0, x1, y, z)
    for xa, xb in ((x0 - 6, x0), (x1, x1 + 6)):
        drum = drum.fuse(box(xa, xb, y - r - 2, y + r + 2, floor, z + r))
    for fx, fy, wx, wy in feet:
        tab = box(fx - wx / 2, fx + wx / 2, fy - wy / 2, fy + wy / 2, floor, floor + 5.0)
        drum = drum.fuse(tab.cut(Part.makeCylinder(2.75, 7.0, V(fx, fy, floor - 1))))
    return drum


def chain_link(P=20.0, W=38.0, H=21.0, t=2.4, inner_layer=False):
    """Drag-chain link (simplified) between pins at x = 0 and x = P; y across, z up.

    Alternate links sit on the inner/outer layer so neighbours overlap at the pins.
    """
    r = H / 2
    y_out = W / 2 - (t if inner_layer else 0.0)
    parts_ = []
    for sy in (-1, 1):
        y0, y1 = sorted((sy * (y_out - t), sy * y_out))
        parts_.append(box(0, P, y0, y1, -r, r).fuse([cyl_v(r, y0, y1, 0, 0), cyl_v(r, y0, y1, P, 0)]))
    yb = W / 2 - t
    parts_ += [box(P / 2 - 4, P / 2 + 4, -yb, yb, r - 2.5, r), box(P / 2 - 4, P / 2 + 4, -yb, yb, -r, -r + 2.5)]
    parts_.append(cyl_v(2.5, -W / 2 - 0.6, W / 2 + 0.6, P, 0))
    return parts_[0].multiFuse(parts_[1:])


def steam_pan(cx, y0, z0, L, W, D, rim=12.0, t=1.2, perforated=False):
    """Stainless steam-table (gastronorm-style) pan: rim L x W at the top, body tapered 1:10,
    depth D. L along y from y0, W across x centerd on cx, standing on z0."""
    top, taper = z0 + D, D * 0.1

    def rect(inset, z):
        xa, ya, yb = W / 2 - inset, y0 + inset, y0 + L - inset
        return Part.Wire(Part.makePolygon([V(cx - xa, ya, z), V(cx + xa, ya, z), V(cx + xa, yb, z),
                                           V(cx - xa, yb, z), V(cx - xa, ya, z)]))
    outer = Part.makeLoft([rect(rim + taper, z0), rect(rim, top)], True)
    inner = Part.makeLoft([rect(rim + taper + t, z0 + t), rect(rim + t, top + 1)], True)
    flange = soften(box(cx - W / 2, cx + W / 2, y0, y0 + L, top - 2.0, top), 15.0, parallel((0, 0, 1)))
    pan = outer.fuse(flange).cut(inner)
    if perforated:
        nx, ny = int((W - 2 * (rim + taper)) / 16) - 1, int((L - 2 * (rim + taper)) / 16) - 1
        holes = [Part.makeCylinder(3.0, 4.0, V(cx + 16.0 * (i - (nx - 1) / 2), y0 + L / 2 + 16.0 * (j - (ny - 1) / 2), z0 - 1))
                 for i in range(nx) for j in range(ny)]
        pan = pan.cut(Part.makeCompound(holes))
    return pan


def coolant_sump(cx, y0, z0, L=527.0, W=324.0, D=101.6):
    """Slide-out sump under the base: a full-size 4 in stainless steam-table pan (~13 L).

    Front to back (+y): 1/3-size perforated pan as the chip basket (under the drain), a magnet
    bar on the floor, an underflow baffle (3 mm ACM offcut), a 100 um filter screen in a printed
    frame, then the clean end with a 24 V brushless submersible pump (no mains in the coolant). Origin: front of the rim at y0,
    centerd on cx, standing on z0. Returns (parts, pump outlet).
    """
    top = z0 + D
    out = [('Pan', steam_pan(cx, y0, z0, L, W, D), 'steel')]
    out.append(('ChipBasket', steam_pan(cx, y0, top - 63.5 + 2.0, 176.0, W, 63.5, perforated=True), 'mesh'))
    fl = z0 + 1.5
    out.append(('Magnet', cyl_u(12.5, cx - 50.0, cx + 50.0, y0 + 200.0, fl + 12.5), 'steel'))   # 100 x 25 bar
    def plate(y, z_a, z_b, t=4.0):
        w = W - 2 * 12.0 - 4.0
        return box(cx - w / 2, cx + w / 2, y, y + t, z_a, z_b)
    out.append(('Baffle', plate(y0 + 235.0, fl + 25.0, top - 2.0, 3.0), 'acm'))
    screen = plate(y0 + 275.0, fl + 6.0, top - 2.0, 6.0).cut(
        box(cx - W / 2 + 40, cx + W / 2 - 40, y0 + 274.0, y0 + 282.0, fl + 18.0, top - 14.0))
    out.append(('FilterFrame', screen, 'printed'))
    out.append(('FilterScreen', box(cx - W / 2 + 40, cx + W / 2 - 40, y0 + 277.5, y0 + 278.5, fl + 18.0, top - 14.0), 'filter'))
    py = y0 + L - 110.0
    # 24 V brushless submersible pump (~800 L/h, 5 m), ~80 x 50 x 55
    pump = soften(box(cx - 50.0, cx, py - 40.0, py + 40.0, fl, fl + 55.0), 10.0, parallel((0, 0, 1)))
    pump = pump.fuse(Part.makeCylinder(6.0, top + 14.0 - (fl + 55.0), V(cx - 25.0, py, fl + 55.0)))
    out.append(('Pump', pump, 'motor'))
    return out, V(cx - 25.0, py, top + 14.0)    # pump outlet
