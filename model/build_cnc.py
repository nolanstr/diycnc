"""Parametric layout model of a fixed-gantry, epoxy-granite desktop CNC mill.

Target envelope is the Shariff DMC2 Mini (12 x 7 x 5.5 in travel). The long
axis rides on the table so the gantry beam stays short and stiff. Component
geometry (rails, blocks, ballscrew hardware, motors, spindle) lives in parts.py.
The frame is five bolt-together epoxy-granite castings with cast-in steel, and the
enclosure bolts to the base top.

Headless (collision check, docs/report.txt and the print/ STLs):
    /Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd model/build_cnc.py
In the FreeCAD GUI (also rebuilds the colored DIYCNC.FCStd and DIYCNC.step):
    Macro > Macros... > select model/build_cnc.py > Execute

Edit P below and re-run. In the GUI, jog the axes and open the door by editing
posX / posY / posZ / doorAngle in the Params spreadsheet.

Coordinates: X right, Y toward the back (operator stands at -Y), Z up.
Origin is on the casting's underside directly below the spindle axis with all
axes at home (X and Y centered, Z fully up).
"""

import importlib
import itertools
import math
import os
import subprocess
import sys

import FreeCAD as App
import Part
from FreeCAD import Matrix, Vector

try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:
    HERE = os.getcwd()
ROOT = os.path.dirname(HERE)          # repository root: docs/, renders/, print/ live here
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import moulds  # noqa: E402
import parts  # noqa: E402

importlib.reload(parts)  # pick up edits when re-run inside one GUI session
importlib.reload(moulds)

# --------------------------------------------------------------------------
# Parameters (mm)
# --------------------------------------------------------------------------
P = dict(
    # Work envelope
    travel_x=180.0,      # spindle along the beam
    travel_y=300.0,      # table front/back
    travel_z=140.0,
    work_clear=160.0,    # table top -> collet nut tip, Z at top (DMC2: 6.25 in table to spindle)
    beam_clear=180.0,    # table top -> underside of beam

    riser_w=31.75,       # 1-1/4 in cold-rolled steel flat bar under every rail

    # Table axis (Y): new HGR15 rails + SFU1605
    # Rails at the length they're sold in (2 x 600 mm kit, no cutting), shifted back 20 mm so
    # the front ends stay clear of the coolant trough.
    table_rail_len=600.0, table_rail_y=20.0, table_rail_spacing=180.0, table_blk_pitch=150.0,
    table_screw_len=550.0, table_riser_t=19.05,   # 3/4 in risers clear the 43 mm BK12
    table_len=320.0, table_w=260.0, table_t=19.05, table_hole_pitch=25.0,

    # Beam axis (X): owned HGR15-400 pair + SFU1204-400 kit
    beam_rail_len=400.0, beam_rail_spacing=100.0, beam_blk_pitch=100.0,
    beam_screw_len=400.0, beam_riser_t=15.875,    # 5/8 in risers clear the 39 mm BK10
    carriage_w=170.0, carriage_t=15.875,

    # Z axis: moving-rail (blocks fixed to the carriage), HGR15-300 + SFU1204-300
    z_rail_len=300.0, z_rail_spacing=100.0, z_blk_pitch=80.0,
    z_screw_len=300.0, z_nut_on_plate=230.0, z_riser_t=15.875,
    zplate_w=150.0, zplate_t=15.875,     # clamp foot is 148 wide

    # Motors (parts.MOTORS): closed loop on X/Y, the owned open-loop NEMA 23 on Z
    motor_x='23HS30-5004D-E1000', motor_y='23HS30-5004D-E1000', motor_z='23HS30-3004S',

    # Epoxy-granite castings: base (front + rear halves), two uprights, beam
    # The base's underside pockets follow a topology optimization (analysis/, see base_pockets).
    base_h=110.0, base_corner_r=40.0, base_split_y=0.0, split_wall=15.0,
    base_core_skin=25.0,    # top skin over the pockets
    base_girder_w=80.0,     # full-depth girder under each table rail, rail tube in the middle
    base_tie=90.0,          # full-depth tie between the girders, this far either side of the split
    base_front_wall=70.0,   # the coolant trough and outlet run through it
    # Uprights are raked buttresses (from the frame topology optimization, analysis/): the foot runs
    # forward along the base and the front face slopes up to just ahead of the beam.
    upright_t=80.0, upright_d=180.0, upright_front=40.0,
    upright_foot=290.0, upright_top_front=70.0,   # foot front / top front, mm ahead of the beam face
    upright_nose=20.0, upright_nose_r=12.0,       # blunt toe: vertical nose, rounded into the slope
    front_tie_rods=(60.0, 160.0),                 # extra tie rods, mm behind the foot's front edge
    beam_d=140.0, beam_h=140.0, beam_back_r=40.0, edge_r=6.0,   # beam as deep as the upright tops
    # Outside edge rounds (quarter-round strips in the mould corners): castings' outer edges,
    # the beam's lower back edge (meets the uprights' back faces) and its rail-face edges
    round_r=10.0, beam_back_low_r=10.0, beam_face_r=3.0,

    # Cast-in steel and joints (tube = (size, wall)): US stock sizes in stock lengths, so
    # nothing is cut to length: 2 x 2 x 1/8 in and 1-1/2 x 1-1/2 x 1/8 in mild steel.
    frame_tube=(50.8, 3.175), post_tube=(38.1, 3.175),
    # Bought lengths, nothing cut: 12 in base (the split sockets), 18 in beam, 12 in posts, 6 in spigots.
    tube_len=dict(base=304.8, beam=457.2, post=304.8, spigot=152.4),
    # Printed PETG sleeves take up the clearance: socket liners (cast in, posts slide in),
    # spigot sleeves (1-1/2 in spigot in the 2 in tube); (outer size, wall)
    socket_liner=(44.5, 3.0), socket_depth=80.0, spigot_sleeve=70.0,
    # Legs: 6 in pieces of the 1-1/2 in tube cast into the base corners, with threaded inserts
    # for the leveling feet. The coolant sump slides in underneath, between them.
    leg_len=152.4, leg_embed=35.0, leg_inset=35.0,
    # O-ring cord seals at the epoxy-to-epoxy joints: the faces still bear on each other,
    # the cord sits in a groove (3 mm cord, 4 x 2.3 groove = ~25 % squeeze)
    gasket_cord=3.0, gasket_groove=(4.0, 2.3), gasket_split_z=92.0,
    # Joint hardware in hardware-store inch sizes: 1/2-13 rod, couplers and nuts, 3/8-16 grade 8
    # beam bolts, 3/8 in dowels.
    top_plate_t=10.0, tie_rod_d=12.7, beam_bolt_d=9.525, dowel_d=9.525,
    # Cast-in threaded inserts (thread, outer diameter, length): the risers are bedded in epoxy
    # AND held down by counterbored low-head M5 screws under the rail; the BK/BF supports bolt
    # straight into M6 inserts. Nothing bolts to the cast-in tubes.
    # On the beam face the X BK/BF sit over the front beam tube, so they bolt to steel pads
    # (1/4 x 2-1/2 in flat bar, tapped M6) cast flush into the face against the tube.
    insert_m5=(5.0, 8.0, 12.0), insert_m6=(6.0, 10.0, 15.0), riser_cbore=(9.5, 4.5),
    support_pad=(6.35, 63.5),
    side_clear=10.0,

    # Spindle: GDZ80-2.2 water-cooled, ER20, in the 80 mm cast foot clamp (bore 50 off the foot)
    clamp_off=50.0, clamp_lift=5.0, tool_stickout=30.0,

    # Enclosure: 2020 frame bolted to the base top, 4 mm polycarbonate, lift-up front door.
    # The base footprint matches the enclosure; its sealed top is the coolant floor.
    foot_h=20.0, enc_clear=15.0, panel_t=4.0, door_lap=30.0,
    motor_cutout=72.0,

    eg_density=2.35,     # kg/L, epoxy granite
    # The beam and uprights use aluminium oxide grit instead of sand, same volume: brown #16 for the
    # coarse sand, black 70 grit for the fine sand (analysis/alumina.py).
    # (name, share of the sand mix by weight, density relative to sand)
    alumina_castings=('Upright', 'Beam'),
    alumina=(('brown #16 (coarse sand)', 0.275, 3.95 / 2.65), ('black 70 grit (fine sand)', 0.15, 3.75 / 2.65)),
    eg_epoxy_frac=0.085,  # epoxy mass fraction, with well-graded aggregate + whiting (calcium carbonate) fines;
                          # check it with the jar test and test bars (build guide)
)

# rgb, shininess (0..1), transparency (0..100)
LOOKS = {
    'granite': ((0.22, 0.22, 0.24), 0.05, 0),
    'steeltube': ((0.36, 0.38, 0.42), 0.35, 0),
    'alu': ((0.80, 0.81, 0.84), 0.45, 0),
    'steel': ((0.62, 0.64, 0.68), 0.70, 0),
    'black': ((0.13, 0.13, 0.14), 0.30, 0),
    'motor': ((0.09, 0.09, 0.10), 0.20, 0),
    'seal': ((0.70, 0.12, 0.10), 0.20, 0),
    'brass': ((0.80, 0.62, 0.30), 0.60, 0),
    'spindle': ((0.86, 0.87, 0.89), 0.60, 0),
    'tin': ((0.86, 0.68, 0.22), 0.70, 0),
    'rubber': ((0.08, 0.08, 0.08), 0.00, 0),
    'granite_hi': ((0.62, 0.63, 0.65), 0.05, 0),  # lighter castings in the frame-only renders
    'gasket_hi': ((0.10, 0.45, 1.00), 0.10, 0),   # gaskets highlighted in the frame renders
    'extrusion': ((0.17, 0.17, 0.18), 0.35, 0),
    'panel': ((0.70, 0.82, 0.92), 0.80, 72),
    'acm': ((0.80, 0.81, 0.82), 0.25, 0),
    'tank': ((0.88, 0.89, 0.90), 0.20, 35),
    'mesh': ((0.70, 0.72, 0.75), 0.50, 45),
    'filter': ((0.95, 0.95, 0.90), 0.00, 20),
    'hose': ((0.20, 0.45, 0.80), 0.30, 0),
    'drainhose': ((0.85, 0.86, 0.80), 0.30, 30),
    'locline': ((0.15, 0.32, 0.72), 0.30, 0),
    'printed': ((0.95, 0.45, 0.10), 0.25, 0),
    'printed_dark': ((0.22, 0.22, 0.24), 0.05, 0),   # printed in dark grey to match the castings (pocket caps)
    'shim': ((0.80, 0.81, 0.84), 0.85, 0),
    'wood': ((0.74, 0.58, 0.40), 0.10, 0),
}
SHADED = ('granite',)   # drawn without edge lines


class Frame:
    """Local coordinates: u along the axis, v across it, w away from the mounting face."""

    def __init__(self, origin, u, v):
        u, v, o = Vector(*u), Vector(*v), Vector(*origin)
        w = u.cross(v)
        self.m = Matrix(u.x, v.x, w.x, o.x,
                        u.y, v.y, w.y, o.y,
                        u.z, v.z, w.z, o.z,
                        0, 0, 0, 1)

    def place(self, s):
        s = s.copy()
        s.transformShape(self.m)
        return s


class Model:
    def __init__(self):
        self.parts = []
        self.bom = []
        self.cutlist = []
        self.dims = {}
        self.warnings = []
        self.frame_container = 'FrameBaseRear'
        self.dynamic = []
        self.structure = set()   # castings, cast-in steel, joint hardware, gaskets
        self.anchors = []        # (point on the casting face, unit normal out of it, insert)

    def add_dynamic(self, name, look, fn, container, touches=()):
        """A part whose shape depends on the axis positions: fn(x, y, z) -> shape or None.

        Way covers, the cable chain and the nozzle hose. `touches` names parts it is
        attached to (ignored by the collision check).
        """
        self.dynamic.append(dict(name=name, look=look, fn=fn, container=container, touches=set(touches)))

    def add(self, name, group, shape, look, comp=None, container=None, proxy=None):
        """proxy: smaller shapes used instead of `shape` by the collision check (hollow or sprawling parts).

        Fixed ('frame') parts without a container go to frame_container: the casting they bolt to.
        """
        if container is None and group == 'frame':
            container = self.frame_container
        self.parts.append(dict(name=name, group=group, shape=shape, look=look, comp=comp or name,
                               container=container, proxy=proxy or [shape]))

    def add_all(self, prefix, group, pieces, place=None, container=None):
        for suffix, shape, look in pieces:
            self.add(prefix + suffix, group, place(shape) if place else shape, look, comp=prefix, container=container)


# --------------------------------------------------------------------------
# Axes
# --------------------------------------------------------------------------
def riser_holddowns(length, pitch=60.0, end=20.0):
    """Hold-down screw positions along a rail: midway between rail screws, from each end inward
    every 120 mm (mirrored), so they sit under the rail between its own screws."""
    n = int((length - 2 * end) // pitch) + 1
    last = (n - 1) * pitch / 2 - pitch / 2         # outermost midpoint
    us = []
    u = last
    while u > -1e-6:
        us += [u, -u] if u > 1e-6 else [0.0]
        u -= 2 * pitch
    return sorted(us)


def rail_pair(m, f, tag, t, length, spacing, blk_pitch, rail_group, blk_group, rail_u0=0.0, blk_u0=0.0):
    for side, v in (('L', -spacing / 2), ('R', spacing / 2)):
        u0, u1 = rail_u0 - length / 2, rail_u0 + length / 2
        riser = parts.plate(u0, u1, v - P['riser_w'] / 2, v + P['riser_w'] / 2, 0, t, 0.6)
        if rail_group == 'frame':
            # counterbored M5 hold-downs into cast-in inserts; the heads sit below the rail
            cb_d, cb_h = P['riser_cbore']
            for u in riser_holddowns(length):
                uu = rail_u0 + u
                riser = riser.cut([parts.cyl_w(2.75, -1, t + 1, uu, v), parts.cyl_w(cb_d / 2, t - cb_h, t + 1, uu, v)])
                m.anchors.append((f.m.multVec(Vector(uu, v, 0)), f.m.multVec(Vector(0, 0, 1)) - f.m.multVec(Vector(0, 0, 0)),
                                  'insert_m5'))
        m.add(f'{tag}_Riser{side}', rail_group, f.place(riser), 'steeltube')
        m.add(f'{tag}_Rail{side}', rail_group, f.place(parts.hgr15_rail(length).translated(Vector(rail_u0, v, t))), 'steel')
        for i, du in enumerate((-blk_pitch / 2, blk_pitch / 2)):
            off = Vector(blk_u0 + du, v, t)
            m.add_all(f'{tag}_Block{side}{i + 1}', blk_group, parts.hgh15_block(), lambda s: f.place(s.translated(off)))


def screw_axis(m, f, tag, kind, length, u0, bf, bk, fixed_group, nut_group, nut_u, carrier_w, motor_min_u, motor):
    """Ballscrew, BF/BK supports, coupler, bracket and motor on fixed_group; nut + housing on nut_group.

    u0 is the BF outer face; length is the overall machined screw length. The nut housing
    bolts under the moving part at w = carrier_w. Returns the motor face position along u.
    """
    a = parts.SUPPORT[bk]['h']
    e = parts.ENDS[kind]
    place = f.place
    screw, u1, s0, s1 = parts.ballscrew(kind, u0, length, bf, bk, a)
    m.add(f'{tag}_Screw', fixed_group, place(screw), 'steel')
    m.add_all(f'{tag}_{bf}', fixed_group, parts.support(bf, u0, a, e['bf_a'] / 2), place)
    m.add_all(f'{tag}_{bk}', fixed_group, parts.support(bk, u1 - parts.SUPPORT[bk]['L'], a, e['bk_a'] / 2,
                                                        lock_r=e['bk_a'] / 2), place)
    if fixed_group == 'frame':
        # BK/BF bolt into M6 inserts cast into the base top / beam face
        n = f.m.multVec(Vector(0, 0, 1)) - f.m.multVec(Vector(0, 0, 0))
        for sup, us in ((bf, u0), (bk, u1 - parts.SUPPORT[bk]['L'])):
            sp = parts.SUPPORT[sup]
            for c in sp['C']:
                for v in (-sp['P'] / 2, sp['P'] / 2):
                    m.anchors.append((f.m.multVec(Vector(us + c, v, 0)), n, 'insert_m6'))

    # The motor shaft (21 long) reaches 15 into the 30 mm coupler that sits on the stub.
    c0 = s0
    face = max(c0 + 30.0 + parts.SHAFT_LEN - 15.0, motor_min_u)
    c1 = face - (parts.SHAFT_LEN - 15.0)
    if c1 - c0 > 30.5:
        m.warnings.append(f'{tag}: motor pushed out to clear the moving parts; needs a {c1 - c0:.0f} mm '
                          f'coupler or a {length + c1 - c0 - 30:.0f} mm screw')
    shaft_r = parts.MOTORS[motor]['shaft_d'] / 2
    m.add(f'{tag}_Coupler', fixed_group, place(parts.coupler(c0, c1, a, e['stub'] / 2, shaft_r)), 'alu')
    m.add(f'{tag}_MotorBracket', fixed_group, place(parts.motor_bracket(u1, face, a)), 'black')
    m.add_all(f'{tag}_Motor', fixed_group, parts.nema23(face, a, motor), place)

    m.add(f'{tag}_Nut', nut_group, place(parts.sfu_nut(kind, nut_u, a)), 'steel')
    m.add_all(f'{tag}_NutHousing', nut_group, parts.nut_housing(kind, nut_u, a, carrier_w), place)
    return face


def fillet_safe(shape, radii, pred):
    """Fillet with the first radius OCC accepts."""
    for r in radii:
        out = parts.soften(shape, r, pred)
        if out is not shape:
            return out
    return shape


def on_z(z):
    return lambda e: all(abs(v.Point.z - z) < 1e-6 for v in e.Vertexes)


def on_y(y):
    return lambda e: all(abs(v.Point.y - y) < 1e-6 for v in e.Vertexes)


def hex_y(af, x, y0, length, z):
    """Hex prism (nut) along +y from y0."""
    h = parts.hexagon(af, 0.0, length)
    h.rotate(Vector(0, 0, 0), Vector(1, 0, 0), -90)
    h.translate(Vector(x, y0, z))
    return h


def frame_layout(d):
    """Positions shared by the castings, the cast-in steel and the joints."""
    g = dict(d)
    g['ux'] = (d['inner'] + d['outer']) / 2                    # upright centre line
    g['sock_bot'] = d['base_top'] - P['socket_depth']
    g['post_ys'] = (d['up_y0'] + 35.0, d['up_y1'] - 35.0)
    g['rod_y'] = (d['up_y0'] + d['up_y1']) / 2                 # upright tie rods
    g['pocket_bot'] = d['beam_bot'] - 18.0                     # tie-rod nut pocket floor
    g['up_front'] = d['beam_face'] - P['upright_foot']         # front of the upright foot
    g['up_top_front'] = d['beam_face'] - P['upright_top_front']
    toe = d['base_top'] + P['upright_nose']
    slope = lambda y: toe + (y - g['up_front']) / (g['up_top_front'] - g['up_front']) * (d['beam_bot'] - toe)
    # tie rods (x from the centre line outward, y, nut-pocket floor): two at the top, two through the slope
    g['tie_rods'] = [(g['ux'] - 20.0, g['rod_y'], g['pocket_bot']), (g['ux'] + 20.0, g['rod_y'], g['pocket_bot'])]
    # (the sloped pockets go 38 mm deep, so a printed cap closes them flush over the nut)
    g['tie_rods'] += [(g['ux'], g['up_front'] + dy, slope(g['up_front'] + dy) - 38.0) for dy in P['front_tie_rods']]
    g['bolt_xs'] = (g['ux'] - 22.0, g['ux'] + 22.0)            # beam cap screws
    g['bolt_ys'] = (d['beam_face'] + 25.0, d['beam_face'] + P['beam_d'] - 25.0)
    g['beam_dowel_y'] = d['beam_face'] + 70.0
    g['tube_z'] = 42.5                                         # rail tubes: 17 mm of casting under them
    g['split'] = P['base_split_y']
    g['draw_x'] = d['base_half'] - 20.0                        # base draw rods, in the side walls
    g['outlet'] = (0.0, d['base_y0'] + 30.0)                   # coolant drain (x, y): straight down into the sump
    g['legs'] = [(sx * (d['base_half'] - P['leg_inset']), y)
                 for y in (d['base_y0'] + P['leg_inset'], d['base_y1'] - P['leg_inset']) for sx in (-1, 1)]
    g['gasket_len'] = 0.0
    g['draw_z'] = 55.0
    return g


class Steel:
    """Collects cast-in steel and joint hardware for the mass total."""

    def __init__(self, m):
        self.m, self.volume = m, 0.0

    def add(self, name, container, shape, look='steeltube'):
        self.m.add(name, 'frame', shape, look, container=container)
        self.m.structure.add(name)
        if look != 'printed':
            self.volume += shape.Volume

    def plug(self, name, container, axis, c1, c2, size, a0, a1):
        """Printed end plug that keeps the casting out of a hollow tube."""
        env, _ = parts.square_tube(axis, c1, c2, size - 2.0, 0.1, a0, a1)
        self.add(name, container, env, 'printed')


def chamfered(x0, x1, y0, y1, c):
    """Rectangle outline (x, y) with 45-degree corner chamfers c."""
    return [(x0 + c, y0), (x1 - c, y0), (x1, y0 + c), (x1, y1 - c), (x1 - c, y1), (x0 + c, y1), (x0, y1 - c), (x0, y0 + c)]


def base_pockets(g):
    """Underside pockets of the base: (outline [(x, y), ...], pocket top z, name). All open to the
    bottom, so the cores (printed shells or foam) pull straight out.

    The layout follows the topology optimization in analysis/ (see the design notes): two full-depth girders
    under the table rails, a full-depth tie between them behind the split, solid knees from
    the girders out to the upright sockets, and thin skin nearly everywhere else.
    """
    top, half, y0, y1 = g['base_top'], g['base_half'], g['base_y0'], g['base_y1']
    zp = top - P['base_core_skin']
    s2, gw = P['table_rail_spacing'] / 2, P['base_girder_w'] / 2
    gi, go = s2 - gw, s2 + gw                       # girder inner and outer faces
    yf0, yf1 = y0 + P['base_front_wall'], g['split'] - P['split_wall']
    tie = g['split'] + P['base_tie']
    ry = g['rod_y']
    foot = g['up_front']             # the upright feet stand on full-depth casting from here back
    out = [(chamfered(-gi, gi, yf0, g['split'] - P['base_tie'], 10.0), zp, 'centre'),   # front, between the girders
           (chamfered(-gi, gi, tie, 245.0, 30.0), zp, 'centre')]        # rear, between the girders
    for sx in (-1, 1):
        side = [
            # front, outboard: stops short of the upright foot, which stands on full-depth casting
            (chamfered(go, half - 40.0, yf0, foot - 20.0, 10.0), zp, 'outboard'),
            (chamfered(go + 5.0, 236.0, y0 + 15.0, yf0, 10.0), 40.0, 'trough-band'),      # under the coolant trough band
            (chamfered(half - 45.0, half - 8.0, yf0, yf1 - 5.0, 8.0), 40.0, 'draw-rod'),  # under the front draw rods
            (chamfered(go, g['inner'] - 5.0, tie, 318.0, 10.0), 40.0, 'knee'),            # under the knee, inboard of the sockets
            (chamfered(g['outer'] - 8.0, half - 8.0, 60.0, ry - 32.0, 8.0), 65.0, 'outer-a'),   # outboard of the sockets,
            (chamfered(g['outer'] - 8.0, half - 8.0, ry + 32.0, 312.0, 8.0), 65.0, 'outer-b'),  # either side of the coupler
            (chamfered(60.0, 230.0, 318.0, y1 - 10.0, 10.0), zp, 'rear'),                 # behind the sockets
        ]
        for poly, z, name in side:
            pts = [(sx * x, y) for x, y in poly]
            out.append((pts if sx > 0 else pts[::-1], z, f"{name}-{'R' if sx > 0 else 'L'}"))
    return out


def base_envelope(g, front, edges=True):
    """Outside shape of a base half, before any cuts (the mould cavity). edges=False leaves off the
    small edge rounds (the mould fillers only need the big corner radii)."""
    half, base_top, ys = g['base_half'], g['base_top'], g['split']
    ya, yb = (g['base_y0'], ys) if front else (ys, g['base_y1'])
    outer_y = ya if front else yb
    blk = parts.box(-half, half, ya, yb, 0, base_top)
    blk = parts.soften(blk, P['base_corner_r'], lambda e: parts.parallel((0, 0, 1))(e) and on_y(outer_y)(e))
    if not edges:
        return blk
    blk = fillet_safe(blk, (P['round_r'], P['edge_r'], 3.0), lambda e: on_z(base_top)(e) and not on_y(ys)(e))
    return fillet_safe(blk, (2.0,), lambda e: on_z(0.0)(e) and not on_y(ys)(e))


def base_top_formers(g, front):
    """Recesses in a base half's top face (named solids): the side gutters, the coolant trough
    (front) and the table-motor relief (rear). Cut from the casting; printed as mould formers."""
    half, base_top, ys = g['base_half'], g['base_top'], g['split']
    ya, yb = (g['base_y0'], ys) if front else (ys, g['base_y1'])
    out = []
    # Coolant floor: a trough across the front, falling toward the outlet, fed by side gutters
    # that run between the uprights and the enclosure walls.
    gx0, gx1 = half - 35.0, half - 20.0
    gy0, gy1 = g['base_y0'] + 20.0, g['base_y1'] - 20.0
    side = [(gy0, base_top + 1), (gy0, base_top - 15), (gy1, base_top - 8), (gy1, base_top + 1)]
    for sx in (-1, 1):
        xa = min(sx * gx0, sx * gx1)
        gutter = Part.Face(Part.makePolygon([Vector(xa, y, z) for y, z in side] + [Vector(xa, *side[0])])).extrude(
            Vector(gx1 - gx0, 0, 0))
        out.append((f"gutter-{'R' if sx > 0 else 'L'}", gutter.common(parts.box(-half, half, ya, yb, 0, base_top + 1))))
    if front:
        ox = g['outlet'][0]
        trough = [(-gx1, base_top + 1), (-gx1, base_top - 15), (ox, base_top - 25), (gx1, base_top - 18), (gx1, base_top + 1)]
        out.append(('trough', Part.Face(Part.makePolygon([Vector(x, gy0, z) for x, z in trough] +
                                                         [Vector(trough[0][0], gy0, trough[0][1])])).extrude(Vector(0, 35.0, 0))))
    else:
        # relief under the table motor, which hangs off the back below the base top
        c = P['motor_cutout'] / 2
        out.append(('motor-relief', parts.box(-c, c, g['y_bk'], yb + 1, base_top - 8, base_top + 1)))
    return out


def base_half(m, g, st, front):
    """Front or rear half of the base. The halves meet at y = split: two 40x40 spigots
    slide inside the rail tubes and two 1/2-13 draw rods pull the front half onto the rear."""
    half, base_top, ys = g['base_half'], g['base_top'], g['split']
    ya, yb = (g['base_y0'], ys) if front else (ys, g['base_y1'])
    tag, cont = ('Front', 'FrameBaseFront') if front else ('Rear', 'FrameBaseRear')
    blk = base_envelope(g, front)

    s2 = P['table_rail_spacing'] / 2
    cuts = []
    for poly, z_top, _ in base_pockets(g):
        if (sum(y for _, y in poly) / len(poly) < ys) == front:
            face = Part.Face(Part.makePolygon([Vector(x, y, -1) for x, y in poly + poly[:1]]))
            cuts.append(face.extrude(Vector(0, 0, z_top + 1)))

    tube_s, tube_w = P['frame_tube']
    spig_s, spig_w = P['post_tube']
    inner = tube_s - 2 * tube_w
    tl, sl, sv = P['tube_len']['base'], P['tube_len']['spigot'], P['spigot_sleeve']
    ta, tb = (ys - tl, ys) if front else (ys, ys + tl)
    for sx, side in ((-1, 'L'), (1, 'R')):
        x = sx * s2
        # The tube stays hollow (no epoxy inside); a printed plug closes the outer end and
        # the spigot fills the split end. Fill it with dry sand for extra damping if wanted.
        env, shell = parts.square_tube('y', x, g['tube_z'], tube_s, tube_w, ta, tb)
        cuts.append(env)
        st.add(f'Base{tag}Tube{side}', cont, shell)
        st.plug(f'Base{tag}TubePlug{side}', cont, 'y', x, g['tube_z'], inner, *((ta, ta + 10) if front else (tb - 10, tb)))
        # printed sleeve between the spigot and the tube, one per half
        _, sleeve = parts.square_tube('y', x, g['tube_z'], inner - 0.2, (inner - 0.2 - spig_s - 0.4) / 2,
                                      *((ys - sv, ys - 1) if front else (ys + 1, ys + sv)))
        st.add(f'Base{tag}SpigotSleeve{side}', cont, sleeve, 'printed')
        if not front:
            _, spigot = parts.square_tube('y', x, g['tube_z'], spig_s, spig_w, ys - sl / 2, ys + sl / 2)
            st.add(f'BaseSpigot{side}', cont, spigot)

        dx, dz = sx * g['draw_x'], g['draw_z']
        if front:
            y0 = ya
            cuts += [parts.cyl_v(16.0, y0 - 1, y0 + 28, dx, dz), parts.cyl_v(7.0, y0 + 27, ys + 1, dx, dz)]
            rod = parts.cyl_v(P['tie_rod_d'] / 2, y0 + 15.5, ys + 28, dx, dz)
            washer = parts.cyl_v(12.0, y0 + 25.5, y0 + 28, dx, dz)
            nut = hex_y(19.0, dx, y0 + 15.5, 10.0, dz).fuse(washer)
            st.add(f'DrawRod{side}', cont, rod, 'steel')
            st.add(f'DrawRodNut{side}', cont, nut.cut(parts.cyl_v(P['tie_rod_d'] / 2, y0, y0 + 30, dx, dz)), 'steel')
        else:
            env = hex_y(19.0, dx, ys + 10, 36.0, dz)
            cuts += [env, parts.cyl_v(7.0, ys - 1, ys + 11, dx, dz)]
            st.add(f'DrawRodCoupler{side}', cont, env.cut(parts.cyl_v(P['tie_rod_d'] / 2, ys, ys + 50, dx, dz)), 'steel')

    cuts += [shape for _, shape in base_top_formers(g, front)]
    if front:
        ox, oy = g['outlet']
        # drain: straight down through the front wall to a cast-in brass nipple over the chip basket
        cuts += [Part.makeCylinder(7.0, base_top - 25 + 1, Vector(ox, oy, 0)),
                 parts.hexagon(22.0, -0.5, 12.5, ox, oy)]
        nipple = parts.hexagon(22.0, 0.0, 12.0, ox, oy).fuse(Part.makeCylinder(8.0, 20.0, Vector(ox, oy, -20.0)))
        st.add('DrainOutlet', cont, nipple.cut(Part.makeCylinder(5.5, 34.0, Vector(ox, oy, -21.0))), 'brass')

    # legs cast into the corners (hollow, plugged at the top)
    leg_s, leg_w = P['post_tube']
    for i, (lx, ly) in enumerate(g['legs']):
        if ya <= ly < yb:
            name = f"Leg{'Front' if front else 'Rear'}{'L' if lx < 0 else 'R'}"
            z1 = P['leg_embed']
            env, shell = parts.square_tube('z', lx, ly, leg_s, leg_w, z1 - P['leg_len'], z1)
            cuts.append(env)
            st.add(name, cont, shell)
            st.plug(name + 'Plug', cont, 'z', lx, ly, leg_s - 2 * leg_w, z1 - 10, z1)
            # threaded insert for the leveling foot
            insert = parts.square_tube('z', lx, ly, leg_s - 2 * leg_w - 1.2, 0.1, z1 - P['leg_len'], z1 - P['leg_len'] + 22)[0]
            st.add(name + 'Insert', cont, insert.cut(Part.makeCylinder(6.0, 30, Vector(lx, ly, z1 - P['leg_len'] - 5))), 'steel')

    # cast-in M5 inserts for the enclosure's bottom rails
    for i, (bx, by) in enumerate(g['rail_bolts']):
        if ya <= by < yb:
            cuts.append(Part.makeCylinder(4.0, 13.0, Vector(bx, by, base_top - 12)))
            st.add(f'Insert{tag}{i + 1}', cont, Part.makeCylinder(4.0, 12.0, Vector(bx, by, base_top - 12)).cut(
                Part.makeCylinder(2.5, 14.0, Vector(bx, by, base_top - 13))), 'brass')

    if not front:
        sock_s, sock_w = P['socket_liner']
        for sx, side in ((-1, 'L'), (1, 'R')):
            for i, py in enumerate(g['post_ys']):
                # printed liner: the mould core for the socket, left in as a sliding fit for the post
                env, shell = parts.square_tube('z', sx * g['ux'], py, sock_s, sock_w, g['sock_bot'], base_top)
                cuts.append(env)
                st.add(f'SocketLiner{side}{i + 1}', cont, shell, 'printed')
            dowel = Part.makeCylinder(P['dowel_d'] / 2, 30.0, Vector(sx * g['ux'], g['rod_y'], base_top - 15))
            cuts.append(dowel)
            st.add(f'DowelBase{side}', cont, dowel, 'steel')

    # tie-rod coupling nuts for the uprights, in whichever half each rod lands
    for sx, side in ((-1, 'L'), (1, 'R')):
        for j, (rx, ry, _) in enumerate(g['tie_rods']):
            if ya <= ry < yb:
                env = parts.hexagon(19.0, base_top - 70, 36.0, sx * rx, ry)
                cuts += [env, Part.makeCylinder(7.0, 36, Vector(sx * rx, ry, base_top - 35))]
                st.add(f'TieRodCoupler{side}{j + 1}', cont,
                       env.cut(Part.makeCylinder(P['tie_rod_d'] / 2, 40, Vector(sx * rx, ry, base_top - 72))), 'steel')

    if front:
        # Seal on the split face: a U under the floor gutters, rising at both ends to near the top.
        groove, cord = split_gasket(g)
        cuts.append(groove)
        st.add('GasketBaseSplit', cont, cord, 'rubber')
        g['gasket_len'] += cord.Volume / (P['gasket_groove'][0] * P['gasket_groove'][1])

    shape = blk.cut(cuts).removeSplitter()
    m.add(f'Base{tag}Casting', 'frame', shape, 'granite', container=cont)
    return shape.Volume


def split_gasket(g):
    """Groove (cut from the front half) and the cord that fills it, on the split face y = split."""
    w, dpt = P['gasket_groove']
    ys, half = g['split'], g['base_half']
    xl, zb, zt = half - 12.0, P['gasket_split_z'], g['base_top'] - 6.0
    pieces = [parts.box(-xl - w / 2, xl + w / 2, ys - dpt, ys, zb - w / 2, zb + w / 2)]
    pieces += [parts.box(sx * xl - w / 2, sx * xl + w / 2, ys - dpt, ys, zb - w / 2, zt) for sx in (-1, 1)]
    shape = pieces[0].multiFuse(pieces[1:]).removeSplitter()
    return shape, shape.copy()


def foot_gasket(g, sx):
    """Groove loop in the upright's underside, 8 mm in from its edges."""
    w, dpt = P['gasket_groove']
    x0, x1 = sorted((sx * (g['inner'] + 8.0), sx * (g['outer'] - 8.0)))
    y0, y1 = g['up_front'] + 8.0, g['up_y1'] - 8.0
    z = g['base_top']
    ring = parts.box(x0 - w / 2, x1 + w / 2, y0 - w / 2, y1 + w / 2, z, z + dpt).cut(
        parts.box(x0 + w / 2, x1 - w / 2, y0 + w / 2, y1 - w / 2, z - 1, z + dpt + 1))
    return ring, 2 * ((x1 - x0) + (y1 - y0))


def upright_envelope(g, sx, edges=True):
    """Outside shape of an upright, before any cuts (the mould cavity): a raked buttress, the
    foot running forward along the base and the front face sloping up to the beam."""
    inner, outer, base_top, beam_bot = g['inner'], g['outer'], g['base_top'], g['beam_bot']
    x0 = inner if sx > 0 else -outer
    toe = base_top + P['upright_nose']
    prof = [(g['up_front'], base_top), (g['up_front'], toe), (g['up_top_front'], beam_bot), (g['up_y1'], beam_bot),
            (g['up_y1'], base_top)]
    up = Part.Face(Part.makePolygon([Vector(x0, y, z) for y, z in prof + prof[:1]])).extrude(Vector(P['upright_t'], 0, 0))
    # the nose rounds into the slope (part of the mould: a printed toe filler)
    up = fillet_safe(up, (P['upright_nose_r'],), lambda e: parts.parallel((1, 0, 0))(e) and on_z(toe)(e))
    if not edges:
        return up
    # outside edges well rounded; the top face (under the beam and the top plate) only lightly
    up = fillet_safe(up, (P['round_r'], 6.0), lambda e: not on_z(base_top)(e) and not on_z(beam_bot)(e)
                     and not (parts.parallel((1, 0, 0))(e) and on_z(toe)(e)))
    return fillet_safe(up, (4.0, 2.0), lambda e: on_z(beam_bot)(e))


def upright(m, g, st, sx):
    """Upright casting: posts drop into the base sockets, tie rods pull it down, the beam bolts to its top plate."""
    tag = 'L' if sx < 0 else 'R'
    cont = f'FrameUpright{tag}'
    inner, outer, base_top, beam_bot = g['inner'], g['outer'], g['base_top'], g['beam_bot']
    up_y0, up_y1 = g['up_y0'], g['up_y1']
    up = upright_envelope(g, sx)

    plate_t = P['top_plate_t']
    post_s, post_w = P['post_tube']
    xa, xb = sorted((sx * (inner + 6), sx * (outer - 6)))
    cuts = [parts.box(xa, xb, up_y0 + 6, up_y1 - 6, beam_bot - plate_t, beam_bot + 1),
            Part.makeCylinder(P['dowel_d'] / 2, 16.0, Vector(sx * g['ux'], g['rod_y'], base_top - 1))]   # base dowel
    post_top = beam_bot - plate_t - 2
    for i, py in enumerate(g['post_ys']):
        # hollow post, printed plug at the top
        env, shell = parts.square_tube('z', sx * g['ux'], py, post_s, post_w, post_top - P['tube_len']['post'], post_top)
        cuts.append(env)
        st.add(f'Post{tag}{i + 1}', cont, shell)
        st.plug(f'Post{tag}{i + 1}Plug', cont, 'z', sx * g['ux'], py, post_s - 2 * post_w, post_top - 10, post_top)
    pockets, taps = [], []
    for j, (rx, ry, pb) in enumerate(g['tie_rods']):
        x = sx * rx
        # nut pocket: up from its floor through the top (or the sloped front) of the casting
        pockets.append(Part.makeCylinder(16.0, beam_bot - pb + 1, Vector(x, ry, pb)))
        cuts.append(Part.makeCylinder(7.0, pb - base_top + 1, Vector(x, ry, base_top - 0.5)))
        st.add(f'TieRod{tag}{j + 1}', cont, Part.makeCylinder(P['tie_rod_d'] / 2, pb + 12.5 - (base_top - 52),
                                                               Vector(x, ry, base_top - 52)), 'steel')
        washer = Part.makeCylinder(12.0, 2.5, Vector(x, ry, pb)).cut(Part.makeCylinder(6.5, 3, Vector(x, ry, pb - 0.25)))
        nut = parts.hexagon(19.0, pb + 2.5, 10.0, x, ry).cut(
            Part.makeCylinder(P['tie_rod_d'] / 2, 11, Vector(x, ry, pb + 2)))
        st.add(f'TieRodNut{tag}{j + 1}', cont, washer.fuse(nut), 'steel')
        if pb < g['pocket_bot'] - 1:
            # pocket in the slope: a printed push-fit cap, flush with the face, resting on the nut
            cap = Part.makeCylinder(15.85, beam_bot - pb, Vector(x, ry, pb + 12.6)).common(up)
            m.add(f'PocketCap{tag}{j + 1}', 'frame', cap, 'printed_dark', container=cont)
    for bx in g['bolt_xs']:
        for by in g['bolt_ys']:
            taps.append(Part.makeCylinder(P['beam_bolt_d'] / 2, plate_t + 2, Vector(sx * bx, by, beam_bot - plate_t - 1)))
    taps.append(Part.makeCylinder(P['dowel_d'] / 2, plate_t + 2, Vector(sx * g['ux'], g['beam_dowel_y'], beam_bot - plate_t - 1)))
    plate = parts.plate(xa, xb, up_y0 + 6, up_y1 - 6, beam_bot - plate_t, beam_bot, 0.8)
    st.add(f'TopPlate{tag}', cont, plate.cut(pockets + taps))
    ring, ring_len = foot_gasket(g, sx)
    cuts.append(ring)
    st.add(f'GasketUpright{tag}', cont, ring.copy(), 'rubber')
    g['gasket_len'] += ring_len
    shape = up.cut(cuts + pockets).removeSplitter()
    m.add(f'Upright{tag}Casting', 'frame', shape, 'granite', container=cont)
    return shape.Volume


def beam_envelope(g, edges=True):
    """Outside shape of the beam, before any cuts (the mould cavity)."""
    outer, bf, bot, top = g['outer'], g['beam_face'], g['beam_bot'], g['beam_top']
    by1 = bf + P['beam_d']
    shape = parts.box(-outer, outer, bf, by1, bot, top)
    back = lambda e: parts.parallel((1, 0, 0))(e) and on_y(by1)(e)
    shape = fillet_safe(shape, (P['beam_back_r'], 30.0), lambda e: back(e) and on_z(top)(e))
    shape = fillet_safe(shape, (P['beam_back_low_r'],), lambda e: parts.parallel((1, 0, 0))(e) and on_z(bot)(e)
                        and all(v.Point.y > by1 - 1 for v in e.Vertexes))
    if not edges:
        return shape
    shape = fillet_safe(shape, (P['beam_face_r'],), lambda e: parts.parallel((1, 0, 0))(e) and on_y(bf)(e))
    return fillet_safe(shape, (P['round_r'], 6.0, 3.0), lambda e: all(abs(abs(v.Point.x) - outer) < 1e-6 for v in e.Vertexes))


def beam(m, g, st):
    """Beam casting: two tubes span the uprights; four 3/8-16 bolts and a dowel per side."""
    outer, inner, bf = g['outer'], g['inner'], g['beam_face']
    bot, top = g['beam_bot'], g['beam_top']
    by1 = bf + P['beam_d']
    shape = beam_envelope(g)
    tube_s, tube_w = P['frame_tube']
    cz = (bot + top) / 2
    cuts = []
    half_len = P['tube_len']['beam'] / 2
    for i, ty in enumerate((bf + 32.0, by1 - 32.0)):
        _, shell = parts.square_tube('x', ty, cz, tube_s, tube_w, -half_len, half_len)
        # 14 mm holes through the tube where the inner cap screws pass (drill press)
        holes = [Part.makeCylinder(7.0, top - bot + 2, Vector(sx * bx, by, bot - 1))
                 for sx in (-1, 1) for bx in g['bolt_xs'] for by in g['bolt_ys'] if bx < half_len]
        shell = shell.cut(holes) if holes else shell
        cuts.append(shell)
        st.add(f'BeamTube{i + 1}', 'FrameBeam', shell)
    plate_t = P['top_plate_t']
    n = 0
    for sx in (-1, 1):
        dowel = Part.makeCylinder(P['dowel_d'] / 2, plate_t + 15.0, Vector(sx * g['ux'], g['beam_dowel_y'], bot - plate_t))
        cuts.append(dowel)
        st.add(f'DowelBeam{"L" if sx < 0 else "R"}', 'FrameBeam', dowel, 'steel')
        for bx in g['bolt_xs']:
            for by in g['bolt_ys']:
                x = sx * bx
                n += 1
                cuts.append(Part.makeCylinder(P['beam_bolt_d'] / 2 + 0.75, top - bot + 2, Vector(x, by, bot - 1)))
                bolt = Part.makeCylinder(P['beam_bolt_d'] / 2, top - bot + plate_t, Vector(x, by, bot - plate_t))
                washer = Part.makeCylinder(10.0, 2.0, Vector(x, by, top))
                head = Part.makeCylinder(8.0, 10.0, Vector(x, by, top + 2)).cut(parts.hexagon(8.0, top + 6, 7, x, by))
                st.add(f'BeamBolt{n}', 'FrameBeam', bolt.fuse([washer, head]), 'black')
    shape = shape.cut(cuts).removeSplitter()
    m.add('BeamCasting', 'frame', shape, 'granite', container='FrameBeam')
    return shape.Volume


def frame_modules(m, d):
    """Five bolt-together epoxy-granite castings with cast-in steel (see README)."""
    g = frame_layout(d)
    st = Steel(m)
    vols = {'Base front': base_half(m, g, st, True), 'Base rear': base_half(m, g, st, False),
            'Upright L': upright(m, g, st, -1), 'Upright R': upright(m, g, st, 1), 'Beam': beam(m, g, st)}
    d['casting_vols'] = {k: v / 1e6 for k, v in vols.items()}
    d['casting_L'] = sum(vols.values()) / 1e6
    d['steel_kg'] = st.volume / 1e6 * 7.85
    d['gasket_m'] = g['gasket_len'] / 1000
    plate_t = P['top_plate_t']
    tl = P['tube_len']
    inch = lambda mm: f'{mm / 25.4:.0f} in'
    ys, y0 = g['split'], d['base_y0']
    # each tube: any cap screw inside its length passes through its top and bottom walls
    n_holes = sum(1 for bx in g['bolt_xs'] if bx < tl['beam'] / 2) * 2 * 2
    drill = f"drill {n_holes} x 14 mm holes per tube" if n_holes else "no drilling"
    d['steel_bom'] = [
        ('frame', 'Steel square tube 2 x 2 x 1/8 in (or 0.120 wall)',
         f"4 x {inch(tl['base'])} (base), 2 x {inch(tl['beam'])} (beam, {drill})", 'buy'),
        ('frame', 'Steel square tube 1-1/2 x 1-1/2 x 1/8 in (or 0.120 wall), bought at length',
         f"4 x {inch(tl['post'])} (posts), 2 x {inch(tl['spigot'])} (spigots), 4 x {inch(P['leg_len'])} (legs)", 'buy'),
        ('frame', 'Printed PETG: 4 socket liners, 4 spigot sleeves, 12 tube end plugs, 4 dark grey pocket caps', '~300 g', 'PRINT'),
        ('frame', f'Steel plate 3/8 in, cut to size by the supplier (upright tops)',
         f"2 x {d['outer'] - d['inner'] - 12:.0f} x {d['up_y1'] - d['up_y0'] - 12:.0f}", 'buy'),
        ('frame', '1/2-13 threaded rod + coupling nut + nut/washer (hardware store)', ', '.join(f"2 x {pb + 12.5 - (d['base_top'] - 52):.0f}" for _, _, pb in g['tie_rods'])
         + " (uprights), "
                                                         f"2 x {ys + 28 - y0 - 15.5:.0f} (base)", 'buy'),
        ('frame', f"3/8-16 x 6 in grade 8 bolt + washer (beam; {d['beam_top'] - d['beam_bot'] + plate_t:.0f} mm under the head)", '8 pcs', 'buy'),
        ('frame', 'Dowel pin 3/8 x 1-1/4 in', '4 pcs', 'buy'),
        ('frame', f"Nitrile O-ring cord {P['gasket_cord']:.0f} mm (base split + upright feet), glue the ends",
         f"{d['gasket_m'] + 0.3:.1f} m", 'buy'),
        ('frame', '1/2 in brass hex nipple, cast-in coolant drain', '1 pc', 'buy'),
    ]


def cast_anchors(m, d):
    """Cut the inserts recorded by rail_pair / screw_axis into the castings they land on.

    On the beam face the X BK/BF bolt holes fall over the front beam tube, so there each support
    gets a steel pad instead: 1/4 in flat bar cast flush into the face, tapped M6, bearing on the tube.
    """
    parts_by_name = {p['name']: p for p in m.parts}
    holes, count = {}, {}
    beam_m6 = []
    for pt, n, kind in m.anchors:
        thread, od, ln = P[kind]
        if abs(n.z) > 0.5:
            cast = 'BaseFrontCasting' if pt.y < P['base_split_y'] else 'BaseRearCasting'
        else:
            cast = 'BeamCasting'
        if cast == 'BeamCasting' and kind == 'insert_m6':
            beam_m6.append(pt)
            continue
        body = Part.makeCylinder(od / 2, ln, pt - n * ln, n)
        holes.setdefault(cast, []).append(body)
        insert = body.cut(Part.makeCylinder(thread / 2, ln + 2, pt - n * (ln + 1), n))
        cont = parts_by_name[cast]['container']
        name = f"Anchor{cast.replace('Casting', '')}{len(holes[cast])}"
        m.add(name, 'frame', insert, 'brass', container=cont)
        m.structure.add(name)
        count[kind] = count.get(kind, 0) + 1
    # beam pads, one per support (anchors clustered along x)
    pad_t, pad_h = P['support_pad']
    groups = []
    for pt in sorted(beam_m6, key=lambda p: p.x):
        if groups and pt.x - groups[-1][-1].x < 30.0:
            groups[-1].append(pt)
        else:
            groups.append([pt])
    beam_face, cz = d['beam_face'], (d['beam_bot'] + d['beam_top']) / 2
    for i, grp in enumerate(groups):
        x0, x1 = min(p.x for p in grp) - 18.0, max(p.x for p in grp) + 18.0
        pad = parts.box(x0, x1, beam_face, beam_face + pad_t, cz - pad_h / 2, cz + pad_h / 2)
        holes.setdefault('BeamCasting', []).append(pad)
        taps = [Part.makeCylinder(2.5, pad_t + 2, Vector(p.x, beam_face - 1, p.z), Vector(0, 1, 0)) for p in grp]
        m.add(f'BeamSupportPad{i + 1}', 'frame', pad.cut(taps), 'steeltube', container='FrameBeam')
        m.structure.add(f'BeamSupportPad{i + 1}')
    count['beam_pad'] = len(groups)
    count['beam_pad_holes'] = len(beam_m6)
    for cast, hs in holes.items():
        p = parts_by_name[cast]
        p['shape'] = p['shape'].cut(hs)
        p['proxy'] = [p['shape']]
    d['anchor_count'] = count


MOULD_GROUPS = {'base-front': 'MouldBaseFront', 'base-rear': 'MouldBaseRear', 'upright': 'MouldUpright',
                'beam': 'MouldBeam'}
CASTING_FOLDERS = {'FrameBaseFront': 'base-front', 'FrameBaseRear': 'base-rear', 'FrameUprightL': 'upright',
                   'FrameBeam': 'beam'}


def mould_parts(m, d):
    """Printed mould pieces and printed cast-in parts: (folder, name, shape, kind, qty, note).
    The two uprights are identical, so their pieces are listed once with qty 2."""
    g = frame_layout(d)
    out = []
    top = g['base_top']
    for front, folder in ((True, 'base-front'), (False, 'base-rear')):
        for poly, z_top, name in base_pockets(g):
            if (sum(y for _, y in poly) / len(poly) < g['split']) == front:
                out.append((folder, name, moulds.shell_core(poly, z_top), 'core', 1,
                            'Shell core, stays in the casting. Fill with dry sand while casting so it cannot float.'))
        for name, shape in base_top_formers(g, front):
            out.append((folder, name, shape.common(parts.box(-1e3, 1e3, -1e3, 1e3, 0, top)), 'former', 1,
                        'Stick to the mould floor (the base is cast top-down), wax.'))
        for i, f in enumerate(moulds.fillers(base_envelope(g, front, edges=False))):
            out.append((folder, f'corner-{i + 1}', f, 'filler', 1, 'Rounded corner of the mould box; wax.'))
    # drain liner (stays in): from the brass nipple up to the trough floor
    ox, oy = g['outlet']
    out.append(('base-front', 'drain', Part.makeCylinder(7.0, top - 25 - 12.0, Vector(ox, oy, 12.0)).cut(
        Part.makeCylinder(5.0, top, Vector(ox, oy, 0))), 'liner', 1, 'Drain liner; sits on the nipple and stays in.'))
    out.append(('base-front', 'split-gasket-groove', split_gasket(g)[0], 'former', 1,
                'Stick to the split-face mould wall, wax.'))
    sx = -1
    out.append(('upright', 'foot-gasket-groove', foot_gasket(g, sx)[0], 'former', 2,
                'Stick to the mould floor (the upright is cast foot-down), wax.'))
    pb, rod_r = g['pocket_bot'], 7.2
    plug = Part.makeCylinder(16.0, g['beam_bot'] - pb, Vector(0, 0, pb)).cut(Part.makeCylinder(rod_r, 1e3, Vector(0, 0, 0)))
    top_rods = [r for r in g['tie_rods'] if r[2] >= pb - 1]
    out.append(('upright', 'tie-rod-pocket', plug, 'plug', 2 * len(top_rods),
                'Forms a top nut pocket; slides down the greased tie-rod core rod. Wax; pull after curing.'))
    slope_rods = [r for r in g['tie_rods'] if r[2] < pb - 1]
    if slope_rods:
        rx, ry, spb = slope_rods[0]
        env = upright_envelope(g, sx, edges=False)
        sp = Part.makeCylinder(16.0, g['beam_bot'] - spb, Vector(sx * rx, ry, spb)).common(env).cut(
            Part.makeCylinder(rod_r, 1e3, Vector(sx * rx, ry, 0)))
        out.append(('upright', 'slope-pocket', sp, 'plug', 2 * len(slope_rods),
                    'Forms a nut pocket in the slope: its sloped end screws to the front board. Wax; pull after curing.'))
    for i, f in enumerate(moulds.fillers(beam_envelope(g, edges=False))):
        out.append(('beam', f'back-edge-{i + 1}', f, 'filler', 1, 'Rounded back edge of the beam mould; wax.'))
    # printed parts already in the model: cast-in liners, sleeves and plugs, and the machine's own
    seen = {}
    for p in m.parts:
        if not p['look'].startswith('printed') or p['container'] == 'FrameUprightR':
            continue
        cast_in = p['name'] in m.structure
        folder = CASTING_FOLDERS.get(p['container'], 'machine') if cast_in else 'machine'
        bb = p['shape'].BoundBox
        key = (folder, round(p['shape'].Volume), tuple(sorted(round(v) for v in (bb.XLength, bb.YLength, bb.ZLength))))
        qty = 2 if folder == 'upright' or p['container'] == 'FrameUprightL' else 1
        if key in seen:
            seen[key][4] += qty
            continue
        name = ''.join('-' + c.lower() if c.isupper() and i else c.lower() for i, c in enumerate(p['name'])).replace('--', '-')
        row = [folder, name, p['shape'], 'cast-in' if cast_in else 'part', qty, 'Cast in, stays.' if cast_in else '']
        seen[key] = row
        out.append(row)
    m.moulds = [tuple(r) for r in out]


def build():
    m = Model()
    d = m.dims
    y_stack = P['table_riser_t'] + 28.0     # mounting face -> moving part (HGH15CA H = 28)
    x_stack = P['beam_riser_t'] + 28.0
    z_stack = P['z_riser_t'] + 28.0

    # ---- vertical stack -------------------------------------------------
    base_top = P['base_h']
    table_bot = base_top + y_stack
    table_top = table_bot + P['table_t']
    tip_up = table_top + P['work_clear']            # collet nut tip, Z at top
    front = tip_up + parts.SPINDLE['nut_tip']        # spindle body front face
    beam_bot = table_top + P['beam_clear']
    beam_top = beam_bot + P['beam_h']
    beam_cz = (beam_bot + beam_top) / 2
    zp_bot = front + P['clamp_lift']     # Z plate bottom (= clamp bottom) with Z at top

    # ---- front/back stack (spindle axis at y = 0) -----------------------
    zp_front = P['clamp_off']
    zp_back = zp_front + P['zplate_t']
    car_front = zp_back + z_stack
    car_back = car_front + P['carriage_t']
    beam_face = car_back + x_stack

    # ---- widths ---------------------------------------------------------
    inner = max(P['travel_x'] / 2 + P['carriage_w'] / 2, P['table_w'] / 2) + P['side_clear']
    outer = inner + P['upright_t']
    up_y0 = beam_face - P['upright_front']
    up_y1 = up_y0 + P['upright_d']
    sweep = P['travel_y'] / 2 + P['table_len'] / 2
    ty_u1 = sweep + 10.0                 # table screw sits behind the table's travel
    # The base is as big as the enclosure frame that bolts to its top.
    E = 20.0
    base_half = outer + P['enc_clear'] + E
    ry, rl = P['table_rail_y'], P['table_rail_len'] / 2
    base_y0 = min(-sweep, ry - rl) - P['enc_clear'] - E
    base_y1 = max(up_y1 + 35.0, ty_u1, ry + rl) + P['enc_clear'] + E
    d.update(base_top=base_top, table_top=table_top, nut_tip=tip_up, beam_bot=beam_bot, beam_top=beam_top,
             beam_face=beam_face, inner=inner, outer=outer, up_y0=up_y0, up_y1=up_y1,
             base_half=base_half, base_y0=base_y0, base_y1=base_y1, sweep=sweep, y_bk=ty_u1)

    # ---- frame castings + feet ------------------------------------------
    hx = base_half - 10.0
    d['rail_bolts'] = ([(x, base_y0 + 10.0) for x in (-200.0, 0.0, 200.0)] +
                       [(sx * hx, y) for sx in (-1, 1) for y in (base_y0 + 150.0, (base_y0 + base_y1) / 2, base_y1 - 150.0)] +
                       [(x, base_y1 - 10.0) for x in (-150.0, 150.0)])
    d['bulkhead'] = (-170.0, 600.0)          # coolant return through the back panel (x, z)
    frame_modules(m, d)
    leg_bot = P['leg_embed'] - P['leg_len']
    d['bench_top'] = leg_bot - P['foot_h']
    for i, (x, y) in enumerate(frame_layout(d)['legs']):
        m.add_all(f'Foot{i + 1}', 'frame', parts.leveling_foot(x, y, leg_bot, P['foot_h']),
                  container='FrameBaseFront' if y < P['base_split_y'] else 'FrameBaseRear')
    m.frame_container = 'FrameBaseRear'

    # ---- table axis (Y) -------------------------------------------------
    tf = Frame((0, 0, base_top), (0, 1, 0), (-1, 0, 0))
    rail_pair(m, tf, 'Y', P['table_riser_t'], P['table_rail_len'], P['table_rail_spacing'], P['table_blk_pitch'],
              'frame', 'table', rail_u0=P['table_rail_y'])
    y_tail = parts.ENDS['SFU1605']['bk_e'] - parts.SUPPORT['BK12']['L'] + parts.ENDS['SFU1605']['stub_l']
    screw_axis(m, tf, 'Y', 'SFU1605', P['table_screw_len'], ty_u1 - (P['table_screw_len'] - y_tail), 'BF12', 'BK12',
               'frame', 'table', 0.0, y_stack, 0.0, P['motor_y'])
    tw, tl, pitch = P['table_w'], P['table_len'], P['table_hole_pitch']
    table = parts.plate(-tw / 2, tw / 2, -tl / 2, tl / 2, table_bot, table_top, 1.0)
    nx, ny = int((tw - 30) // pitch) + 1, int((tl - 30) // pitch) + 1
    holes = [Part.makeCylinder(2.5, P['table_t'] + 2, Vector((i - (nx - 1) / 2) * pitch, (j - (ny - 1) / 2) * pitch, table_bot - 1))
             for i in range(nx) for j in range(ny)]
    m.add('Table', 'table', table.cut(holes), 'alu')
    d['table_holes'] = (nx, ny)

    # ---- beam axis (X) --------------------------------------------------
    m.frame_container = 'FrameBeam'
    bf = Frame((0, beam_face, beam_cz), (1, 0, 0), (0, 0, 1))
    rail_pair(m, bf, 'X', P['beam_riser_t'], P['beam_rail_len'], P['beam_rail_spacing'], P['beam_blk_pitch'],
              'frame', 'xcar')
    hl = parts.SFU['SFU1204']['L'] / 2 + 3   # nut half-length + clearance
    x_u0 = -(P['travel_x'] / 2 + hl + parts.SUPPORT['BF10']['L'] + 5)
    x_flange = screw_axis(m, bf, 'X', 'SFU1204', P['beam_screw_len'], x_u0, 'BF10', 'BK10',
                          'frame', 'xcar', 0.0, x_stack, outer + 5.0, P['motor_x'])
    m.frame_container = 'FrameBaseRear'

    # ---- Z axis ---------------------------------------------------------
    # Rails ride on the moving Z plate; blocks are fixed to the X carriage.
    zr = Frame((0, zp_back, 0), (0, 0, 1), (1, 0, 0))
    z_rail_mid = zp_bot + P['z_rail_len'] / 2
    z_blk_mid = zp_bot + 10 + 61.4 / 2 + P['z_blk_pitch'] / 2
    rail_pair(m, zr, 'Z', P['z_riser_t'], P['z_rail_len'], P['z_rail_spacing'], P['z_blk_pitch'], 'zaxis', 'xcar',
              rail_u0=z_rail_mid, blk_u0=z_blk_mid)
    zs = Frame((0, car_front, 0), (0, 0, 1), (-1, 0, 0))
    z_nut = zp_bot + P['z_nut_on_plate']
    z_u0 = z_nut - P['travel_z'] - hl - parts.SUPPORT['BF10']['L'] - 5
    zp_top = zp_bot + P['z_rail_len']
    z_flange = screw_axis(m, zs, 'Z', 'SFU1204', P['z_screw_len'], z_u0, 'BF10', 'BK10',
                          'xcar', 'zaxis', z_nut, z_stack, zp_top + 10.0, P['motor_z'])

    x_blk_bot = beam_cz - P['beam_rail_spacing'] / 2 - 17.0
    car_z0 = min(z_blk_mid - P['z_blk_pitch'] / 2 - 61.4 / 2, z_u0, x_blk_bot) - 5
    m.add('XCarriagePlate', 'xcar', parts.plate(-P['carriage_w'] / 2, P['carriage_w'] / 2, car_front, car_back,
                                                car_z0, z_flange), 'alu')
    m.add('ZPlate', 'zaxis', parts.plate(-P['zplate_w'] / 2, P['zplate_w'] / 2, zp_front, zp_back, zp_bot, zp_top), 'alu')
    cast_anchors(m, d)

    # ---- spindle --------------------------------------------------------
    m.add_all('SpindleClamp', 'zaxis', parts.spindle_clamp(zp_bot, P['clamp_off']))
    m.add_all('Spindle', 'zaxis', parts.spindle(front, P['tool_stickout']))
    d['tip'] = tip_up - P['tool_stickout']

    # ---- enclosure ------------------------------------------------------
    d['x_motor'] = (beam_face - parts.SUPPORT['BK10']['h'], beam_cz)          # (y, z) of the X motor axis
    d['y_motor'] = (0.0, base_top + parts.SUPPORT['BK12']['h'])                # (x, z) of the Y motor axis
    enclosure(m, d)

    # ---- chips, coolant, cable chain -------------------------------------
    d.update(table_bot=table_bot, beam_cz=beam_cz, car_back=car_back, zp_bot=zp_bot)
    covers(m, d)
    chain_and_coolant(m, d)
    workbench(m, d)

    # ---- BOM ------------------------------------------------------------
    m.bom = [
        ('Y table', 'HGR15 rail x2 + HGH15CA block x4', f"{P['table_rail_len']:.0f} mm", 'buy'),
        ('Y table', 'SFU1605 ballscrew + BK12/BF12 + housing + coupler', f"{P['table_screw_len']:.0f} mm", 'buy'),
        ('X beam', 'HGR15 rail x2 + HGH15CA block x4', f"{P['beam_rail_len']:.0f} mm", 'OWNED'),
        ('X beam', 'SFU1204 ballscrew + BK10/BF10 + housing + coupler', f"{P['beam_screw_len']:.0f} mm", 'OWNED'),
        ('Z', 'HGR15 rail x2 + HGH15CA block x4', f"{P['z_rail_len']:.0f} mm", 'buy'),
        ('Z', 'SFU1204 ballscrew + BK10/BF10 + housing + coupler', f"{P['z_screw_len']:.0f} mm", 'buy'),
        ('X beam', 'NEMA 23 bracket for BK10', '1 pc', 'OWNED'),
        ('Z', 'NEMA 23 bracket for BK10', '1 pc', 'buy'),
        ('Y table', 'NEMA 23 bracket for BK12', '1 pc', 'buy'),
        ('X, Y', f"NEMA 23 closed loop {P['motor_x']} + CL57T driver", '2 pcs', 'buy'),
        ('Z', f"NEMA 23 open loop (modeled as {P['motor_z']})", '1 pc', 'OWNED'),
        ('Y table', parts.HOUSING['SFU1605']['name'] + ' nut housing', '1 pc', 'buy (comes in SFU1605 kits)'),
        ('X, Z', parts.HOUSING['SFU1204']['name'] + ' nut housing', '2 pcs', 'X OWNED, Z buy'),
        ('spindle', 'GDZ80-2.2 water-cooled ER20 + VFD + 80 mm cast clamp', '1 set', 'buy'),
        ('all', 'MIC6 plate: table', f"{tw:.0f} x {tl:.0f} x 3/4 in, M6 grid {nx}x{ny} @ {pitch:.0f}", 'buy'),
        ('all', 'MIC6 plate: X carriage', f"{P['carriage_w']:.0f} x {z_flange - car_z0:.0f} x 5/8 in", 'buy'),
        ('all', 'MIC6 plate: Z plate', f"{P['zplate_w']:.0f} x {P['z_rail_len']:.0f} x 5/8 in", 'buy'),
        ('all', 'Cold-rolled steel flat bar rail risers, bedded + epoxy-replicated', "1-1/4 in wide, 3/4 in (Y) and 5/8 in (X, Z)", 'buy'),
        ('all', 'Feet: 1/2-13 x 2 in bolt + jam nut + rubber pad (into the nut in each leg end)', '4 sets', 'buy'),
        ('enclosure', 'M5 x 35 cap screw through the bottom rails into cast-in inserts', f"{len(d['rail_bolts'])} pcs", 'buy (part 3)'),
        ('frame', 'Cast-in threaded inserts for epoxy (knurled brass or steel)',
         f"M5 x 12 long: {d['anchor_count'].get('insert_m5', 0)} (riser hold-downs); "
         f"M6 x 15 long: {d['anchor_count'].get('insert_m6', 0)} (Y BK/BF on the base)", 'buy'),
        ('frame', 'Steel flat bar 1/4 x 2-1/2 in: X BK/BF pads, drilled + tapped M6, cast flush in the beam face',
         f"{d['anchor_count'].get('beam_pad', 0)} pads (~4 in of bar), {d['anchor_count'].get('beam_pad_holes', 0)} tapped holes", 'buy'),
        ('frame', 'Cap screws: DIN 7984 low-head M5 x 20 (X risers), M5 x 25 (Y risers); M6 x 40 (Y BK/BF); '
                  'M6 x 35 + 2 DIN 433 small washers under each head (X BK/BF, so they stop short of the tube)',
         f"8 + {d['anchor_count'].get('insert_m5', 0) - 8}; {d['anchor_count'].get('insert_m6', 0)}; "
         f"{d['anchor_count'].get('beam_pad_holes', 0)}", 'buy'),
    ] + d['steel_bom'] + [
        ('coolant', 'Sump: full-size 4 in stainless steam-table pan (~13 L), slides in under the base', '1', 'buy'),
        ('coolant', 'Chip basket: 1/3-size perforated steam-table pan, 2.5 in deep', '1', 'buy'),
        ('coolant', '100 um filter mesh (printed frame), printed baffle, 100 x 25 magnet bar', '1 set', 'buy (part 3)'),
        ('coolant', 'Submersible pump 24 V brushless, ~800 L/h, 5 m head, on the controller M8 MOSFET output', '1', 'buy (part 3)'),
        ('coolant', 'Return hose 8 mm OD PU, push-to-connect at the pump so the sump slides out', f"{d['hose_return']:.1f} m", 'buy (part 3)'),
        ('frame', 'Leg feet: printed plug + 1/2-13 nut bonded into each leg end', '4 pcs', 'PRINT'),
        ('coolant', '1/4 in bulkhead fitting, ball valve, manifold, 2x Loc-Line 1/4 in nozzles', '1 set', 'buy (part 3)'),
        ('covers', 'Roll-up way cover: spring roller + 0.1 mm stainless strip', '1x 250 wide, 2x 85 wide', 'buy or DIY'),
        ('covers', 'Spiral ballscrew cover for the table screw', '1', 'buy'),
        ('covers', 'Drip shield over the beam rails, aluminium or ACM offcut', f"{2 * d['outer'] - 20:.0f} x 57", 'buy'),
        ('covers', 'Brush seal plates for the motor cutouts', '2', 'buy (part 3)'),
        ('printed', f"Drag chain links, PETG: {CHAIN['width']:.0f} x {CHAIN['height']:.0f} outer, {CHAIN['pitch']:.0f} pitch, "
                    f"R{CHAIN['radius']:.0f} bend", f"{CHAIN['links']} + 2 end mounts", 'PRINT'),
    ]
    mould_parts(m, d)
    return m


# --------------------------------------------------------------------------
# Enclosure
# --------------------------------------------------------------------------
def enclosure(m, d):
    """2020 frame + polycarbonate panels bolted straight onto the base top, with a top-hinged door.

    The base is the floor: gutters run coolant to an outlet at the front. The X and Y motors
    stick out through panel cutouts so coolant stays off them (take them off before
    lifting the enclosure away).
    """
    E = 20.0
    add = lambda name, shape, look, **kw: m.add(name, 'frame', shape, look, container='Enclosure', **kw)
    moving_top = max(p['shape'].BoundBox.ZMax for p in m.parts if p['group'] in ('xcar', 'zaxis'))
    x1o = d['base_half']
    x0o, y0o, y1o = -x1o, d['base_y0'], d['base_y1']
    z0 = d['base_top']
    z1o = moving_top + P['enc_clear'] + E
    d.update(enc=(x0o, x1o, y0o, y1o, z0, z1o))
    c = P['motor_cutout'] / 2
    ymx, zmx = d['x_motor']
    xmy, zmy = d['y_motor']

    def member(name, origin, u, v, length, adder=add, holes=()):
        """2020 member; holes = positions along it drilled through for M5 screws into the base."""
        shape = parts.tslot20(length)
        if holes:
            shape = shape.cut([parts.cyl_w(2.75, -11, 11, h) for h in holes] +
                              [parts.cyl_w(4.5, 3, 11, h) for h in holes])    # head recessed under the panel
        adder(name, Frame(origin, u, v).place(shape), 'extrusion')
        m.cutlist.append((name, length))

    bolts = d['rail_bolts']
    H = z1o - z0
    for cx, cy, tag in ((x0o + 10, y0o + 10, 'FL'), (x1o - 10, y0o + 10, 'FR'),
                        (x0o + 10, y1o - 10, 'BL'), (x1o - 10, y1o - 10, 'BR')):
        member(f'Post{tag}', (cx, cy, z0), (0, 0, 1), (1, 0, 0), H)
    wx, wy = (x1o - x0o) - 2 * E, (y1o - y0o) - 2 * E
    for zc, lvl in ((z0 + 10, 'Bottom'), (z1o - 10, 'Top')):
        low = lvl == 'Bottom'
        member(f'{lvl}RailFront', (x0o + E, y0o + 10, zc), (1, 0, 0), (0, 1, 0), wx,
               holes=[bx - (x0o + E) for bx, by in bolts if low and abs(by - (y0o + 10)) < 1])
        member(f'{lvl}RailLeft', (x0o + 10, y0o + E, zc), (0, 1, 0), (-1, 0, 0), wy,
               holes=[by - (y0o + E) for bx, by in bolts if low and abs(bx - (x0o + 10)) < 1])
        member(f'{lvl}RailRight', (x1o - 10, y0o + E, zc), (0, 1, 0), (-1, 0, 0), wy,
               holes=[by - (y0o + E) for bx, by in bolts if low and abs(bx - (x1o - 10)) < 1])
    member('TopRailBack', (x0o + E, y1o - 10, z1o - 10), (1, 0, 0), (0, 1, 0), wx)
    # The back bottom rail stops either side of the Y motor bracket.
    seg = (xmy - c) - (x0o + E)
    back = [bx for bx, by in bolts if abs(by - (y1o - 10)) < 1]
    member('BottomRailBackL', (x0o + E, y1o - 10, z0 + 10), (1, 0, 0), (0, 1, 0), seg,
           holes=[bx - (x0o + E) for bx in back if bx < xmy])
    member('BottomRailBackR', (xmy + c, y1o - 10, z0 + 10), (1, 0, 0), (0, 1, 0), seg,
           holes=[bx - (xmy + c) for bx in back if bx > xmy])
    for i, (bx, by) in enumerate(bolts):
        screw = Part.makeCylinder(2.5, 25.0, Vector(bx, by, z0 - 12)).fuse(Part.makeCylinder(4.25, 5.0, Vector(bx, by, z0 + 13)))
        add(f'RailScrew{i + 1}', screw.cut(parts.hexagon(4.0, z0 + 15, 4, bx, by)), 'black')

    t = P['panel_t'] / 2
    bx_, bz_ = d['bulkhead']
    panels = [
        ('PanelLeft', parts.box(x0o + 10 - t, x0o + 10 + t, y0o + E, y1o - E, z0 + E, z1o - E), []),
        ('PanelRight', parts.box(x1o - 10 - t, x1o - 10 + t, y0o + E, y1o - E, z0 + E, z1o - E),
         [parts.box(x1o - 20, x1o, ymx - c, ymx + c, zmx - c, zmx + c)]),
        ('PanelBack', parts.box(x0o + E, x1o - E, y1o - 10 - t, y1o - 10 + t, z0 + E, z1o - E),
         [parts.box(xmy - c, xmy + c, y1o - 20, y1o, z0, zmy + c), parts.cyl_v(8.0, y1o - 20, y1o, bx_, bz_)]),
        ('PanelRoof', parts.box(x0o + E, x1o - E, y0o + E, y1o - E, z1o - 10 - t, z1o - 10 + t), []),
    ]
    # Opaque aluminium composite panel (ACM) for the walls and roof; only the door is clear.
    for name, shape, cut in panels:
        add(name, shape.cut(cut) if cut else shape, 'acm')
        bb = shape.BoundBox
        dims = sorted((bb.XLength, bb.YLength, bb.ZLength), reverse=True)[:2]
        m.cutlist.append((name, f'{dims[0]:.0f} x {dims[1]:.0f} ACM 3 mm'))

    # Brush seals around the motors where they pass through the panels (outside face).
    s_out, s_in = c + 10.0, 31.0
    seal_x = parts.box(x1o - 10 + t, x1o - 10 + t + 3, ymx - s_out, ymx + s_out, zmx - s_out, zmx + s_out).cut(
        parts.box(x1o - 20, x1o, ymx - s_in, ymx + s_in, zmx - s_in, zmx + s_in))
    add('BrushSealX', seal_x, 'black')
    seal_y = parts.box(xmy - s_out, xmy + s_out, y1o - 10 + t, y1o - 10 + t + 3, z0 + E, zmy + s_out).cut(
        parts.box(xmy - s_in, xmy + s_in, y1o - 20, y1o, z0, zmy + s_in))
    add('BrushSealY', seal_y, 'black')
    # Bulkhead fitting for the coolant return line.
    pc = y1o - 10
    bulk = parts.cyl_v(6.0, pc - 22, pc + 22, bx_, bz_).fuse([hex_y(17.0, bx_, pc - t - 5, 5.0, bz_), hex_y(17.0, bx_, pc + t, 5.0, bz_)])
    add('Bulkhead', bulk.cut(parts.cyl_v(3.5, pc - 30, pc + 30, bx_, bz_)), 'brass')

    # Door: 2020 frame + panel in front of the frame, hinged along the top front edge.
    # Its bottom laps over the base front face.
    door_y0 = y0o - E
    hinge = Vector(0, door_y0 - 5.0, z1o + 5.0)   # pin just clear of the door's top front edge
    d['hinge'] = hinge
    dz0 = z0 - P['door_lap']
    dadd = lambda name, shape, look, **kw: m.add(name, 'door', shape, look, container='Door', **kw)
    dyc = door_y0 + 10
    member('DoorTop', (x0o, dyc, z1o - 10), (1, 0, 0), (0, 1, 0), x1o - x0o, dadd)
    member('DoorBottom', (x0o, dyc, dz0 + 10), (1, 0, 0), (0, 1, 0), x1o - x0o, dadd)
    member('DoorStileL', (x0o + 10, dyc, dz0 + E), (0, 0, 1), (1, 0, 0), z1o - dz0 - 2 * E, dadd)
    member('DoorStileR', (x1o - 10, dyc, dz0 + E), (0, 0, 1), (1, 0, 0), z1o - dz0 - 2 * E, dadd)
    dadd('DoorPanel', parts.box(x0o + E, x1o - E, dyc - t, dyc + t, dz0 + E, z1o - E), 'panel')
    m.cutlist.append(('DoorPanel', f'{x1o - x0o - 2 * E:.0f} x {z1o - dz0 - 2 * E:.0f} polycarbonate'))
    hz = z0 + 60
    handle = parts.cyl_u(7.0, -110, 110, door_y0 - 32, hz)
    for x in (-95, 95):
        handle = handle.fuse(parts.cyl_v(6.0, door_y0 - 32, door_y0, x, hz))
    dadd('DoorHandle', handle, 'steel')
    for i, x in enumerate((x0o + 90, x1o - 90)):
        barrel = parts.cyl_u(5.0, x - 20, x + 20, hinge.y, hinge.z)
        leaf = parts.box(x - 20, x + 20, hinge.y, y0o + 18, z1o, z1o + 2)
        add(f'Hinge{i + 1}', barrel.fuse(leaf), 'steel')
        dadd(f'Hinge{i + 1}Leaf', parts.box(x - 20, x + 20, door_y0 - 3, door_y0, z1o - 45, z1o - 6), 'steel')


# --------------------------------------------------------------------------
# Chips and coolant
# --------------------------------------------------------------------------
def covers(m, d):
    """Keep chips off the ways.

    Table: roll-up 0.1 mm stainless strips on spring rollers in front of and behind the
    table (running just over the BF/BK12 supports and under the table), plus a spiral
    spring cover on the screw behind the table. Beam: a drip shield over the rails.
    """
    base_top, tl, r = d['base_top'], P['table_len'], 18.0
    zs = base_top + parts.SUPPORT['BK12']['H'] + 0.5          # strip underside
    zr = zs - r
    rail_end = P['table_rail_len'] / 2
    yf, yr = P['table_rail_y'] - rail_end - r - 1.0, P['table_rail_y'] + rail_end + r + 1.0
    m.add('CoverRollerFront', 'frame', parts.roll_cover(-125, 125, yf, zr, base_top, r), 'black',
          container='FrameBaseFront')
    rear_x = ((-125.0, -40.0), (40.0, 125.0))                 # either side of the BK12
    for (x0, x1), side in zip(rear_x, 'LR'):
        m.add(f'CoverRollerRear{side}', 'frame', parts.roll_cover(x0, x1, yr, zr, base_top, r), 'black',
              container='FrameBaseRear')

    def front_strip(x, y, z):
        edge = y - tl / 2
        return parts.box(-122, 122, yf, edge, zs, zs + 0.5) if edge > yf + 1 else None

    m.add_dynamic('CoverStripFront', 'shim', front_strip, 'WayCovers', touches=('CoverRollerFront',))
    for (x0, x1), side in zip(rear_x, 'LR'):
        def rear_strip(x, y, z, x0=x0, x1=x1):
            edge = y + tl / 2
            return parts.box(x0 + 2, x1 - 2, edge, yr, zs, zs + 0.5) if edge < yr - 1 else None
        m.add_dynamic(f'CoverStripRear{side}', 'shim', rear_strip, 'WayCovers', touches=(f'CoverRollerRear{side}',))

    s = parts.SFU['SFU1605']
    az = base_top + parts.SUPPORT['BK12']['h']
    bk_face = d['y_bk'] - parts.SUPPORT['BK12']['L']

    def screw_cover(x, y, z):
        y0 = y - s['L'] / 2 + s['T'] + parts.HOUSING['SFU1605']['L']     # housing rear face
        if bk_face - y0 < 5:
            return None
        cone = Part.makeCone(12.0, 16.0, bk_face - y0, Vector(0, y0, az), Vector(0, 1, 0))
        return cone.cut(Part.makeCylinder(9.0, bk_face - y0 + 2, Vector(0, y0 - 1, az), Vector(0, 1, 0)))

    m.add_dynamic('CoverScrewRear', 'black', screw_cover, 'WayCovers', touches=('Y_NutHousing', 'Y_BK12'))

    m.add('DripShield', 'frame', parts.box(-(d['outer'] - 10), d['outer'] - 10, d['car_back'] + 2.0,
                                           d['beam_face'] + 15.0, d['beam_top'], d['beam_top'] + 1.5),
          'shim', container='FrameBeam')


CHAIN = dict(pitch=20.0, width=38.0, height=21.0, radius=38.0, links=17, fixed_x=-110.0, carriage_dx=-20.0)


def chain_and_coolant(m, d):
    """Printed drag chain on the beam (coolant, Z motor and spindle lines), the coolant return
    from the bulkhead to the nozzles, and the flexible loop down to the spindle clamp."""
    C = CHAIN
    p_, h_, rad, n = C['pitch'], C['height'], C['radius'], C['links']
    length = n * p_
    bt = d['beam_top']
    cy = d['beam_face'] + 60.0
    zl, zu = bt + h_ / 2, bt + h_ / 2 + 2 * rad
    xf, dx = C['fixed_x'], C['carriage_dx']
    links = [parts.chain_link(p_, C['width'], h_), parts.chain_link(p_, C['width'], h_, inner_layer=True)]
    d['chain'] = dict(y=cy, zl=zl, zu=zu)

    def path(s_, xm):
        xb = (length - math.pi * rad + xf + xm) / 2
        if s_ <= xb - xf:
            return xf + s_, zl
        s_ -= xb - xf
        if s_ <= math.pi * rad:
            th = -math.pi / 2 + s_ / rad
            return xb + rad * math.cos(th), zl + rad + rad * math.sin(th)
        return xb - (s_ - math.pi * rad), zu

    def chain(x, y, z):
        xm = x + dx
        out = []
        for i in range(n):
            (x0, z0), (x1, z1) = path(i * p_, xm), path((i + 1) * p_, xm)
            link = links[i % 2].copy()
            link.rotate(Vector(0, 0, 0), Vector(0, 1, 0), math.degrees(math.atan2(-(z1 - z0), x1 - x0)))
            link.translate(Vector(x0, cy, z0))
            out.append(link)
        return Part.makeCompound(out)

    hw = C['width'] / 2
    m.add('ChainMountFixed', 'frame', parts.box(xf - 25, xf, cy - hw, cy + hw, bt, bt + h_), 'printed', container='FrameBeam')
    mount = parts.box(dx - 15, dx + 15, d['car_back'], d['car_back'] + 3, zu - 25, zu + 20)
    mount = mount.fuse([parts.box(dx - 12, dx + 12, d['car_back'], cy + hw, zu + h_ / 2 + 0.5, zu + h_ / 2 + 3.5),
                        parts.box(dx - 22, dx + 2, cy - hw, cy + hw, zu - h_ / 2, zu + h_ / 2)])
    m.add('ChainMountMoving', 'xcar', mount, 'printed')
    m.add_dynamic('XChain', 'printed', chain, 'CableChain', touches=('ChainMountFixed', 'ChainMountMoving'))

    # Coolant return: bulkhead -> chain fixed end, along the chain, carriage -> loop -> clamp manifold.
    bx, bz = d['bulkhead']
    pc = d['base_y1'] - 10
    m.add('CoolantReturnInside', 'frame', parts.hose([(bx, pc - 22, bz), (bx, pc - 32, bz), (-160, 300, 585), (-150, cy, 560),
                                                      (-150, cy, zl), (xf - 25, cy, zl)], 4.0),
          'hose', container='CoolantLines')
    m.add('CoolantFeedCarriage', 'xcar', parts.hose([(dx - 10, cy - 24, zu - 8), (95, cy - 24, zu - 8),
                                                     (95, 135, zu - 10), (95, 95, 600)], 4.0), 'hose')
    zm = d['zp_bot'] + 5.0
    man = parts.box(52, 72, -32, -8, zm, zm + 20).fuse(parts.box(44, 52, -24, -16, zm, zm + 20))
    m.add('CoolantManifold', 'zaxis', man, 'brass', comp='SpindleClamp')
    z0 = zm - 5.5
    m.add('CoolantNozzle1', 'zaxis', parts.loc_line([(62, -20, z0), (58, -22, z0 - 20), (45, -20, z0 - 45), (28, -14, z0 - 62)]),
          'locline', comp='SpindleClamp')
    m.add('CoolantNozzle2', 'zaxis', parts.loc_line([(62, -28, z0), (45, -45, z0 - 22), (18, -45, z0 - 45), (4, -30, z0 - 60)]),
          'locline', comp='SpindleClamp')

    def loop(x, y, z):
        return parts.hose([(x + 95, 95, 600), (x + 100, 60, 520 + z / 2), (x + 80, 0, 470 + z), (x + 62, -20, zm + 20 + z)], 4.0)

    m.add_dynamic('CoolantLoop', 'hose', loop, 'CoolantLines', touches=('CoolantFeedCarriage', 'CoolantManifold'))
    # return line from the bulkhead: inside run + along the chain + carriage + loop
    d['hose_return_inside'] = (400.0 + length + 330.0 + 300.0) / 1000


def workbench(m, d):
    """Bench the machine stands on, and the coolant sump that slides in under the base.

    Drain: trough -> nipple in the base -> chip basket. Pump (clean end) -> return hose under
    the base and up the back -> bulkhead in the enclosure's back panel.
    """
    add = lambda name, shape, look: m.add(name, 'frame', shape, look, container='Workbench')
    y0, y1, half = d['base_y0'], d['base_y1'], d['base_half']
    bx0, bx1, by0, by1 = -(half + 200), half + 200, y0 - 250, y1 + 200
    top1 = d['bench_top']
    top0 = top1 - 30.0
    add('BenchTop', parts.box(bx0, bx1, by0, by1, top0, top1), 'wood')
    shelf_top = top0 - 300.0
    legs = [parts.box(lx, lx + 60, ly, ly + 60, top0 - 800, top0)
            for lx, ly in ((bx0, by0), (bx1 - 60, by0), (bx0, by1 - 60), (bx1 - 60, by1 - 60))]
    add('BenchShelf', parts.box(bx0 + 30, bx1 - 30, by0 + 30, by1 - 30, shelf_top - 18, shelf_top).cut(legs), 'wood')
    for i, leg in enumerate(legs):
        add(f'BenchLeg{i + 1}', leg, 'wood')

    sump, outlet = parts.coolant_sump(0.0, y0 + 5.0, top1)
    for suffix, shape, look in sump:
        m.add('Sump' + suffix, 'frame', shape, look, comp='Sump', container='CoolantSump')
    d['sump_top'] = top1 + 101.6
    # return line: up off the pump, back under the base, up behind the enclosure to the bulkhead
    bx, bz = d['bulkhead']
    zr = -12.0
    pts = [outlet, Vector(outlet.x, outlet.y, zr), Vector(outlet.x, y1 + 60.0, zr), Vector(bx, y1 + 60.0, zr),
           Vector(bx, y1 + 60.0, bz), Vector(bx, y1 + 12.0, bz)]
    m.add('ReturnHose', 'frame', parts.hose([(p.x, p.y, p.z) for p in pts], 4.0), 'hose', container='FrameBaseRear')
    run = sum((b - a).Length for a, b in zip(pts, pts[1:]))
    d['hose_return'] = d['hose_return_inside'] + (run + 300.0) / 1000          # plus slack


# --------------------------------------------------------------------------
# Checks
# --------------------------------------------------------------------------
MOVING = ('table', 'xcar', 'zaxis')


def offset(group, x, y, z):
    return {'table': Vector(0, y, 0), 'xcar': Vector(x, 0, 0), 'zaxis': Vector(x, 0, z)}.get(group, Vector(0, 0, 0))


def collisions(m, tol=1.0):
    hx, hy = P['travel_x'] / 2, P['travel_y'] / 2
    poses = list(itertools.product((-hx, 0.0, hx), (-hy, 0.0, hy), (-P['travel_z'], 0.0)))
    hits = {}
    checked = [p for p in m.parts if not p['name'].startswith('SpindleFlutes') and not p['name'].startswith('SpindleShank')]
    for x, y, z in poses:
        home = (x, y, z) == (0.0, 0.0, 0.0)
        placed = []
        for p in checked:
            off = offset(p['group'], x, y, z)
            pieces = []
            for s in p['proxy']:
                bb = App.BoundBox(s.BoundBox)
                bb.move(off)
                pieces.append((s, bb))
            placed.append((p, off, pieces))
        for (a, oa, pa), (b, ob, pb) in itertools.combinations(placed, 2):
            if a['comp'] == b['comp']:
                continue
            if not home and a['group'] == b['group']:
                continue
            if not home and a['group'] not in MOVING and b['group'] not in MOVING:
                continue
            vol = 0.0
            for sa, ba in pa:
                for sb, bb in pb:
                    if ba.intersect(bb):
                        vol += sa.translated(oa).common(sb.translated(ob)).Volume
            if vol > tol:
                hits.setdefault((a['name'], b['name']), []).append(((x, y, z), vol))
        # parts that change shape with the axes, against everything placed at this pose
        for dd in m.dynamic:
            shape = dd['fn'](x, y, z)
            if shape is None:
                continue
            dbb = shape.BoundBox
            for p, off, pieces in placed:
                if p['name'] in dd['touches'] or p['comp'] in dd['touches']:
                    continue
                vol = sum(shape.common(s.translated(off)).Volume for s, bb in pieces if dbb.intersect(bb))
                if vol > tol:
                    hits.setdefault((dd['name'], p['name']), []).append(((x, y, z), vol))
    return hits


def report(m, hits):
    d = m.dims
    bb = App.BoundBox()
    for x, y in itertools.product((-P['travel_x'] / 2, P['travel_x'] / 2), (-P['travel_y'] / 2, P['travel_y'] / 2)):
        for p in m.parts:
            if p['container'] == 'Workbench':
                continue
            b = App.BoundBox(p['shape'].BoundBox)
            b.move(offset(p['group'], x, y, 0.0))
            bb.add(b)
    x0o, x1o, y0o, y1o, z0, z1o = d['enc']
    sand_kg = {k: v * P['eg_density'] for k, v in d['casting_vols'].items()}       # the plain mix
    grit = {name: {k: m_ * frac * sg for k, m_ in sand_kg.items() if k.startswith(P['alumina_castings'])}
            for name, frac, sg in P['alumina']}
    kg = dict(sand_kg)
    for name, frac, sg in P['alumina']:
        for k, g_ in grit[name].items():
            kg[k] += g_ - g_ / sg
    mass = sum(kg.values())
    lines = [
        'DIY CNC layout report',
        '=====================',
        f"Travel X/Y/Z:                 {P['travel_x']:.0f} / {P['travel_y']:.0f} / {P['travel_z']:.0f} mm",
        f"Base footprint (= enclosure): {2 * d['base_half']:.0f} W x {d['base_y1'] - d['base_y0']:.0f} D mm",
        f"Enclosure frame:              {x1o - x0o:.0f} W x {y1o - y0o:.0f} D x {z1o - z0:.0f} H mm",
        f"Overall incl. door, motors:   {bb.XLength:.0f} W x {bb.YLength:.0f} D x {bb.ZLength:.0f} H mm",
        f"Table top height:             {d['table_top']:.0f} mm above casting underside",
        f"Table top -> collet nut tip:  {d['nut_tip'] - d['table_top']:.0f} mm (Z up)",
        f"Table top -> beam underside:  {d['beam_bot'] - d['table_top']:.0f} mm",
        f"Tool tip above table, Z up:   {d['tip'] - d['table_top']:.0f} mm ({P['tool_stickout']:.0f} mm stickout)",
        f"Tool tip above table, Z down: {d['tip'] - P['travel_z'] - d['table_top']:.0f} mm",
        f"Beam face -> spindle axis:    {d['beam_face']:.0f} mm (overhang)",
        f"Gap between uprights:         {2 * d['inner']:.0f} mm",
        '',
        f"Epoxy granite volume:         {d['casting_L']:.1f} L",
        f"Casting mass:                 {mass:.0f} kg ({mass * 2.2046:.0f} lb)",
    ] + [f"  {k + ':':12s}                {v:5.1f} L  {kg[k]:5.1f} kg" + ('  (alumina grit)' if kg[k] != sand_kg[k] else '')
         for k, v in d['casting_vols'].items()] + [
        f"Cast-in steel + joint hardware: {d['steel_kg']:.1f} kg",
        f"Epoxy needed (~{P['eg_epoxy_frac'] * 100:.1f}% of the sand mix by mass): {sum(sand_kg.values()) * P['eg_epoxy_frac']:.1f} kg",
    ] + [f"Aluminium oxide grit, {name}: {sum(grit[name].values()):.1f} kg (beam + uprights)" for name, _, _ in P['alumina']] + [
        '',
        'Linear motion / plate BOM',
        '-------------------------',
    ]
    lines += [f"  {a:8s} {b:52s} {c:36s} {s}" for a, b, c, s in m.bom]
    lines += ['', 'Enclosure cut list (2020 extrusion, 3 mm ACM walls, 4 mm polycarbonate door)', '-' * 56]
    lengths = {}
    for name, val in m.cutlist:
        if isinstance(val, float):
            lengths[round(val)] = lengths.get(round(val), 0) + 1
        else:
            lines.append(f"  {name:18s} {val}")
    lines += [f"  2020 x {n:<2d}         {L} mm" for L, n in sorted(lengths.items(), reverse=True)]
    lines.append(f"  2020 total         {sum(L * n for L, n in lengths.items()) / 1000:.2f} m")
    if m.warnings:
        lines += ['', 'Warnings', '--------'] + [f'  {w}' for w in m.warnings]
    lines += ['', 'Collision check (18 poses: X/Y at both ends + center, Z top/bottom; door closed, cutter excluded)',
              '-' * 98]
    if hits:
        for (a, b), where in sorted(hits.items()):
            (x, y, z), v = where[0]
            lines.append(f"  {a} <-> {b}: {v:.0f} mm^3 at X{x:+.0f} Y{y:+.0f} Z{z:+.0f} ({len(where)} poses)")
    else:
        lines.append('  No collisions.')
    return '\n'.join(lines)


# --------------------------------------------------------------------------
# Document
# --------------------------------------------------------------------------
def style(obj, look):
    rgb, shine, transp = LOOKS[look]
    vo = obj.ViewObject
    try:
        mat = App.Material()
        mat.DiffuseColor = rgb
        mat.AmbientColor = tuple(0.3 * c for c in rgb)
        mat.SpecularColor = (shine * 0.6,) * 3
        mat.Shininess = shine
        vo.ShapeAppearance = (mat,)
    except Exception:
        vo.ShapeColor = rgb
    vo.Transparency = transp
    vo.LineColor = (0.12, 0.12, 0.12)
    vo.LineWidth = 1.0
    vo.Deviation = 0.1               # finer tessellation: smooth fillets and cylinders
    vo.AngularDeflection = 8.0
    vo.DisplayMode = 'Shaded' if look in SHADED else 'Flat Lines'


def make_document(m, path):
    name = 'DIYCNC'
    if name in App.listDocuments():
        App.closeDocument(name)
    doc = App.newDocument(name)
    if os.path.exists(path):
        os.remove(path)  # avoid FreeCAD's .FCBak copies

    sheet = doc.addObject('Spreadsheet::Sheet', 'Params')
    for row, (alias, note) in enumerate((('posX', f"range {-P['travel_x'] / 2:.0f} .. {P['travel_x'] / 2:.0f} mm"),
                                         ('posY', f"range {-P['travel_y'] / 2:.0f} .. {P['travel_y'] / 2:.0f} mm"),
                                         ('posZ', f"range {-P['travel_z']:.0f} .. 0 mm"),
                                         ('doorAngle', 'range 0 .. 100 deg'),
                                         ('explode', 'frame exploded view, mm (0 = assembled)'),
                                         ('sumpOut', 'coolant sump pulled out, mm (0 .. 450)')), start=1):
        sheet.set(f'A{row}', alias)
        sheet.set(f'B{row}', '0')
        sheet.setAlias(f'B{row}', alias)
        sheet.set(f'C{row}', note)

    names = ['Frame', 'FrameBaseFront', 'FrameBaseRear', 'FrameUprightL', 'FrameUprightR', 'FrameBeam',
             'TableAxis', 'XCarriage', 'ZAxis', 'Enclosure', 'Door']
    names += sorted(({p['container'] for p in m.parts if p['container']} | {dd['container'] for dd in m.dynamic}) - set(names))
    containers = {n: doc.addObject('App::Part', n) for n in names}
    for n in ('FrameBaseFront', 'FrameBaseRear', 'FrameUprightL', 'FrameUprightR', 'FrameBeam'):
        containers['Frame'].addObject(containers[n])
    containers['XCarriage'].addObject(containers['ZAxis'])
    # Exploded view: uprights lift and spread, the beam lifts twice as far.
    for n, sx in (('FrameUprightL', -1), ('FrameUprightR', 1)):
        containers[n].setExpression('.Placement.Base.z', 'Params.explode')
        containers[n].setExpression('.Placement.Base.x', f'{sx * 0.5} * Params.explode')
    containers['FrameBeam'].setExpression('.Placement.Base.z', '2 * Params.explode')
    containers['FrameBaseFront'].setExpression('.Placement.Base.y', '-1.2 * Params.explode')
    containers['Enclosure'].addObject(containers['Door'])
    containers['CoolantSump'].setExpression('.Placement.Base.y', '-Params.sumpOut')
    containers['TableAxis'].setExpression('.Placement.Base.y', 'Params.posY')
    containers['XCarriage'].setExpression('.Placement.Base.x', 'Params.posX')
    containers['ZAxis'].setExpression('.Placement.Base.z', 'Params.posZ')
    h = m.dims['hinge']
    containers['Door'].setExpression(
        '.Placement', f'placement(vector(0; {h.y:.3f}; {h.z:.3f}); rotation(vector(-1; 0; 0); Params.doorAngle))')
    default = {'frame': 'Frame', 'table': 'TableAxis', 'xcar': 'XCarriage', 'zaxis': 'ZAxis', 'door': 'Door'}

    for p in m.parts:
        obj = doc.addObject('Part::Feature', p['name'])
        obj.Shape = p['shape'].translated(-h) if p['group'] == 'door' else p['shape']
        containers[p['container'] or default[p['group']]].addObject(obj)
        if App.GuiUp:
            style(obj, p['look'])
    # Way covers, chain and nozzle hose are drawn at the home pose; re-run the macro (or
    # the snapshots) to redraw them elsewhere.
    for dd in m.dynamic:
        obj = doc.addObject('Part::Feature', dd['name'])
        shape = dd['fn'](0.0, 0.0, 0.0)
        obj.Shape = shape if shape is not None else Part.Shape()
        containers[dd['container']].addObject(obj)
        if App.GuiUp:
            style(obj, dd['look'])
    # Printed mould pieces, hidden: shown in the build renders, left out of the STEP export.
    mtop = doc.addObject('App::Part', 'Moulds')
    for folder, name, shape, kind, qty, note in getattr(m, 'moulds', []):
        if kind in ('cast-in', 'part'):
            continue                     # already in the model as real parts
        cname = MOULD_GROUPS[folder]
        grp = doc.getObject(cname) or doc.addObject('App::Part', cname)
        if grp.getParentGeoFeatureGroup() is None:
            mtop.addObject(grp)
        obj = doc.addObject('Part::Feature', f"{cname}_{kind}_{name}".replace('-', '_'))
        obj.Shape = shape
        grp.addObject(obj)
        if App.GuiUp:
            style(obj, 'printed')
    mtop.Visibility = False
    doc.recompute()
    doc.saveAs(path)
    return doc


def export_step(doc, path):
    try:
        import Import
        tops = [o for o in doc.Objects if o.TypeId == 'App::Part' and o.getParentGeoFeatureGroup() is None
                and o.Name != 'Moulds']
        Import.export(tops, path)
    except Exception as exc:
        print(f'STEP export failed: {exc}')


def zoom_to(view, objs):
    """Aim the orthographic camera at the combined bounding box of objs (global placement)."""
    from pivy import coin
    bb = App.BoundBox()
    for o in objs:
        if o is not None:
            s = o.Shape.copy()
            s.Placement = o.getGlobalPlacement()
            bb.add(s.BoundBox)
    c = bb.Center
    dv = view.getViewDirection()
    cam = view.getCameraNode()
    cam.position.setValue(coin.SbVec3f(c.x - dv.x * 3000, c.y - dv.y * 3000, c.z - dv.z * 3000))
    cam.focalDistance.setValue(3000)
    if hasattr(cam, 'height'):
        cam.height.setValue(bb.DiagonalLength * 1.05)


def snapshots(doc, out_dir, m):
    import FreeCADGui as Gui
    view = Gui.ActiveDocument.ActiveView
    view.setAnimationEnabled(False)
    sheet = doc.getObject('Params')
    enc, bench = doc.getObject('Enclosure'), doc.getObject('Workbench')
    axes = [doc.getObject(n) for n in ('TableAxis', 'XCarriage', 'WayCovers', 'CableChain', 'CoolantLines')]
    castings = [o for o in doc.Objects if o.Name.endswith('Casting')]
    hx, hy, hz = P['travel_x'] / 2, P['travel_y'] / 2, P['travel_z']

    def rear_iso():
        view.viewIsometric()
        view.setCameraOrientation(App.Rotation(Vector(0, 0, 1), 180).multiply(view.getCameraOrientation()))

    def look(d, up=Vector(0, 0, 1)):
        """Camera looking along direction d (world), with `up` towards the top of the image."""
        z = -Vector(*d).normalize()
        x = up.cross(z).normalize()
        y = z.cross(x)
        view.setCameraOrientation(App.Rotation(App.Matrix(x.x, y.x, z.x, 0, x.y, y.y, z.y, 0,
                                                          x.z, y.z, z.z, 0, 0, 0, 0, 1)))

    iso, front, right = view.viewIsometric, view.viewFront, view.viewRight
    # name, (x, y, z), view, focus objects, options
    shots = (
        ('enclosure_closed', (0, 0, 0), iso, None, dict(enc=True)),
        ('enclosure_open', (0, -hy, 0), iso, None, dict(enc=True, door=75)),
        ('machine_iso', (0, 0, 0), iso, None, {}),
        ('machine_extreme', (hx, hy, -hz), iso, None, {}),
        ('machine_right', (0, -hy, 0), right, None, {}),
        ('machine_front', (0, 0, 0), front, None, {}),
        ('coolant_system', (0, 0, 0), iso, None, dict(enc=True, bench=True)),
        ('detail_z_axis', (0, 0, -70), iso, ('ZPlate', 'SpindleBody', 'SpindleClamp', 'Z_MotorBody', 'XCarriagePlate'), {}),
        ('detail_nozzles', (0, 0, -100), iso, ('SpindleClamp', 'CoolantNozzle1', 'CoolantNozzle2', 'SpindleER20Nut', 'CoolantManifold'), {}),
        ('detail_way_covers', (0, -hy, 0), rear_iso, ('Table', 'CoverRollerRearL', 'CoverRollerRearR', 'CoverScrewRear', 'Y_BK12'), {}),
        ('detail_cable_chain', (hx, 0, 0), rear_iso, ('XChain', 'ChainMountFixed', 'ChainMountMoving'), {}),
        ('detail_table_drive', (0, 0, 0), rear_iso, ('Y_BK12', 'Y_MotorBody', 'Y_MotorEncoder', 'Y_MotorBracket', 'Y_Coupler'), {}),
        ('detail_coolant_sump', (0, 0, 0), lambda: look((0.55, 0.8, -0.25)),
         ('SumpPan', 'LegFrontL', 'LegFrontR', 'DrainOutlet'), dict(bench=True, enc=True)),
        ('detail_coolant_sump_out', (0, 0, 0), lambda: look((0.55, 0.8, -0.45)),
         ('SumpPan', 'SumpPump', 'LegFrontL', 'LegFrontR', 'BaseFrontCasting'), dict(bench=True, enc=True, sump=300)),
        ('frame_exploded', (0, 0, 0), iso, None, dict(mode='exploded')),
        ('frame_xray', (0, 0, 0), iso, None, dict(mode='xray')),
        # Frame on its own: castings, cast-in steel, joint hardware; gaskets in orange.
        ('frame_bare', (0, 0, 0), iso, None, dict(mode='bare')),
        ('frame_bare_rear', (0, 0, 0), rear_iso, None, dict(mode='bare')),
        ('frame_bare_exploded', (0, 0, 0), iso, None, dict(mode='bare', explode=180)),
        ('frame_bare_xray', (0, 0, 0), rear_iso, None, dict(mode='bare', xray=True)),
        ('frame_section_uprights', (0, 0, 0), iso, None, dict(mode='bare', section=('y', 'TieRodL1'))),
        ('frame_section_split', (0, 0, 0), lambda: look((1.0, 0.45, -0.5)), None,
         dict(mode='bare', section=('x', 'BaseSpigotR'))),
        ('frame_base_underside', (0, 0, 0), lambda: look((0.35, 0.55, 1.0)), ('BaseFrontCasting', 'BaseRearCasting'),
         dict(mode='bare', only=('FrameBaseFront', 'FrameBaseRear'))),
        ('gasket_base_split', (0, 0, 0), rear_iso, ('BaseFrontCasting',), dict(mode='bare', only=('FrameBaseFront',))),
        # Build steps (renders/build/): cast-in steel, moulds, frame assembly, axes
        ('build/01-steel-base-front', (0, 0, 0), iso, ('BaseFrontCasting',),
         dict(mode='bare', only=('FrameBaseFront',), xray=True)),
        ('build/02-mould-base-front', (0, 0, 0), lambda: look((0.35, 0.55, 1.0)), ('BaseFrontCasting',),
         dict(mode='bare', only=('FrameBaseFront',), xray=True, moulds=('MouldBaseFront',))),
        ('build/03-steel-base-rear', (0, 0, 0), rear_iso, ('BaseRearCasting',),
         dict(mode='bare', only=('FrameBaseRear',), xray=True)),
        ('build/04-mould-base-rear', (0, 0, 0), lambda: look((0.35, 0.55, 1.0)), ('BaseRearCasting',),
         dict(mode='bare', only=('FrameBaseRear',), xray=True, moulds=('MouldBaseRear',))),
        ('build/05-mould-upright', (0, 0, 0), lambda: look((0.8, 0.55, -0.45)), ('UprightLCasting',),
         dict(mode='bare', only=('FrameUprightL',), xray=True, moulds=('MouldUpright',))),
        ('build/06-mould-beam', (0, 0, 0), lambda: look((0.45, 0.8, -0.5)), ('BeamCasting',),
         dict(mode='bare', only=('FrameBeam',), xray=True, moulds=('MouldBeam',))),
        ('build/07-frame-base', (0, 0, 0), iso, ('BaseFrontCasting', 'BaseRearCasting'),
         dict(mode='bare', only=('FrameBaseFront', 'FrameBaseRear'))),
        ('build/08-frame-uprights', (0, 0, 0), iso, None,
         dict(mode='bare', only=('FrameBaseFront', 'FrameBaseRear', 'FrameUprightL', 'FrameUprightR'))),
        ('build/09-frame-beam', (0, 0, 0), iso, None, dict(mode='bare')),
        ('build/10-risers-supports', (0, 0, 0), iso, None,
         dict(mode='bare', extra=('Y_Riser', 'X_Riser', 'Y_BK12', 'Y_BF12', 'X_BK10', 'X_BF10'))),
        ('build/11-rails-screws-motors', (0, 0, 0), iso, None,
         dict(mode='bare', extra=('Y_Riser', 'X_Riser', 'Y_Rail', 'X_Rail', 'Y_BK12', 'Y_BF12', 'X_BK10', 'X_BF10',
                                  'Y_Screw', 'X_Screw', 'Y_Coupler', 'X_Coupler', 'Y_Motor', 'X_Motor'))),
        ('build/12-axes-spindle', (0, 0, 0), iso, None, {}),
        ('build/13-enclosure-coolant', (0, 0, 0), iso, None, dict(enc=True, bench=True)),
        ('gasket_upright_foot', (0, 0, 0), lambda: look((0.55, 0.65, 0.75)), ('UprightLCasting',),
         dict(mode='bare', only=('FrameUprightL',))),
    )
    structure = [o for o in doc.Objects if o.TypeId == 'Part::Feature'
                 and (o.Name in m.structure or o.Name.endswith('Casting'))]
    gaskets = [o for o in structure if o.Name.startswith('Gasket')]
    features = [o for o in doc.Objects if o.TypeId == 'Part::Feature']
    tops = [o for o in doc.Objects if o.TypeId == 'App::Part' and o.getParentGeoFeatureGroup() is None]

    def section(axis, through):
        """Cut the visible structure at the plane through `through`'s centre; keep the far side."""
        c = doc.getObject(through).Shape.BoundBox.Center
        big = 5000.0
        keep = (parts.box(-big, big, c.y, big, -big, big) if axis == 'y'
                else parts.box(c.x, big, -big, big, -big, big))
        saved = {}
        for o in structure:
            if o.Visibility:
                saved[o.Name] = o.Shape
                o.Shape = o.Shape.common(keep)
        return saved
    for name, (x, y, z), orient, focus, o in shots:
        mode = o.get('mode')
        for alias, val in (('posX', x), ('posY', y), ('posZ', z), ('doorAngle', o.get('door', 0)),
                           ('explode', o.get('explode', 180 if mode == 'exploded' else 0)), ('sumpOut', o.get('sump', 0))):
            sheet.set(alias, str(val))
        for dd in m.dynamic:
            shape = dd['fn'](x, y, z)
            doc.getObject(dd['name']).Shape = shape if shape is not None else Part.Shape()
        doc.recompute()
        enc.Visibility = o.get('enc', False)
        bench.Visibility = o.get('bench', False)
        for a in axes:
            a.Visibility = mode is None
        bare = mode == 'bare'
        shown_moulds = o.get('moulds', ())
        for t in tops:
            if t not in (enc, bench) and t not in axes:
                t.Visibility = (not bare and t.Name != 'Moulds') or t.Name == 'Frame' or (
                    t.Name == 'Moulds' and bool(shown_moulds))
        for f in features:
            parent = f.getParentGeoFeatureGroup()
            in_only = 'only' not in o or (parent is not None and parent.Name in o['only'])
            f.Visibility = (not bare or (f in structure and in_only)
                            or ('extra' in o and f.Name.startswith(o['extra']) and in_only)
                            or (parent is not None and parent.Name in shown_moulds))
        for c in castings:
            style(c, 'granite_hi' if bare else 'granite')
            c.ViewObject.Transparency = 75 if mode == 'xray' or o.get('xray') else 0
        for gk in gaskets:
            style(gk, 'gasket_hi' if bare else 'rubber')
        saved = section(*o['section']) if 'section' in o else {}
        orient()
        view.fitAll()
        if focus:
            zoom_to(view, [doc.getObject(n) for n in focus])
        Gui.updateGui()
        path = os.path.join(out_dir, f'{name}.png')
        os.makedirs(os.path.dirname(path), exist_ok=True)
        view.saveImage(path, 2800, 2100, 'White')
        subprocess.run(['sips', '-Z', '1400', path], capture_output=True)
        for n, shp in saved.items():
            doc.getObject(n).Shape = shp

    for alias in ('posX', 'posY', 'posZ', 'doorAngle', 'explode', 'sumpOut'):
        sheet.set(alias, '0')
    for dd in m.dynamic:
        shape = dd['fn'](0.0, 0.0, 0.0)
        doc.getObject(dd['name']).Shape = shape if shape is not None else Part.Shape()
    enc.Visibility = bench.Visibility = True
    for a in axes + tops + features:
        a.Visibility = True
    doc.getObject('Moulds').Visibility = False
    for gk in gaskets:
        style(gk, 'rubber')
    for c in castings:
        style(c, 'granite')
    doc.recompute()
    view.viewIsometric()
    view.fitAll()
    doc.save()


FOLDER_TITLES = [('base-front', 'Base, front half'), ('base-rear', 'Base, rear half'),
                 ('upright', 'Uprights (both the same: print quantities are for two)'), ('beam', 'Beam'),
                 ('machine', 'Machine parts')]


def export_prints(m):
    """STLs for every printed piece under print/, and docs/src/print-guide.md listing them."""
    root = os.path.join(ROOT, 'print')
    for dp, _, fn in os.walk(root):
        for f in fn:
            if f.endswith('.stl') or f == 'manifest.csv':
                os.remove(os.path.join(dp, f))
    rows = moulds.export(m.moulds, root)
    d = m.dims
    kinds = {'core': 'Pocket core (shell, stays in)', 'former': 'Former (removable)', 'filler': 'Corner filler (removable)',
             'plug': 'Pocket plug (removable)', 'liner': 'Liner (stays in)', 'cast-in': 'Cast-in part (stays in)',
             'part': 'Machine part'}
    boxes = {'base-front': f"{2 * d['base_half']:.0f} x {-d['base_y0']:.0f} x {d['base_top']:.0f}",
             'base-rear': f"{2 * d['base_half']:.0f} x {d['base_y1']:.0f} x {d['base_top']:.0f}",
             'upright': f"{P['upright_t']:.0f} x {d['up_y1'] - (d['beam_face'] - P['upright_foot']):.0f}"
                        f" x {d['beam_bot'] - d['base_top']:.0f}, sloped front board",
             'beam': f"{2 * d['outer']:.0f} x {P['beam_d']:.0f} x {P['beam_h']:.0f}"}
    faces = {'base-front': 'top face down', 'base-rear': 'top face down', 'upright': 'foot down',
             'beam': 'front (rail) face down'}
    total_g = sum(r['grams'] for r in rows)
    total_n = sum(r['qty'] for r in rows)
    lines = ['# Print guide', '',
             'Every printed part for the castings and the machine, cut to fit a Bambu A1 mini',
             f'(180 mm cube; no piece is over {moulds.BED:.0f} mm). The STL files are in `print/`, one folder per',
             'casting, with the list in `print/manifest.csv`. They are written by `model/build_cnc.py` on every run.', '',
             f'**About {total_n} prints, roughly {total_g / 1000:.1f} kg of PETG.** The filament figures are rough estimates.', '',
             '## Settings', '',
             '- **PETG for everything.** Thick sections of curing epoxy get warm, and PLA softens at about 55 °C.',
             '- 0.4 mm nozzle, 0.2 mm layers.',
             f'- **Cores** (`core-*`): thin shells, {moulds.WALL:.1f} mm walls, so they print solid with any infill setting. '
             'They are already turned with the closed face on the bed.',
             '- **Fillers, formers, plugs** (`filler-*`, `former-*`, `plug-*`): 3 walls, 15 % infill.',
             '- **Liners and cast-in parts** (`liner-*`, `cast-in-*`): 4 walls, 40 % infill.',
             '- Anything named `-partNofM` was cut to fit the bed. Glue the parts edge to edge with CA or epoxy',
             '  and tape over the seam. Check the joined piece against the drawing before casting.', '',
             '## How the pieces are used', '',
             '- The mould boxes are 18 mm melamine board, not printed: the flat board is what the important',
             '  faces are cast against. Box sizes (inside) and casting orientation are in the table below.',
             '- **Removable pieces** (formers, fillers, plugs): screw or hot-glue them to the board, then 3-5 coats',
             '  of paste wax and PVA like the rest of the mould. Reuse the fillers for the second upright.',
             '- **Pieces that stay in** (cores, liners, cast-in parts): no wax; scuff and degrease them so the',
             '  epoxy grips. Cores float: fill them with dry sand and hold them down with a bridge across the mould.', '',
             '| Casting | Mould box inside (mm) | Cast with |', '|---|---|---|']
    lines += [f'| {t} | {boxes[k]} | {faces[k]} |' for k, t in FOLDER_TITLES if k in boxes]
    lines += ['', '![Base rear mould: cores (orange) in the pockets](../../renders/build/04-mould-base-rear.png)', '',
              '## Foam cores instead of printed ones', '',
              f"The pocket cores are about {sum(r['grams'] for r in rows if r['kind'] == 'core') / 1000:.1f} kg of the PETG. "
              'The rectangular ones are quick to cut from XPS foam board on a table saw or with a hot wire;',
              'wrap them in packing tape and wax them. The corners are chamfered 8-10 mm (30 mm on the rear',
              'centre core), and the triangles are right triangles. Glue foam cores to the bridge so they',
              'cannot float. Sizes (outline x depth from the underside):', '',
              '| Casting | Core | Outline (mm) | Depth (mm) |', '|---|---|---|---|']
    for folder, name, shape, kind, qty, note in m.moulds:
        if kind == 'core':
            bb = shape.BoundBox
            lines.append(f'| {folder} | {name} | {bb.XLength:.0f} x {bb.YLength:.0f} | {bb.ZLength:.0f} |')
    lines.append('')
    for key, title in FOLDER_TITLES:
        sub = [r for r in rows if r['folder'] == key]
        if not sub:
            continue
        lines += [f'## {title}', '', f'Folder `print/{key}/`, about {sum(r["grams"] for r in sub):.0f} g.', '',
                  '| File | What | Qty | Size (mm) | Notes |', '|---|---|---|---|---|']
        for r in sub:
            lines.append(f"| `{r['file']}` | {kinds[r['kind']]} | {r['qty']} | {r['size']} | {r['note']} |")
        lines.append('')
    with open(os.path.join(ROOT, 'docs', 'src', 'print-guide.md'), 'w') as fh:
        fh.write('\n'.join(lines))
    print(f'print/: {len(rows)} STL files, about {total_g / 1000:.1f} kg PETG')


def main():
    m = build()
    hits = collisions(m)
    text = report(m, hits)
    print(text)
    with open(os.path.join(ROOT, 'docs', 'report.txt'), 'w') as fh:
        fh.write(text + '\n')
    export_prints(m)
    if not App.GuiUp:
        return  # a headless save would drop the colors from DIYCNC.FCStd
    doc = make_document(m, os.path.join(HERE, 'DIYCNC.FCStd'))
    export_step(doc, os.path.join(HERE, 'DIYCNC.step'))
    if os.environ.get('CNC_SNAPSHOTS'):
        img = os.path.join(ROOT, 'renders')
        os.makedirs(img, exist_ok=True)
        for dp, _, fn in os.walk(img):
            for f in fn:
                if f.endswith('.png'):
                    os.remove(os.path.join(dp, f))
        snapshots(doc, img, m)
        App.closeDocument(doc.Name)
        for f in os.listdir(HERE):
            if f.endswith('.FCBak'):
                os.remove(os.path.join(HERE, f))
        import FreeCADGui as Gui
        from PySide import QtCore
        QtCore.QTimer.singleShot(0, Gui.getMainWindow().close)


main()
