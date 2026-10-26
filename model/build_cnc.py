"""Parametric layout model of a fixed-gantry, epoxy-granite desktop CNC mill.

Target envelope is the Shariff DMC2 Mini (12 x 7 x 5.5 in travel). The long
axis rides on the table so the gantry beam stays short and stiff. Component
geometry (rails, blocks, ballscrew hardware, motors, spindle) lives in parts.py.
The frame is five bolt-together epoxy-granite castings with cast-in steel, and the
enclosure bolts to the base top.

Headless (collision check, docs/5-design/report.txt and the print/ STLs):
    /Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd model/build_cnc.py
In the FreeCAD GUI (also rebuilds the colored DIYCNC.FCStd and DIYCNC.step):
    Macro > Macros... > select model/build_cnc.py > Execute

Edit P below and re-run. In the GUI, jog the axes and open the door by editing
posX / posY / posZ / doorAngle in the Params spreadsheet.

Coordinates: X right, Y toward the back (operator stands at -Y), Z up.
Origin is on the casting's underside directly below the spindle axis with all
axes at home (X and Y centered, Z fully up).
"""

import collections
import csv
import importlib
import itertools
import json
import math
import os
import re
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
import molds  # noqa: E402
import moldbox  # noqa: E402
import parts  # noqa: E402
import skeleton as sk  # noqa: E402

importlib.reload(parts)  # pick up edits when re-run inside one GUI session
importlib.reload(molds)
importlib.reload(moldbox)
importlib.reload(sk)
from molds import HW, Fix  # noqa: E402
from skeleton import T12, T14, T38  # noqa: E402

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
    # The aluminum plates are stock 6061 flat-bar widths (10 in table, 6 in X carriage and Z plate), so the only cut
    # is their length.
    table_len=320.0, table_w=254.0, table_t=19.05, table_hole_pitch=25.0,

    # Beam axis (X): owned HGR15-400 pair + SFU1204-400 kit
    beam_rail_len=400.0, beam_rail_spacing=100.0, beam_blk_pitch=90.0,   # blocks span 151.4 on the 6 in carriage
    beam_screw_len=400.0, beam_riser_t=15.875,    # 5/8 in risers clear the 39 mm BK10
    carriage_w=152.4, carriage_t=15.875,

    # Z axis: moving-rail (blocks fixed to the carriage), HGR15-300 + SFU1204-300
    z_rail_len=300.0, z_rail_spacing=100.0, z_blk_pitch=80.0,
    z_screw_len=300.0, z_nut_on_plate=230.0, z_riser_t=15.875,
    zplate_w=152.4, zplate_t=15.875,     # clamp foot is 148 wide

    # Motors (parts.MOTORS): closed loop on X/Y, the owned open-loop NEMA 23 on Z
    motor_x='23HS30-5004D-E1000', motor_y='23HS30-5004D-E1000', motor_z='23HS30-3004S',
    # Integrated bearing seat + motor brackets (parts.HM); None = the kit BK and a separate bracket. X and Z get
    # the HM10-57 once the one on hand is measured.
    bracket_y='HM12-57',

    # Epoxy-granite castings: base (front + rear halves), two uprights, beam
    # The base's underside pockets follow a topology optimization (analysis/, see base_pockets).
    base_h=110.0, base_corner_r=40.0, base_split_y=0.0, split_wall=15.0,
    base_core_skin=20.0,    # top skin over the pockets
    base_girder_w=80.0,     # full-depth girder under each table rail, rail tube in the middle
    base_tie=90.0,          # full-depth tie between the girders, this far ahead of the split
    base_tie_rear=55.0,     # ... and this far behind it
    base_foot_pockets=True, # pockets under the upright feet, between ribs and around the tie-rod couplers
    base_front_wall=70.0,   # the coolant trough and outlet run through it
    # The base's lower outside edge beveled (in, up), 1-1/2 x 2-1/2 in: its outside face reads as a 46 mm
    # slab, the pockets keep clear of it, and the mold's bevel strips are a 2x3 ripped corner to corner
    # (or printed). It costs no stiffness (design notes).
    base_bevel=(38.1, 63.5),
    # Uprights are raked buttresses (from the frame topology optimization, analysis/): the foot runs
    # forward along the base and the front face slopes up to just ahead of the beam.
    upright_t=80.0, upright_d=180.0, upright_front=40.0,
    upright_foot=260.0, upright_top_front=70.0,   # foot front / top front, mm ahead of the beam face
    upright_nose=20.0, upright_nose_r=12.0,       # blunt toe: vertical nose, rounded into the slope
    # The back face rakes too, the foot running 40 mm behind the beam's back: the upright reads as a tapered
    # buttress instead of a block, and it is stiffer (+1-2 %, design notes). The enclosure's rail is 10 mm behind it.
    upright_back_rake=40.0,
    # Upright skeleton, all stock: a 3/8 x 2 in flat-bar foot, two 2x2 tube columns (a tie rod inside each,
    # screwed into the top plate's lower bar) and the top plate
    column_ys=(35.0, 45.0),  # column center lines: this far behind the upright's top front / ahead of its back
    toe_rod=35.5,            # the toe tie rod, mm behind the foot's front edge; its nut sits on the foot plate
    column_len=206.4,        # 8-1/8 in, bought at length: 5 mm short, bedded in thickened epoxy on the foot bar
    beam_d=140.0, beam_h=146.05, beam_back_r=40.0, edge_r=6.0,  # 5 in face bar between two 3/8 in end bars
    # Outside edge rounds (quarter-round strips in the mold corners): castings' outer edges,
    # the beam's lower back edge (meets the uprights' back faces) and its rail-face edges
    round_r=10.0, beam_back_low_r=10.0, beam_face_r=3.0,

    # Cast-in steel and joints (tube = (size, wall)): US stock sizes in stock lengths, so
    # nothing is cut to length: 2 x 2 x 3/16 in (the upright and pedestal columns: the heavier wall is
    # steel in place of alumina grit) and 1-1/2 x 1-1/2 x 1/8 in mild steel.
    frame_tube=(50.8, 4.7625), post_tube=(38.1, 3.175),
    # Bought lengths, nothing cut: 12 in base (the split sockets), 18 in beam, 6 in spigots.
    tube_len=dict(base=304.8, spigot=152.4),
    # Real tube isn't nominal. A supplier's saw cut is good to about +/-1/8 in, and A500 tube is
    # +/-0.5 mm across the flats with a +/-10 % wall and a weld seam inside. So every cast-in piece is
    # set from one end (its datum) and its other end has room in the casting (the report checks it
    # against tube_cut_tol), and every printed part that slips on or into a tube has tube_fit a side
    # and clears the seam. Once the steel is here, caliper it, put the real sizes in frame_tube and
    # post_tube (outside across the flats, (outside - inside) / 2), set tube_fit to 0.25 and re-run
    # before printing those parts.
    tube_cut_tol=3.2, tube_fit=0.5, tube_seam=(6.0, 1.2),   # seam relief (width, depth) in printed faces
    stud_tol=1.6,        # a bought stud's length, +/-1/16 in
    # Printed PETG spigot sleeves (1-1/2 in spigot in the 2 in tube), this long in each tube.
    # The uprights have no posts: the tie rods clamp each foot to the base through steel, friction under
    # that clamp carries the side load, and two dowels per foot, grouted into oversize holes in the upright
    # at first assembly, locate it (the grout takes up whatever the two molds differ by).
    spigot_sleeve=70.0,
    # Legs: 6 in pieces of the 1-1/2 in tube cast into the base corners, with threaded inserts
    # for the leveling feet. The coolant sump slides in underneath, between them.
    leg_len=152.4, leg_embed=35.0,
    # Leg centers in from the base's sides, front and back: tucked in behind the bevel, which shortens the
    # span the base bends over between its feet (modes +11-31 %). The rear pair stays clear of the pedestal bars.
    leg_inset=(65.0, 65.0, 62.0),
    # O-ring cord seals at the epoxy-to-epoxy joints: the faces still bear on each other,
    # the cord sits in a groove (3 mm cord, 4 x 2.3 groove = ~25 % squeeze)
    gasket_cord=3.0, gasket_groove=(4.0, 2.3), gasket_split_z=92.0,
    # Joint hardware in hardware-store inch sizes: 1/2-13 rod, couplers and nuts, 3/8-16 grade 8
    # beam bolts, 3/8 in dowels.
    tie_rod_d=12.7, beam_bolt_d=9.525, dowel_d=9.525, dowel_proud=15.0,
    # The uprights are tied to steel top and bottom. Each top plate is two 1/2 x 2-1/2 in flat bars: the
    # lower one is tapped for the beam's studs and for the two column tie rods. At the bottom every tie rod
    # runs right through the base pedestal to its bottom bar, nut and washer below it. So the beam, the top
    # plate, the columns, the pedestal and the rods are one steel chain, with the epoxy granite clamped in
    # it, and there is no thread in the epoxy granite to come loose: every nut can be retightened.
    top_plate_t=25.4, plate_layer=12.7,
    beam_stud=190.5,         # the beam's eight 3/8-16 grade B7 studs, 7-1/2 in bought at length, screwed into the top plates
    drip_shield_t=3.0,       # ACM offcut over the X rails; the front studs' nuts clamp it to the beam top
    beam_bar_t=19.05,        # the beam's 5 in face and back bars, 3/4 in: steel in place of alumina grit (design notes)
    beam_spacer=63.5,        # 1/2 in x 2-1/2 in pipe nipples between the beam's face and back bars
    rod_tail=6.0,            # rod past its far nut; the rods are B7 studs bought in 1/4 in steps, and the step ends up here
    slope_pocket_d=32.0,     # toe tie-rod nut pocket, down to the foot plate
    # In the uprights the tie-rod holes are cast on 5/8 in rods (1.6 mm clearance a side) and the base
    # dowel's hole is 1/2 in, grouted with the posts: the uprights' own mold sets them.
    up_rod_hole=15.875, up_dowel_hole=12.7,
    beam_bolt_hole=12.7,     # the beam's cap-screw holes, cast on 1/2 in rods (1.6 mm a side over 3/8 in)
    plate_dowel_hole=14.0,   # the beam's dowels in the top plates: oversize, grouted at assembly
    # Cast-in threaded inserts (thread, outer diameter, length): the risers are bedded in epoxy
    # AND held down by counterbored low-head M5 screws under the rail; the BK/BF supports bolt
    # straight into M6 inserts. Nothing bolts to the cast-in tubes.
    # On the beam face the X BK/BF sit over the front beam tube, so they bolt to steel pads
    # (1/4 x 2-1/2 in flat bar, tapped M6) cast flush into the face against the tube.
    insert_m5=(5.0, 8.0, 12.0), insert_m6=(6.0, 10.0, 15.0), riser_cbore=(9.5, 4.5),
    side_clear=10.0,

    # Spindle: GDZ80-2.2 water-cooled, ER20, in the 80 mm cast foot clamp (bore 50 off the foot)
    clamp_off=50.0, clamp_lift=5.0, tool_stickout=30.0,

    # Enclosure: 2020 frame bolted to the base top, 4 mm polycarbonate, lift-up front door.
    # The base footprint matches the enclosure; its sealed top is the coolant floor.
    foot_h=20.0, enc_clear=15.0, panel_t=4.0, door_lap=30.0,
    motor_cutout=72.0,

    # Molds: melamine board (measure yours: the printed saddles and brackets are drawn for it), every
    # wall this much taller than its casting, so all the bolts go through above the pour line.
    mold_board=19.05, mold_freeboard=25.0,    # Home Depot 3/4 in white melamine is a true 0.750 in
    # XPS foam (one 2 in board) instead of PETG for the base pocket cores (only their posts are printed):
    # hidden, and they only need to be within a millimeter or two. False prints them
    # (about 1.4 kg more PETG). foam_formers also cuts the coolant trough and gutters and the beam's back
    # edge from foam; they shape faces you see and drain coolant, so they print by default.
    foam=True, foam_formers=False,

    eg_density=2.35,     # kg/L, epoxy granite
    # Aluminum oxide grit for the coarse sand in the beam and uprights, same volume (analysis/alumina.py):
    # about +9 % frame stiffness for $110. The 3/4 in beam bars and 3/16 in column walls give more for about
    # half that, so the mix is plain sand everywhere and the grit is an option, decided before the pour:
    # alumina=(('brown #16 (coarse sand)', 0.275, 3.95 / 2.65),).
    # (name, share of the sand mix by weight, density relative to sand)
    alumina_castings=('Upright', 'Beam'),
    alumina=(),
    eg_epoxy_frac=0.085,  # epoxy mass fraction, with well-graded aggregate + whiting (calcium carbonate) fines;
                          # check it with the jar test and test bars (build guide)
)

# rgb, shininess (0..1), transparency (0..100)
LOOKS = {
    'granite': ((0.50, 0.50, 0.52), 0.05, 0),     # as cast: gray aggregate and whiting in clear epoxy
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
    'printed_dark': ((0.50, 0.50, 0.52), 0.05, 0),   # printed in gray to match the castings (pocket caps)
    'shim': ((0.80, 0.81, 0.84), 0.85, 0),
    'wood': ((0.74, 0.58, 0.40), 0.10, 0),
    'melamine': ((0.93, 0.93, 0.90), 0.30, 62),   # mold boards, see-through in the renders
    'foam': ((0.45, 0.68, 0.92), 0.05, 30),       # XPS foam mold pieces
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
        self.coupler_len = {}
        self.dims = {}
        self.warnings = []
        self.frame_container = 'FrameBaseRear'
        self.dynamic = []
        self.structure = set()   # castings, cast-in steel, joint hardware, gaskets
        self.anchors = []        # (point on the casting face, unit normal out of it, insert)
        self.plates = []         # flat bar in the skeletons (skeleton.Plate)
        self.base_tapped = []    # (plate, container): base plates cast_anchors taps, then adds
        self.tubes = []          # stock tube in the skeletons (skeleton.Tube)

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


def screw_axis(m, f, tag, kind, length, u0, bf, bk, fixed_group, nut_group, nut_u, carrier_w, motor_min_u, motor,
               bracket=None):
    """Ballscrew, BF/BK supports, coupler, bracket and motor on fixed_group; nut + housing on nut_group.

    u0 is the BF outer face; length is the overall machined screw length. The nut housing
    bolts under the moving part at w = carrier_w. Returns the motor face position along u.
    bracket: an integrated HM bearing seat + motor bracket (parts.HM) in place of the BK and kit bracket, its
    bearing end where the BK's inner face would be, so the BK-machined screw end fits it.
    """
    a = parts.SUPPORT[bk]['h']
    e = parts.ENDS[kind]
    place = f.place
    screw, u1, s0, s1 = parts.ballscrew(kind, u0, length, bf, bk, a)
    m.add(f'{tag}_Screw', fixed_group, place(screw), 'steel')
    m.add_all(f'{tag}_{bf}', fixed_group, parts.support(bf, u0, a, e['bf_a'] / 2), place)
    ub = u1 - parts.SUPPORT[bk]['L']
    if bracket:
        m.add(f'{tag}_MotorBracket', fixed_group, place(parts.hm_bracket(bracket, ub)), 'black')
        m.add(f'{tag}_LockNut', fixed_group, place(parts.ring_u(parts.SUPPORT[bk]['lock'][0], e['bk_a'] / 2, u1,
                                                                u1 + parts.SUPPORT[bk]['lock'][1], 0, a)), 'black')
    else:
        m.add_all(f'{tag}_{bk}', fixed_group, parts.support(bk, ub, a, e['bk_a'] / 2, lock_r=e['bk_a'] / 2), place)
    if fixed_group == 'frame':
        # the BF and the BK (or HM bracket) bolt into M6 holes tapped in the steel of the base top / beam face
        n = f.m.multVec(Vector(0, 0, 1)) - f.m.multVec(Vector(0, 0, 0))
        sp = parts.SUPPORT[bf]
        pts = [(u0 + c, v) for c in sp['C'] for v in (-sp['P'] / 2, sp['P'] / 2)]
        if bracket:
            pts += parts.hm_holes(bracket, ub)
        else:
            sp = parts.SUPPORT[bk]
            pts += [(ub + c, v) for c in sp['C'] for v in (-sp['P'] / 2, sp['P'] / 2)]
        for u, v in pts:
            m.anchors.append((f.m.multVec(Vector(u, v, 0)), n, 'insert_m6'))

    shaft_r = parts.MOTORS[motor]['shaft_d'] / 2
    if bracket:
        # The bracket sets the motor face; the coupler bridges the stub and the motor shaft, centered on the gap.
        hm = parts.HM[bracket]
        face = ub + hm['L']
        tip, lo, hi = face - parts.SHAFT_LEN, *hm['coupler']
        span = min(max(tip + 15.0 - (s1 - 15.0), lo), hi)
        c0 = (s1 + tip) / 2 - span / 2
        c1 = c0 + span
        if min(s1 - c0, c1 - tip) < 10.0:
            m.warnings.append(f'{tag}: the {span:.0f} mm coupler takes only {min(s1 - c0, c1 - tip):.0f} mm of the '
                              f'stub or the motor shaft')
        m.coupler_len[tag] = span
    else:
        # The motor shaft (21 long) reaches 15 into the 30 mm coupler that sits on the stub.
        c0 = s0
        face = max(c0 + 30.0 + parts.SHAFT_LEN - 15.0, motor_min_u)
        c1 = face - (parts.SHAFT_LEN - 15.0)
        if c1 - c0 > 30.5:
            m.warnings.append(f'{tag}: motor pushed out to clear the moving parts; needs a {c1 - c0:.0f} mm '
                              f'coupler or a {length + c1 - c0 - 30:.0f} mm screw')
        m.coupler_len[tag] = c1 - c0
        m.add(f'{tag}_MotorBracket', fixed_group, place(parts.motor_bracket(u1, face, a)), 'black')
    if face < motor_min_u:
        m.warnings.append(f'{tag}: the bracket puts the motor {motor_min_u - face:.0f} mm into the moving parts')
    m.add(f'{tag}_Coupler', fixed_group, place(parts.coupler(c0, c1, a, e['stub'] / 2, shaft_r)), 'alu')
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
    g['ux'] = (d['inner'] + d['outer']) / 2                    # upright center line
    g['rod_y'] = (d['up_y0'] + d['up_y1']) / 2                 # middle of the upright's top
    g['pocket_bot'] = d['beam_bot'] - P['top_plate_t']         # underside of the upright's top plate
    g['up_front'] = d['beam_face'] - P['upright_foot']         # front of the upright foot
    g['up_top_front'] = d['beam_face'] - P['upright_top_front']
    g['up_back_foot'] = d['up_y1'] + P['upright_back_rake']    # back of the upright foot
    g['foot_top'] = d['base_top'] + T38                        # top of the upright's foot plate (3/8 in)
    # tie rods (x, y, nut seat), all on the upright's center line: one inside each column (nut in the
    # top plate) and one at the toe (nut on the foot plate, in a pocket from the slope)
    g['columns'] = (d['up_y0'] + P['column_ys'][0], d['up_y1'] - P['column_ys'][1])
    nut_seat = d['beam_bot'] - P['plate_layer']
    g['tie_rods'] = [(g['ux'], cy, nut_seat) for cy in g['columns']]
    g['tie_rods'].append((g['ux'], g['up_front'] + P['toe_rod'], g['foot_top']))
    g['dowel_ys'] = (g['columns'][0] - 64.5, sum(g['columns']) / 2)   # the two base dowels under each upright
    g['bolt_xs'] = (g['ux'] - 22.0, g['ux'] + 22.0)            # beam cap screws
    g['bolt_ys'] = (d['beam_face'] + 25.0, d['beam_face'] + P['beam_d'] - 25.0)
    g['beam_dowel_y'] = d['beam_face'] + 70.0
    # base grid: a girder under each Y rail (web 12 mm outboard of the rail line, clear of the riser
    # hold-downs), a pedestal under each upright, cross plates at the split, the Y ballscrew supports and
    # the front; the draw rods run along the girders from the front face to the back face
    g['rail_x'] = g['girder_x'] = g['draw_rod_x'] = P['table_rail_spacing'] / 2   # girder tube under each rail
    g['pin_x'] = P['table_rail_spacing'] / 2 + 32.0                               # split dowel pins, beside it
    g['front_web'] = d['base_y0'] + 56.5                       # front cross plate (y of its front face)
    g['rear_end'] = d['base_y1'] - 29.5                        # girders' rear end plates (y of their front face)
    y_tail = parts.ENDS['SFU1605']['bk_e'] - parts.SUPPORT['BK12']['L'] + parts.ENDS['SFU1605']['stub_l']
    g['y_bf'] = d['y_bk'] - (P['table_screw_len'] - y_tail) + parts.SUPPORT['BF12']['L'] / 2   # BF12 center line
    g['y_bkc'] = d['y_bk'] - parts.SUPPORT['BK12']['L'] / 2                                       # BK12 center line
    g['split'] = P['base_split_y']
    g['outlet'] = (0.0, d['base_y0'] + max(30.0, P['base_bevel'][0] + 15.0))   # coolant drain (x, y): straight down into the sump
    ix, iy0, iy1 = P['leg_inset']
    g['legs'] = [(sx * (d['base_half'] - ix), y) for y in (d['base_y0'] + iy0, d['base_y1'] - iy1) for sx in (-1, 1)]
    g['gasket_len'] = 0.0
    g['draw_z'] = d['base_top'] - T38 - GIRDER[1] / 2              # the girders' center (and their draw rods)
    g['tie_z'] = d['base_top'] - T38 - CROSS / 2 - 3.5               # the cross tubes' center (and their rods)
    return g


GIRDER = (50.8, 76.2, 3.175)      # 2 x 3 x 1/8 in rectangular tube (wide, tall, wall)
CROSS = 38.1                      # 1-1/2 x 1-1/2 x 1/8 in square tube


BEVEL_WOOD = ('Or, instead of printing the strips: rip a 2x3 corner to corner on a table saw and screw the halves '
              'to the wall from outside (#8 x 1-1/4 in, every 150 mm).')
BASE_BRIDGES = {'base-front': (-230.0, -130.0, -60.0), 'base-rear': (100.0, 170.0, 280.0)}   # y of the base mold's bridges


class Steel:
    """Collects cast-in steel and joint hardware for the mass total."""

    def __init__(self, m):
        self.m, self.volume = m, 0.0

    def add(self, name, container, shape, look='steeltube'):
        self.m.add(name, 'frame', shape, look, container=container)
        self.m.structure.add(name)
        if look != 'printed':
            self.volume += shape.Volume

    def plug(self, name, container, axis, c1, c2, size, a0, a1, closed):
        """Printed end plug that keeps the casting out of a hollow tube: a cup, closed (2 mm) at the
        tube's end (`closed`, a0 or a1) and open toward the inside of the tube. `size` is the tube's
        inside; the cup is tube_fit a side smaller, with rounded corners and seam grooves."""
        s = size - 2 * P['tube_fit']
        env, _ = parts.square_tube(axis, c1, c2, s, 2.5, a0, a1)      # 3.75 mm corner rounds
        b0, b1 = (a0 + 2.0, a1 + 1.0) if closed == a0 else (a0 - 1.0, a1 - 2.0)
        cup = env.cut(parts.square_tube(axis, c1, c2, s - 4.8, 0.1, b0, b1)[0])
        self.add(name, container, seam_relief(cup, axis, c1, c2, s, a0, a1), 'printed')


def seam_relief(shape, axis, c1, c2, s, a0, a1):
    """Groove down the middle of each outside face of a printed square section (size s, along
    `axis` from a0 to a1, centered on (c1, c2)) that goes inside a steel tube: clears the weld seam."""
    w, dp = P['tube_seam']
    h = s / 2
    cuts = []
    for p0, p1, q0, q1 in ((h - dp, h + 1, -w / 2, w / 2), (-h - 1, -h + dp, -w / 2, w / 2),
                           (-w / 2, w / 2, h - dp, h + 1), (-w / 2, w / 2, -h - 1, -h + dp)):
        if axis == 'x':
            cuts.append(parts.box(a0 - 1, a1 + 1, c1 + p0, c1 + p1, c2 + q0, c2 + q1))
        elif axis == 'y':
            cuts.append(parts.box(c1 + p0, c1 + p1, a0 - 1, a1 + 1, c2 + q0, c2 + q1))
        else:
            cuts.append(parts.box(c1 + p0, c1 + p1, c2 + q0, c2 + q1, a0 - 1, a1 + 1))
    return shape.cut(cuts)


def chamfered(x0, x1, y0, y1, c):
    """Rectangle outline (x, y) with 45-degree corner chamfers c."""
    return [(x0 + c, y0), (x1 - c, y0), (x1, y0 + c), (x1, y1 - c), (x1 - c, y1), (x0 + c, y1), (x0, y1 - c), (x0, y0 + c)]


def bevel_clamp(pockets, g):
    """Pull the pockets in clear of the beveled lower edge (20 mm of casting inside it), dropping any
    that end up too narrow to bother with."""
    bi = P['base_bevel'][0]
    if bi <= 0:
        return pockets
    lim = bi + 20.0
    x1, y0, y1 = g['base_half'] - lim, g['base_y0'] + lim, g['base_y1'] - lim
    out = []
    for poly, z, name in pockets:
        pts = [(math.copysign(min(abs(x), x1), x), min(max(y, y0), y1)) for x, y in poly]
        pts = [p for i, p in enumerate(pts) if p != pts[i - 1]]
        xs, ys = [x for x, _ in pts], [y for _, y in pts]
        if max(xs) - min(xs) >= 25.0 and max(ys) - min(ys) >= 25.0:
            out.append((pts, z, name))
    return out


def rounded_rect(x0, x1, y0, y1, r, z):
    """Closed wire: a rectangle with corner radius r at height z, always started at the same corner."""
    c = [(x1 - r, y0 + r, -90), (x1 - r, y1 - r, 0), (x0 + r, y1 - r, 90), (x0 + r, y0 + r, 180)]
    edges = []
    for i, (cx, cy, a) in enumerate(c):
        pts = [Vector(cx + r * math.cos(math.radians(a + t)), cy + r * math.sin(math.radians(a + t)), z) for t in (0, 45, 90)]
        edges.append(Part.Arc(*pts).toShape())
        nx, ny, na = c[(i + 1) % 4]
        edges.append(Part.LineSegment(pts[2], Vector(nx + r * math.cos(math.radians(na)), ny + r * math.sin(math.radians(na)), z)).toShape())
    return Part.Wire(edges)


def base_pockets(g):
    """Underside pockets of the base: (outline [(x, y), ...], pocket top z, name). All open to the
    bottom, so the cores (printed shells or foam) pull straight out.

    The layout follows the topology optimization in analysis/ (see the design notes): two full-depth girders
    under the table rails, a full-depth tie between them behind the split, solid knees from
    the girders out under the upright feet, and thin skin nearly everywhere else.
    """
    top, half, y0, y1 = g['base_top'], g['base_half'], g['base_y0'], g['base_y1']
    zp = top - P['base_core_skin']
    s2, gw = P['table_rail_spacing'] / 2, P['base_girder_w'] / 2
    gi, go = s2 - gw, s2 + gw                       # girder inner and outer faces
    yf0, yf1 = y0 + P['base_front_wall'], g['split'] - P['split_wall']
    tie = g['split'] + P['base_tie_rear']
    ry = g['rod_y']
    foot = g['up_front']
    sw = P['split_wall'] + 10.0                      # full-depth band either side of the split
    ob = g['ux'] + 38.1 + 9.0                        # outboard of the pedestal (and the cross-rod nuts)
    bfw = g['y_bf'] + 12.0                           # the BF12 cross plate, just behind the screws
    leg_y = g['legs'][0][1] + P['post_tube'][0] / 2  # back face of the front legs
    out = [(chamfered(-gi, gi, yf0, bfw - 20.0, 10.0), zp, 'center-a'),       # front, between the girders
           (chamfered(-gi, gi, bfw + 20.0, g['split'] - P['base_tie'], 10.0), zp, 'center-b'),
           (chamfered(-gi + 6, gi - 6, tie, 245.0, 30.0), zp, 'center')]   # rear, clear of the cross rods' nuts
    for sx in (-1, 1):
        if P['base_foot_pockets']:
            # Under the upright feet: a full-depth rib across the foot's front end, another along the
            # split, and pockets between them that keep clear of the solid band under each upright's
            # center line, where the tie rods run down to the steel anchor bar.
            # The outboard pocket runs up to the front rib.
            cx = g['ux'] - 38.1 - 12.0                    # inboard of the pedestal
            sock = g['up_y0'] - 0.5                          # a rib across the foot
            front_end = foot + 10.0
            feet = [(chamfered(go + 6.0, cx, g['split'] + sw, sock - 5.0, 10.0), zp, 'foot-b')]
            knee_y0, outer_y0 = sock + 5.0, sock + 15.0
        else:
            front_end, feet, knee_y0, outer_y0 = foot - 20.0, [], tie, 60.0
        side = [
            (chamfered(go + 10.0, half - 40.0, max(yf0, leg_y + 12.0), front_end - 20.0, 10.0), zp, 'outboard'),  # front, outboard
            (chamfered(go + 5.0, 236.0, y0 + 15.0, yf0, 10.0), 40.0, 'trough-band'),      # under the coolant trough band
            (chamfered(ob, half - 8.0, yf0, yf1 - 5.0, 8.0), 40.0, 'draw-rod'),            # under the front draw rods
        ] + feet + [
            (chamfered(go, g['inner'] - 5.0, knee_y0, g['y_bkc'] - 34.0, 10.0), 40.0, 'knee'),   # under the knee, inboard of the pedestal
            (chamfered(ob, half - 8.0, outer_y0, ry - 32.0, 8.0), 65.0, 'outer-a'),        # outboard of the anchor bar,
            (chamfered(ob, half - 8.0, ry + 32.0, 312.0, 8.0), 65.0, 'outer-b'),           # either side of the rods
            (chamfered(go + 15.0, 230.0, 318.0, y1 - 10.0, 10.0), zp, 'rear'),            # behind the feet, outboard of the girder
        ]
        for poly, z, name in side:
            pts = [(sx * x, y) for x, y in poly]
            out.append((pts if sx > 0 else pts[::-1], z, f"{name}-{'R' if sx > 0 else 'L'}"))
    return bevel_clamp(out, g)


def base_envelope(g, front, edges=True):
    """Outside shape of a base half, before any cuts (the mold cavity). edges=False leaves off the
    small edge rounds (the mold fillers only need the big corner radii)."""
    half, base_top, ys = g['base_half'], g['base_top'], g['split']
    ya, yb = (g['base_y0'], ys) if front else (ys, g['base_y1'])
    outer_y = ya if front else yb
    blk = parts.box(-half, half, ya, yb, 0, base_top)
    blk = parts.soften(blk, P['base_corner_r'], lambda e: parts.parallel((0, 0, 1))(e) and on_y(outer_y)(e))
    bi, bh = P['base_bevel']
    if bi > 0:
        # the bevel: a ruled loft from the outline pulled in at the underside up to the full outline
        r, y0, y1 = P['base_corner_r'], g['base_y0'], g['base_y1']
        low = rounded_rect(-half + bi, half - bi, y0 + bi, y1 - bi, r - bi, 0.0)
        high = rounded_rect(-half, half, y0, y1, r, bh)
        keep = Part.makeLoft([low, high], True, True).fuse(Part.Face(high).extrude(Vector(0, 0, base_top - bh + 1)))
        blk = blk.common(keep).removeSplitter()
    if not edges:
        return blk
    blk = fillet_safe(blk, (P['round_r'], P['edge_r'], 3.0), lambda e: on_z(base_top)(e) and not on_y(ys)(e))
    if bi > 0:
        blk = fillet_safe(blk, (P['round_r'], 6.0), lambda e: on_z(bh)(e) and not on_y(ys)(e))
    return fillet_safe(blk, (2.0,), lambda e: on_z(0.0)(e) and not on_y(ys)(e))


def base_top_formers(g, front):
    """Recesses in a base half's top face (named solids): the side gutters, the coolant trough
    (front) and, with a short Y bracket, the table-motor relief (rear). Cut from the casting; printed as mold formers."""
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
    elif not P['bracket_y'] or g['y_bk'] - parts.SUPPORT['BK12']['L'] + parts.HM[P['bracket_y']]['L'] < yb:
        # relief under the table motor, which hangs below the base top: from the bracket's motor end
        c = P['motor_cutout'] / 2
        y_m = g['y_bk'] - parts.SUPPORT['BK12']['L'] + parts.HM[P['bracket_y']]['L'] if P['bracket_y'] else g['y_bk']
        out.append(('motor-relief', parts.box(-c, c, y_m, yb + 1, base_top - 8, base_top + 1)))
    return out


def base_grid(m, g, st, front, cont, tag):
    """The steel grid of a base half, all stock, drilled from the templates and bolted: a 2x3 tube girder
    under each Y rail with a 3/8 x 1-1/2 in rail bar bolted on top (tapped for the riser hold-downs) and a
    3/8 x 3 in end plate at each end; a pedestal under each upright (3/8 x 2-1/2 in seat and bottom bars,
    a 2x2 tube spacer round each tie rod); and 1-1/2 in cross tubes, each clamped by a 1/2-13 rod through
    it and the tubes it joins: girder to girder (at the split, and under the Y ballscrew supports, whose
    3/8 x 2 in pads bolt on top) and girder to pedestal. The draw rods run inside the girders, from end
    plate to end plate, and clamp the halves together. Returns the plates and tubes cut from the casting,
    and the plates cast_anchors taps."""
    base_top, ys = g['base_top'], g['split']
    H = base_top - T38                               # underside of the bars on top
    gw, gh, gt = GIRDER
    gz = g['draw_z']
    tz = g['tie_z']
    sides = ((-1, 'L'), (1, 'R'))
    parts_, tapped = [], []
    gx = g['girder_x']
    if front:
        tube_y = (g['front_web'] + T38, ys - T38)
        bar_y = (g['front_web'], ys - 0.5)
        ends = [('Front', g['front_web']), ('Split', ys - T38)]
    else:
        tube_y = (ys + T38, g['rear_end'])
        bar_y = (ys + 0.5, g['rear_end'] + T38)
        ends = [('Split', ys), ('Back', g['rear_end'])]
    # cross rods (y): girder to girder at the split and under the supports, girder to pedestal beside each
    # pedestal column's tie rod
    tie_ys = ([ys - 34.0, g['y_bf'] + 12.0] if front else [ys + 34.0, g['y_bkc'] - 17.5])
    ped_ys = [y_ - 15.0 for _, y_, _ in g['tie_rods'] if (y_ < ys) == front]
    # through-bolts that hold each rail bar down on its girder: midway between the riser hold-downs, clear of
    # the cross rods
    holds = [P['table_rail_y'] + u for u in riser_holddowns(P['table_rail_len'])]
    marks = sorted([bar_y[0]] + [h_ for h_ in holds if bar_y[0] < h_ < bar_y[1]] + [bar_y[1]])
    bolt_ys = [(a + b) / 2 for a, b in zip(marks, marks[1:]) if b - a > 30
               and all(abs((a + b) / 2 - t_) > 13 for t_ in tie_ys + ped_ys)]
    girders = {}
    for sx, side in sides:
        x0 = sx * gx
        tube = sk.Tube(f'BaseGirder{tag}{side}', 'y', x0, gz, gw, gh, gt, *tube_y)
        rail = sk.flat_bar(f'BaseRailBar{tag}{side}', 'z', H, T38, x0 - 19.05, bar_y[0], x0 + 19.05, bar_y[1])
        for by in bolt_ys:
            for dx in (-12.0, 12.0):
                tube.drill('z', by, x0 + dx, 6.6, '1/4-20 bolt (rail bar)')
                rail.hole(x0 + dx, by, 6.6)
        for hy in (P['table_rail_y'] + u for u in riser_holddowns(P['table_rail_len'])):
            if tube_y[0] < hy < tube_y[1]:
                tube.drill('z', hy, x0, 6.5, 'relief under a riser hold-down', both=False)
        for kind, c0 in ends:
            e = sk.flat_bar(f'BaseGirderEnd{kind}{tag}{side}', 'y', c0, T38, x0 - 38.1, H - 76.2, x0 + 38.1, H - 12.7)
            e.hole(x0, gz, 14.3)
            if kind == 'Split':
                for dx in (-32.0, 32.0):
                    e.hole(x0 + dx, gz, 9.6)                 # dowel pins: glued in the rear plate, into the front one
            parts_.append(e)
        girders[side] = tube
        parts_.append(tube)
        tapped.append(rail)
    # pedestals under the uprights
    peds = {}
    for sx, side in sides:
        ux = sx * g['ux']
        rods = [(sx * x_, y_) for x_, y_, _ in g['tie_rods'] if (y_ < ys) == front]
        sy0, sy1 = (g['up_front'] + 12.5, ys - 12.0) if front else (ys + 12.0, g['up_y1'] - 12.5)
        seat = sk.flat_bar(f'BaseSeat{tag}{side}', 'z', H, T38, ux - 31.75, sy0, ux + 31.75, sy1)
        pbar = sk.flat_bar(f'BasePedestalBar{tag}{side}', 'z', 0.0, T38, ux - 31.75, sy0, ux + 31.75, sy1)
        cols = []
        for k, (x_, y_) in enumerate(rods):
            seat.hole(x_, y_, 14.3)
            pbar.hole(x_, y_, 14.3)
            c = sk.Tube(f'BasePedestalColumn{tag}{side}{k + 1}', 'z', x_, y_, P['frame_tube'][0], P['frame_tube'][0], P['frame_tube'][1],
                        T38, H)
            cols.append((y_, c))
            parts_.append(c)
        if not front:
            for dy in g['dowel_ys']:
                seat.hole(ux, dy, 9.6)
        peds[side] = cols
        parts_ += [seat, pbar]
    # cross tubes, each clamped by a 1/2-13 rod through it and the tubes it butts against
    ties, rods_ = [], []
    def cross(name, y, xa, xb, through):
        c = sk.Tube(name, 'x', y, tz, CROSS, CROSS, 3.175, xa, xb)
        for t_ in through:
            t_.drill('x', y if t_.axis == 'y' else tz, tz if t_.axis == 'y' else y, 14.3, '1/2-13 cross rod')
        ties.append((name, y, through))
        parts_.append(c)
        # the rod: through the cross tube and both tubes it joins, a washer and nut on each outside face
        lo = min(t_.env.BoundBox.XMin for t_ in through)
        hi = max(t_.env.BoundBox.XMax for t_ in through)
        tail = 13.6 + P['rod_tail']
        rod = parts.cyl_u(P['tie_rod_d'] / 2, lo - tail, hi + tail, y, tz)
        nuts = [parts.cyl_u(13.5, lo - 2.5, lo, y, tz).fuse(parts.cyl_u(11.0, lo - 13.6, lo - 2.5, y, tz)),
                parts.cyl_u(13.5, hi, hi + 2.5, y, tz).fuse(parts.cyl_u(11.0, hi + 2.5, hi + 13.6, y, tz))]
        st.add(name.replace('BaseCross', 'CrossRod'), cont, rod.fuse(nuts), 'steel')
        rods_.append(rod.fuse(nuts))
        return c
    inner_x = gx - gw / 2
    cross(f'BaseCrossSplit{tag}', tie_ys[0], -inner_x, inner_x, [girders['L'], girders['R']])
    cross(f'BaseCross{"BF" if front else "BK"}{tag}', tie_ys[1], -inner_x, inner_x, [girders['L'], girders['R']])
    for sx, side in sides:
        for k, ((y_, col), py) in enumerate(zip(peds[side], ped_ys)):
            a, b = sorted((sx * (gx + gw / 2), sx * (g['ux'] - 25.4)))
            cross(f'BaseCrossPed{tag}{side}{k + 1}', py, a, b, [girders[side], col])
    # pads for the Y ballscrew supports, bolted down onto their cross tube
    for nm, y_, _ in ties:
        if nm.startswith(('BaseCrossBF', 'BaseCrossBK')):
            bf = nm.startswith('BaseCrossBF')
            py0, py1 = (g['y_bf'] - 20.4, g['y_bf'] + 30.4) if bf else (g['y_bk'] - 50.8, g['y_bk'])
            if not bf and P['bracket_y']:
                # the HM bracket's six holes, the rear rollers' inner feet and the pad's own bolts, 8 mm in from
                # its edges, on the narrowest stock flat bar that covers them
                ub = g['y_bk'] - parts.SUPPORT['BK12']['L']
                ys_ = [ub + c for c in parts.HM[P['bracket_y']]['C']] + [y_ - 12.0] + \
                      [ub + parts.HM[P['bracket_y']]['L'] - parts.HM[P['bracket_y']]['E']] + \
                      [yy for _, yy in roller_layout()['tapped']]
                need = max(ys_) - min(ys_) + 16.0
                w_ = next(w for w in (50.8, 63.5, 76.2, 88.9, 101.6) if w >= need)
                py0 = (max(ys_) + min(ys_)) / 2 - w_ / 2
                py1 = py0 + w_
                if py1 > g['base_y1'] - 6.0:
                    py0, py1 = g['base_y1'] - 6.0 - w_, g['base_y1'] - 6.0
            pad = sk.flat_bar('BasePadBF' if bf else 'BasePadBK', 'z', H, T38, -45.0, py0, 45.0, py1)
            tube = next(p_ for p_ in parts_ if getattr(p_, 'name', '') == nm)
            by = y_ + (12.0 if bf else -12.0)
            for bx in (-32.0, 32.0):
                pad.hole(bx, by, 6.6)
                tube.drill('z', bx, by, 6.6, '1/4-20 bolt (pad)')
            # reliefs in the tube's top under the support's screws
            sup = parts.SUPPORT['BF12' if bf else 'BK12']
            us = (g['y_bf'] - sup['L'] / 2) if bf else (g['y_bk'] - sup['L'])
            for c_ in sup['C']:
                for vx in (-sup['P'] / 2, sup['P'] / 2):
                    if abs(us + c_ - y_) < CROSS / 2 - 4:
                        tube.drill('z', vx, us + c_, 7.0, 'relief under a support screw', both=False)
            tapped.append(pad)
    m.half_rods = rods_
    for p_ in parts_:
        st.add(p_.name, cont, p_.shape)
        if isinstance(p_, sk.Plate):
            m.plates.append(p_)
        else:
            m.tubes.append(p_)
    return parts_, tapped


def base_half(m, g, st, front):
    """Front or rear half of the base: its steel grid (base_grid) cast into epoxy granite. The halves
    meet at y = split, end plate to end plate, on dowel pins, clamped by the two draw rods."""
    half, base_top, ys = g['base_half'], g['base_top'], g['split']
    ya, yb = (g['base_y0'], ys) if front else (ys, g['base_y1'])
    tag, cont = ('Front', 'FrameBaseFront') if front else ('Rear', 'FrameBaseRear')
    blk = base_envelope(g, front)

    cuts = []
    for poly, z_top, _ in base_pockets(g):
        if (sum(y for _, y in poly) / len(poly) < ys) == front:
            face = Part.Face(Part.makePolygon([Vector(x, y, -1) for x, y in poly + poly[:1]]))
            cuts.append(face.extrude(Vector(0, 0, z_top + 1)))
    plates, tapped = base_grid(m, g, st, front, cont, tag)
    cuts += [pl.env if isinstance(pl, sk.Tube) else pl.slab for pl in plates + tapped]
    cuts += m.half_rods
    m.base_tapped += [(pl, cont) for pl in tapped]
    # draw rods: from a nut pocket in the front face to a nut pocket in the back face, beside the girders
    for sx, side in ((-1, 'L'), (1, 'R')):
        dx, dz = sx * g['draw_rod_x'], g['draw_z']
        if front:
            y0 = ya
            seat = g['front_web']
            cuts += [parts.cyl_v(16.0, y0 - 1, seat, dx, dz), parts.cyl_v(8.0, seat, ys + 1, dx, dz)]
            nut = hex_y(19.05, dx, seat - 13.6, 11.1, dz).fuse(parts.cyl_v(13.5, seat - 2.5, seat, dx, dz))
            st.add(f'DrawRodNut{tag}{side}', cont, nut.cut(parts.cyl_v(P['tie_rod_d'] / 2, seat - 20, seat + 1, dx, dz)), 'steel')
            rod = parts.cyl_v(P['tie_rod_d'] / 2, seat - 13.6 - P['rod_tail'], ys, dx, dz)
            st.add(f'DrawRod{side}', cont, rod, 'steel')
        else:
            seat = g['rear_end'] + T38
            cuts += [parts.cyl_v(8.0, ys - 1, seat, dx, dz), parts.cyl_v(16.0, seat, yb + 1, dx, dz)]
            nut = hex_y(19.05, dx, seat + 2.5, 11.1, dz).fuse(parts.cyl_v(13.5, seat, seat + 2.5, dx, dz))
            st.add(f'DrawRodNut{tag}{side}', cont, nut.cut(parts.cyl_v(P['tie_rod_d'] / 2, seat - 1, seat + 20, dx, dz)), 'steel')
            rod = parts.cyl_v(P['tie_rod_d'] / 2, ys, seat + 13.6 + P['rod_tail'], dx, dz)
            st.add(f'DrawRodRear{side}', cont, rod, 'steel')
        for k, dx in enumerate((-32.0, 32.0)):
            px = sx * g['girder_x'] + dx
            if not front:
                pin = parts.cyl_v(P['dowel_d'] / 2, ys - 12.7, ys + 12.7, px, dz)   # 3/8 x 1 in
                st.add(f'SplitPin{side}{k + 1}', cont, pin, 'steel')
                cuts.append(pin)
            else:
                cuts.append(parts.cyl_v(P['dowel_d'] / 2 + 0.05, ys - 13.2, ys + 0.1, px, dz))

    cuts += [shape for _, shape in base_top_formers(g, front)]
    if front:
        ox, oy = g['outlet']
        # drain: straight down through the front wall to a cast-in brass nipple over the chip basket
        cuts += [Part.makeCylinder(7.0, base_top - 25 + 1, Vector(ox, oy, 0)),
                 parts.hexagon(22.0, -0.5, 12.5, ox, oy)]
        nipple = parts.hexagon(22.0, 0.0, 12.0, ox, oy).fuse(Part.makeCylinder(8.0, 20.0, Vector(ox, oy, -20.0)))
        st.add('DrainOutlet', cont, nipple.cut(Part.makeCylinder(5.5, 34.0, Vector(ox, oy, -21.0))), 'brass')

    # legs cast in near the corners, behind the bevel (hollow, plugged at the top)
    leg_s, leg_w = P['post_tube']
    for i, (lx, ly) in enumerate(g['legs']):
        if ya <= ly < yb:
            name = f"Leg{'Front' if front else 'Rear'}{'L' if lx < 0 else 'R'}"
            z1 = P['leg_embed']
            env, shell = parts.square_tube('z', lx, ly, leg_s, leg_w, z1 - P['leg_len'], z1)
            cuts.append(env)
            st.add(name, cont, shell)
            st.plug(name + 'Plug', cont, 'z', lx, ly, leg_s - 2 * leg_w, z1 - 10, z1, z1)
            # threaded insert for the leveling foot
            insert = parts.square_tube('z', lx, ly, leg_s - 2 * leg_w - 1.2, 0.1, z1 - P['leg_len'], z1 - P['leg_len'] + 22)[0]
            st.add(name + 'Insert', cont, insert.cut(Part.makeCylinder(6.0, 30, Vector(lx, ly, z1 - P['leg_len'] - 5))), 'steel')

    # cast-in M5 inserts for the enclosure's bottom rails and the way-cover rollers
    for i, (bx, by) in enumerate(g['rail_bolts'] + g['cover_inserts'] + g['ychain_inserts']):
        if ya <= by < yb:
            cuts.append(Part.makeCylinder(4.0, 13.0, Vector(bx, by, base_top - 12)))
            st.add(f'Insert{tag}{i + 1}', cont, Part.makeCylinder(4.0, 12.0, Vector(bx, by, base_top - 12)).cut(
                Part.makeCylinder(2.5, 14.0, Vector(bx, by, base_top - 13))), 'brass')

    if not front:
        for sx, side in ((-1, 'L'), (1, 'R')):
            for i, dy in enumerate(g['dowel_ys']):
                dowel = Part.makeCylinder(P['dowel_d'] / 2, 30.0, Vector(sx * g['ux'], dy, base_top - 15))
                cuts.append(dowel)
                st.add(f'DowelBase{side}{i + 1}', cont, dowel, 'steel')

    # the uprights' tie rods: 5/8 in holes right through (cast on greased rods), between the pedestal webs
    for sx in (-1, 1):
        cuts += [Part.makeCylinder(P['up_rod_hole'] / 2, base_top + 2, Vector(sx * rx, ry, -1))
                 for rx, ry, _ in g['tie_rods'] if ya <= ry < yb]

    if not front:
        # Seal on the split face: a U under the floor gutters, rising at both ends to near the top. It is
        # in the rear half, which is cast first against a board; the front half is cast against it.
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
    pieces = [parts.box(-xl - w / 2, xl + w / 2, ys, ys + dpt, zb - w / 2, zb + w / 2)]
    pieces += [parts.box(sx * xl - w / 2, sx * xl + w / 2, ys, ys + dpt, zb - w / 2, zt) for sx in (-1, 1)]
    shape = pieces[0].multiFuse(pieces[1:]).removeSplitter()
    return shape, shape.copy()


def foot_gasket(g, sx):
    """Groove loop in the upright's underside, 8 mm in from its edges."""
    w, dpt = P['gasket_groove']
    x0, x1 = sorted((sx * (g['inner'] + 8.0), sx * (g['outer'] - 8.0)))
    y0, y1 = g['up_front'] + 8.0, g['up_back_foot'] - 8.0
    z = g['base_top']
    ring = parts.box(x0 - w / 2, x1 + w / 2, y0 - w / 2, y1 + w / 2, z, z + dpt).cut(
        parts.box(x0 + w / 2, x1 - w / 2, y0 + w / 2, y1 - w / 2, z - 1, z + dpt + 1))
    return ring, 2 * ((x1 - x0) + (y1 - y0))


def upright_envelope(g, sx, edges=True):
    """Outside shape of an upright, before any cuts (the mold cavity): a raked buttress, the
    foot running forward along the base and the front face sloping up to the beam."""
    inner, outer, base_top, beam_bot = g['inner'], g['outer'], g['base_top'], g['beam_bot']
    x0 = inner if sx > 0 else -outer
    toe = base_top + P['upright_nose']
    prof = [(g['up_front'], base_top), (g['up_front'], toe), (g['up_top_front'], beam_bot), (g['up_y1'], beam_bot),
            (g['up_back_foot'], base_top)]
    up = Part.Face(Part.makePolygon([Vector(x0, y, z) for y, z in prof + prof[:1]])).extrude(Vector(P['upright_t'], 0, 0))
    # the nose rounds into the slope (part of the mold: a printed toe filler)
    up = fillet_safe(up, (P['upright_nose_r'],), lambda e: parts.parallel((1, 0, 0))(e) and on_z(toe)(e))
    if not edges:
        return up
    # outside edges well rounded; the top face (under the beam and the top plate) only lightly
    up = fillet_safe(up, (P['round_r'], 6.0), lambda e: not on_z(base_top)(e) and not on_z(beam_bot)(e)
                     and not (parts.parallel((1, 0, 0))(e) and on_z(toe)(e)))
    return fillet_safe(up, (4.0, 2.0), lambda e: on_z(beam_bot)(e))


def upright(m, g, st, sx):
    """Upright: a steel skeleton of stock parts (flat-bar foot, two tube columns, a top plate of two flat
    bars) cast into epoxy granite. The tie rods run inside the columns and screw into the top plate's
    lower bar, and one from the toe pocket bears on the foot, all right through the base, so the whole
    upright is clamped down through steel; two dowels locate it."""
    tag = 'L' if sx < 0 else 'R'
    cont = f'FrameUpright{tag}'
    inner, outer, base_top, beam_bot = g['inner'], g['outer'], g['base_top'], g['beam_bot']
    up_y0, up_y1 = g['up_y0'], g['up_y1']
    ux, ft = sx * g['ux'], g['foot_top']
    up = upright_envelope(g, sx)
    plate_t, lay = P['top_plate_t'], P['plate_layer']
    plate_bot = beam_bot - plate_t
    rod_r = P['tie_rod_d'] / 2

    # ---- the skeleton, all stock: a 3/8 x 2 in flat-bar foot, two 2x2 tube columns, and a top plate of two
    # 1/2 x 2-1/2 in flat bars (the lower one tapped for the column rods and the beam's studs)
    xa, xb = sorted((sx * (g['ux'] - 31.75), sx * (g['ux'] + 31.75)))
    py0, py1 = g['up_top_front'] + 6, up_y1 - 6
    lower = sk.flat_bar(f'TopPlate{tag}Lower', 'z', plate_bot, lay, xa, py0, xb, py1)
    upper = sk.flat_bar(f'TopPlate{tag}Upper', 'z', plate_bot + lay, lay, xa, py0, xb, py1)
    fa, fb = sorted((sx * (g['ux'] - 25.4), sx * (g['ux'] + 25.4)))   # inside the foot's gasket groove
    foot = sk.flat_bar(f'UprightFoot{tag}', 'z', base_top, T38, fa, g['up_front'] + 12.5, fb, up_y1 - 12.5)
    tl, tw = P['column_len'], P['frame_tube'][1]
    cols = []
    for i, cy in enumerate(g['columns']):
        env, shell = parts.square_tube('z', ux, cy, P['frame_tube'][0], tw, plate_bot - tl, plate_bot)
        cols.append(env)
        st.add(f'UprightColumn{tag}{i + 1}', cont, shell)
        # printed rings center the column on its rod at both ends (cast in)
        inner_s = P['frame_tube'][0] - 2 * tw - 2 * P['tube_fit']
        for k, z0 in enumerate((plate_bot - tl, plate_bot - 12.0)):
            ring = parts.box(ux - inner_s / 2, ux + inner_s / 2, cy - inner_s / 2, cy + inner_s / 2, z0, z0 + 12.0)
            ring = parts.soften(ring, 3.0, parts.parallel((0, 0, 1)), chamfer=True)
            ring = seam_relief(ring.cut(Part.makeCylinder(6.6, 14, Vector(ux, cy, z0 - 1))), 'z', ux, cy, inner_s, z0, z0 + 12)
            st.add(f'ColumnRing{tag}{i + 1}{"ab"[k]}', cont, ring, 'printed')
    for rx, ry, pb in g['tie_rods']:
        foot.hole(sx * rx, ry, 14.3)
        if pb >= g['pocket_bot'] - 1:
            lower.hole(sx * rx, ry, 0, tap='1/2-13')
    for dy in g['dowel_ys']:
        foot.hole(ux, dy, P['up_dowel_hole'])
    for bx in g['bolt_xs']:
        for by in g['bolt_ys']:
            lower.hole(sx * bx, by, 0, tap='3/8-16')
            upper.hole(sx * bx, by, 10.5)
    for pl in (lower, upper):
        pl.hole(ux, g['beam_dowel_y'], P['plate_dowel_hole'])
    for pl in (foot, lower, upper):
        st.add(pl.name, cont, pl.shape)
        m.plates.append(pl)

    # ---- the casting around it
    cuts = [foot.slab, parts.box(xa, xb, py0, py1, plate_bot, beam_bot + 1)] + cols
    cuts += [Part.makeCylinder(P['up_dowel_hole'] / 2, 10.0, Vector(ux, dy, ft - 1)) for dy in g['dowel_ys']]
    cuts += [Part.makeCylinder(rod_r + 1.0, plate_bot - tl - ft + 2, Vector(ux, cy, ft - 1)) for cy in g['columns']]
    pockets = []
    for j, (rx, ry, pb) in enumerate(g['tie_rods']):
        x = sx * rx
        # under the base: washer and nut against the anchor bar
        low = Part.makeCylinder(13.5, 2.5, Vector(x, ry, -2.5)).fuse(parts.hexagon(19.05, -13.6, 11.1, x, ry))
        st.add(f'TieRodNutLow{tag}{j + 1}', cont, low.cut(Part.makeCylinder(rod_r, 20, Vector(x, ry, -15))), 'steel')
        if pb >= g['pocket_bot'] - 1:
            rod_top = beam_bot - lay                     # screwed into the lower bar, flush with its top
            nut = None
        else:
            # toe: washer and nut on the foot plate, in a pocket from the slope; a printed cap closes it
            r = P['slope_pocket_d'] / 2
            pockets.append(Part.makeCylinder(r, beam_bot - pb + 1, Vector(x, ry, pb)))
            nut = Part.makeCylinder(13.5, 2.5, Vector(x, ry, pb)).fuse(parts.hexagon(19.05, pb + 2.5, 11.1, x, ry))
            rod_top = pb + 13.5
            cap = Part.makeCylinder(r - 0.15, beam_bot - pb, Vector(x, ry, pb + 13.7)).common(up)
            m.add(f'PocketCap{tag}{j + 1}', 'frame', cap, 'printed_dark', container=cont)
        if nut is not None:
            st.add(f'TieRodNut{tag}{j + 1}', cont, nut.cut(Part.makeCylinder(rod_r, 1e3, Vector(x, ry, 0))), 'steel')
        tail = 13.6 + P['rod_tail']
        st.add(f'TieRod{tag}{j + 1}', cont, Part.makeCylinder(rod_r, rod_top + tail, Vector(x, ry, -tail)), 'steel')
    ring, ring_len = foot_gasket(g, sx)
    cuts.append(ring)
    st.add(f'GasketUpright{tag}', cont, ring.copy(), 'rubber')
    g['gasket_len'] += ring_len
    shape = up.cut(cuts + pockets).removeSplitter()
    m.add(f'Upright{tag}Casting', 'frame', shape, 'granite', container=cont)
    return shape.Volume


def beam_envelope(g, edges=True):
    """Outside shape of the beam, before any cuts (the mold cavity)."""
    outer, bf, bot, top = g['outer'], g['beam_face'], g['beam_bot'], g['beam_top']
    by1 = bf + P['beam_d']
    shape = parts.box(-outer, outer, bf, by1, bot, top)
    back = lambda e: parts.parallel((1, 0, 0))(e) and on_y(by1)(e)
    shape = fillet_safe(shape, (P['beam_back_r'], 30.0), lambda e: back(e) and on_z(top)(e))
    shape = fillet_safe(shape, (P['beam_back_low_r'],), lambda e: parts.parallel((1, 0, 0))(e) and on_z(bot)(e)
                        and all(v.Point.y > by1 - 1 for v in e.Vertexes))
    # over the uprights the back top corner stays square: the cap plates and the back cap screws sit there
    shape = shape.fuse([parts.box(*sorted((sx * (g['inner'] - 5.0), sx * outer)), by1 - 50.0, by1, top - 50.0, top)
                        for sx in (-1, 1)]).removeSplitter()
    if not edges:
        return shape
    shape = fillet_safe(shape, (P['beam_face_r'],), lambda e: parts.parallel((1, 0, 0))(e) and on_y(bf)(e))
    return fillet_safe(shape, (P['round_r'], 6.0, 3.0), lambda e: all(abs(abs(v.Point.x) - outer) < 1e-6 for v in e.Vertexes))


def stud(mm, exact=False):
    """The nearest stud length sold (1/4 in steps), so every rod is bought at length instead of sawn.
    exact=True gives the length the rod would be cut to (rod_tail past the far nut exactly)."""
    return mm if exact else round(mm / 6.35) * 6.35


def beam_tie_length():
    """The beam ties: from 0.5 mm inside the face bar's front, through the nipple and back bar, about 12 mm past it."""
    return stud(2 * P['beam_bar_t'] + P['beam_spacer'] + 11.5)


def beam(m, g, st):
    """Beam: a steel box of stock flat bar cast into epoxy granite. A 5 in face bar (the rail face,
    tapped for the X risers and ballscrew supports, cast_anchors) and a back bar, held apart by pipe
    nipples on studs screwed into the face bar, both beam_bar_t thick; at each end a 3/8 x 2-1/2 in seat bar under and cap bar
    over them. Eight 3/8-16 studs, screwed into the upright top plates, clamp cap bar, face and back bars
    and seat bar down onto the top plates."""
    outer, inner, bf = g['outer'], g['inner'], g['beam_face']
    bot, top = g['beam_bot'], g['beam_top']
    by1 = bf + P['beam_d']
    cz = (bot + top) / 2
    shape = beam_envelope(g)
    cont = 'FrameBeam'
    xe = 254.0                                                         # 20 in bars
    tb = P['beam_bar_t']
    yb0 = bf + tb + P['beam_spacer']                                   # back bar, behind the spacers
    face = sk.flat_bar('BeamFacePlate', 'y', bf, tb, -xe, bot + T38, xe, top - T38)
    back = sk.flat_bar('BeamBackPlate', 'y', yb0, tb, -xe, bot + T38, xe, top - T38)
    ends = []
    for sx, side in ((-1, 'L'), (1, 'R')):
        xa, xb = sorted((sx * (g['ux'] - 31.75), sx * (g['ux'] + 31.75)))
        ends.append(sk.flat_bar(f'BeamSeat{side}', 'z', bot, T38, xa, bf, xb, bf + 133.35))
        ends.append(sk.flat_bar(f'BeamCap{side}', 'z', top - T38, T38, xa, bf, xb, bf + 133.35))
    for pl in ends:
        for sx in (-1, 1):
            for bx in g['bolt_xs']:
                for by in g['bolt_ys']:
                    if pl.slab.common(Part.makeCylinder(1, 1000, Vector(sx * bx, by, 0))).Volume > 0:
                        pl.hole(sx * bx, by, 13.5)
        if pl.name.startswith('BeamSeat'):
            pl.hole(math.copysign(g['ux'], pl.slab.BoundBox.Center.x), g['beam_dowel_y'], 9.6)
    # ties: studs screwed into the face bar, through pipe nipples and the back bar, nut behind
    cuts, ties = [], (-120.0, 0.0, 120.0)
    for tx in ties:
        face.hole(tx, cz, 0, tap='3/8-16')
        back.hole(tx, cz, 10.5)
        pipe = parts.cyl_v(10.65, bf + tb, yb0, tx, cz).cut(parts.cyl_v(7.9, bf, yb0 + 1, tx, cz))
        st.add(f'BeamSpacer{int(tx)}', cont, pipe)
        cuts.append(parts.cyl_v(10.65, bf + tb, yb0, tx, cz))
        stud = parts.cyl_v(P['beam_bolt_d'] / 2, bf + 0.5, bf + 0.5 + beam_tie_length(), tx, cz)
        nut = hex_y(14.3, tx, yb0 + tb, 8.4, cz).cut(parts.cyl_v(P['beam_bolt_d'] / 2, yb0, yb0 + 20, tx, cz))
        st.add(f'BeamTie{int(tx)}', cont, stud.fuse(nut), 'steel')
        cuts.append(parts.cyl_v(13.0, yb0 + tb, yb0 + tb + 14.0, tx, cz))           # its nut, in the casting
    plates = [back] + ends
    for pl in plates:
        st.add(pl.name, cont, pl.shape)
        m.plates.append(pl)
    m.beam_face_plate = face             # cast_anchors taps it, then adds it
    cuts += [pl.slab for pl in plates + [face]]
    n = 0
    for sx in (-1, 1):
        dowel = Part.makeCylinder(P['dowel_d'] / 2, P['dowel_proud'] + 15.0, Vector(sx * g['ux'], g['beam_dowel_y'],
                                                                                   bot - P['dowel_proud']))
        cuts.append(dowel)
        st.add(f'DowelBeam{"L" if sx < 0 else "R"}', cont, dowel, 'steel')
        for bx in g['bolt_xs']:
            for by in g['bolt_ys']:
                x = sx * bx
                n += 1
                cuts.append(Part.makeCylinder(P['beam_bolt_hole'] / 2, top - bot + 2, Vector(x, by, bot - 1)))
                z0 = bot - P['top_plate_t']                              # bottom of the top plate's lower bar
                stud = Part.makeCylinder(P['beam_bolt_d'] / 2, P['beam_stud'], Vector(x, by, z0))
                zw = top + (P['drip_shield_t'] if by == g['bolt_ys'][0] else 0.0)   # the front row clamps the shield
                washer = Part.makeCylinder(10.0, 2.0, Vector(x, by, zw))
                nut = parts.hexagon(14.3, zw + 2, 8.4, x, by)
                st.add(f'BeamBolt{n}', cont, stud.fuse([washer, nut]), 'black')
    # cast-in M5 inserts in the top for the cable chain's fixed mount
    for i, (ix, iy) in enumerate(g['chain_inserts'], 1):
        cuts.append(Part.makeCylinder(4.0, 13.0, Vector(ix, iy, top - 12)))
        st.add(f'InsertBeam{i}', cont, Part.makeCylinder(4.0, 12.0, Vector(ix, iy, top - 12)).cut(
            Part.makeCylinder(2.5, 14.0, Vector(ix, iy, top - 13))), 'brass')
    shape = shape.cut(cuts).removeSplitter()
    m.add('BeamCasting', 'frame', shape, 'granite', container=cont)
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
    inch = lambda mm: f'{sk.inch(mm)} in'
    ys, y0 = g['split'], d['base_y0']
    d['steel_bom'] = [
        ('frame', f"Steel square tube 2 x 2 x {sk.inch(P['frame_tube'][1])} in, bought at length",
         f"4 x {inch(P['column_len'])} (upright columns; the base's short ones are in the cut list)", 'buy'),
        ('frame', 'Steel square tube 1-1/2 x 1-1/2 x 1/8 in (or 0.120 wall), bought at length',
         f"4 x {inch(P['leg_len'])} (legs)", 'buy'),
        ('frame', 'Printed PETG: 8 column rings, 4 leg plugs, 2 gray pocket caps', '~60 g', 'PRINT'),
        ('frame', '1/2-13 grade B7 fully threaded studs, bought at length (nothing sawn)',
         ', '.join(f"{2 * n_} x {inch(L)}" for L, n_ in sorted(collections.Counter(tie_rod_lengths(g)).items(),
                                                              reverse=True))
         + f" (uprights), 2 x {inch(draw_rod_length(g))} (base draw rods), 4 x {inch(cross_rod_lengths(g)[0])} + "
           f"6 x {inch(cross_rod_lengths(g)[1])} (base cross rods)", 'buy'),
        ('frame', '1/2-13 nut + 1/2 in SAE washer', '32 of each', 'buy'),
        ('frame', '3/8-16 grade B7 fully threaded studs, bought at length: beam studs (into the upright top plates) and '
                  'beam ties, + 3/8-16 nuts and washers', f"8 x {inch(P['beam_stud'])} + 3 x {inch(beam_tie_length())}; 11 nuts",
         'buy'),
        ('frame', f"1/2 in x {inch(P['beam_spacer'])} black pipe nipple (beam spacers)", '3 pcs', 'buy'),
        ('frame', '1/4-20 hex bolt + nut + washers: rail bars onto the girders (4 in), pads onto their cross tubes '
                  '(2-1/4 in)', 'about 20 x 4 in + 4 x 2-1/4 in', 'buy'),
        ('frame', 'Dowel pin 3/8 x 1-1/4 in (4 base dowels, 2 beam) and 3/8 x 1 in (4 at the base split)', '6 + 4 pcs', 'buy'),
        ('frame', f"Nitrile O-ring cord {P['gasket_cord']:.0f} mm (base split + upright feet), glue the ends",
         f"{d['gasket_m'] + 0.3:.1f} m", 'buy'),
        ('frame', '1/2 in brass hex nipple, cast-in coolant drain', '1 pc', 'buy'),
    ]


def cross_rod_lengths(g, exact=False):
    """The base cross rods: girder to girder, and girder to pedestal column, a nut, washer and rod_tail past
    each outside face."""
    tail = 2 * (13.6 + P['rod_tail'])
    gw = GIRDER[0]
    return (stud(2 * (g['girder_x'] + gw / 2) + tail, exact), stud((g['ux'] + 25.4) - (g['girder_x'] - gw / 2) + tail, exact))


def draw_rod_length(g, exact=False):
    """The base draw rods: from the front cross plate to the girders' rear end plates, a nut, a washer
    and a rod_tail past each."""
    return stud(g['rear_end'] + T38 - g['front_web'] + 2 * (13.6 + P['rod_tail']), exact)


def tie_rod_lengths(g, exact=False):
    """Each upright's tie rods, stud length: from rod_tail under the bottom nut (washer, nut) to flush with
    the top plate (top two) or with the top of the slope nut."""
    return [stud((g['beam_bot'] - P['plate_layer'] if pb >= g['pocket_bot'] - 1 else pb + 13.5) + 13.6 + P['rod_tail'], exact)
            for _, _, pb in g['tie_rods']]


def free_end_room(cast, axis, c1, c2, size, end, sgn, cover=2.0, most=30.0):
    """How far a cast-in tube could run past its free end (at `end`, growing toward sgn) and stay in
    solid casting: a slab of its section plus `cover` all round, grown until it leaves the casting."""
    def slab(t):
        a0, a1 = sorted((end, end + sgn * t))
        h = size / 2 + cover
        lo1, hi1, lo2, hi2 = c1 - h, c1 + h, c2 - h, c2 + h
        if axis == 'y':
            return parts.box(lo1, hi1, a0, a1, lo2, hi2)
        return parts.box(lo1, hi1, lo2, hi2, a0, a1)
    crop = cast.common(slab(most))
    inside = lambda t: slab(t).cut(crop).Volume < 0.5
    if inside(most):
        return most
    lo, hi = 0.0, most
    while hi - lo > 0.25:
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if inside(mid) else (lo, mid)
    return lo


def steel_tolerance(m, d):
    """Where each cast-in piece's length error goes, and whether there's room for tube_cut_tol."""
    g = frame_layout(d)
    cast = {p['name']: p['shape'] for p in m.parts if p['name'].endswith('Casting')}
    tol, ys = P['tube_cut_tol'], g['split']
    tube_s, post_s = P['frame_tube'][0], P['post_tube'][0]
    s2 = P['table_rail_spacing'] / 2
    rows = []
    rooms = [free_end_room(cast['BaseFrontCasting' if ly < ys else 'BaseRearCasting'], 'z', lx, ly, post_s, P['leg_embed'], 1)
             for lx, ly in g['legs']]
    rows.append(('Legs (4)', 'set proud of the leg holder', 'top end, in the casting', min(rooms)))
    # upright columns: clamped up against the top plate; the bottom end sits in an epoxy bed on the foot plate
    rows.append(('Upright columns (4)', 'top end, against the top plate', 'an epoxy bed on the foot bar',
                 g['pocket_bot'] - P['column_len'] - g['foot_top']))
    # the studs are bought in 1/4 in steps: the step shortens or lengthens the tail past the far nut, and the
    # stud's own length error (stud_tol) has to fit in the shortest tail
    def tail(n, x):
        return P['rod_tail'] + min(a - b for a, b in zip(n, x))
    rows.append(('Draw rods (2, studs)', 'flush with the front nut', 'the tail behind the back nut',
                 tail([draw_rod_length(g)], [draw_rod_length(g, True)]), P['stud_tol']))
    rows.append(('Girders (4)', 'the split end plate', 'the far end plate, clamped by the draw rod', 6.0))
    rows.append(('Top plates (2)', 'bolted to the mold bridge', 'all edges, 6 mm inside the casting', 6.0))
    rows.append(('Tie and cross rods (studs)', 'screwed up to a stop, or flush with one nut', 'the tail past the far nut',
                 tail(tie_rod_lengths(g) + list(cross_rod_lengths(g)), tie_rod_lengths(g, True) + list(cross_rod_lengths(g, True))),
                 P['stud_tol']))
    d['steel_tol'] = [(r[0], r[1], r[2], r[3], r[3] >= (r[4] if len(r) > 4 else tol)) for r in rows]
    for n, _, _, room, ok in d['steel_tol']:
        if not ok:
            m.warnings.append(f'{n}: only {room:.1f} mm for its length error')


def cast_anchors(m, d):
    """Threads for the rails and ballscrew supports recorded by rail_pair / screw_axis, tapped into the
    steel: the beam's face plate, and the base's rail bars and support pads. Behind each the casting is
    relieved where the greased mold screw stood, so the screws that go in later have room."""
    parts_by_name = {p['name']: p for p in m.parts}
    holes, count = {}, {}
    face = m.beam_face_plate
    for pt, n, kind in m.anchors:
        thread, od, ln = P[kind]
        if abs(n.z) < 0.5:
            face.hole(pt.x, pt.z, 0, tap='M5' if kind == 'insert_m5' else 'M6')
            holes.setdefault('BeamCasting', []).append(
                Part.makeCylinder(thread / 2 + 0.5, 12.0, Vector(pt.x, d['beam_face'] + P['beam_bar_t'] - 0.5, pt.z), Vector(0, 1, 0)))
            count['face_' + kind] = count.get('face_' + kind, 0) + 1
            continue
        cast = 'BaseFrontCasting' if pt.y < P['base_split_y'] else 'BaseRearCasting'
        probe = Part.Vertex(pt - n * (T38 / 2))
        pl = next((pl for pl, _ in m.base_tapped if pl.slab.distToShape(probe)[0] < 1e-6), None)
        if pl is None:
            raise ValueError(f'no steel under the {kind} at {pt}')
        pl.hole(pt.x, pt.y, 0, tap='M5' if kind == 'insert_m5' else 'M6')
        holes.setdefault(cast, []).append(Part.makeCylinder(thread / 2 + 0.5, 12.0, pt - n * (T38 + 11.5), n))
        count['base_' + kind] = count.get('base_' + kind, 0) + 1
    for pl, cont in [(face, 'FrameBeam')] + m.base_tapped:
        m.add(pl.name, 'frame', pl.shape, 'steeltube', container=cont)
        m.structure.add(pl.name)
        m.plates.append(pl)
        d['steel_kg'] += pl.mass
    by_stock = {}
    for pt, qty, stock, ln, _ in steel_parts(m):
        by_stock.setdefault(stock, []).append((ln, qty))
    for stock, items in sorted(by_stock.items(), reverse=True):
        merged = collections.Counter()
        for ln, q in items:
            merged[round(ln)] += q
        d['steel_bom'].insert(0, ('frame', f'{stock}, cut to length (docs/1-sourcing/steel/)',
                                  ', '.join(f'{q} x {ln}' for ln, q in sorted(merged.items(), reverse=True)), 'buy'))
    for cast, hs in holes.items():
        p = parts_by_name[cast]
        p['shape'] = p['shape'].cut(hs)
        p['proxy'] = [p['shape']]
    d['anchor_count'] = count


MOLD_GROUPS = {'base-rear': 'MoldBaseRear', 'base-front': 'MoldBaseFront', 'upright': 'MoldUpright',
                'beam': 'MoldBeam'}
CASTING_FOLDERS = {'FrameBaseFront': 'base-front', 'FrameBaseRear': 'base-rear', 'FrameUprightL': 'upright',
                   'FrameBeam': 'beam'}


def mold_parts(m, d):
    """The mold kit (moldbox.py): melamine boards with their hole maps, the printed brackets and
    pieces that bolt to them, and the printed cast-in parts. m.molds: printed rows for print/;
    m.mold_kit: the kit (boards, hardware) for the mold guide."""
    molds.BOARD = P['mold_board']
    molds.BOARD_MAX = P['mold_board'] + 0.6
    g = frame_layout(d)
    kit = moldbox.Kit()
    mold_base(kit, m, g)
    mold_upright(kit, g)
    mold_beam(kit, m, g)
    # the pour line on every wall: where the casting's open face meets the board
    for mold, up, level in (('base', Vector(0, 0, -1), 0.0), ('upright', Vector(0, 0, 1), g['beam_bot']),
                            ('beam', Vector(0, 1, 0), g['beam_face'] + P['beam_d'])):
        for b in kit.boards:
            vu = b.V.dot(up)
            if b.mold == mold and abs(vu) > 0.3 and abs(b.U.dot(up)) < 1e-6:
                v = (level - b.o.dot(up)) / vu
                vs = [v_ for _, v_ in b.outline]
                b.pour_v = v if min(vs) + 1 < v < max(vs) - 1 else None
    mold_tools(kit)
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
            seen[key]['qty'] += qty
            continue
        name = ''.join('-' + c.lower() if c.isupper() and i else c.lower() for i, c in enumerate(p['name'])).replace('--', '-')
        up = None
        if name.startswith('pocket-cap'):
            # its face (flush with the sloped front) on the bed
            sl = Vector(0, g['up_top_front'] - g['up_front'], g['beam_bot'] - g['base_top'] - P['upright_nose'])
            sl.normalize()
            up = Vector(0, sl.z, -sl.y)
        seen[key] = kit.add(folder, name, 'cast-in' if cast_in else 'part', p['shape'], qty,
                            'Cast in, stays.' if cast_in else '', up=up, placed=[])
    for mold, f in kit.loose:
        print(f'mold kit: {f.what} at {f.p} ({mold}) lands on no board')
    m.molds, m.mold_kit = kit.rows, kit


def fixed_piece(kit, folder, mold, name, kind, shape, contacts, qty=1, note='', up=None, show=None, mult=1,
                sizes=('M4', 'M3', 'pin'), lim=None, avoid=()):
    """A printed mold piece cut to the bed (peg and socket on each cut), each part fixed to the
    boards it sits against. contacts: [(point on the board face, n out of the piece, fixings per part)]."""
    parts_out, fixes = [], []
    for p in molds.keyed(molds.split(shape, lim or molds.BED)):
        for c0, n, k in contacts:
            if k == 'auto':
                k = 2 if max(p.BoundBox.XLength, p.BoundBox.YLength, p.BoundBox.ZLength) > 110 else 1
            p, fx = molds.fasten(p, c0, n, k, sizes, what=name, avoid=avoid)
            fixes += fx
        parts_out.append(p)
    if up is None:
        # flat face against the board on the bed; pins (if any) point up, so then the other way round
        n0 = contacts[0][1]
        up = n0 if any(f.kind == 'pin' for f in fixes) else -n0
    row = kit.add(folder, name, kind, parts_out, qty, note, up, show=show)
    kit.fix(fixes, mold, mult)
    return row


def mold_base(kit, m, g):
    """Both base halves in one box on one floor board: the rear half first, against a partition at
    the split; then the partition comes out and the front half is cast against the rear half's
    waxed split face, on the same floor. So the two top faces come out flush, the split faces match,
    and the front girders' end plates go straight onto the rear ones' dowel pins. Each half's steel grid
    goes in as one piece: its rail bars and pads screwed to the floor, its seats on the dowels.

    The base is cast top face down: the floor board is at z = base_top and 'up' in the mold is -z."""
    T, fb = P['mold_board'], P['mold_freeboard']
    half, top, y0, y1, ys = g['base_half'], g['base_top'], g['base_y0'], g['base_y1'], g['split']
    up, Z = Vector(0, 0, -1), Vector(0, 0, 1)
    X, Y = Vector(1, 0, 0), Vector(0, 1, 0)
    wt = -fb                                  # wall tops (z)
    both, REAR, FRONT = ['base-rear', 'base-front'], ['base-rear'], ['base-front']
    M = 'base'
    B = moldbox.box_board
    xo = half + T                             # outer faces of the side walls
    kit.board(B('Base floor', M, (-xo - 40, y0 - T - 40, top), (xo + 40, y1 + T + 40, top + T), Z, Y,
                note='both halves are cast on it', show=both))
    kit.board(B('Base front wall', M, (-xo, y0 - T, wt), (xo, y0, top), -Y, up, show=both))
    kit.board(B('Base rear wall', M, (-xo, y1, wt), (xo, y1 + T, top), Y, up, show=both))
    for sx, tag in ((-1, 'left'), (1, 'right')):
        kit.board(B(f'Base side wall, {tag}', M, (sx * half, y0, wt), (sx * xo, y1, top), sx * X, up, show=both))
    kit.board(B('Base partition', M, (-half, ys - T, wt), (half, ys, top), -Y, up,
                note='rear half only; comes out before the front half', show=REAR))
    for sx in (-1, 1):
        kit.board(B('Base partition strut', M, (sx * 150 - T / 2, y0, top - 60), (sx * 150 + T / 2, ys - T, top), X, up,
                    note='offcut, stands on edge; holds the partition foot (rear half only)', show=REAR))

    # corner brackets at the four outside corners, floor brackets along every wall foot
    for sx in (-1, 1):
        for yw, sy in ((y0 - T, -1), (y1 + T, 1)):
            c = Vector(sx * xo, yw, wt)
            kit.add_many('base-box', 'corner-bracket', 'kit', [moldbox.angle_bracket(
                c, -sx * X, sy * Y, -sy * Y, sx * X, up, fb - 2)], mold=M, show=both, merge=True, up=up)
    cleat(kit, M, 'Base cleat, front', Vector(-xo, y0 - T, top), Vector(xo, y0 - T, top), -Y, up, both)
    cleat(kit, M, 'Base cleat, rear', Vector(-xo, y1 + T, top), Vector(xo, y1 + T, top), Y, up, both)
    for sx, tag in ((-1, 'left'), (1, 'right')):
        cleat(kit, M, f'Base cleat, {tag}', Vector(sx * xo, y0, top), Vector(sx * xo, y1, top), sx * X, up, both)
    # partition: brackets to the side walls on its front face, above the pour line
    kit.add_many('base-box', 'partition-bracket', 'kit',
                 [moldbox.angle_bracket(Vector(sx * half, ys - T, wt), -sx * X, -Y, -Y, -sx * X, up, fb - 2, hole_at=20)
                  for sx in (-1, 1)], mold=M, show=REAR, up=up)

    # bridges: boards on edge across the box, in saddles on the side walls; the cores bolt to their sides
    bh, bz = 60.0, wt - TH_SADDLE
    lines = BASE_BRIDGES
    legs_y = {'base-front': g['legs'][0][1], 'base-rear': g['legs'][2][1]}
    for folder, ys_ in lines.items():
        for yb in ys_:
            xb = xo + moldbox.SLOT + TH_SADDLE
            kit.board(B(f'Base bridge y={yb:.0f}', M, (-xb, yb - T / 2, bz - bh), (xb, yb + T / 2, bz), -Y, up,
                        view='outside', show=[folder]))
            sad = []
            for sx in (-1, 1):
                s, wf, bf = moldbox.saddle(Vector(sx * half, yb, wt), sx * X, up, Y)
                sad.append((s, wf + [bf]))
            kit.add_many('base-box', 'saddle', 'kit', sad, mold=M, show=[folder], merge=True, reuse=True, up=X,
                         note='The rear half needs six; four move over for the front half.')
    next(r for r in kit.rows if r['folder'] == 'base-box' and r['name'] == 'saddle')['qty'] = \
        2 * max(len(v) for v in lines.values())
    # legs: a holder in each corner above the pour line, with a pinch screw that holds the leg at its
    # cast-in depth; a short bridge between each pair of holders
    lx_in = half - leg_reach()
    for folder, ly in legs_y.items():
        sy = -1 if ly < 0 else 1
        yw = y0 if sy < 0 else y1
        kit.board(B(f'Base leg bridge y={ly:.0f}', M, (-lx_in - 12, ly - T / 2, bz - bh), (lx_in + 12, ly + T / 2, bz),
                    -Y, up, view='outside', show=[folder]))
        holders = []
        for sx in (-1, 1):
            lx = sx * (half - P['leg_inset'][0])
            holders.append(leg_holder(Vector(lx, ly, 0), sx, sy, half, yw, fb, lx_in))
        kit.add_many('base-box', 'leg-holder', 'kit', holders, mold=M, show=[folder], merge=True, up=up,
                     note=f"Set the leg {P['leg_len'] - P['leg_embed'] - fb:.0f} mm proud of the holder and tighten "
                          'the pinch screw (M4 x 20).')
    kit.count('M4 x 20 bolt (leg pinch screw)', 4, M)
    kit.count('M4 nut', 4, M)
    # anchor bars: each hangs flush with the pour line from its bridges, on printed posts with an M5 screw
    # down through each into a tapped hole in the bar

    # pieces on the floor and walls
    floor = (Vector(0, 0, top), Z)
    for front, folder in ((False, 'base-rear'), (True, 'base-front')):
        yo = y0 if front else y1
        formers = dict(base_top_formers(g, front))
        cav = parts.box(-half, half, *((y0, ys) if front else (ys, y1)), 0, top)
        for name, shape in formers.items():
            shape = shape.common(cav)
            if name.startswith('gutter') and 'trough' in formers:
                shape = shape.cut(formers['trough'])
            if P['foam_formers'] and name != 'motor-relief':
                kit.add(folder, name, 'foam', shape, 1, foam_note(name, shape), show=[folder])
                continue
            if name == 'trough':
                ox, oy = g['outlet']
                shape = shape.fuse(Part.makeCylinder(5.0 - FIT_PLUG, 9.0, Vector(ox, oy, top - 25 - 8), Z))   # drain liner spigot
            fixed_piece(kit, folder, M, name, 'former', shape, [(*floor, 'auto')], lim=120.0 if name == 'trough' else molds.BED,
                        note='Bolts to the floor from underneath (the base is cast top face down).', show=[folder])
        # The rounded corners, and the bevel along the lower edge: one ring, cut into corners and straight
        # strips. The strips sit at the pour line against the walls, so their bolts are covered.
        fill = Part.makeCompound(molds.fillers(base_envelope(g, front, edges=False)))
        c = P['base_corner_r'] + 5.0
        sy = -1 if front else 1
        yc = yo - sy * c
        end_wall, big = (Vector(0, yo, 0), Y * sy, 1), 2000.0
        for sx in (-1, 1):
            side_wall = (Vector(sx * half, 0, 0), sx * X, 1)
            corner = fill.common(parts.box(*sorted((sx * (half - c), sx * big)), *sorted((yc, yo + sy * big)), -big, big))
            if corner.Volume > 1:
                fixed_piece(kit, folder, M, f'corner-{"R" if sx > 0 else "L"}', 'filler', corner,
                            [(*floor, 1), end_wall, side_wall], note='Rounded corner; bolts to the floor and both walls.',
                            show=[folder])
            strip = fill.common(parts.box(*sorted((sx * (half - c), sx * big)), *sorted((yc, ys)), -big, big))
            if strip.Volume > 1:
                fixed_piece(kit, folder, M, f'bevel-{"R" if sx > 0 else "L"}', 'filler', strip, [side_wall],
                            note='The bevel along the lower edge: at the pour line, bolted to the side wall. ' + BEVEL_WOOD,
                            show=[folder])
        strip = fill.common(parts.box(-half + c, half - c, *sorted((yc, yo + sy * big)), -big, big))
        if strip.Volume > 1:
            fixed_piece(kit, folder, M, 'bevel-end', 'filler', strip, [end_wall],
                        note=f"The bevel along the lower edge: at the pour line, bolted to the {'front' if front else 'rear'} wall. "
                             + BEVEL_WOOD,
                        show=[folder])
    groove = split_gasket(g)[0]
    fixed_piece(kit, 'base-rear', M, 'split-gasket-groove', 'former', groove, [(Vector(0, ys, 0), -Y, 2)],
                note='Pins into the partition.', up=-Y, show=REAR, sizes=('pin',))

    # cores: each hangs from a bridge by a post beside it. Where two pockets overlap, the shallower
    # core stops at the deeper one's wall.
    pockets = base_pockets(g)
    for k, (poly, z_top, name) in enumerate(pockets):
        face = Part.Face(Part.makePolygon([Vector(x, y, 0) for x, y in poly + poly[:1]]))
        for poly2, z2, _ in pockets:
            if z2 > z_top:
                face = face.cut(Part.Face(Part.makePolygon([Vector(x, y, 0) for x, y in poly2 + poly2[:1]])))
        face = max(face.Faces, key=lambda f_: f_.Area)
        poly = [(v.Point.x, v.Point.y) for v in face.OuterWire.OrderedVertexes]
        pockets[k] = (poly, z_top, name)
    for poly, z_top, name in pockets:
        front = sum(y for _, y in poly) / len(poly) < ys
        folder = 'base-front' if front else 'base-rear'
        cands = list(lines[folder]) + [legs_y[folder]]
        xs, ycs = [x for x, _ in poly], [y for _, y in poly]
        cx = (min(xs) + max(xs)) / 2
        post = None
        for yb in sorted(cands, key=lambda b: abs(b - (min(ycs) + max(ycs)) / 2)):
            if yb == legs_y[folder] and abs(cx) > lx_in - 8:
                continue
            for side in (-1, 1):
                py = yb + side * (T / 2 + molds.POST / 2)
                if min(ycs) + molds.POST / 2 + 2.0 <= py <= max(ycs) - molds.POST / 2 - 2.0:   # post inside the wall
                    post = (cx, py, (0, -side), bz - 12.0, bz - 20.0)
                    break
            if post:
                break
        if not post:
            print(f'mold kit: no bridge over core {name}')
        if P['foam']:
            # foam block cut to the pocket; only its post is printed, pushed 30 mm into the foam
            p, fx = molds.core_post(*post, min(30.0, z_top - 10.0))
            kit.add(folder, f'{name}-post', 'core', p, 1, 'Post for a foam core: push it 30 mm into a snug hole in '
                    'the foam and glue it.', show=[folder])
            block = molds.prism(poly, 0.0, z_top).cut(p)
            kit.add(folder, name, 'foam', block, 1, foam_note(name, block, poly), show=[folder])
        else:
            shells, fx = molds.core(poly, z_top, [post] if post else [])
            for what, n in (('M3 x 10 bolt', 2), ('M3 nut', 2), ('M3 washer', 4)):
                kit.count(what, n * (len(shells) - 1), M)
            kit.add(folder, name, 'core', shells, 1, 'Shell core, stays in. Bolts to the bridge by its post.', show=[folder])
        kit.fix(fx, M)

    # draw rods: printed plugs on the front and back walls form the nut pockets down to the girders' end plates
    # (the rods run inside the girder tubes, so nothing else forms their holes)
    for front, folder, yw, seat, n_ in ((True, 'base-front', y0, g['front_web'], -Y), (False, 'base-rear', y1,
                                                                                     g['rear_end'] + T38, Y)):
        for sx in (-1, 1):
            dx, dz = sx * g['draw_rod_x'], g['draw_z']
            a, b = sorted((yw, seat))
            plug = parts.cyl_v(16.0 - FIT_PLUG, a, b, dx, dz)
            fixed_piece(kit, folder, M, f'draw-pocket-{"R" if sx > 0 else "L"}', 'plug', plug,
                        [(Vector(0, yw, 0), n_, 1)], up=n_ * -1,
                        note='Forms a draw-rod nut pocket down to the girder\'s end plate; bolts to the wall.',
                        show=[folder])

    # everything else through the boards: insert screws, bolts into the cast-in nuts, dowels
    holes = []
    for pt, n, kind in m.anchors:
        if abs(n.z) > 0.5:
            holes.append(Fix('hole', pt, Z, 5.5 if kind == 'insert_m5' else 6.5,
                             'M5 screw into the steel' if kind == 'insert_m5' else 'M6 screw into a pad'))
    for bx, by in g['rail_bolts'] + g['cover_inserts'] + g['ychain_inserts']:
        holes.append(Fix('hole', Vector(bx, by, top), Z, 5.5, 'M5 insert screw'))
    for sx in (-1, 1):
        holes += [Fix('hole', Vector(sx * g['ux'], dy, top), Z, 9.6, '3/8 dowel') for dy in g['dowel_ys']]
        holes += [Fix('hole', Vector(sx * g['girder_x'] + dx, ys, g['draw_z']), -Y, 9.6, '3/8 dowel pin (split)')
                  for dx in (-32.0, 32.0)]
    kit.fix(holes, M)
    kit.count('M5 x 30 screw, greased (holds a rail bar or the BK pad)',
              sum(1 for f in holes if f.what == 'M5 screw into the steel'), M)
    kit.count('M6 x 30 screw, greased (holds a support pad)', sum(1 for f in holes if f.what == 'M6 screw into a pad'), M)
    kit.count('M5 x 20 screw, greased (holds an insert)', sum(1 for f in holes if f.what == 'M5 insert screw'), M)



TH_SADDLE = 6.0
FIT_PLUG = 0.15
CLEAT = 38.1       # 1x2 strips along each wall's foot, flat on the floor, bolted down through it (any 1x2 lumber)


def cleat(kit, M, name, p0, p1, n_out, up, show, qty=1, mult=1):
    """A strip of board lying on the floor against a wall's outer face, from p0 to p1 (on that face, at
    the floor), bolted down through the floor: the wall's foot can't move out."""
    T = P['mold_board']
    a = p1 - p0
    length = a.Length
    a.normalize()
    cs = [p0, p1, p0 + n_out * CLEAT + up * T, p1 + n_out * CLEAT + up * T]
    lo = tuple(min(c[i] for c in cs) for i in range(3))
    hi = tuple(max(c[i] for c in cs) for i in range(3))
    kit.board(moldbox.box_board(name, M, lo, hi, up, n_out, qty=qty, note='flat on the floor', show=show,
                                 view='outside', stock='1x2'))
    n = max(1, math.ceil((length - 80.0) / 250.0) + 1) if length > 120 else 1
    at = [length / 2] if n == 1 else [40.0 + (length - 80.0) * k / (n - 1) for k in range(n)]
    kit.fix([Fix('bolt', p0 + a * t + n_out * (CLEAT / 2), -up, 4.5, 'cleat', 'M4',
                 molds.bolt_length(2 * molds.BOARD_MAX + 1.0 + HW['M4']['t'] + 1.0)) for t in at], M, mult)


def foam_note(name, shape, poly=None):
    """How to cut a foam piece: its size, and the profile where it isn't a plain block."""
    bb = shape.BoundBox
    size = f'{bb.XLength:.0f} x {bb.YLength:.0f} x {bb.ZLength:.0f} mm'

    def depth(ax, at):
        lo = [bb.XMin - 1, bb.YMin - 1, bb.ZMin - 1]
        ln = [bb.XLength + 2, bb.YLength + 2, bb.ZLength + 2]
        lo[ax], ln[ax] = at - 0.25, 0.5
        return shape.common(Part.makeBox(*ln, Vector(*lo))).BoundBox.ZLength
    if name.startswith('gutter'):
        return (f'XPS strip {size}: a wedge, {depth(1, bb.YMin + 0.5):.0f} mm deep at the front end tapering to '
                f'{depth(1, bb.YMax - 0.5):.0f} mm at the back.')
    if name == 'trough':
        return (f'XPS {size}: {depth(0, bb.XMin + 0.5):.0f} mm deep at the left end, {depth(0, 0.0):.0f} mm at the drain '
                f'(center), {depth(0, bb.XMax - 0.5):.0f} mm at the right, straight between. Push the drain liner into it.')
    if name.startswith('back-edge'):
        return f'XPS {size}: a 40 mm quarter-round hollow, cut with a hot wire or sanded on a 80 mm tube; taped.'
    return f'XPS block {size}, outline as the pocket (chamfered corners); taped, with its printed post glued in.'


def leg_reach():
    """How far a leg holder runs in from the mold walls: past the leg, with room for the pinch screw."""
    return max(P['leg_inset']) + 37.0


def leg_holder(c, sx, sy, half, yw, fb, x_in):
    """Holds a leg in a base corner, above the pour line: bolted through the side wall and the end
    wall; a square hole for the leg (which hangs from its sleeve) and a cradle for the leg bridge.
    c: the leg's center at the pour line."""
    T = P['mold_board']
    xw = sx * half
    z0, z1 = -fb, -fb + 12.0                    # a 12 mm plate at the top of the freeboard band
    xa, xb = sorted((xw, sx * x_in))
    ya, yb = sorted((yw, yw - sy * leg_reach()))
    s = parts.box(xa, xb, ya, yb, z0, z1)
    q = P['post_tube'][0] + 2 * P['tube_fit']
    s = s.cut(parts.box(c.x - q / 2, c.x + q / 2, c.y - q / 2, c.y + q / 2, z0 - 1, z1 + 1))
    # lighten: in (u, v) from the leg's center, positive toward the side wall and the end wall, keep a
    # 7 mm ring round the leg, the plate out to both walls, the cradle arm and the pinch-screw boss
    def uv_box(u0, u1, v0, v1):
        return parts.box(*sorted((c.x + sx * u0, c.x + sx * u1)), *sorted((c.y + sy * v0, c.y + sy * v1)), z0 - 1, z1 + 1)
    ring = q / 2 + 7.0
    band = T / 2 + moldbox.SLOT / 2 + TH_SADDLE + 1.0
    inner = abs(c.x) - x_in + 1.0                   # out to the holder's inner edges (and past them)
    s = s.cut([uv_box(-inner, -ring, -inner, -band), uv_box(-inner, -ring, band, ring),
               uv_box(-ring, -8.0, -inner, -ring), uv_box(8.0, inner, -inner, -ring)])
    # cradle: a pad under the leg bridge's end and two cheeks
    ca, cb = sorted((sx * x_in, sx * (x_in + 12.0)))
    slot = T + moldbox.SLOT
    s = s.fuse(parts.box(ca, cb, c.y - slot / 2 - TH_SADDLE, c.y + slot / 2 + TH_SADDLE, z0 - TH_SADDLE, z0))
    for e in (-1, 1):
        y_in = c.y + e * slot / 2
        s = s.fuse(parts.box(ca, cb, *sorted((y_in, y_in + e * TH_SADDLE)), z0 - TH_SADDLE - 22.0, z0 - TH_SADDLE))
    fixes = []
    zb = (z0 + z1) / 2
    # pinch screw: in from the holder's inner edge, through a captive nut, onto the leg
    pe = Vector(c.x, yw - sy * leg_reach(), zb)
    s = s.cut(molds.nut_trap(pe, Vector(0, -sy, 0), Vector(0, 0, -1), 'M4', mode='side', run=30.0,
                              depth=abs(pe.y - c.y) - q / 2 + 2.0))
    for p, n in ((Vector(xw, c.y, zb), Vector(sx, 0, 0)), (Vector(c.x, yw, zb), Vector(0, sy, 0))):
        s = s.cut(molds.nut_trap(p, n, Vector(0, 0, -1), 'M4', mode='side', run=30.0))
        fixes.append(Fix('bolt', p, n, 4.5, 'leg holder', 'M4', molds.nut_bolt('M4')[0]))
    qb = Vector((ca + cb) / 2, c.y, z0 - TH_SADDLE - 11.0)
    s = s.cut(Part.makeCylinder(2.25, slot + 2 * TH_SADDLE + 2, qb - Vector(0, slot / 2 + TH_SADDLE + 1, 0), Vector(0, 1, 0)))
    s = s.cut(molds.nut_recess(qb + Vector(0, slot / 2 + TH_SADDLE, 0), Vector(0, -1, 0), 'M4'))
    fixes.append(Fix('bolt', qb - Vector(0, T / 2, 0), Vector(0, 1, 0), 4.5, 'leg holder', 'M4',
                     molds.bolt_length(molds.BOARD_MAX + 2 * TH_SADDLE + moldbox.SLOT + 0.5)))
    return s.removeSplitter(), fixes


def mold_upright(kit, g):
    """Upright mold (one: the two uprights are the same part, so it casts one, comes apart after the
    cure and casts the other): cast foot down, so 'up' is +z. Two side plates cut to the profile stand
    on the floor; sloped back and front boards fit between them. The front board's foot sits
    on the printed toe filler. The posts come up through bushings in the floor, 5/8 in rods form the
    tie-rod holes, and a bridge across the top carries the top plate. The two top tie-rod holes are lined with printed
    sleeves, centered on greased 1/2 in rods that run up through the plate and the bridge."""
    T, fb = P['mold_board'], P['mold_freeboard']
    M, folder, show, mult = 'upright', 'upright', ['upright'], 1
    sx = -1
    x0, x1 = -g['outer'], -g['inner']
    top, bb = g['base_top'], g['beam_bot']
    zt = bb + fb
    X, Y, Z = Vector(1, 0, 0), Vector(0, 1, 0), Vector(0, 0, 1)
    toe = top + P['upright_nose']
    L0 = Vector(0, g['up_front'], toe)
    a = (Vector(0, g['up_top_front'], bb) - L0)
    a.normalize()
    nrm = Vector(0, -a.z, a.y)                  # out of the slope, forward and up
    s_of = lambda z, off: (z - L0.z - nrm.z * off) / a.z
    at = lambda s, off: L0 + a * s + nrm * off
    s0, s_top = 20.0, s_of(zt, T)
    K0 = Vector(0, g['up_back_foot'], top)            # back slope: foot to the top's back edge
    b = Vector(0, g['up_y1'], bb) - K0
    b.normalize()
    nb = Vector(0, b.z, -b.y)                    # out of the back, back and up
    sb_of = lambda z, off: (z - K0.z - nb.z * off) / b.z
    bat = lambda s, off: K0 + b * s + nb * off
    yb = bat(sb_of(top, T), T).y                 # back board's outside face at the floor
    B = moldbox.box_board
    kit.board(B('Upright floor', M, (x0 - T - 40, at(s_of(top, T), T).y - 40, top - T), (x1 + T + 40, yb + 40, top),
                -Z, Y, qty=1, show=show))
    prof = [(at(s_of(top, T), T).y, top), (yb, top), (bat(sb_of(zt, T), T).y, zt), (at(s_top, T).y, zt)]
    kit.board(moldbox.Board('Upright side plate, outer', M, Vector(x0, 0, 0), -X, Z, [(y, z) for y, z in prof],
                             qty=1, note='cut to the profile', show=show))
    kit.board(moldbox.Board('Upright side plate, inner', M, Vector(x1, 0, 0), X, Z, [(-y, z) for y, z in prof],
                             qty=1, note='cut to the profile', show=show))
    kit.board(moldbox.Board('Upright back board', M, K0 + X * x0, nb, b,
                             [(0, 0), (x1 - x0, 0), (x1 - x0, sb_of(zt, T)), (0, sb_of(zt, T))], qty=1,
                             note='ends cut square', show=show))
    kit.board(moldbox.Board('Upright front board', M, at(s0, 0) + X * x1, nrm, a,
                             [(0, 0), (x1 - x0, 0), (x1 - x0, s_top - s0), (0, s_top - s0)], qty=1,
                             note='ends cut square', show=show))
    by0 = min(g['bolt_ys'][0], g['columns'][0]) - 10.0               # bridge: over the plate bolts and the rods
    by1_ = max(g['bolt_ys'][1], g['columns'][1]) + 8.5
    kit.board(B('Upright bridge', M, (x0 - T - SLOT_W - TH_SADDLE, by0, zt + TH_SADDLE),
                (x1 + T + SLOT_W + TH_SADDLE, by1_, zt + TH_SADDLE + T), Z, Y, qty=1, view='outside', show=show))

    # corner brackets: back corners, and top and foot of the front board (the foot one only bears on it)
    back, fr = [], []
    for xs, m1 in ((x0 - T, -X), (x1 + T, X)):
        back.append(moldbox.angle_bracket(Vector(xs, bat(sb_of(zt, T), T).y, zt), -nb, m1, -m1, nb, b, fb - 2,
                                          leg=27.0, hole_at=22.5))
        fr.append(moldbox.angle_bracket(Vector(xs, 0, 0) + Vector(0, at(s_top, T).y, at(s_top, T).z), -nrm, m1, -m1, nrm,
                                         a, 22.0))
    kit.add_many(folder, 'back-bracket', 'kit', back, mold=M, show=show, per=2, mult=mult, up=b)
    kit.add_many(folder, 'front-bracket', 'kit', fr, mold=M, show=show, per=2, mult=mult, up=a,
                 note='At the top of the front board; its foot sits in the toe filler\'s lip.')
    yf = at(s_of(top, T), T).y
    for xs, n, tag in ((x0 - T, -X, 'outer'), (x1 + T, X, 'inner')):
        cleat(kit, M, f'Upright cleat, {tag}', Vector(xs, yf + 90.0, top), Vector(xs, yb, top), n, Z, show, 1, mult)
    cleat(kit, M, 'Upright cleat, back', Vector(x0, yb, top), Vector(x1, yb, top), Y, Z, show, 1, mult)
    sad = []
    for xs, n in ((x0, -X), (x1, X)):
        s, wf, _ = moldbox.saddle(Vector(xs, (by0 + by1_) / 2, zt), n, Z, Y, width=24.0, cheeks=False)
        sad.append((s, wf))
    kit.add_many(folder, 'saddle-flat', 'kit', sad, mold=M, show=show, per=2, mult=mult, up=X,
                 note='The bridge rests on them; its rods locate it.')

    # toe filler: under the front board's foot, rounding the nose into the slope
    env = upright_envelope(g, sx, edges=False)
    big = 400.0
    pts = [at(s0, T), at(s0 - big, T), at(s0 - big, -big), at(s0, -big)]
    lip = [at(s0 + 12.0, T + 6.0), at(s0 - big, T + 6.0), at(s0 - big, T - 0.01), at(s0 + 12.0, T - 0.01)]  # holds the board's foot
    region = molds.poly([Vector(x0 + FIT_PLUG, p.y, p.z) for p in pts]).fuse(
        molds.poly([Vector(x0 + FIT_PLUG, p.y, p.z) for p in lip])).extrude(X * (x1 - x0 - 2 * FIT_PLUG))
    region = region.common(parts.box(x0, x1, -1e3, 1e3, top, 1e3))
    toe_shape = max(region.cut(env).Solids, key=lambda s_: s_.Volume)
    fixed_piece(kit, folder, M, 'toe-filler', 'filler', toe_shape, [(Vector(0, 0, top), -Z, 2)], qty=1,
                note='Rounds the nose into the slope; the front board\'s foot sits in its lip. Bolts to the floor.',
                show=show, mult=mult)

    # foot gasket groove: pins into the floor
    keep_clear = [(Vector(sx * rx, ry, top), 8.0) for rx, ry, _ in g['tie_rods']]
    keep_clear += [(Vector(sx * g['ux'], dy, top), 6.4) for dy in g['dowel_ys']]
    fixed_piece(kit, folder, M, 'foot-gasket-groove', 'former', foot_gasket(g, sx)[0], [(Vector(0, 0, top), -Z, 2)],
                qty=1, note='Pins into the floor.', up=-Z, show=show, mult=mult, sizes=('pin',), avoid=keep_clear)

    # tie-rod holes: the top two on greased 1/2 in rods in printed sleeves, up through the plate and the
    # bridge; the slope ones on 5/8 in rods up into plugs that form the nut pockets
    rod = P['up_rod_hole'] / 2 + FIT_PLUG
    holes = []
    for rx, ry, pb in g['tie_rods']:
        x = sx * rx
        if pb >= g['pocket_bot'] - 1:
            holes.append(Fix('hole', Vector(x, ry, top), -Z, 13.5, 'column tie rod, from below'))
        else:
            ys_ = L0.z + (ry - L0.y) * a.z / a.y          # slope height over the rod
            p = Part.makeCylinder(P['slope_pocket_d'] / 2, bb - pb, Vector(x, ry, pb)).common(env).cut(
                Part.makeCylinder(rod, ys_ - 12.0 - pb + 1, Vector(x, ry, pb - 1)))
            nm = 'toe-plug'
            fixed_piece(kit, folder, M, nm, 'plug', p, [(L0, nrm, 1)], qty=1,
                        note='Forms a nut pocket in the slope; bolts to the front board; its rod stops inside it.',
                        show=show, mult=mult, sizes=('M4', 'M3'))
    holes += [Fix('hole', Vector(sx * g['ux'], dy, top), -Z, 13.1, '1/2-13 bolt, base dowel hole') for dy in g['dowel_ys']]
    plate_bolts = [(sx * (g['ux'] - 22.0), g['bolt_ys'][0]), (sx * (g['ux'] + 22.0), g['bolt_ys'][1])]
    sp = []
    for px, py in plate_bolts:
        holes.append(Fix('hole', Vector(px, py, zt + TH_SADDLE), Z, 10.0, '3/8-16 bolt into the top plate'))
        sp.append(Part.makeCylinder(8.0, zt + TH_SADDLE - bb, Vector(px, py, bb)).cut(
            Part.makeCylinder(5.0, 1e3, Vector(px, py, 0))))
    kit.add(folder, 'plate-spacer', 'kit', sp[0], 2, 'Between the bridge and the top plate, on its greased 3/8 bolt.',
            placed=sp, show=show)
    kit.fix(holes, M, mult)
    rod_bot = top - T - 20.0                       # the rods stand 20 mm out under the floor
    kit.count('Block of 2x4, laid flat: four under the upright mold (room under the floor for the rod ends)', 4, M)
    kit.count('the two column tie rods themselves, greased: up through the floor and the columns into the top '
              'plate, to center the columns while the casting goes off', 2, M)
    kit.count('3/8-16 x 3 in bolt, greased (holds the top plate, both layers)', 2, M)
    kit.count('1/2-13 x 1-1/2 in bolt + nut, greased (forms a dowel hole)', len(g['dowel_ys']), M)


SLOT_W = 0.4


def mold_tools(kit):
    """Two small printed tools for the pour line, which is the freeboard below every wall top.
    Pour-line gauge: clips over a wall top; its inner leg ends on the pour line, to pencil the line round
    the mold and to check the fill. Screed shoes: a pair that hang a straight board from the wall tops
    with its bottom edge on the pour line, to strike the top off level."""
    T, fb = P['mold_board'], P['mold_freeboard']
    slot = T + SLOT_W
    # wall top at z = 0, the wall from x = 0 (cast face) to x = T
    gauge = parts.box(-3.0, slot + 3.0, 0, 24.0, 0, 4.0).fuse([parts.box(-3.0, 0, 0, 24.0, -fb, 0),
                                                                parts.box(slot, slot + 3.0, 0, 24.0, -12.0, 0)])
    gauge = parts.soften(gauge.removeSplitter(), 1.0, lambda e: parts.parallel((0, 1, 0))(e)
                         and all(abs(v.Point.z + fb) < 1e-6 for v in e.Vertexes) and all(v.Point.x > -2 for v in e.Vertexes),
                         chamfer=True)
    kit.add('tools', 'pour-gauge', 'kit', gauge, 2, f'Clips over a wall top; its inner leg ends {fb:.0f} mm down, on the '
            'pour line. Pencil along it all round the mold, and check the fill against it.', up=Vector(0, 1, 0), placed=[])
    w = slot + 8.0
    shoe = parts.box(-24.0, T + 6.0, -w / 2, w / 2, 0, 5.0).fuse(parts.box(-24.0, -2.0, -w / 2, w / 2, -fb - 2.0, 0))
    shoe = shoe.cut(parts.box(-25.0, -4.0, -slot / 2, slot / 2, -fb, 1.0)).removeSplitter()
    kit.add('tools', 'screed-shoe', 'kit', shoe, 2, 'A pair: rest them on two facing wall tops and drop a straight board '
            f'(on edge) into them; its bottom edge sits on the pour line. Slide it along to strike off.',
            up=Vector(0, 0, -1), placed=[])


def mold_beam(kit, m, g):
    """Beam mold: cast front (rail) face down on the floor board, so 'up' is +y; the back is open.
    The steel box goes in as one piece: its face plate screwed to the floor, its end plates on the
    1/2 in rods that form the cap-screw holes."""
    T, fb = P['mold_board'], P['mold_freeboard']
    M, folder, show = 'beam', 'beam', ['beam']
    outer, bf, bot, top = g['outer'], g['beam_face'], g['beam_bot'], g['beam_top']
    by1 = bf + P['beam_d']
    yt = by1 + fb
    X, Y, Z = Vector(1, 0, 0), Vector(0, 1, 0), Vector(0, 0, 1)
    xo = outer + T
    B = moldbox.box_board
    kit.board(B('Beam floor', M, (-xo - 40, bf - T, bot - T - 40), (xo + 40, bf, top + T + 40), -Y, Z, show=show))
    kit.board(B('Beam top wall', M, (-xo, bf, top), (xo, yt, top + T), Z, Y, show=show))
    kit.board(B('Beam bottom wall', M, (-xo, bf, bot - T), (xo, yt, bot), -Z, Y, show=show))
    for sx, tag in ((-1, 'left'), (1, 'right')):
        kit.board(B(f'Beam end wall, {tag}', M, (sx * outer, bf, bot), (sx * xo, yt, top), sx * X, Y, show=show))
    br = []
    for sx in (-1, 1):
        for zw, sz in ((top + T, 1), (bot - T, -1)):
            br.append(moldbox.angle_bracket(Vector(sx * xo, yt, zw), -sz * Z, sx * X, -sx * X, sz * Z, Y, fb - 2))
    kit.add_many(folder, 'corner-bracket', 'kit', br, mold=M, show=show, merge=True, up=Y)
    cleat(kit, M, 'Beam cleat, top', Vector(-xo, bf, top + T), Vector(xo, bf, top + T), Z, Y, show)
    cleat(kit, M, 'Beam cleat, bottom', Vector(-xo, bf, bot - T), Vector(xo, bf, bot - T), -Z, Y, show)
    for sx, tag in ((-1, 'left'), (1, 'right')):
        cleat(kit, M, f'Beam cleat, {tag}', Vector(sx * xo, bf, bot), Vector(sx * xo, bf, top), sx * X, Y, show)
    rods = [Part.makeCylinder(P['beam_bolt_hole'] / 2 + FIT_PLUG, top - bot + 2, Vector(sx * bx, by, bot - 1))
            for sx in (-1, 1) for bx in g['bolt_xs'] for by in g['bolt_ys']]
    fl = molds.fillers(beam_envelope(g, edges=False))
    for i, f in enumerate(fl):
        nm = 'back-edge' if len(fl) == 1 else f'back-edge-{i + 1}'
        if P['foam_formers']:
            kit.add(folder, nm, 'foam', f, 1, foam_note('back-edge', f), show=show)
            continue
        f = f.cut(rods)
        fixed_piece(kit, folder, M, nm, 'filler', f, [(Vector(0, 0, top), Z, 1)], up=-Z,
                    note='Rounded back edge between the uprights; bolts to the top wall.', show=show)
    # the face plate lies on the floor, held by greased screws through it into its tapped holes; they stand
    # 10 mm through the plate, so the screws that go in later have room
    holes = []
    for pt, n, kind in m.anchors:
        if abs(n.y) > 0.5:
            holes.append(Fix('hole', pt, -Y, 5.5 if kind == 'insert_m5' else 6.5,
                             f"{'M5' if kind == 'insert_m5' else 'M6'} screw into the face plate"))
    for sx in (-1, 1):
        for bx in g['bolt_xs']:
            for by in g['bolt_ys']:
                holes.append(Fix('hole', Vector(sx * bx, by, top), Z, 13.1, '1/2 core rod'))
                holes.append(Fix('hole', Vector(sx * bx, by, bot), -Z, 13.1, '1/2 core rod'))
        holes.append(Fix('hole', Vector(sx * g['ux'], g['beam_dowel_y'], bot), -Z, 9.6, '3/8 dowel'))
    holes += [Fix('hole', Vector(ix, iy, top), Z, 5.5, 'M5 insert screw') for ix, iy in g['chain_inserts']]
    kit.fix(holes, M)
    stops = [Part.makeCylinder(4.7, T - P['dowel_proud'], Vector(sx * g['ux'], g['beam_dowel_y'], bot - T)).fuse(
        Part.makeCylinder(9.0, 2.0, Vector(sx * g['ux'], g['beam_dowel_y'], bot - T - 2.0))) for sx in (-1, 1)]
    kit.add(folder, 'dowel-stop', 'kit', stops[0], 2, 'Pushes into the dowel hole from outside so the dowel stands '
            f"{P['dowel_proud']:.0f} mm proud.", placed=stops, show=show)
    stand = 5 * math.ceil((P['mold_board'] + P['beam_bar_t'] + 10.0) / 5)      # through the floor and plate, 10 mm proud
    kit.count(f'M6 x {stand} screw, greased (holds the face plate)',
              sum(1 for f in holes if f.what == 'M6 screw into the face plate'), M)
    kit.count(f'M5 x {stand} screw, greased (holds the face plate)',
              sum(1 for f in holes if f.what == 'M5 screw into the face plate'), M)
    kit.count(f"1/2 in plain steel rod, greased (forms a beam bolt hole), {top - bot + 2 * T + 20:.0f} mm", 8, M)
    kit.count('M5 x 20 screw, greased (holds an insert)', len(g['chain_inserts']), M)


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
    # fixings for the parts that bolt on later (way-cover rollers, cable-chain mount), cast in now
    d['cover_inserts'] = roller_layout()['inserts']
    # a Y cable chain for a table-mounted 4th/5th axis (add later): its fixed end on two M5 inserts in the base
    # top, in the 49 mm gap between the table and the right upright, a little behind the split
    d['ychain_x'] = (P['table_w'] / 2 + inner) / 2
    d['ychain_inserts'] = [(d['ychain_x'], 40.0 + dy) for dy in (-11.0, 11.0)]
    d['chain_inserts'] = [(CHAIN['fixed_x'] - 12.5, beam_face + CHAIN['beam_y'] + dy) for dy in (-11.0, 11.0)]
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
               'frame', 'table', 0.0, y_stack, 0.0, P['motor_y'], bracket=P['bracket_y'])
    # the rear way-cover rollers' inner brackets screw into the BK12 pad beside the support (tapped M5)
    for x, y in roller_layout()['tapped']:
        m.anchors.append((Vector(x, y, base_top), Vector(0, 0, 1), 'insert_m5'))
    tw, tl, pitch = P['table_w'], P['table_len'], P['table_hole_pitch']
    table = parts.plate(-tw / 2, tw / 2, -tl / 2, tl / 2, table_bot, table_top, 1.0)
    nx, ny = int((tw - 30) // pitch) + 1, int((tl - 30) // pitch) + 1
    holes = [Part.makeCylinder(2.5, P['table_t'] + 2, Vector((i - (nx - 1) / 2) * pitch, (j - (ny - 1) / 2) * pitch, table_bot - 1))
             for i in range(nx) for j in range(ny)]
    # The table is the module interface: a vise plate, a 4th-axis plate or a trunnion base bolts to the M6 grid and
    # lands square on two 8 mm dowels on the X center line, halfway between grid rows.
    dowel_y = (4.0 if ny % 2 == 0 else 4.5) * pitch
    holes += [Part.makeCylinder(4.0, P['table_t'] + 2, Vector(0, sy * dowel_y, table_bot - 1)) for sy in (-1, 1)]
    # the Y cable chain's moving end: two M5 holes tapped into the table's right edge
    holes += [Part.makeCylinder(2.1, 12.0, Vector(tw / 2 - 12.0, dy, (table_bot + table_top) / 2), Vector(1, 0, 0))
              for dy in (-11.0, 11.0)]
    m.add('Table', 'table', table.cut(holes), 'alu')
    d['table_holes'] = (nx, ny)
    d['table_dowels'] = 2 * dowel_y

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
    steel_tolerance(m, d)

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
        ('Y table', f"{P['bracket_y']} integrated bearing seat + NEMA 23 bracket (in place of the kit's BK12, which is "
                    f"spare); D25 coupler 8 x 10 mm, about {m.coupler_len['Y']:.0f} mm long" if P['bracket_y'] else
         'NEMA 23 bracket for BK12', '1 pc', 'buy'),
        ('X, Y', f"NEMA 23 closed loop {P['motor_x']} + CL57T driver", '2 pcs', 'buy'),
        ('Z', f"NEMA 23 open loop (modeled as {P['motor_z']})", '1 pc', 'OWNED'),
        ('Y table', parts.HOUSING['SFU1605']['name'] + ' nut housing', '1 pc', 'buy (comes in SFU1605 kits)'),
        ('X, Z', parts.HOUSING['SFU1204']['name'] + ' nut housing', '2 pcs', 'X OWNED, Z buy'),
        ('spindle', 'GDZ80-2.2 water-cooled ER20 + VFD + 80 mm cast clamp', '1 set', 'buy'),
        ('all', '6061 flat bar cut to length: table', f"3/4 x {sk.inch(tw)} in x {sk.inch(tl)} in long, M6 grid {nx}x{ny} @ {pitch:.0f}, "
                                                 f"2 x 8 mm H7 dowel holes {d['table_dowels']:.0f} apart on the X center line",
         'buy'),
        ('all', '6061 flat bar cut to length: X carriage', f"5/8 x {sk.inch(P['carriage_w'])} in x {sk.inch(z_flange - car_z0)} in long",
         'buy'),
        ('all', '6061 flat bar cut to length: Z plate', f"5/8 x {sk.inch(P['zplate_w'])} in x {sk.inch(P['z_rail_len'])} in long", 'buy'),
        ('all', 'Cold-rolled steel flat bar rail risers, bedded + epoxy-replicated', "1-1/4 in wide, 3/4 in (Y) and 5/8 in (X, Z)", 'buy'),
        ('all', 'Feet: 1/2-13 x 2 in bolt + jam nut + rubber pad (into the nut in each leg end)', '4 sets', 'buy'),
        ('enclosure', 'M5 x 35 cap screw through the bottom rails into cast-in inserts', f"{len(d['rail_bolts'])} pcs", 'buy (part 3)'),
        ('frame', 'Cast-in M5 threaded inserts (knurled brass): the enclosure, the way-cover rollers, the cable-chain mounts '
                  '(beam and Y)',
         f"{len(d['rail_bolts'])} + {len(d['cover_inserts'])} + {len(d['chain_inserts'])} + {len(d['ychain_inserts'])} pcs", 'buy'),
        ('frame', 'Cap screws into the tapped steel: DIN 7984 low-head M5 x 20 (X risers) and M5 x 25 (Y risers); '
                  'M6 x 40 (the Y and X BK/BF)',
         f"{d['anchor_count'].get('face_insert_m5', 0)} + "
         f"{d['anchor_count'].get('base_insert_m5', 0) - len(roller_layout()['tapped'])}; "
         f"{d['anchor_count'].get('face_insert_m6', 0) + d['anchor_count'].get('base_insert_m6', 0)}", 'buy'),
    ] + d['steel_bom'] + [
        ('coolant', 'Sump: full-size 4 in stainless steam-table pan (~13 L), slides in under the base', '1', 'buy'),
        ('coolant', 'Chip basket: 1/3-size perforated steam-table pan, 2.5 in deep', '1', 'buy'),
        ('coolant', '100 um filter mesh (printed frame), printed baffle, a bag of N52 bar magnets', '1 set', 'buy (part 3)'),
        ('coolant', 'Submersible pump 24 V brushless, ~800 L/h, 5 m head, on the controller M8 MOSFET output', '1', 'buy (part 3)'),
        ('coolant', 'Return hose 8 mm OD PU, push-to-connect at the pump so the sump slides out', f"{d['hose_return']:.1f} m", 'buy (part 3)'),
        ('frame', 'Leg feet: printed plug + 1/2-13 nut bonded into each leg end', '4 pcs', 'PRINT'),
        ('coolant', '1/4 in bulkhead fitting, ball valve, manifold, 2x Loc-Line 1/4 in nozzles', '1 set', 'buy (part 3)'),
        ('covers', 'Roll-up way cover: spring roller + 0.1 mm stainless strip; M5 x 12 into the inserts and the BK pad',
         '1x 250 wide, 2x 85 wide', 'buy or DIY (add later)'),
        ('covers', 'Spiral ballscrew cover for the table screw', '1', 'buy (add later)'),
        ('covers', 'Drip shield over the beam rails, ACM offcut, clamped under the front beam stud nuts',
         f"{d['drip_shield'][0]:.0f} x {d['drip_shield'][1]:.0f}", 'buy (add later)'),
        ('electronics', 'Homing switches: Y on the Y motor bracket (the table\'s rear edge trips it), X and Z on the X '
                        'carriage; they need nothing cast in', '3', 'buy (part 2)'),
        ('covers', 'Brush seal plates for the motor cutouts', '2', 'buy (part 3)'),
        ('printed', f"Drag chain links, PETG: {CHAIN['width']:.0f} x {CHAIN['height']:.0f} outer, {CHAIN['pitch']:.0f} pitch, "
                    f"R{CHAIN['radius']:.0f} bend", f"{CHAIN['links']} + 2 end mounts", 'PRINT'),
    ]
    mold_parts(m, d)
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
    # Opaque aluminum composite panel (ACM) for the walls and roof; only the door is clear.
    for name, shape, cut in panels:
        add(name, shape.cut(cut) if cut else shape, 'acm')
        bb = shape.BoundBox
        dims = sorted((bb.XLength, bb.YLength, bb.ZLength), reverse=True)[:2]
        m.cutlist.append((name, f'{dims[0]:.0f} x {dims[1]:.0f} ACM 3 mm'))

    # Brush seals around the motors where they pass through the panels (outside face).
    s_out, s_in = c + 10.0, 33.0     # the opening clears the motor (28.2 a side) and the Y bracket's flange (31.5 up)
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
ROLLER_R = 18.0


def roller_layout():
    """The way covers' spring rollers {name: (x0, x1, y, feet)} and their fixings, cast in with the base so
    the covers bolt on whenever they are bought. The front roller sits over the coolant trough, so its end
    brackets reach back past it to an M5 insert each; the rear rollers' outer brackets reach outboard to an
    insert, their inner ones forward onto the BK12 pad beside the support, tapped M5. feet: (x, y, wx, wy)."""
    r, rail_end = ROLLER_R, P['table_rail_len'] / 2
    yf = P['table_rail_y'] - rail_end - r - 1.0
    yr = P['table_rail_y'] + rail_end + r + 1.0
    rollers = {'Front': (-125.0, 125.0, yf, [(sx * 128.0, yf + 30.0, 12.0, 24.0) for sx in (-1, 1)])}
    for sx, side in ((-1, 'L'), (1, 'R')):
        x0, x1 = sorted((sx * 125.0, sx * 40.0))                 # either side of the BK12
        rollers[f'Rear{side}'] = (x0, x1, yr, [(sx * 137.0, yr, 14.0, 18.0), (sx * 39.0, yr - 31.0, 12.0, 24.0)])
    feet = [f_ for *_, fs in rollers.values() for f_ in fs]
    return dict(rollers=rollers, inserts=[(x, y) for x, y, *_ in feet if abs(x) > 60],
                tapped=[(x, y) for x, y, *_ in feet if abs(x) <= 60])


def covers(m, d):
    """Keep chips off the ways.

    Table: roll-up 0.1 mm stainless strips on spring rollers in front of and behind the
    table (running just over the BF/BK12 supports and under the table), plus a spiral
    spring cover on the screw behind the table. Beam: a drip shield over the rails. All of
    them bolt on later to fixings already in the castings (roller_layout, the beam studs).
    """
    base_top, tl, r = d['base_top'], P['table_len'], ROLLER_R
    zs = base_top + parts.SUPPORT['BK12']['H'] + 0.5          # strip underside
    zr = zs - r
    rl = roller_layout()['rollers']
    yf, yr = rl['Front'][2], rl['RearL'][2]
    for name, (x0, x1, y, feet) in rl.items():
        m.add(f'CoverRoller{name}', 'frame', parts.roll_cover(x0, x1, y, zr, base_top, r, feet), 'black',
              container='FrameBaseFront' if y < 0 else 'FrameBaseRear')
    rear_x = (rl['RearL'][:2], rl['RearR'][:2])

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

    # drip shield: from over the X rails back past the front row of beam studs, whose nuts clamp it
    g = frame_layout(d)
    xs = g['ux'] + 22.0 + 12.0
    y0, y1 = d['car_back'] + 2.0, g['bolt_ys'][0] + 12.0
    shield = parts.box(-xs, xs, y0, y1, d['beam_top'], d['beam_top'] + P['drip_shield_t'])
    shield = shield.cut([Part.makeCylinder(5.5, 10.0, Vector(sx * bx, g['bolt_ys'][0], d['beam_top'] - 1))
                         for sx in (-1, 1) for bx in g['bolt_xs']])
    m.add('DripShield', 'frame', shield, 'shim', container='FrameBeam')
    d['drip_shield'] = (2 * xs, y1 - y0)


CHAIN = dict(pitch=20.0, width=38.0, height=21.0, radius=38.0, links=17, fixed_x=-110.0, carriage_dx=-20.0,
             beam_y=60.0)   # chain center line, this far behind the beam face


def chain_and_coolant(m, d):
    """Printed drag chain on the beam (coolant, Z motor and spindle lines), the coolant return
    from the bulkhead to the nozzles, and the flexible loop down to the spindle clamp."""
    C = CHAIN
    p_, h_, rad, n = C['pitch'], C['height'], C['radius'], C['links']
    length = n * p_
    bt = d['beam_top']
    cy = d['beam_face'] + C['beam_y']
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
    fixed = parts.box(xf - 25, xf, cy - hw, cy + hw, bt, bt + h_)       # screws into the two inserts in the beam top
    fixed = fixed.cut([Part.makeCylinder(2.75, h_ + 2, Vector(ix, iy, bt - 1)) for ix, iy in d['chain_inserts']])
    m.add('ChainMountFixed', 'frame', fixed, 'printed', container='FrameBeam')
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
    ] + [f"Aluminum oxide grit, {name}: {sum(grit[name].values()):.1f} kg (beam + uprights)" for name, _, _ in P['alumina']] + [
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
    lines += ['', f"Steel cut to length (+/-{P['tube_cut_tol']:.1f} mm allowed; studs +/-{P['stud_tol']:.1f} mm; tubes +/-0.5 mm "
              f"across the flats, printed fits {P['tube_fit']:.2f} mm a side)", '-' * 98,
              f"  {'Piece':18s} {'Set from (datum)':50s} {'Error goes to':36s} Room"]
    lines += [f"  {n:18s} {dat:50s} {fr:36s} {room:4.1f} mm {'ok' if ok else 'TOO LITTLE'}"
              for n, dat, fr, room, ok in d['steel_tol']]
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
    # The molds, hidden: boards and printed pieces, one group per casting step; shown in the build
    # renders, left out of the STEP export.
    mtop = doc.addObject('App::Part', 'Molds')
    groups = {}
    for key, cname in MOLD_GROUPS.items():
        groups[key] = doc.addObject('App::Part', cname)
        mtop.addObject(groups[key])

    def show(key, label, shape, look):
        obj = doc.addObject('Part::Feature', f"{MOLD_GROUPS[key]}_{label}".replace('-', '_').replace(' ', '_')
                            .replace(',', '').replace('=', '').replace('.', '_'))
        obj.Shape = shape
        groups[key].addObject(obj)
        if App.GuiUp:
            style(obj, look)
    kit = getattr(m, 'mold_kit', None)
    for b in (kit.boards if kit else []):
        for key in b.show:
            show(key, b.name, b.solid(), 'melamine')
    for r in getattr(m, 'molds', []):
        for i, (shape, keys) in enumerate(r['placed']):
            for key in keys:
                show(key, f"{r['kind']}_{r['name']}_{i}", shape, 'foam' if r['kind'] == 'foam' else 'printed')
    mtop.Visibility = False
    doc.recompute()
    doc.saveAs(path)
    return doc


def export_step(doc, path):
    try:
        import Import
        tops = [o for o in doc.Objects if o.TypeId == 'App::Part' and o.getParentGeoFeatureGroup() is None
                and o.Name != 'Molds']
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
         dict(mode='bare', section=('x', 'BaseGirderRearR'))),
        ('frame_base_underside', (0, 0, 0), lambda: look((0.35, 0.55, 1.0)), ('BaseFrontCasting', 'BaseRearCasting'),
         dict(mode='bare', only=('FrameBaseFront', 'FrameBaseRear'))),
        ('gasket_base_split', (0, 0, 0), iso, ('BaseRearCasting',), dict(mode='bare', only=('FrameBaseRear',))),
        # Build steps (renders/build/): cast-in steel, molds, frame assembly, axes
        ('build/01-steel-base-rear', (0, 0, 0), rear_iso, ('BaseRearCasting',),
         dict(mode='bare', only=('FrameBaseRear',), xray=True)),
        ('build/02-mold-base-rear', (0, 0, 0), lambda: look((0.45, 0.6, 0.65), Vector(0, 0, -1)), ('BaseRearCasting',),
         dict(mode='bare', only=('FrameBaseRear',), xray=True, molds=('MoldBaseRear',))),
        ('build/03-steel-base-front', (0, 0, 0), iso, ('BaseFrontCasting',),
         dict(mode='bare', only=('FrameBaseFront',), xray=True)),
        ('build/04-mold-base-front', (0, 0, 0), lambda: look((0.45, 0.6, 0.65), Vector(0, 0, -1)),
         ('BaseFrontCasting', 'BaseRearCasting'),
         dict(mode='bare', only=('FrameBaseFront', 'FrameBaseRear'), xray=True, molds=('MoldBaseFront',))),
        ('build/05-mold-upright', (0, 0, 0), lambda: look((0.8, 0.55, -0.45)), ('UprightLCasting',),
         dict(mode='bare', only=('FrameUprightL',), xray=True, molds=('MoldUpright',))),
        ('build/06-mold-beam', (0, 0, 0), lambda: look((0.4, -0.75, -0.5), Vector(0, 1, 0)), ('BeamCasting',),
         dict(mode='bare', only=('FrameBeam',), xray=True, molds=('MoldBeam',))),
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
        """Cut the visible structure at the plane through `through`'s center; keep the far side."""
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
        shown_molds = o.get('molds', ())
        for t in tops:
            if t not in (enc, bench) and t not in axes:
                t.Visibility = (not bare and t.Name != 'Molds') or t.Name == 'Frame' or (
                    t.Name == 'Molds' and bool(shown_molds))
        for f in features:
            parent = f.getParentGeoFeatureGroup()
            in_only = 'only' not in o or (parent is not None and parent.Name in o['only'])
            f.Visibility = (not bare or (f in structure and in_only)
                            or ('extra' in o and f.Name.startswith(o['extra']) and in_only)
                            or (parent is not None and parent.Name in shown_molds))
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
    doc.getObject('Molds').Visibility = False
    for gk in gaskets:
        style(gk, 'rubber')
    for c in castings:
        style(c, 'granite')
    doc.recompute()
    view.viewIsometric()
    view.fitAll()
    doc.save()


FOLDER_TITLES = [('tools', 'Tools: pour-line gauge and screed shoes'), ('base-box', 'Base mold kit (both halves)'), ('base-rear', 'Base, rear half (cast first)'),
                 ('base-front', 'Base, front half'),
                 ('upright', 'Uprights (one mold, cast twice: cast-in parts are for both)'), ('beam', 'Beam'),
                 ('machine', 'Machine parts')]


def export_prints(m):
    """STLs for every printed piece under print/, and docs/src/print-guide.md listing them."""
    root = os.path.join(ROOT, 'print')
    for dp, _, fn in os.walk(root):
        for f in fn:
            if f.endswith('.stl') or f == 'manifest.csv':
                os.remove(os.path.join(dp, f))
    rows = molds.export(m.molds, root)
    kinds = {'core': 'Pocket core (shell, stays in)', 'former': 'Former (removable)', 'filler': 'Filler (removable)',
             'plug': 'Plug (removable)', 'liner': 'Liner (stays in)', 'cast-in': 'Cast-in part (stays in)',
             'kit': 'Mold kit (reused)', 'part': 'Machine part'}
    # sliced figures (model/slice_prints.py), if they are for these files
    sliced, hours = {}, None
    path = os.path.join(root, 'sliced.csv')
    if os.path.exists(path):
        sl = {(r['folder'], r['file']): r for r in csv.DictReader(open(path))}
        if all((r['folder'], r['file']) in sl and sl[(r['folder'], r['file'])]['estimate'] == f"{r['grams']:.0f}"
               and sl[(r['folder'], r['file'])]['grams'] != '' for r in rows):
            for r in rows:
                x = sl[(r['folder'], r['file'])]
                r['grams'], r['time'] = float(x['grams']), x['time_each']
            sliced = True
    total_g = sum(r['grams'] for r in rows)
    total_n = sum(r['qty'] for r in rows)
    how = ('sliced in Bambu Studio (A1 mini, 0.4 mm nozzle, 0.2 mm layers, PETG) with the settings below, by '
           '`model/slice_prints.py`' if sliced else 'rough estimates; run `python3 model/slice_prints.py` for sliced figures')
    lines = ['# Print guide', '',
             'Every printed part for the molds, the castings and the machine, cut to fit a Bambu A1 mini',
             f'(180 mm cube; no piece is over {molds.BED:.0f} mm). The STL files are in `print/`, one folder per',
             'casting, with the list in `print/manifest.csv`. They are written by `model/build_cnc.py` on every run.',
             'How the molds go together is in the mold guide.', '',
             f'**{total_n} prints, {total_g / 1000:.2f} kg of PETG** (two 1 kg rolls). The filament figures are {how}.', '',
             '## Settings', '',
             '- **PETG for everything.** Thick sections of curing epoxy get warm, and PLA softens at about 55 °C.',
             '- 0.4 mm nozzle, 0.2 mm layers, 4 top and 3 bottom layers. Every file is already turned the way it prints',
             '  best, without supports.',
             f'- **Cores** (`core-*`): thin shells, {molds.WALL:.1f} mm walls (three lines), so they print solid; the',
             '  posts get 2 walls and 10 % infill. The sand inside holds the walls while casting.',
             '- **Fillers, formers, plugs** (`filler-*`, `former-*`, `plug-*`): 2 walls, 10 % infill. They only have to',
             '  hold their shape against the mix; the nut pockets have their own walls.',
             '- **Mold kit** (`kit-*`: brackets, saddles, holders, bushings) and machine parts: 3 walls, 15 % infill. Print one,'
             f'  check it over a {P["mold_board"]:.0f} mm offcut of your board, then the rest.',
             '- **Liners and cast-in parts** (`liner-*`, `cast-in-*`): 3 walls, 40 % infill.',
             '- **Fits.** Slip fits are 0.15 mm a side, nut pockets 0.15 mm over the nut, pins 3.0 mm into a 1/8 in',
             '  hole. If your printer runs tight, print a bracket and a former first and adjust the',
             '  horizontal expansion (XY compensation) rather than the files.', '',
             '## Joining the pieces', '',
             '- **Nuts.** Every piece that bolts to a board has its nut built in. On cast faces the nut drops into a',
             '  pocket in the face against the board and slides sideways under the bolt hole; on brackets it',
             '  presses into a hex pocket. Fit the nuts before the piece goes on the board.',
             '- **Parts cut to fit the bed** (`-partNofM`) have a peg on one cut face and a socket on the other:',
             '  push them together, no glue. Each part has its own bolts or pins to the board.',
             '- **Cores** cut in two have a bulkhead on each side of the cut with two M3 x 10 bolts through them.',
             '- **Pins.** Thin formers (gasket-groove beads, the shallow end of a gutter) have 3 mm pins that push into',
             '  1/8 in holes. Nothing else holds them; the casting presses them onto the board.',
             '- **Removable pieces** (formers, fillers, plugs, kit): 3-5 coats of paste wax and PVA like the boards.',
             '  **Pieces that stay in** (core posts, cast-in parts): no wax; scuff and degrease them so the',
             '  epoxy grips.', '',
             '![Base rear mold: boards, kit and cores (orange)](../../renders/build/02-mold-base-rear.png)', '',
             '## Foam pieces', '',
             'The base pocket cores are XPS foam board (`foam=True`, the default in',
             '`model/build_cnc.py`); only their posts are printed. They are hidden and',
             'only need to be within a millimeter or two. The coolant trough, gutters and the beam\'s back edge print,',
             'because they shape faces you see and drain coolant (`foam_formers=True` cuts those from foam too). The',
             'mold guide lists the foam pieces with their sizes. `foam=False` prints the cores (about 1.4 kg more).', '']
    lines.append('')
    for key, title in FOLDER_TITLES:
        sub = [r for r in rows if r['folder'] == key]
        if not sub:
            continue
        lines += [f'## {title}', '', f'Folder `print/{key}/`, about {sum(r["grams"] for r in sub):.0f} g.', '',
                  '| File | What | Qty | Size (mm) | g (all) | Notes |', '|---|---|---|---|---|---|']
        for r in sub:
            lines.append(f"| `{r['file']}` | {kinds[r['kind']]} | {r['qty']} | {r['size']} | {r['grams']:.0f} | {r['note']} |")
        lines.append('')
    with open(os.path.join(ROOT, 'docs', 'src', 'print-guide.md'), 'w') as fh:
        fh.write('\n'.join(lines))
    print(f'print/: {len(rows)} STL files, about {total_g / 1000:.1f} kg PETG')


DRILLS = {3.2: '1/8 in', 3.4: '9/64 in', 4.5: '11/64 in', 5.5: '7/32 in', 6.5: '17/64 in', 9.6: '25/64 in',
          10.0: '25/64 in', 13.1: '33/64 in', 13.5: '17/32 in', 16.3: '41/64 in', 63.5: '2-1/2 in hole saw'}
MOLD_TITLES = {'base': 'Base', 'upright': 'Uprights', 'beam': 'Beam'}


def board_svg(b, path):
    """Drawing of a board from the side it is marked on, holes numbered."""
    us = [u for u, _ in b.outline]
    vs = [v for _, v in b.outline]
    u0, u1, v0, v1 = min(us), max(us), min(vs), max(vs)
    flip = b.view == 'outside'
    X = (lambda u: u1 - u) if flip else (lambda u: u - u0)
    Yv = lambda v: v1 - v
    fs = 2.6 * max(1.0, (u1 - u0 + 20) / 180.0)          # about 2.6 mm high once the page shrinks it to fit
    pad = 2 * fs
    w, h = u1 - u0 + 2 * pad, v1 - v0 + 2 * pad
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-pad:.1f} {-pad:.1f} {w:.1f} {h:.1f}" '
           f'width="{w:.0f}mm" height="{h:.0f}mm" font-family="Helvetica, Arial, sans-serif">',
           '<polygon points="' + ' '.join(f'{X(u):.1f},{Yv(v):.1f}' for u, v in b.outline) +
           '" fill="#f4f4f1" stroke="#222" stroke-width="0.8"/>']
    for k, (u, v, d, what) in enumerate(hole_order(b), 1):
        x, y = X(u), Yv(v)
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{max(d / 2, fs / 4):.1f}" fill="none" stroke="#a8641a" '
                   f'stroke-width="{fs / 8:.2f}"/>')
        out.append(f'<text x="{x + max(d / 2, fs / 4) + fs / 6:.1f}" y="{y - fs / 6:.1f}" font-size="{fs:.1f}" '
                   f'fill="#1d2422">{k}</text>')
    span = b.pour_span()
    if span:
        xa, xb = sorted((X(span[0]), X(span[1])))
        y = Yv(b.pour_v)
        out.append(f'<line x1="{xa:.1f}" y1="{y:.1f}" x2="{xb:.1f}" y2="{y:.1f}" stroke="#2b72c9" stroke-width="{fs / 6:.2f}" '
                   f'stroke-dasharray="{fs:.1f},{fs / 2:.1f}"/>')
        out.append(f'<text x="{xa + fs:.1f}" y="{y + 1.2 * fs:.1f}" font-size="{fs * 0.9:.1f}" fill="#2b72c9">pour line '
                   f'({v1 - b.pour_v:.0f} mm below the top)</text>')
    out.append(f'<text x="0" y="{v1 - v0 + 1.4 * fs:.1f}" font-size="{fs:.1f}" fill="#5b6662">0,0 · {u1 - u0:.0f} x {v1 - v0:.0f} mm · '
               f'seen from the {"outside (top)" if flip else "cast side"}</text>')
    out.append('</svg>')
    with open(path, 'w') as fh:
        fh.write('\n'.join(out))


def hole_order(b):
    return sorted(b.holes, key=lambda h: (round(h[1] / 5), h[0]))


SHEET = (2440.0, 1220.0)        # 4 x 8 ft
KERF = 4.0


def sheet_layout(boards):
    """Three-stage cut of the melamine boards (not the lumber): rip each sheet into strips along its length,
    as wide as the widest piece left; crosscut each strip into columns as long as their first piece; rip a
    column into narrower pieces side by side (two bridges out of a wall-wide strip). Widest first.
    Returns [[(x, y, w, h, label)]]."""
    pcs = []
    for b in boards:
        if b.stock:
            continue
        su, sv = b.size()
        for k in range(b.qty):
            L, W = max(su, sv), min(su, sv)
            pcs.append((W, L, b.name + (f' ({k + 1})' if b.qty > 1 else '')))
    pcs.sort(key=lambda p: (-p[0], -p[1]))
    sheets = []
    while pcs:
        sheet, y = [], 0.0
        while pcs:
            first = next((p for p in pcs if y + p[0] <= SHEET[1] + 0.1), None)
            if first is None:
                break
            w, x = first[0], 0.0
            while True:
                col = next((p for p in pcs if p[0] <= w + 0.1 and x + p[1] <= SHEET[0] + 0.1), None)
                if col is None:
                    break
                lc, yc = col[1], y
                for p in list(pcs):
                    if p[1] <= lc + 0.1 and yc + p[0] <= y + w + 0.1:
                        sheet.append((x, yc, p[1], p[0], p[2]))
                        yc += p[0] + KERF
                        pcs.remove(p)
                x += lc + KERF
            y += w + KERF
        sheets.append(sheet)
    return sheets


def sheet_svg(sheet, k, path):
    W, H = SHEET
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-20 -40 {W + 40:.0f} {H + 70:.0f}" '
           f'font-family="Helvetica, Arial, sans-serif">',
           f'<text x="0" y="-12" font-size="34" fill="#1d2422">Sheet {k}: 4 x 8 ft (1220 x 2440 mm)</text>',
           f'<rect x="0" y="0" width="{W}" height="{H}" fill="#f4f4f1" stroke="#222" stroke-width="3"/>']
    cols = ['#e9d8c4', '#d8e4ef', '#dfe9d6', '#efe1ea']
    for i, (x, y, w, h, label) in enumerate(sheet):
        out.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" fill="{cols[i % 4]}" '
                   f'stroke="#a8641a" stroke-width="2.5"/>')
        fs = max(13.0, min(30.0, h / 3.2, w / max(len(label), 1) * 1.7))
        out.append(f'<text x="{x + w / 2:.0f}" y="{y + h / 2 - fs * 0.15:.0f}" font-size="{fs:.0f}" text-anchor="middle" '
                   f'fill="#1d2422">{label}</text>')
        out.append(f'<text x="{x + w / 2:.0f}" y="{y + h / 2 + fs * 0.95:.0f}" font-size="{fs * 0.8:.0f}" '
                   f'text-anchor="middle" fill="#5b6662">{w:.0f} x {h:.0f}</text>')
    out.append('</svg>')
    with open(path, 'w') as fh:
        fh.write('\n'.join(out))


MOLD_FOLDERS = {'base': ('base-box', 'base-rear', 'base-front'), 'upright': ('upright',), 'beam': ('beam',)}
MOLD_DOCS = {None: ('molds-complete', 'Mold guide'), 'base': ('base-mold', 'Base mold'),
             'upright': ('upright-molds', 'Upright molds'), 'beam': ('beam-mold', 'Beam mold')}


def write_mold_guide(m):
    """The mold guides in docs/src/: the complete one and one per mold (base, uprights, beam), with the
    board drawings in docs/src/boards/ and the illustrations from model/mold_figures.py in renders/mold/."""
    bdir = os.path.join(ROOT, 'docs', 'src', 'boards')
    os.makedirs(bdir, exist_ok=True)
    for f in os.listdir(bdir):
        if f.endswith('.svg'):
            os.remove(os.path.join(bdir, f))
    for k, sh in enumerate(sheet_layout(m.mold_kit.boards), 1):
        sheet_svg(sh, k, os.path.join(bdir, f'sheet-{k}.svg'))
    for b in m.mold_kit.boards:
        if b.holes:
            board_svg(b, os.path.join(bdir, board_file(b)))
    for only, (name, _) in MOLD_DOCS.items():
        with open(os.path.join(ROOT, 'docs', 'src', name + '.md'), 'w') as fh:
            fh.write('\n'.join(mold_guide(m, only)))
    # the boards as drawn (x from the left, y from the bottom, as marked), for the printable templates
    out = []
    for b in m.mold_kit.boards:
        us = [u for u, _ in b.outline]
        vs = [v for _, v in b.outline]
        u0, u1, v0 = min(us), max(us), min(vs)
        X = (lambda u: u1 - u) if b.view == 'outside' else (lambda u: u - u0)
        span = b.pour_span()
        out.append(dict(name=b.name, mold=b.mold, qty=b.qty, view=b.view, note=b.note,
                        size=[round(u1 - u0, 1), round(max(vs) - v0, 1)],
                        outline=[[round(X(u), 2), round(v - v0, 2)] for u, v in b.outline],
                        holes=[[round(X(u), 2), round(v - v0, 2), d, w, DRILLS.get(round(d, 1), '')]
                               for u, v, d, w in hole_order(b)],
                        pour=None if span is None else [round(b.pour_v - v0, 2), round(min(X(span[0]), X(span[1])), 2),
                                                        round(max(X(span[0]), X(span[1])), 2)]))
    with open(os.path.join(bdir, 'boards.json'), 'w') as fh:
        json.dump(dict(freeboard=P['mold_freeboard'], board=P['mold_board'], boards=out), fh, indent=1)


def board_file(b):
    return re.sub(r'[^a-z0-9]+', '-', b.name.lower()).strip('-') + '.svg'


def mold_guide(m, only=None):
    """The mold guide's lines: everything (only=None), or one mold ('base', 'upright', 'beam')."""
    kit = m.mold_kit
    T, fb = P['mold_board'], P['mold_freeboard']
    molds_ = ('base', 'upright', 'beam') if only is None else (only,)
    folders = [f for mo in molds_ for f in MOLD_FOLDERS[mo]] + ['tools']
    boards = [b for b in kit.boards if b.mold in molds_]
    hw = kit.hardware if only is None else kit.by_mold.get(only, {})
    fig = lambda name, cap: [f'![{cap}](../../renders/mold/{name}.png)', '']
    sheets = sheet_layout(kit.boards)
    foam = [r for r in m.molds if r['kind'] == 'foam' and r['folder'] in folders]
    sl_path = os.path.join(ROOT, 'print', 'sliced.csv')
    sliced = [r for r in csv.DictReader(open(sl_path)) if r['folder'] in folders] if os.path.exists(sl_path) else []
    area = sum(b.size()[0] * b.size()[1] * b.qty for b in boards if not b.stock) / 1e6
    lumber = {}
    for b in boards:
        if b.stock:
            lumber[b.stock] = lumber.get(b.stock, 0.0) + (max(b.size()) + KERF) * b.qty
    lumber_txt = ', '.join(f'{math.ceil(v / 2438.4)} x 8 ft {k} ({v / 1000:.1f} m)' for k, v in sorted(lumber.items()))
    title = MOLD_DOCS[only][1]
    tmpl = ', '.join(f'`templates/{mo}-templates.pdf`' for mo in molds_)
    expl = {'base': ('exploded-base', 'The base mold (rear half), pulled apart'),
            'upright': ('exploded-upright', 'An upright mold, pulled apart'),
            'beam': ('exploded-beam', 'The beam mold, pulled apart')}

    L = [f'# {title}', '']
    if only is None:
        L += ['How to make the molds for the five castings. Each mold also has its own shorter guide in this folder',
              '(base, uprights, beam), and its own printable drilling templates in `templates/`.', '']
    else:
        L += [f"How to make the {title.lower()}. Drilling templates: {tmpl}. The sheet layout for the boards is",
              '`docs/src/boards/sheet-1.svg`; `docs/src/make_pdfs.py` also makes `molds-complete.pdf`, all the molds in one',
              '(not kept in the repo).', '']
    for mo in molds_:
        L += fig(*expl[mo])
    L += ['**In short:** melamine boards bolt together with printed brackets. Every printed piece bolts or pins to',
          'its board from outside. The walls stand 25 mm above the pour line, so no bolt goes through a face the',
          'mix touches. Nothing is glued, and it all comes apart for the next casting.', '',
          '**Order of work:** print &rarr; cut the boards &rarr; mark them with the templates and drill &rarr;' +
          (' cut the foam &rarr;' if foam else '') + ' wax &rarr; assemble &rarr; pour &rarr; take apart.', '',
          '## 1. How it works', '',
          f'- **Walls** stand on the floor against bolted-down **cleats**; **corner brackets** square the tops. All the',
          f'  bolts go through the top {fb:.0f} mm, above the pour line.']
    L += [''] + fig('detail-corner', 'A corner of the base mold')
    L += ['- **Printed pieces** have a nut built in: it goes into a pocket on the board side and slides under the',
          '  hole; an M4 bolt comes through the board from outside.', ''] + fig('fixing-nut', 'The captive nut')
    L += ['- **Thin pieces** (gasket-groove beads) have 3 mm pins that push into 1/8 in holes.', '']
    L += fig('fixing-pins', 'Pins on a gasket-groove bead')
    L += ['- **Long pieces** are printed in parts that peg together; each part bolts down on its own.', '']
    L += fig('fixing-peg', 'Peg and socket')
    if 'base' in molds_:
        L += ['- **Cores** are taped foam blocks with a printed post that bolts to a bridge across the mold.', '']
        L += fig('detail-core', 'A foam core on its bridge')
    L += [f'- **Fits** are 0.15 mm a side, and drawn for {T:.2f} mm board (Home Depot\'s 3/4 in melamine is a true',
          '  0.750 in). Measure yours; if it differs, set `mold_board` in `model/build_cnc.py` and re-run it.', '',
          '## 2. What you need', '', '| Material | Amount | Notes |', '|---|---|---|']
    n_sh = f"{len(sheets)} sheet{'s' if len(sheets) > 1 else ''}"
    L.append(f'| Melamine board, 3/4 in | {n_sh}, 4 x 8 ft | layout in section 4 |' if only is None
             else f'| Melamine board, 3/4 in | about {area:.1f} m2 | all the molds come out of {n_sh}, 4 x 8 ft |')
    if lumber:
        L.append(f'| 1x2 lumber (furring strip is fine) | {lumber_txt} | the cleats: they lie on the floor outside the walls |')
    if foam:
        L.append('| XPS foam board, 2 in | 1 sheet, 2 x 8 ft | the cores |')
    if sliced:
        g = sum(float(r['grams']) for r in sliced)
        L.append(f'| PETG | {g / 1000:.2f} kg | sliced; everything printed for the machine fits in two 1 kg rolls |')
    if foam:
        L.append('| Packing tape, double-sided carpet tape | 1 roll each | wrapping and holding the foam |')
    L += ['| Paste wax and PVA | 1 each | release |',
          '| 3/8 in quarter-round PVC molding | ' + ('about 6 m' if only is None else 'a few meters') + ' | the rounded outside edges |']
    if 'upright' in molds_:
        L.append('| 2x4 offcut | 4 blocks per upright mold, about 50 mm | feet |')
    L += ['', '| Hardware | Qty |', '|---|---|']
    for k in sorted(hw, key=lambda k: (not k.startswith('M'), k)):
        if not k.startswith('Block of 2x4'):
            L.append(f'| {k} | {hw[k]} |')
    L += ['', 'Add about 10 % spare small bolts, nuts and washers. **Tools:** drill and brad-point bits (sizes in section 5)' +
          (', a 2-1/2 in hole saw' if only in (None, 'base', 'upright') else '') +
          (', a jigsaw for the side plates\' slope' if only in (None, 'upright') else '') +
          ', a square, clamps, a 7 mm nut driver, a 3 mm hex key, an awl' +
          (', a fine saw or hot wire for the foam' if foam else '') + '.', '',
          '## 3. Print', '']
    if sliced:
        hours = sum(_minutes(r['time_each']) * int(r['qty']) for r in sliced if r['time_each'] != 'FAILED') / 60
        L += [f'{sum(int(r["qty"]) for r in sliced)} prints, {sum(float(r["grams"]) for r in sliced) / 1000:.2f} kg, about '
              f'{hours:.0f} hours (sliced; settings in the print guide). Print one corner bracket and one saddle first',
              'and check them on a board offcut. Press or slide the nuts in before the pieces go on the boards.', '']
    if only is None:
        L += fig('gallery-kit', 'The printed mold kit') + fig('gallery-pieces', 'Formers, fillers and plugs')
    L += ['| File | Qty | g | Time each |', '|---|---|---|---|']
    for r in sliced:
        L.append(f"| `{r['folder']}/{r['file']}` | {r['qty']} | {float(r['grams']):.0f} | {r['time_each']} |")
    L += ['', '## 4. Cut the boards', '',
          'Have the store rip the strips; crosscut at home. Write each board\'s name on its outside face, and mark',
          'the cast face (the melamine face the mix touches). The cleats are cut from 1x2 lumber, not the sheet;',
          'the bridges and struts come out of the sheet\'s offcuts.', '']
    if only is None:
        for k in range(1, len(sheets) + 1):
            L += [f'![Sheet {k}](boards/sheet-{k}.svg)', '']
    L += ['| Board | Qty | Size (mm) | Notes |', '|---|---|---|---|']
    cut = {}
    for b in boards:
        su, sv = b.size()
        key = (b.name, round(su), round(sv))
        if key in cut:
            cut[key][2] += b.qty
        else:
            cut[key] = [b, f"{su:.0f} x {sv:.0f}{'' if b.rect() else ' (profile)'}", b.qty]
    for b, size, qty in cut.values():
        L.append(f"| {b.name} | {qty} | {size} | {(b.stock + ' lumber' + ('; ' if b.note else '')) if b.stock else ''}{b.note} |")
    L += ['', '## 5. Mark and drill', '',
          f'1. Print the drilling templates ({tmpl}) at **actual size** and check the 100 mm square.',
          '2. Tape each board\'s pages onto it: printed edges on the board\'s edges, grid lines lined up.',
          '3. Awl through every crosshair. Pencil the dashed **pour line** on the walls.',
          '4. Drill from the marked face, at the size the color legend gives. Pilot the big ones; the 63.5 mm',
          '   holes are a 2-1/2 in hole saw.', '',
          'The appendix has every board as a drawing and a table, if you would rather measure.', '',
          '| Hole | Drill | For |', '|---|---|---|']
    used = {}
    for b in boards:
        for _, _, d, what in b.holes:
            used.setdefault(round(d, 1), set()).add(what.split(' (')[0])
    for d in sorted(used):
        L.append(f"| {d:g} mm | {DRILLS.get(d, '')} | {', '.join(sorted(used[d]))} |")
    L.append('')
    n = 6
    if foam:
        L += [f'## {n}. Cut the foam', '',
              'Fine saw, hot wire or a long knife. Stack and glue two layers of 2 in foam for the 90 mm cores. Wrap',
              'each piece smooth in packing tape. Cut a snug 12 mm square hole 30 mm deep for each core\'s post and',
              'glue the post in.', '', '| Casting | Piece | Qty | Size and how |', '|---|---|---|---|']
        for r in foam:
            L.append(f"| {r['folder']} | {r['name']} | {r['qty']} | {r['note']} |")
        n += 1
    L += [f'## {n}. Wax', '',
          '- 3-5 coats of paste wax on every face the mix touches, boards and removable printed pieces, then PVA.',
          '  Don\'t wax pieces that stay in (core posts, cast-in parts): scuff and degrease them.',
          '- Glue quarter-round into the floor-to-wall corners that make outside edges; silicone fillets elsewhere.',
          '- Grease every screw, bolt and rod that comes out of the casting.', '',
          f'## {n + 1}. Assemble', '']
    if 'base' in molds_:
        L += ['### Base, rear half (first)', '',
              'Cast upside down, top face on the floor; shown the right way up. New parts in color. Bolt each half\'s '
              'steel grid together first (the build guide, section 1), then it goes in as one piece.', '']
        L += fig('skeleton-base', 'The base grids, both halves')
        for k in range(1, 7):
            L += [f'{k}. ' + STEPS_TEXT[f'step-base-rear-{k}'], ''] + fig(f'step-base-rear-{k}', f'Base rear, step {k}')
        L += ['### Base, front half (against the rear half)', '']
        for k in range(1, 4):
            L += [f'{k}. ' + STEPS_TEXT[f'step-base-front-{k}'], ''] + fig(f'step-base-front-{k}', f'Base front, step {k}')
    if 'upright' in molds_:
        L += ['### Uprights (one mold, cast twice)', '', 'Cast foot down. The two uprights are the same part: cast one, '
              'take the mold apart after the cure, scrape and re-wax it and cast the other. The skeleton: the foot bar, '
              'two columns and the top plate (two flat bars), clamped later by the column tie rods.', '']
        L += fig('skeleton-upright', 'An upright skeleton')
        for k, t in enumerate(UP_TEXT, 1):
            L += [f'{k}. {t}', ''] + fig(f'step-upright-{k}', f'Upright, step {k}')
        L += fig('detail-toe', 'The toe filler holds the front board\'s foot')
    if 'beam' in molds_:
        L += ['### Beam', '', 'Cast front (rail) face down, back open. Bolt the steel together on the bench: the '
              'three studs into the face bar, a pipe spacer on each, the back bar over them and a nut on each.', '']
        L += fig('skeleton-beam', 'The beam\'s steel box')
        for k, t in enumerate(BEAM_TEXT, 1):
            L += [f'{k}. {t}', ''] + fig(f'step-beam-{k}', f'Beam, step {k}')
    L += [f'## {n + 2}. Pour', '',
          f'- Fill to the **pour line**, {fb:.0f} mm below the wall tops (pencilled from the templates, or with the',
          '  printed pour-line gauge clipped over a wall).',
          '- Vibrate each layer until it stops bubbling; check the brackets halfway through.',
          '- Strike the top off with a straight board in the two printed **screed shoes**: they hang it from the wall',
          '  tops with its bottom edge on the pour line.', ''] + fig('detail-pour', 'Pour-line gauge and screed shoes')
    L += [f'## {n + 3}. Take apart', '',
          '1. After the full cure: bridges and saddles off, then corner brackets, then cleats; pull the walls off.',
          '2. Screws, bolts and rods out from outside; lift the casting off the floor.',
          '3. Unbolt and pull the formers and fillers.',
          '4. Scrape and re-wax the boards; keep each mold\'s kit in a box. The kit is reused.', '',
          f'## {n + 4}. If something doesn\'t fit', '',
          '| Problem | Fix |', '|---|---|',
          '| Nut won\'t slide under the hole | Clean the pocket with a nut on a bolt; warm the nut |',
          '| Bracket or saddle loose on the board | Board thinner than set: tape shim, or set `mold_board` and reprint |',
          '| Pin won\'t go in | Run the 1/8 in bit through again; trim the pin tip |',
          '| Foam core moves | Tighten its post bolt; carpet tape under it |',
          '| Printed part won\'t go on or into a steel tube | File the weld seam; sand the part. Several tight: caliper the tube, '
          'put its sizes in `frame_tube` / `post_tube`, re-run and reprint |',
          '| Printed part loose on a tube | A wrap of tape round the part |',
          '| Leak at a corner | Silicone fillet inside before waxing; check the brackets and diagonals |',
          '| Former stuck after curing | Bolts out first, then a dowel and a light tap |', '',
          '## Appendix: hole maps', '',
          'Every board as seen from the face you mark: x from the left edge, y from the bottom edge (for a wall, the',
          'edge on the floor). The templates carry the same holes at full size.', '']
    for mold in molds_:
        if only is None:
            L += [f'### {MOLD_TITLES[mold]}', '']
        for b in boards:
            if b.mold != mold or not b.holes:
                continue
            us = [u for u, _ in b.outline]
            vs = [v for _, v in b.outline]
            u0, u1, v0 = min(us), max(us), min(vs)
            X = (lambda u: u1 - u) if b.view == 'outside' else (lambda u: u - u0)
            L += [f'#### {b.name}' + (f' (x{b.qty})' if b.qty > 1 else ''), '', f'![{b.name}](boards/{board_file(b)})', '',
                  '| # | x | y | Hole | For |', '|---|---|---|---|---|']
            for k, (u, v, d, what) in enumerate(hole_order(b), 1):
                L.append(f'| {k} | {X(u):.0f} | {v - v0:.0f} | {d:g} | {what} |')
            if not b.rect():
                L += ['', 'Outline corners (x, y): ' + ', '.join(f'({X(u):.0f}, {v - v0:.0f})' for u, v in b.outline)]
            L.append('')
    return L


STEPS_TEXT = {
    'step-base-rear-1': 'Floor on three battens. Bolt the cleats down.',
    'step-base-rear-2': 'Walls against the cleats; corner brackets at the top. Diagonals equal within 2 mm, then tighten.',
    'step-base-rear-3': 'Partition between the side walls: two brackets, two struts to the front wall. Beads on its pins.',
    'step-base-rear-4': 'Gutter formers, corner fillers and the draw-rod pocket plugs on. Bevel strips on '
                        'the side and rear walls, their 1-1/2 in face flush with the pour line.',
    'step-base-rear-5': 'The steel grid in, bolted up and upside down: its rail bars and the BK pad screwed to the floor '
                        '(greased M5 and M6), its seats over the dowels, the split end plates against the partition with '
                        'their dowel pins through it. Tape over the holes in the pedestals\' bottom bars. Inserts; leg '
                        'holders, legs set to height, pinch screws tight.',
    'step-base-rear-6': 'Pour the 20 mm skin. Foam cores on it between the steel, bridges into the saddles, each post '
                        'bolted to its bridge. Fill to the pour line, packing the mix up under the bevel strips.',
    'step-base-front-1': 'After the cure: bridges, partition and struts off. Pull the beads, tape the groove, and wax the '
                         'rear half\'s split face, end plates and dowel pins.',
    'step-base-front-2': 'Trough and gutter formers, corner fillers, bevel strips and pocket plugs on; the front grid in, its rail bars and '
                         'BF pad screwed down and its split end plates onto the dowel pins; inserts and legs.',
    'step-base-front-3': 'Skin, cores, bridges, fill (packed under the bevel strips). After the cure, take it apart and '
                         'split the halves with wedges.',
}
UP_TEXT = [
    'Gasket bead pinned on; cleats bolted down.',
    'Side plates against their cleats, back board between them (it leans in, like the front board), two back brackets.',
    'Toe filler bolted down, the front board\'s foot in its lip, two front brackets at the top.',
    'Mold on its four 2x4 blocks. The foot bar on the floor; the two columns on beds of thickened epoxy on it, the top '
    'plate and bridge set on them while it goes off, then lifted away; the toe pocket plug on the foot bar; the two '
    'dowel-hole bolts from underneath.',
    'Fill to the line. Top plate (both bars) back on, hung from the bridge; bridge onto its saddles. Then the two '
    'column tie rods, greased, up from under the floor through the foot bar and the columns into the top plate: they '
    'center the columns while it cures.',
]
BEAM_TEXT = [
    'Cleats bolted down.',
    'Walls against the cleats; four corner brackets.',
    'The steel in, face bar down: greased M5 and M6 screws up through the floor into its tapped holes; the back bar on '
    'its pipe spacers and studs; greased 1/2 in rods through the top wall, the cap bars, the seat bars and the bottom '
    'wall; back-edge filler on the top wall between the uprights; dowels on their stops. Fill to the line.',
]


def _minutes(t):
    return sum(int(v) * {'d': 1440, 'h': 60, 'm': 1, 's': 1 / 60}[u] for v, u in re.findall(r'(\d+)([dhms])', t))


def steel_parts(m):
    """The skeletons' stock parts, identical ones (left and right) grouped: (part, qty, stock, length)."""
    groups = {}
    for pt in m.plates + m.tubes:
        bb = pt.shape.BoundBox
        key = (pt.stock[:-1] if pt.stock[0] == 'flat' else pt.stock, round(pt.shape.Volume),
               tuple(sorted(round(v) for v in (bb.XLength, bb.YLength, bb.ZLength))))
        groups.setdefault(key, []).append(pt)
    out = []
    for key, pts in groups.items():
        pt = pts[0]
        words = []
        for p_ in pts:
            base = re.sub(r'\d+$', '', re.sub(r'(?<=[a-z])[LR](?=[A-Z0-9]|$)', '', p_.name))
            words.append(re.sub(r'(?<=[a-z0-9])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])', ' ', base).split())
        # words every member shares (drops "Front" / "Rear" when the part is in both base halves); identical
        # parts with different jobs are named for both
        tags = {'Base', 'Front', 'Rear'}
        common = [w_ for w_ in words[0] if all(w_ in ws for ws in words)]
        if [w_ for w_ in words[0] if w_ not in tags] == [w_ for w_ in common if w_ not in tags]:
            name = ' '.join(w_ for w_ in common if w_ != 'Base')
        else:
            name = ' / '.join(sorted(set(' '.join(w_ for w_ in ws if w_ not in tags) for ws in words)))
            if all(w_ in ws for ws in words for w_ in ('Front',)):
                name += ' Front'
        name = ' '.join(w_ if (w_.isupper() and len(w_) > 1) else w_.lower() for w_ in name.split())
        name = name.replace('plate lower', 'plate, lower').replace('plate upper', 'plate, upper')
        name = name[0].upper() + name[1:]
        if pt.stock[0] == 'flat':
            _, t, w, ln, _ = pt.stock
            stock = f'Flat bar {sk.inch(t)} x {sk.inch(w)} in'
        else:
            _, w1, w2, wall, ln = pt.stock
            a, b = sorted((w1, w2))
            stock = f'{"Square" if abs(a - b) < 0.1 else "Rectangular"} tube {sk.inch(a)} x {sk.inch(b)} x {sk.inch(wall)} in'
        out.append((pt, len(pts), stock, ln, name))
    return sorted(out, key=lambda r: (r[2], -r[3]))


def write_steel_parts(m):
    """The steel to buy and how to work it: docs/1-sourcing/steel/README.md (a cut list by stock size and a
    list of parts), and docs/src/boards/steel.json for the 1:1 drilling templates (make_templates.py)."""
    out = os.path.join(ROOT, 'docs', '1-sourcing', 'steel')
    os.makedirs(out, exist_ok=True)
    rows = steel_parts(m)
    templates, parts_md, by_stock = [], [], {}
    for pt, qty, stock, ln, name in rows:
        by_stock.setdefault(stock, []).append((ln, qty))
        holes = []
        if pt.stock[0] == 'flat':
            ps = [pp for pp, _ in pt.outline]
            qs = [qq for _, qq in pt.outline]
            p0, q0 = min(ps), min(qs)
            along_p = pt.stock[4] == 'p'
            w = pt.stock[2]
            for p_, q_, d, tap in pt.holes:
                x, y = ((p_ - p0, q_ - q0) if along_p else (q_ - q0, p_ - p0))
                holes.append([round(x, 2), round(y, 2), round(d, 2), tap or '', sk.drill_name(d, tap)])
            faces = [('', w, holes)]
        else:
            faces = {}
            for face, a, c, d, what, both in pt.holes:
                faces.setdefault(face, []).append([round(a, 2), round(c, 2), round(d, 2),
                                                   what + ('' if both else ' (near wall only)'), sk.drill_name(d)])
            i = sk.AXES[pt.axis]
            others = [k for k in range(3) if k != i]
            faces = [(f'{face}-face', (pt.w2 if sk.AXES[face] == others[0] else pt.w1), hs) for face, hs in faces.items()]
        drill_txt = []
        for label, w, hs in faces:
            if not hs:
                continue
            templates.append(dict(name=f'{name}{" (" + label + ")" if label else ""}', mold='steel', qty=qty,
                                  view='steel', note=stock, size=[round(ln, 1), round(w, 1)],
                                  outline=[[0, 0], [round(ln, 1), 0], [round(ln, 1), round(w, 1)], [0, round(w, 1)]],
                                  holes=hs, pour=None))
            n_by = collections.Counter(h[4] for h in hs)
            drill_txt.append(', '.join(f'{n} x {k}' for k, n in n_by.items()))
        parts_md.append(f'| {name} | {stock} | {ln:.0f} mm ({sk.inch(ln)} in) | {qty} | '
                        f'{"; ".join(drill_txt) if drill_txt else "-"} |')
    kg = sum(pt.mass * qty for pt, qty, *_ in rows)
    cut = []
    for stock, items in sorted(by_stock.items()):
        total = sum(ln * q for ln, q in items)
        merged = collections.Counter()
        for ln, q in items:
            merged[round(ln)] += q
        pieces = ', '.join(f'{q} x {ln}' for ln, q in sorted(merged.items(), reverse=True))
        cut.append(f'| {stock} | {pieces} | {total / 304.8:.1f} ft |')
    with open(os.path.join(out, 'README.md'), 'w') as fh:
        fh.write('# Steel for the skeletons\n\nAll stock mild steel (A36 / A500), nothing custom: buy it cut to length '
                 '(Metal Supermarkets, Online Metals, a local steel yard; flat bar and tube also come in 3 and 6 ft '
                 'lengths on Amazon and at hardware stores, and a chop saw or hacksaw does the rest). Drill and tap '
                 'it from the printed 1:1 templates in `steel-templates.pdf` (center-punch through the paper, then '
                 'a drill press).\n\n'
                 f'{len(rows)} different parts, {sum(r[1] for r in rows)} pieces, about {kg:.0f} kg.\n\n'
                 '## Cut list (by stock size)\n\n| Stock | Pieces (qty x length, mm) | Total |\n|---|---|---|\n'
                 + '\n'.join(cut) + '\n\n## Parts\n\n| Part | Stock | Length | Qty | Holes |\n|---|---|---|---|---|\n'
                 + '\n'.join(parts_md) + '\n')
    with open(os.path.join(ROOT, 'docs', 'src', 'boards', 'steel.json'), 'w') as fh:
        json.dump(dict(freeboard=0, board=0, boards=templates), fh, indent=0)
    old = os.path.join(ROOT, 'docs', '1-sourcing', 'laser')
    if os.path.isdir(old):
        import shutil
        shutil.rmtree(old)


def main():
    m = build()
    hits = collisions(m)
    text = report(m, hits)
    print(text)
    with open(os.path.join(ROOT, 'docs', '5-design', 'report.txt'), 'w') as fh:
        fh.write(text + '\n')
    export_prints(m)
    write_steel_parts(m)
    write_mold_guide(m)
    if not App.GuiUp:
        return  # a headless save would drop the colors from DIYCNC.FCStd
    doc = make_document(m, os.path.join(HERE, 'DIYCNC.FCStd'))
    export_step(doc, os.path.join(HERE, 'DIYCNC.step'))
    if os.environ.get('CNC_SNAPSHOTS'):
        img = os.path.join(ROOT, 'renders')
        os.makedirs(img, exist_ok=True)
        for dp, _, fn in os.walk(img):
            if os.path.basename(dp) == 'mold':
                continue                  # model/mold_figures.py writes these
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
