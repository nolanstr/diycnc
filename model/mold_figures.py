"""Illustrations for the mold guide: assembly steps for each mold, cut-away details of the joints and
fixings, and a gallery of the printed pieces, with labeled callouts. Writes renders/mold/.

    python model/mold_figures.py

The base is cast upside down; its figures are turned over so the mold is shown the right way up
(floor at the bottom), and the beam's are turned so its open back is up.
"""

import math
import os
import re

from cadrust.freecad import Part, Vector
from cadrust.view import Camera, Item, render
from PIL import Image, ImageDraw, ImageFont

try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:
    HERE = os.path.join(os.getcwd(), 'model')
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, 'renders', 'mold')
FONT = '/System/Library/Fonts/HelveticaNeue.ttc'
VIEW = (400, 300)             # the figure's view; drawn at SCALE x, labeled, then shrunk to 2/3
SCALE = 3
INK, LEADER, BOX = (29, 36, 34), (90, 102, 98), (255, 255, 255)

src = open(os.path.join(HERE, 'build_cnc.py')).read()
src = src[:src.rstrip().rfind('\nmain()')]
NS = {'__file__': os.path.join(HERE, 'build_cnc.py'), '__name__': 'build_cnc'}
exec(compile(src, 'build_cnc.py', 'exec'), NS)
P, parts, molds = NS['P'], NS['parts'], NS['molds']
NS['LOOKS'].update({'hw': ((0.55, 0.57, 0.60), 0.7, 0), 'pour': ((0.30, 0.60, 0.95), 0.2, 60),
                    'ghost': ((0.80, 0.81, 0.82), 0.05, 0), 'melamine_s': ((0.93, 0.93, 0.90), 0.3, 25),
                    'board_new': ((0.97, 0.85, 0.58), 0.2, 30), 'board_old': ((0.91, 0.91, 0.89), 0.2, 72),
                    'mix': ((0.30, 0.31, 0.33), 0.1, 0)})
M = NS['build']()
KIT = M.mold_kit
G = NS['frame_layout'](M.dims)
PARTS = {p['name']: p for p in M.parts}
T = P['mold_board']


# ------------------------------------------------------------------------------------------
# Frames: show each mold the right way up
# ------------------------------------------------------------------------------------------
def flip_base(s):
    s = s.copy()
    s.rotate(Vector(0, 0, 0), Vector(1, 0, 0), 180)
    return s


def turn_beam(s):
    s = s.copy()
    s.rotate(Vector(0, 0, 0), Vector(1, 0, 0), 90)
    return s


def pt(fn, p):
    return fn(Part.Vertex(p)).Point


IDENT = lambda s: s.copy()


# ------------------------------------------------------------------------------------------
# Hardware models
# ------------------------------------------------------------------------------------------
def hexprism(c, axis, af, h):
    axis = molds.unit(axis)
    s_ = molds.perp(axis)
    return molds.hexagon(c, axis, s_, axis.cross(s_), af, h)


def bolt(head_at, axis, length, d=4.0):
    """Socket-head bolt: head outside head_at, shank along axis."""
    axis = molds.unit(axis)
    head = Part.makeCylinder(d * 0.85, d, head_at - axis * d, axis).cut(hexprism(head_at - axis * (d + 0.1), axis, d * 0.75, d * 0.6))
    washer = Part.makeCylinder(d * 1.1, 0.8, head_at - axis * 0.8, axis).cut(Part.makeCylinder(d / 2 + 0.2, 2, head_at - axis, axis))
    return head.fuse([washer, Part.makeCylinder(d / 2, length, head_at - axis * 0.8, axis)])


def nut(c, axis, af=7.0, t=3.2, d=4.0):
    axis = molds.unit(axis)
    return hexprism(c - axis * (t / 2), axis, af, t).cut(Part.makeCylinder(d / 2, t + 2, c - axis * (t / 2 + 1), axis))


# ------------------------------------------------------------------------------------------
# Scene and camera
# ------------------------------------------------------------------------------------------
class Scene:
    def __init__(self):
        self.items = []
        self.cam = None

    def clear(self):
        self.items = []

    def add(self, shape, look, transp=None, lines=True):
        if shape is None or shape.isNull():
            return None
        rgb, shine, tr = NS['LOOKS'][look]
        tr = tr if transp is None else transp
        edges = (0.12, 0.12, 0.12) if lines and look not in NS['SHADED'] else None
        it = Item(shape, color=rgb, opacity=1.0 - tr / 100.0, shine=shine, edges=edges, edge_width=2.5)
        self.items.append(it)
        return it

    def camera(self, d, up=Vector(0, 0, 1), zoom=1.0):
        self.cam = Camera.look(tuple(d), tuple(up))

    def shoot(self, name, labels=(), arrows=()):
        """labels: [(point, text)]; arrows: [(from point, to point)] drawn in 2D."""
        W, H = VIEW[0] * SCALE, VIEW[1] * SCALE
        path = os.path.join(OUT, name + '.png')
        os.makedirs(OUT, exist_ok=True)
        cam = self.cam
        cam.fit_diagonal(NS['union_box'](it.bbox() for it in self.items), margin=1.0)   # the whole scene, as fitAll
        im = render(self.items, cam, 2 * W, 2 * H).resize((W, H), Image.LANCZOS)
        dr = ImageDraw.Draw(im)
        font = ImageFont.truetype(FONT, 62)
        proj = lambda p: tuple(c / 2 for c in cam.project(p))
        for a, b in arrows:
            (x0, y0), (x1, y1) = proj(a), proj(b)
            dr.line([(x0, y0), (x1, y1)], fill=(200, 90, 20), width=7)
            ang = math.atan2(y1 - y0, x1 - x0)
            head = [(x1, y1), (x1 - 34 * math.cos(ang - 0.45), y1 - 34 * math.sin(ang - 0.45)),
                    (x1 - 34 * math.cos(ang + 0.45), y1 - 34 * math.sin(ang + 0.45))]
            dr.polygon(head, fill=(200, 90, 20))
        anchors = [(proj(p), t) for p, t in labels]
        boxes = []
        cx = sum(a[0] for a, _ in anchors) / max(len(anchors), 1) if anchors else W / 2
        cy = sum(a[1] for a, _ in anchors) / max(len(anchors), 1) if anchors else H / 2
        for (ax, ay), text in anchors:
            tw, th = dr.textbbox((0, 0), text, font=font)[2:]
            base = math.atan2(ay - cy, ax - cx) if (ax, ay) != (cx, cy) else -math.pi / 2
            best = None
            for k in range(16):
                for rr in (190, 290, 400):
                    ang = base + (k // 2) * (math.pi / 8) * (1 if k % 2 else -1)
                    lx, ly = ax + rr * math.cos(ang), ay + rr * math.sin(ang)
                    bx0 = lx - tw / 2 - 16 if abs(math.cos(ang)) < 0.4 else (lx if math.cos(ang) > 0 else lx - tw - 32)
                    by0 = ly - th / 2 - 10
                    box = (bx0, by0, bx0 + tw + 32, by0 + th + 20)
                    if box[0] < 10 or box[1] < 10 or box[2] > W - 10 or box[3] > H - 10:
                        continue
                    if any(not (box[2] < b[0] or box[0] > b[2] or box[3] < b[1] or box[1] > b[3]) for b in boxes):
                        continue
                    best = (box, (lx, ly))
                    break
                if best:
                    break
            if not best:
                box = (ax + 20, ay - th - 30, ax + 52 + tw, ay - 10)
                best = (box, (ax + 20, ay - 20))
            box, (lx, ly) = best
            boxes.append(box)
            ex = min(max(ax, box[0]), box[2])
            ey = min(max(ay, box[1]), box[3])
            dr.line([(ax, ay), (ex, ey)], fill=LEADER, width=5)
            dr.ellipse([ax - 11, ay - 11, ax + 11, ay + 11], fill=(200, 90, 20), outline=(255, 255, 255), width=4)
            dr.rounded_rectangle(box, radius=14, fill=BOX, outline=LEADER, width=4)
            dr.text((box[0] + 16, box[1] + 6), text, fill=INK, font=font)
        im = im.resize((W * 2 // 3, H * 2 // 3), Image.LANCZOS)
        im.save(path)


# ------------------------------------------------------------------------------------------
# Lookups
# ------------------------------------------------------------------------------------------
def boards(group, names=None, crop=None):
    out = []
    for b in KIT.boards:
        if group in b.show and (names is None or any(b.name.startswith(n) for n in names)):
            s = b.solid()
            out.append(s.common(crop) if crop is not None else s)
    return out


def pieces(group, names=None, kinds=None, crop=None):
    out = []
    for r in M.molds:
        if names is not None and not any(r['name'].startswith(n) for n in names):
            continue
        if kinds is not None and r['kind'] not in kinds:
            continue
        for s, sh in r['placed']:
            if group in sh:
                if crop is not None:
                    if not s.BoundBox.intersect(crop.BoundBox):
                        continue
                    s = s.common(crop)
                out.append((r['kind'], s))
    return out


def steel(container, crop=None, skip=('Casting', 'Gasket', 'BeamBolt')):
    out = []
    for p in M.parts:
        if p['container'] != container or p['name'] not in M.structure or any(k in p['name'] for k in skip):
            continue
        s = p['shape'] if crop is None else p['shape'].common(crop)
        out.append((p['look'], s))
    return out


def add_all(sc, fn, items, look=None, transp=None):
    for it in items:
        if isinstance(it, tuple):
            kind, s = it
            lk = look or ('foam' if kind == 'foam' else 'printed' if kind in ('kit', 'plug', 'filler', 'former', 'core')
                          else kind if kind in NS['LOOKS'] else 'printed')
        else:
            lk, s = look or 'melamine_s', it
        sc.add(fn(s), lk, transp)


# ------------------------------------------------------------------------------------------
# Figures
# ------------------------------------------------------------------------------------------
def fig_bayonet(sc):
    """How a piece bolts to its board, exploded and cut through the bolt: the nut goes up into the pocket
    in the face that sits on the board, slides over under the hole, and the bolt comes up through the board."""
    sc.clear()
    hw = molds.HW['M4']
    reach = hw['af'] + 3.0
    board = parts.box(-30, 38, -14, 14, -T, 0)
    piece = parts.box(-22, 30, -12, 12, 0, 16)
    p, n, s_ = Vector(0, 0, 0), Vector(0, 0, -1), Vector(1, 0, 0)
    piece = piece.cut(molds.nut_trap(p, n, s_, 'M4'))
    board = board.cut(Part.makeCylinder(2.25, T + 2, Vector(0, 0, -T - 1)))
    lift = Vector(0, 0, 22)
    keep = parts.box(-100, 100, 0, 100, -100, 100)            # cut away the near half
    c_nut = Vector(0, 0, hw['skin'] + hw['t'] / 2 + 0.15)
    sc.add(board.common(keep), 'melamine_s', 10)
    sc.add(piece.common(keep).translated(lift), 'printed')
    entry = Vector(reach, 0, 0)
    nut_below = entry + Vector(0, 0, 9)
    sc.add(nut(nut_below, Vector(0, 0, 1)).common(keep), 'hw')
    sc.add(bolt(Vector(0, 0, -T), Vector(0, 0, 1), 30.0).common(keep), 'hw')
    sc.camera(Vector(-0.12, 1.0, -0.12))
    sc.shoot('fixing-nut', labels=[
        (Vector(-14, 0, 12) + lift, 'Printed piece (cut through the bolt)'),
        (Vector(30, 0, -T / 2), 'Melamine board (cut)'),
        (entry + lift + Vector(0, 0, 1), '1. Nut goes up into this pocket'),
        (c_nut + lift + Vector(-2, 0, 0), '2. ...slides over, under the hole'),
        (Vector(0, 0, -T - 3), '3. M4 bolt + washer, up through the board')],
        arrows=[(nut_below + Vector(0, 0, 2), entry + lift + Vector(0, 0, hw['skin'] + 1)),
                (entry + lift + c_nut + Vector(-1, 0, 0), c_nut + lift + Vector(3.5, 0, 0)),
                (Vector(0, 0, -T - 10), Vector(0, 0, -T - 2))])


def fig_pins(sc):
    """A gasket-groove bead and its pins over the floor board."""
    sc.clear()
    r = next(r for r in M.molds if r['name'] == 'foot-gasket-groove')
    part_ = r['shape'][0]
    bb = part_.BoundBox
    crop = parts.box(bb.XMin - 30, bb.XMax + 30, bb.YMin - 20, bb.YMin + 140, bb.ZMin - 30, bb.ZMax + 10)
    for s in boards('upright', ['Upright floor'], crop):
        sc.add(s, 'melamine_s', 10)
    lift = Vector(0, 0, 18)
    sc.add(part_.common(crop).translated(lift), 'printed')
    sc.camera(Vector(-0.6, 0.55, -0.6), zoom=1.0)
    pins_at = [Vector(e.Curve.Center.x, e.Curve.Center.y, bb.ZMin) for e in part_.Edges
               if isinstance(e.Curve, Part.Circle) and abs(e.Curve.Radius - molds.PIN_D / 2) < 0.05
               and e.Curve.Center.z < bb.ZMin + 1 and crop.isInside(e.Curve.Center, 1, True)]
    lab = [(Vector(bb.XMin, bb.YMin + 60, bb.ZMax) + lift, 'Gasket-groove bead'),
           (Vector(bb.XMax + 20, bb.YMin + 100, bb.ZMin - T / 2), 'Floor board')]
    arr = []
    if pins_at:
        q = pins_at[0]
        lab.append((q + lift - Vector(0, 0, 5), '3 mm pins'))
        lab.append((q, '1/8 in holes'))
        arr = [(q + lift - Vector(0, 0, 7), q + Vector(0, 0, 1))]
    sc.shoot('fixing-pins', labels=lab, arrows=arr)


def fig_peg(sc):
    """Two parts of a former cut for the bed: peg on one, socket in the other."""
    sc.clear()
    r = next(r for r in M.molds if r['folder'] == 'base-front' and r['name'] == 'trough')
    a, b = r['shape'][1], r['shape'][2]
    sc.add(flip_base(a), 'printed')
    sc.add(flip_base(b).translated(Vector(28, 0, 0)), 'printed')
    sc.camera(Vector(-0.45, 0.75, -0.5))
    pa = flip_base(a)
    peg = [f for f in pa.Faces if isinstance(f.Surface, Part.Cylinder) and abs(f.Surface.Radius - molds.PEG_D / 2) < 0.05]
    lab = [(pa.BoundBox.Center + Vector(0, 0, 6), 'Trough former, part 2'),
           (flip_base(b).BoundBox.Center + Vector(28, 0, 6), 'Part 3')]
    if peg:
        lab.append((peg[0].CenterOfMass, 'Peg into the next part'))
    sc.shoot('fixing-peg', labels=lab, arrows=[(flip_base(b).BoundBox.Center + Vector(10, 0, 0),
                                               flip_base(b).BoundBox.Center + Vector(-14, 0, 0))])


def fig_corner(sc):
    """A corner of the base mold, the right way up: walls on cleats, corner bracket, leg holder,
    saddle and bridge, corner filler, and the pour line."""
    sc.clear()
    half, y1 = G['base_half'], G['base_y1']
    crop = parts.box(150, half + T + 60, 220, y1 + T + 60, -140, G['base_top'] + T + 1)
    for s in boards('base-rear', None, crop):
        sc.add(flip_base(s), 'melamine', 55)
    add_all(sc, flip_base, pieces('base-rear', crop=crop))
    for look, s in steel('FrameBaseRear', crop):
        if s.Volume > 1:
            sc.add(flip_base(s), look)
    pour = parts.box(150, half, 220, y1, -0.6, 0)
    sc.add(flip_base(pour), 'pour', 70)
    sc.camera(Vector(-0.55, 0.55, -0.62))
    lx, ly = half - P['leg_inset'][0], G['legs'][2][1]
    lab = [(pt(flip_base, Vector(half + T / 2, 300, 40)), 'Side wall'),
           (pt(flip_base, Vector(200, y1 + T / 2, 40)), 'Rear wall'),
           (pt(flip_base, Vector(half + T + 20, 250, G['base_top'] - T / 2)), 'Cleat, bolted down'),
           (pt(flip_base, Vector(half + T + 5, y1 + T + 5, -12)), 'Corner bracket'),
           (pt(flip_base, Vector(lx - 22, ly, -19)), 'Leg holder + pinch screw'),
           (pt(flip_base, Vector(lx, ly, -100)), 'Leg'),
           (pt(flip_base, Vector(half + 5, 280, -40)), 'Saddle + bridge'),
           (pt(flip_base, Vector(165, 235, -0.3)), 'Pour line: 25 mm below the wall tops'),
           (pt(flip_base, Vector(half - 15, y1 - 15, 60)), 'Corner filler'),
           (pt(flip_base, Vector(half - 10, y1 - 100, 15)), 'Bevel strip (or a ripped 2x3)')]
    sc.shoot('detail-corner', labels=lab)


def fig_core(sc):
    """A foam pocket core hanging from a bridge by its printed post (section through the post)."""
    sc.clear()
    r = next(r for r in M.molds if r['kind'] == 'foam' and r['name'] == 'foot-b-R')
    post = next(r_ for r_ in M.molds if r_['name'] == 'foot-b-R-post')
    blk = r['placed'][0][0]
    pst = post['placed'][0][0]
    bb = blk.BoundBox
    yb = 100.0
    crop = parts.box(bb.XMin - 40, G['base_half'] + T + 40, bb.YMin - 30, bb.YMax + 20, -120, G['base_top'] + T)
    for s in boards('base-rear', ['Base bridge y=100', 'Base side wall, right', 'Base floor'], crop):
        sc.add(flip_base(s), 'melamine', 55)
    sc.add(flip_base(blk), 'foam')
    sc.add(flip_base(pst), 'printed')
    for kind, s in pieces('base-rear', ['saddle'], crop=crop):
        sc.add(flip_base(s), 'printed')
    pour = parts.box(bb.XMin - 40, G['base_half'], bb.YMin - 30, bb.YMax + 20, -0.6, 0)
    sc.add(flip_base(pour), 'pour', 70)
    pc = pst.BoundBox.Center
    sc.camera(Vector(-0.45, 0.7, -0.55))
    sc.shoot('detail-core', labels=[
        (pt(flip_base, Vector(bb.Center.x, bb.Center.y, 60)), 'Foam core (taped XPS)'),
        (pt(flip_base, Vector(pc.x, pc.y, -8)), 'Printed post, glued in'),
        (pt(flip_base, Vector(bb.XMax + 30, yb, -70)), 'Bridge (board on edge)'),
        (pt(flip_base, Vector(pc.x, yb - T / 2, -43)), 'M4 bolt into the post\'s nut'),
        (pt(flip_base, Vector(G['base_half'] + 5, yb, -32)), 'Saddle on the wall top'),
        (pt(flip_base, Vector(bb.XMin - 30, bb.YMax + 10, 0)), 'Pour line')])


def fig_skeletons(sc):
    """Each steel skeleton on its own, labeled: what the builder slots together before it goes in the mold."""
    skip = ('Casting', 'Gasket', 'BeamBolt', 'TieRod', 'Nut', 'Dowel', 'Insert', 'Anchor', 'DrawRod', 'SplitPin',
            'Plug', 'Leg', 'Ring', 'Drain', 'CrossRod')
    for name, conts, cam in (('skeleton-base', ('FrameBaseFront', 'FrameBaseRear'), Vector(-0.55, -0.7, 0.55)),
                             ('skeleton-upright', ('FrameUprightL',), Vector(0.8, -0.5, 0.35)),
                             ('skeleton-beam', ('FrameBeam',), Vector(-0.5, -0.75, 0.45))):
        sc.clear()
        labels, seen = [], set()
        for p in M.parts:
            if p['container'] not in conts or p['name'] not in M.structure or any(k in p['name'] for k in skip):
                continue
            sc.add(p['shape'], p['look'])
            lab = nice(p['name'])
            if lab not in seen:
                seen.add(lab)
                on = p['shape'].distToShape(Part.Vertex(p['shape'].BoundBox.Center))[1][0][0]   # a point on the part
                labels.append((on, lab))
        sc.camera(cam)
        sc.shoot(name, labels=labels)


def fig_toe(sc):
    """Upright: the toe filler and the front board's foot in its lip."""
    sc.clear()
    x0, x1 = -G['outer'], -G['inner']
    crop = parts.box(x0 - T - 50, x1 + T + 50, G['up_front'] - 90, G['up_front'] + 80, G['base_top'] - T - 1, G['base_top'] + 110)
    for s in boards('upright', ['Upright floor', 'Upright front board', 'Upright cleat'], crop):
        sc.add(s, 'melamine', 40)
    for s in boards('upright', ['Upright side plate, inner'], crop):
        sc.add(s, 'melamine', 75)
    add_all(sc, IDENT, pieces('upright', ['toe-filler', 'front-bracket', 'toe-plug'], crop=crop))
    sc.camera(Vector(0.75, 0.55, -0.4))
    tf = next(r for r in M.molds if r['name'] == 'toe-filler')['placed'][0][0].BoundBox
    sc.shoot('detail-toe', labels=[
        (Vector(tf.Center.x, tf.YMin + 15, tf.ZMin + 15), 'Toe filler, bolted to the floor'),
        (Vector(tf.Center.x, tf.YMin + 8, tf.ZMax - 6), 'Lip holds the board\'s foot'),
        (Vector(tf.Center.x, tf.YMax + 20, tf.ZMax + 50), 'Front board (sloped)')])


# ------------------------------------------------------------------------------------------
# Assembly steps
# ------------------------------------------------------------------------------------------
NICE = {'corner-L': 'Corner filler', 'corner-R': 'Corner filler', 'back-edge': 'Back-edge filler',
        'saddle-flat': 'Saddle', 'bar-hanger': 'Bar hanger', 'split-gasket-groove': 'Gasket-groove bead',
        'foot-gasket-groove': 'Gasket-groove bead', 'motor-relief': 'Motor-relief former', 'gutter': 'Gutter former',
        'trough': 'Trough former', 'toe-plug': 'Toe pocket plug', 'draw-pocket': 'Draw-rod pocket plug',
        'BaseRearTubePlug': 'Tube end plug (printed)', 'BaseFrontTubePlug': 'Tube end plug (printed)',
        'BaseRearSpigotSleeve': 'Spigot sleeve (printed)', 'BaseFrontSpigotSleeve': 'Spigot sleeve (printed)',
        'BaseRearTube': 'Rail tube', 'BaseFrontTube': 'Rail tube', 'BaseSpigot': 'Spigot', 'Leg': 'Leg',
        'DrawRodCoupler': 'Draw-rod coupler', 'TieBar': 'Anchor bar', 'RodSleeve': 'Tie-rod sleeve (printed)',
        'DrawRod': 'Draw rod',
        'Anchor': 'Cast-in insert', 'Insert': 'Cast-in insert', 'TopPlate': 'Top plate',
        'UprightFoot': 'Foot bar', 'UprightColumn': 'Column (2x2 tube)',
        'ColumnRing': 'Column ring (printed)', 'BaseRailBar': 'Rail bar (tapped)', 'BasePad': 'Support pad (tapped)',
        'BaseSeat': 'Seat bar', 'BasePedestalBar': 'Bottom bar', 'BasePedestalColumn': 'Pedestal column',
        'BaseGirderEnd': 'End plate', 'BaseGirder': 'Girder (2x3 tube)', 'BaseCross': 'Cross tube', 'CrossRod': 'Cross rod',
        'SplitPin': 'Dowel pin', 'BeamFacePlate': 'Face bar (tapped)', 'BeamSeat': 'Seat bar', 'BeamCap': 'Cap bar',
        'BeamBackPlate': 'Back bar', 'BeamSpacer': 'Pipe spacer', 'BeamTie': 'Stud',
        'BeamTube': 'Beam tube', 'BeamSupportPad': 'Support pad', 'DrainOutlet': 'Drain nipple', 'Dowel': 'Dowel'}


def nice(name):
    for k, v in NICE.items():
        if name.startswith(k):
            return v
    if ' ' not in name and any(c.isupper() for c in name[1:]):
        name = re.sub(r'(?<!^)(?=[A-Z])', ' ', name).replace(' L ', ' ').rstrip(' LR123456789')
    for w in ('Base ', 'Upright ', 'Beam '):
        if name.startswith(w):
            name = name[len(w):]
    name = name.split(' y=')[0].split(',')[0]
    return name[0].upper() + name[1:].replace('-', ' ')


def anchor(shape):
    c = shape.BoundBox.Center
    try:
        return shape.distToShape(Part.Vertex(c))[1][0][0]
    except Exception:
        return c


def steps(sc, name, fn, d, stages, up=Vector(0, 0, 1), max_labels=8):
    """stages: [(title, [(look, shape, label)])]: each image shows everything up to that stage, the new
    parts in color (labeled) and the earlier ones paler."""
    shown = []
    for k, (title, items) in enumerate(stages, 1):
        sc.clear()
        for old in shown:
            for look, s_, _ in old:
                sc.add(fn(s_), 'board_old' if look == 'melamine' else 'pour' if look == 'pour' else 'ghost')
        labels, seen = [], set()
        for look, s_, _ in items:
            sc.add(fn(s_), 'board_new' if look == 'melamine' else look)
        rank = lambda it: 0 if it[0] in ('printed', 'foam') else 1 if it[0] == 'melamine' else 2
        for look, s_, lab in sorted(items, key=rank):
            if lab and lab not in seen and len(labels) < max_labels:
                seen.add(lab)
                labels.append((pt(fn, anchor(s_)), lab))
        shown.append(items)
        sc.camera(d, up)
        sc.shoot(f'{name}-{k}', labels=labels)


def B(group, names):
    return [('melamine', b.solid(holes=False), nice(b.name)) for b in KIT.boards
            if group in b.show and any(b.name.startswith(n) for n in names)]


def K(group, names=None, kinds=None):
    out = []
    for r in M.molds:
        if (names is not None and not any(r['name'].startswith(n) for n in names)) or (kinds and r['kind'] not in kinds):
            continue
        for s_, sh in r['placed']:
            if group in sh:
                if r['kind'] == 'foam':
                    lab = 'Foam socket core' if r['name'] == 'socket' else 'Foam core'
                elif r['name'].endswith('-post'):
                    lab = 'Core post'
                else:
                    lab = nice(r['name'])
                out.append(('foam' if r['kind'] == 'foam' else 'printed', s_, lab))
    return out


def S(container, skip=('Casting', 'Gasket', 'BeamBolt'), keep=None):
    return [(p['look'], p['shape'], nice(p['name'])) for p in M.parts
            if p['container'] == container and p['name'] in M.structure and not any(k in p['name'] for k in skip)
            and (keep is None or keep(p))]


def base_rods(front):
    """The greased 5/8 in rods that form the tie-rod holes through a base half (mold up is -z)."""
    return [('hw', Part.makeCylinder(P['up_rod_hole'] / 2, G['base_top'] + T + 40, Vector(sx * rx, ry, -15)),
             '5/8 in rod (forms a tie-rod hole)')
            for sx in (-1, 1) for rx, ry, _ in G['tie_rods'] if (ry < G['split']) == front]


def draw_rods(front):
    """The greased 5/8 in rods that form the draw-rod holes (along y)."""
    y0, y1 = (G['base_y0'] - T - 20, G['split']) if front else (G['split'] - T - 20, G['base_y1'] + T + 20)
    return [('hw', parts.cyl_v(P['up_rod_hole'] / 2, y0, y1, sx * G['draw_rod_x'], G['draw_z']), '5/8 in rod (forms a draw-rod hole)')
            for sx in (-1, 1)]


def base_steps(sc):
    rear, front = 'base-rear', 'base-front'
    walls = ['Base front wall', 'Base rear wall', 'Base side wall']
    stages = [
        ('floor', B(rear, ['Base floor', 'Base cleat'])),
        ('walls', B(rear, walls) + K(rear, ['corner-bracket'])),
        ('partition', B(rear, ['Base partition']) + K(rear, ['partition-bracket', 'split-gasket'])),
        ('pieces', K(rear, ['gutter', 'motor-relief', 'corner-L', 'corner-R', 'draw-pocket'])),
        ('steel', S('FrameBaseRear') + K(rear, ['leg-holder'])),
        ('cores', K(rear, None, kinds=('foam', 'core')) + K(rear, ['saddle'])
         + B(rear, ['Base bridge', 'Base leg bridge']) + [pour_plane('base')]),
    ]
    steps(sc, 'step-base-rear', flip_base, Vector(-0.5, -0.62, -0.6), stages)
    cast = [('granite', PARTS['BaseRearCasting']['shape'], 'Rear half, cured and waxed')]
    fstages = [
        ('rear cast', B(front, ['Base floor', 'Base cleat'] + walls) + K(front, ['corner-bracket']) + cast),
        ('front pieces', K(front, ['gutter', 'trough', 'corner-L', 'corner-R', 'draw-pocket']) + S('FrameBaseFront')
         + K(front, ['leg-holder'])),
        ('cores', K(front, None, kinds=('foam', 'core')) + K(front, ['saddle'])
         + B(front, ['Base bridge', 'Base leg bridge']) + [pour_plane('base')]),
    ]
    steps(sc, 'step-base-front', flip_base, Vector(0.5, 0.62, -0.6), fstages)


def upright_steps(sc):
    u = 'upright'
    post_bot = G['base_top'] - T - 20.0              # rods stand 20 mm out under the floor
    rods = [('hw', Part.makeCylinder(P['tie_rod_d'] / 2, G['beam_bot'] + P['mold_freeboard'] + 30 - post_bot,
                                     Vector(-rx, ry, post_bot)), 'Column tie rod, from below')
            for rx, ry, pb in G['tie_rods'] if pb >= G['pocket_bot'] - 1]
    st = S('FrameUprightL', skip=('Casting', 'Gasket', 'TieRod', 'Nut', 'TopPlate'))
    plate = PARTS['TopPlateLLower']['shape'].fuse(PARTS['TopPlateLUpper']['shape'])
    stages = [
        ('floor', B(u, ['Upright floor', 'Upright cleat']) + K(u, ['foot-gasket'])),
        ('sides', B(u, ['Upright side plate', 'Upright back board']) + K(u, ['back-bracket'])),
        ('front', B(u, ['Upright front board']) + K(u, ['toe-filler', 'front-bracket'])),
        ('steel', st + K(u, ['toe-plug']) + [pour_plane('upright')]),
        ('top', K(u, ['plate-spacer', 'saddle-flat']) + B(u, ['Upright bridge']) + [('steeltube', plate, 'Top plate')]
         + rods),
    ]
    steps(sc, 'step-upright', IDENT, Vector(0.8, 0.55, -0.45), stages)


def beam_steps(sc):
    b = 'beam'
    rods = [('hw', Part.makeCylinder(P['beam_bolt_hole'] / 2, G['beam_top'] - G['beam_bot'] + 2 * T + 20,
                                     Vector(sx * bx, by, G['beam_bot'] - T - 10)), '1/2 in rod (forms a bolt hole)')
            for sx in (-1, 1) for bx in G['bolt_xs'] for by in G['bolt_ys']]
    on_floor = lambda p: p['name'].startswith('BeamFacePlate')
    stages = [
        ('floor', B(b, ['Beam floor', 'Beam cleat']) + S('FrameBeam', keep=on_floor)),
        ('walls', B(b, ['Beam top wall', 'Beam bottom wall', 'Beam end wall']) + K(b, ['corner-bracket'])),
        ('box', S('FrameBeam', keep=lambda p: not on_floor(p)) + K(b, ['back-edge', 'dowel-stop']) + rods
         + [pour_plane('beam')]),
    ]
    steps(sc, 'step-beam', turn_beam, Vector(-0.45, -0.6, -0.65), stages)


# ------------------------------------------------------------------------------------------
# Exploded views and the pour line
# ------------------------------------------------------------------------------------------
def pour_plane(mold):
    if mold == 'base':
        return ('pour', parts.box(-G['base_half'], G['base_half'], G['base_y0'], G['base_y1'], -0.8, 0), 'Pour line: fill to here')
    if mold == 'upright':
        return ('pour', parts.box(-G['outer'], -G['inner'], G['up_top_front'], G['up_y1'], G['beam_bot'], G['beam_bot'] + 0.8),
                'Pour line: fill to here')
    by1 = G['beam_face'] + P['beam_d']
    return ('pour', parts.box(-G['outer'], G['outer'], by1, by1 + 0.8, G['beam_bot'], G['beam_top']), 'Pour line: fill to here')


def exploded(sc, name, fn, items, d, max_labels=13):
    """items: [(look, shape, label, displacement)]: each part pulled out along its way in."""
    sc.clear()
    labels, seen = [], set()
    for look, s_, lab, v in items:
        moved = s_.translated(v)
        sc.add(fn(moved), {'melamine': 'board_new'}.get(look, look))
        if lab and lab not in seen and len(labels) < max_labels:
            seen.add(lab)
            labels.append((pt(fn, anchor(moved)), lab))
    sc.camera(d)
    sc.shoot(name, labels=labels)


def _out(shape, c, dist, axes=(0, 1)):
    """Push a part away from c along its dominant horizontal axis (both axes for corner parts)."""
    p = shape.BoundBox.Center - c
    comp = [p.x, p.y, p.z]
    v = Vector()
    if len(axes) == 1 or True:
        big = sorted(axes, key=lambda a: -abs(comp[a]))
        for a in (big if len(axes) > 1 and abs(comp[big[1]]) > 0.6 * abs(comp[big[0]]) else big[:1]):
            e = [0, 0, 0]
            e[a] = math.copysign(dist, comp[a])
            v += Vector(*e)
    return v


def base_exploded(sc):
    g = 'base-rear'
    up = Vector(0, 0, -1)
    c = Vector(0, (G['split'] + G['base_y1']) / 2, 55)
    it = []
    for b in KIT.boards:
        if g not in b.show or b.name.startswith(('Base bridge', 'Base leg bridge', 'Base partition strut')):
            continue
        s_ = b.solid(holes=False)
        if b.name.startswith('Base floor'):
            v = Vector()
        elif b.name.startswith('Base cleat'):
            v = _out(s_, c, 70)
        else:
            v = b.N * 170
        it.append(('melamine', s_, nice(b.name), v))
    for r in M.molds:
        for s_, sh in r['placed']:
            if g not in sh:
                continue
            n, k = r['name'], r['kind']
            if n in ('corner-bracket',):
                v = _out(s_, c, 250, (0, 1)) + up * 60
            elif n == 'partition-bracket':
                v = Vector(0, -1, 0) * 170 + up * 60
            elif n == 'split-gasket-groove':
                v = Vector(0, -1, 0) * 130
            elif n == 'leg-holder':
                v = up * 330 + _out(s_, c, 60, (0, 1))
            elif n == 'saddle':
                v = up * 470 + _out(s_, c, 170, (0,))
            elif k == 'foam' or n.endswith('-post'):
                v = up * (180 if n == 'socket' else 250)
            else:
                v = up * 60
            it.append(('foam' if k == 'foam' else 'printed', s_, 'Foam core' if k == 'foam' and n != 'socket' else
                       'Foam socket core' if k == 'foam' else 'Core post' if n.endswith('-post') else nice(n), v))
    for look, s_, lab in S('FrameBaseRear', skip=('Casting', 'Gasket', 'Dowel', 'Insert', 'DrawRod', 'SplitPin')):
        it.append((look, s_, lab, up * (400 if lab == 'Leg' else 120)))
    for b in KIT.boards:
        if g in b.show and b.name.startswith(('Base bridge', 'Base leg bridge')):
            it.append(('melamine', b.solid(holes=False), 'Bridge', up * 470))
    exploded(sc, 'exploded-base', flip_base, it, Vector(-0.5, -0.62, -0.6))


def upright_exploded(sc):
    u = 'upright'
    c = Vector(-(G['outer'] + G['inner']) / 2, (G['up_front'] + G['up_y1']) / 2, (G['base_top'] + G['beam_bot']) / 2)
    Z = Vector(0, 0, 1)
    a = Vector(0, G['up_top_front'] - G['up_front'], G['beam_bot'] - G['base_top'] - P['upright_nose'])
    a.normalize()
    nrm = Vector(0, -a.z, a.y)
    it = []
    for b in KIT.boards:
        if u not in b.show:
            continue
        s_ = b.solid(holes=False)
        if b.name.startswith('Upright floor'):
            v = Vector()
        elif b.name.startswith('Upright cleat'):
            v = _out(s_, c, 60)
        elif b.name.startswith('Upright bridge'):
            v = Z * 230
        else:
            v = b.N * 150
        it.append(('melamine', s_, nice(b.name), v))
    for r in M.molds:
        for s_, sh in r['placed']:
            if u not in sh:
                continue
            n = r['name']
            v = {'back-bracket': _out(s_, c, 190) + Z * 40, 'front-bracket': nrm * 200 + _out(s_, c, 90, (0,)),
                 'toe-filler': nrm * 70, 'foot-gasket-groove': Z * 25,
                 'plate-spacer': Z * 170, 'saddle-flat': Z * 230 + _out(s_, c, 60, (0,))}.get(n)
            if v is None:
                v = nrm * 100 if n.startswith('toe-plug') else Vector()
            it.append(('printed', s_, nice(n), v))
    for look, s_, lab in S('FrameUprightL', skip=('Casting', 'Gasket', 'TieRod', 'Nut', 'Plug', 'Dowel')):
        it.append((look, s_, lab, Z * 150 if lab == 'Top plate' else Vector()))
    exploded(sc, 'exploded-upright', IDENT, it, Vector(0.8, 0.55, -0.45))


def beam_exploded(sc):
    b_ = 'beam'
    c = Vector(0, G['beam_face'] + P['beam_d'] / 2, (G['beam_bot'] + G['beam_top']) / 2)
    Y = Vector(0, 1, 0)
    it = []
    for b in KIT.boards:
        if b_ not in b.show:
            continue
        s_ = b.solid(holes=False)
        if b.name.startswith('Beam floor'):
            v = Vector()
        elif b.name.startswith('Beam cleat'):
            v = _out(s_, c, 60, (0, 2))
        else:
            v = b.N * 140
        it.append(('melamine', s_, nice(b.name), v))
    for r in M.molds:
        for s_, sh in r['placed']:
            if b_ not in sh:
                continue
            n = r['name']
            v = {'corner-bracket': _out(s_, c, 220, (0, 2)) + Y * 40,
                 'back-edge': Vector(0, 0, 1) * 90, 'dowel-stop': Vector(0, 0, -1) * 190}.get(n, Vector())
            it.append(('printed', s_, nice(n), v))
    for look, s_, lab in S('FrameBeam'):
        it.append((look, s_, lab, Y * (0 if lab.startswith('Face plate') else 110)))
    exploded(sc, 'exploded-beam', turn_beam, it, Vector(-0.45, -0.6, -0.65))


def fig_pour(sc):
    """The pour line: a gauge on one wall, screed shoes on two facing walls, a board struck across."""
    sc.clear()
    fb = P['mold_freeboard']
    gauge = next(r for r in M.molds if r['name'] == 'pour-gauge')['shape']
    shoe = next(r for r in M.molds if r['name'] == 'screed-shoe')['shape']
    W, D, Hh = 160.0, 120.0, 120.0
    mirror = lambda s_: s_.mirror(Vector(-W / 2, 0, 0), Vector(1, 0, 0))
    wall = parts.box(0, T, -D / 2, D / 2, -Hh, 0)
    sc.add(wall, 'board_old')
    sc.add(mirror(wall), 'board_old')
    sc.add(parts.box(-W - T - 30, T + 30, -D / 2 - 30, D / 2 + 30, -Hh - T, -Hh), 'board_old')
    sc.add(parts.box(-W, 0, -D / 2, D / 2, -Hh, -fb), 'mix')
    sc.add(gauge.translated(Vector(0, -D / 2 + 6, 0)), 'printed')
    for f in (lambda s_: s_, mirror):
        sc.add(f(shoe.translated(Vector(0, 10, 0))), 'printed')
    slot = T + 0.4
    sc.add(parts.box(-W + 5, -5, 10 - T / 2, 10 + T / 2, -fb, -fb + 60), 'wood')
    sc.camera(Vector(-0.55, 0.75, -0.45))
    sc.shoot('detail-pour', labels=[
        (Vector(-1.5, -D / 2 + 18, -fb + 2), f'Pour-line gauge: its leg ends {fb:.0f} mm down'),
        (Vector(-12, 10, -fb + 2), 'Screed shoe (one on each wall)'),
        (Vector(-W / 2, 10, -fb + 50), 'Straight board on edge: strike off along the walls'),
        (Vector(-W / 2, -D / 2 + 10, -fb), f'Pour line, {fb:.0f} mm below the wall tops'),
        (Vector(T / 2, D / 2 - 10, -40), 'Wall')])


# ------------------------------------------------------------------------------------------
# Gallery of the printed pieces
# ------------------------------------------------------------------------------------------
def gallery(sc, name, rows, cols=5, gap=40.0):
    sc.clear()
    cells = []
    for r in rows:
        shp = r['shape'][0] if isinstance(r['shape'], list) else r['shape']
        pose = molds.print_pose(shp, r.get('up'), r['kind'] == 'core')
        cells.append((r, pose))
    size = max(max(p.BoundBox.XLength, p.BoundBox.YLength) for _, p in cells) + gap
    labels = []
    for i, (r, p) in enumerate(cells):
        cx, cy = (i % cols) * size, -(i // cols) * size
        bb = p.BoundBox
        p = p.translated(Vector(cx - bb.XLength / 2, cy - bb.YLength / 2, 0))
        sc.add(p, 'printed')
        n = r['qty']
        dup = sum(1 for r2, _ in cells if r2['name'] == r['name']) > 1
        c = p.BoundBox.Center
        labels.append((p.distToShape(Part.Vertex(c))[1][0][0],
                       f"{r['folder'].replace('base-box', 'base') + ' ' if dup else ''}{r['name']} x{n}"
                       + (f" ({len(r['shape'])} parts)" if isinstance(r['shape'], list) and len(r['shape']) > 1 else '')))
    sc.camera(Vector(-0.35, 0.55, -0.75), Vector(0, 0, 1))
    sc.shoot(name, labels=labels)


def main():
    os.makedirs(OUT, exist_ok=True)
    sc = Scene()
    for f in (fig_bayonet, fig_pins, fig_peg, fig_corner, fig_core, fig_toe, fig_skeletons):
        try:
            f(sc)
        except Exception as e:
            print('figure failed:', f.__name__, e)
    for f in (base_steps, upright_steps, beam_steps, base_exploded, upright_exploded, beam_exploded, fig_pour):
        try:
            f(sc)
        except Exception as e:
            print('steps failed:', f.__name__, e)
    kit_rows = [r for r in M.molds if r['kind'] == 'kit']
    rest = [r for r in M.molds if r['kind'] in ('former', 'filler', 'plug')]
    try:
        gallery(sc, 'gallery-kit', kit_rows)
        gallery(sc, 'gallery-pieces', rest)
    except Exception as e:
        print('gallery failed:', e)


main()
