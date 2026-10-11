"""Illustrations for the mould guide: assembly steps for each mould, cut-away details of the joints and
fixings, and a gallery of the printed pieces, with labelled callouts. Writes renders/mould/.

Run in the FreeCAD GUI (it needs the 3D view):
    /Applications/FreeCAD.app/Contents/MacOS/FreeCAD "$PWD/model/mould_figures.py"

The base is cast upside down; its figures are turned over so the mould is shown the right way up
(floor at the bottom), and the beam's are turned so its open back is up.
"""

import math
import os
import re

import FreeCAD as App
import FreeCADGui as Gui
import Part
from FreeCAD import Vector
from PIL import Image, ImageDraw, ImageFont
from PySide import QtCore

try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:
    HERE = os.path.join(os.getcwd(), 'model')
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, 'renders', 'mould')
FONT = '/System/Library/Fonts/HelveticaNeue.ttc'
SCALE = 3                     # render at 3x the view, label, then shrink to 2/3
INK, LEADER, BOX = (29, 36, 34), (90, 102, 98), (255, 255, 255)

src = open(os.path.join(HERE, 'build_cnc.py')).read()
src = src[:src.rstrip().rfind('\nmain()')]
NS = {'__file__': os.path.join(HERE, 'build_cnc.py'), '__name__': 'build_cnc'}
exec(compile(src, 'build_cnc.py', 'exec'), NS)
P, parts, moulds, style = NS['P'], NS['parts'], NS['moulds'], NS['style']
NS['LOOKS'].update({'hw': ((0.55, 0.57, 0.60), 0.7, 0), 'pour': ((0.30, 0.60, 0.95), 0.2, 70),
                    'ghost': ((0.62, 0.63, 0.65), 0.05, 80), 'melamine_s': ((0.93, 0.93, 0.90), 0.3, 25)})
M = NS['build']()
KIT = M.mould_kit
G = NS['frame_layout'](M.dims)
PARTS = {p['name']: p for p in M.parts}
T = P['mould_board']


# ------------------------------------------------------------------------------------------
# Frames: show each mould the right way up
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
    axis = moulds.unit(axis)
    s_ = moulds.perp(axis)
    return moulds.hexagon(c, axis, s_, axis.cross(s_), af, h)


def bolt(head_at, axis, length, d=4.0):
    """Socket-head bolt: head outside head_at, shank along axis."""
    axis = moulds.unit(axis)
    head = Part.makeCylinder(d * 0.85, d, head_at - axis * d, axis).cut(hexprism(head_at - axis * (d + 0.1), axis, d * 0.75, d * 0.6))
    washer = Part.makeCylinder(d * 1.1, 0.8, head_at - axis * 0.8, axis).cut(Part.makeCylinder(d / 2 + 0.2, 2, head_at - axis, axis))
    return head.fuse([washer, Part.makeCylinder(d / 2, length, head_at - axis * 0.8, axis)])


def nut(c, axis, af=7.0, t=3.2, d=4.0):
    axis = moulds.unit(axis)
    return hexprism(c - axis * (t / 2), axis, af, t).cut(Part.makeCylinder(d / 2, t + 2, c - axis * (t / 2 + 1), axis))


# ------------------------------------------------------------------------------------------
# Scene and camera
# ------------------------------------------------------------------------------------------
class Scene:
    def __init__(self):
        self.doc = App.newDocument('MouldFigures')
        self.view = Gui.ActiveDocument.ActiveView
        self.view.setAnimationEnabled(False)
        self.n = 0

    def clear(self):
        for o in list(self.doc.Objects):
            self.doc.removeObject(o.Name)
        self.n = 0

    def add(self, shape, look, transp=None, lines=True):
        if shape is None or shape.isNull():
            return None
        self.n += 1
        o = self.doc.addObject('Part::Feature', f'S{self.n}')
        o.Shape = shape
        style(o, look)
        if transp is not None:
            o.ViewObject.Transparency = transp
        if not lines:
            o.ViewObject.DisplayMode = 'Shaded'
        return o

    def camera(self, d, up=Vector(0, 0, 1), zoom=1.0):
        z = -moulds.unit(d)
        x = moulds.unit(up.cross(z))
        y = z.cross(x)
        self.view.setCameraOrientation(App.Rotation(App.Matrix(x.x, y.x, z.x, 0, x.y, y.y, z.y, 0,
                                                               x.z, y.z, z.z, 0, 0, 0, 0, 1)))
        self.doc.recompute()
        self.view.fitAll()
        Gui.updateGui()

    def shoot(self, name, labels=(), arrows=()):
        """labels: [(point, text)]; arrows: [(from point, to point)] drawn in 2D."""
        w, h = self.view.getSize()
        W, H = w * SCALE, h * SCALE
        path = os.path.join(OUT, name + '.png')
        self.view.saveImage(path, W, H, 'White')
        im = Image.open(path).convert('RGB')
        dr = ImageDraw.Draw(im)
        font = ImageFont.truetype(FONT, 62)
        proj = lambda p: (lambda q: (q[0] * SCALE, H - q[1] * SCALE))(self.view.getPointOnScreen(p))
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
    for r in M.moulds:
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
    hw = moulds.HW['M4']
    reach = hw['af'] + 3.0
    board = parts.box(-30, 38, -14, 14, -T, 0)
    piece = parts.box(-22, 30, -12, 12, 0, 16)
    p, n, s_ = Vector(0, 0, 0), Vector(0, 0, -1), Vector(1, 0, 0)
    piece = piece.cut(moulds.nut_trap(p, n, s_, 'M4'))
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
    r = next(r for r in M.moulds if r['name'] == 'foot-gasket-groove')
    part_ = r['shape'][0]
    bb = part_.BoundBox
    crop = parts.box(bb.XMin - 30, bb.XMax + 30, bb.YMin - 20, bb.YMin + 140, bb.ZMin - 30, bb.ZMax + 10)
    for s in boards('upright', ['Upright floor'], crop):
        sc.add(s, 'melamine_s', 10)
    lift = Vector(0, 0, 18)
    sc.add(part_.common(crop).translated(lift), 'printed')
    sc.camera(Vector(-0.6, 0.55, -0.6), zoom=1.0)
    pins_at = [Vector(e.Curve.Center.x, e.Curve.Center.y, bb.ZMin) for e in part_.Edges
               if isinstance(e.Curve, Part.Circle) and abs(e.Curve.Radius - moulds.PIN_D / 2) < 0.05
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
    r = next(r for r in M.moulds if r['folder'] == 'base-front' and r['name'] == 'trough')
    a, b = r['shape'][1], r['shape'][2]
    sc.add(flip_base(a), 'printed')
    sc.add(flip_base(b).translated(Vector(28, 0, 0)), 'printed')
    sc.camera(Vector(-0.45, 0.75, -0.5))
    pa = flip_base(a)
    peg = [f for f in pa.Faces if isinstance(f.Surface, Part.Cylinder) and abs(f.Surface.Radius - moulds.PEG_D / 2) < 0.05]
    lab = [(pa.BoundBox.Center + Vector(0, 0, 6), 'Trough former, part 2'),
           (flip_base(b).BoundBox.Center + Vector(28, 0, 6), 'Part 3')]
    if peg:
        lab.append((peg[0].CenterOfMass, 'Peg into the next part'))
    sc.shoot('fixing-peg', labels=lab, arrows=[(flip_base(b).BoundBox.Center + Vector(10, 0, 0),
                                               flip_base(b).BoundBox.Center + Vector(-14, 0, 0))])


def fig_corner(sc):
    """A corner of the base mould, the right way up: walls on cleats, corner bracket, leg holder,
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
    lx, ly = half - P['leg_inset'], G['legs'][2][1]
    lab = [(pt(flip_base, Vector(half + T / 2, 300, 40)), 'Side wall'),
           (pt(flip_base, Vector(200, y1 + T / 2, 40)), 'Rear wall'),
           (pt(flip_base, Vector(half + T + 20, 250, G['base_top'] - T / 2)), 'Cleat, bolted down'),
           (pt(flip_base, Vector(half + T + 5, y1 + T + 5, -12)), 'Corner bracket'),
           (pt(flip_base, Vector(lx - 22, ly, -19)), 'Leg holder + pinch screw'),
           (pt(flip_base, Vector(lx, ly, -100)), 'Leg'),
           (pt(flip_base, Vector(half + 5, 280, -40)), 'Saddle + bridge'),
           (pt(flip_base, Vector(165, 235, -0.3)), 'Pour line: 25 mm below the wall tops'),
           (pt(flip_base, Vector(half - 15, y1 - 15, 60)), 'Corner filler')]
    sc.shoot('detail-corner', labels=lab)


def fig_core(sc):
    """A foam pocket core hanging from a bridge by its printed post (section through the post)."""
    sc.clear()
    r = next(r for r in M.moulds if r['kind'] == 'foam' and r['name'] == 'foot-b-R')
    post = next(r_ for r_ in M.moulds if r_['name'] == 'foot-b-R-post')
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


def fig_socket(sc):
    """A socket: printed spike bolted to the floor, the foam block pushed over it (lifted)."""
    sc.clear()
    r = next(r for r in M.moulds if r['name'] == 'socket-spike')
    f = next(r for r in M.moulds if r['name'] == 'socket' and r['kind'] == 'foam')
    sp, blk = r['placed'][0][0], f['placed'][0][0]
    bb = blk.BoundBox
    crop = parts.box(bb.XMin - 40, bb.XMax + 40, bb.YMin - 40, bb.YMax + 40, 0, G['base_top'] + T)
    for s in boards('base-rear', ['Base floor'], crop):
        sc.add(flip_base(s), 'melamine', 20)
    sc.add(flip_base(sp), 'printed')
    lift = Vector(0, 0, 45)
    sc.add(flip_base(blk).translated(lift), 'foam', 25)
    sc.camera(Vector(-0.55, 0.6, -0.55))
    top = pt(flip_base, Vector(bb.Center.x, bb.Center.y, G['base_top'] - 20))
    sc.shoot('detail-socket', labels=[
        (top, 'Printed spike, bolted to the floor'),
        (pt(flip_base, bb.Center) + lift, 'Foam socket core: push over the spike'),
        (pt(flip_base, Vector(bb.XMax + 30, bb.Center.y, G['base_top'] + T / 2)), 'Floor board')],
        arrows=[(top + lift + Vector(0, 0, 30), top + Vector(0, 0, 25))])


def fig_toe(sc):
    """Upright: the toe filler and the front board's foot in its lip."""
    sc.clear()
    x0, x1 = -G['outer'], -G['inner']
    crop = parts.box(x0 - T - 50, x1 + T + 50, G['up_front'] - 90, G['up_front'] + 80, G['base_top'] - T - 1, G['base_top'] + 110)
    for s in boards('upright', ['Upright floor', 'Upright front board', 'Upright cleat'], crop):
        sc.add(s, 'melamine', 40)
    for s in boards('upright', ['Upright side plate, inner'], crop):
        sc.add(s, 'melamine', 75)
    add_all(sc, IDENT, pieces('upright', ['toe-filler', 'front-bracket', 'slope-plug'], crop=crop))
    sc.camera(Vector(0.75, 0.55, -0.4))
    tf = next(r for r in M.moulds if r['name'] == 'toe-filler')['placed'][0][0].BoundBox
    sc.shoot('detail-toe', labels=[
        (Vector(tf.Center.x, tf.YMin + 15, tf.ZMin + 15), 'Toe filler, bolted to the floor'),
        (Vector(tf.Center.x, tf.YMin + 8, tf.ZMax - 6), 'Lip holds the board\'s foot'),
        (Vector(tf.Center.x, tf.YMax + 20, tf.ZMax + 50), 'Front board (sloped)')])


def fig_locator(sc):
    """Beam: a tube locator through the end wall into the tube end (section)."""
    sc.clear()
    outer = G['outer']
    half_len = P['tube_len']['beam'] / 2
    bf = G['beam_face']
    crop = parts.box(half_len - 40, outer + T + 30, bf - T - 1, bf + 80, G['beam_bot'] - T - 10, (G['beam_bot'] + G['beam_top']) / 2)
    for s in boards('beam', ['Beam end wall, right', 'Beam floor', 'Beam bottom wall'], crop):
        sc.add(turn_beam(s), 'melamine', 45)
    add_all(sc, turn_beam, pieces('beam', ['tube-locator'], crop=crop))
    for look, s in steel('FrameBeam', crop):
        if s.Volume > 1:
            sc.add(turn_beam(s), look)
    sc.camera(Vector(-0.6, 0.6, -0.5))
    cz = (G['beam_bot'] + G['beam_top']) / 2
    ty = bf + 32.0
    sc.shoot('detail-locator', labels=[
        (pt(turn_beam, Vector(half_len - 30, ty - 25.4 + 1.6, cz - 12)), 'Beam tube'),
        (pt(turn_beam, Vector(half_len - 8, ty, cz)), 'Cross in the tube end'),
        (pt(turn_beam, Vector(half_len + 20, ty + 12, cz)), '16 mm stem'),
        (pt(turn_beam, Vector(outer + T, ty + 12, cz)), 'M4 x 70 through the end wall'),
        (pt(turn_beam, Vector(outer + T / 2, bf + 70, G['beam_bot'])), 'End wall')])


# ------------------------------------------------------------------------------------------
# Assembly steps
# ------------------------------------------------------------------------------------------
NICE = {'BaseRearTubePlug': 'Tube end plug (printed)', 'BaseFrontTubePlug': 'Tube end plug (printed)',
        'BaseRearSpigotSleeve': 'Spigot sleeve (printed)', 'BaseFrontSpigotSleeve': 'Spigot sleeve (printed)',
        'BaseRearTube': 'Rail tube', 'BaseFrontTube': 'Rail tube', 'BaseSpigot': 'Spigot', 'Leg': 'Leg',
        'DrawRodCoupler': 'Draw-rod coupler', 'TieRodCoupler': 'Tie-rod coupler', 'DrawRod': 'Draw rod',
        'Anchor': 'Cast-in insert', 'Insert': 'Cast-in insert', 'Post': 'Post', 'TopPlate': 'Top plate',
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
    parts in colour (labelled) and the earlier ones paler."""
    shown = []
    for k, (title, items) in enumerate(stages, 1):
        sc.clear()
        for old in shown:
            for look, s_, _ in old:
                sc.add(fn(s_), 'ghost' if look != 'melamine' else 'melamine', 82 if look != 'melamine' else 80)
        labels, seen = [], set()
        for look, s_, _ in items:
            sc.add(fn(s_), look, 40 if look == 'melamine' else None)
        rank = lambda it: 0 if it[0] in ('printed', 'foam') else 1 if it[0] == 'melamine' else 2
        for look, s_, lab in sorted(items, key=rank):
            if lab and lab not in seen and len(labels) < max_labels:
                seen.add(lab)
                labels.append((pt(fn, anchor(s_)), lab))
        shown.append(items)
        sc.camera(d, up)
        sc.shoot(f'{name}-{k}', labels=labels)


def B(group, names):
    return [('melamine', b.solid(), nice(b.name)) for b in KIT.boards
            if group in b.show and any(b.name.startswith(n) for n in names)]


def K(group, names=None, kinds=None):
    out = []
    for r in M.moulds:
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


def base_steps(sc):
    rear, front = 'base-rear', 'base-front'
    walls = ['Base front wall', 'Base rear wall', 'Base side wall']
    stages = [
        ('floor', B(rear, ['Base floor', 'Base cleat'])),
        ('walls', B(rear, walls) + K(rear, ['corner-bracket'])),
        ('partition', B(rear, ['Base partition']) + K(rear, ['partition-bracket', 'split-gasket', 'spigot-bushing'])),
        ('pieces', K(rear, ['gutter', 'motor-relief', 'corner-', 'socket'])),
        ('steel', S('FrameBaseRear') + K(rear, ['leg-holder'])),
        ('cores', K(rear, None, kinds=('foam', 'core')) + K(rear, ['saddle']) + B(rear, ['Base bridge', 'Base leg bridge'])),
    ]
    steps(sc, 'step-base-rear', flip_base, Vector(-0.5, -0.62, -0.6), stages)
    cast = [('granite', PARTS['BaseRearCasting']['shape'], 'Rear half, cured and waxed')]
    fstages = [
        ('rear cast', B(front, ['Base floor', 'Base cleat'] + walls) + K(front, ['corner-bracket']) + cast),
        ('front pieces', K(front, ['gutter', 'trough', 'corner-']) + S('FrameBaseFront') + K(front, ['leg-holder'])),
        ('cores', K(front, None, kinds=('foam', 'core')) + K(front, ['saddle']) + B(front, ['Base bridge', 'Base leg bridge'])),
    ]
    steps(sc, 'step-base-front', flip_base, Vector(0.5, 0.62, -0.6), fstages)


def upright_steps(sc):
    u = 'upright'
    post_bot = G['beam_bot'] - P['top_plate_t'] - 2 - P['tube_len']['post']
    rods = []
    for rx, ry, pb in G['tie_rods']:
        z1 = G['beam_bot'] + P['mould_freeboard'] + 30 if pb >= G['pocket_bot'] - 1 else pb + 20
        rods.append(('hw', Part.makeCylinder(P['up_rod_hole'] / 2, z1 - post_bot, Vector(-rx, ry, post_bot)),
                     '5/8 in rod (forms a tie-rod hole)'))
    st = S('FrameUprightL', skip=('Casting', 'Gasket', 'TieRod', 'Nut', 'TopPlate'))
    stages = [
        ('floor', B(u, ['Upright floor', 'Upright cleat']) + K(u, ['post-bushing', 'foot-gasket'])),
        ('sides', B(u, ['Upright side plate', 'Upright back board']) + K(u, ['back-bracket'])),
        ('front', B(u, ['Upright front board']) + K(u, ['toe-filler', 'front-bracket'])),
        ('steel', st + rods + K(u, ['slope-plug'])),
        ('top', K(u, ['tie-rod-pocket', 'plate-spacer', 'saddle-flat']) + B(u, ['Upright bridge'])
         + [('steeltube', PARTS['TopPlateL']['shape'], 'Top plate')]),
    ]
    steps(sc, 'step-upright', IDENT, Vector(0.8, 0.55, -0.45), stages)


def beam_steps(sc):
    b = 'beam'
    rods = [('hw', Part.makeCylinder(P['beam_bolt_hole'] / 2, G['beam_top'] - G['beam_bot'] + 2 * T + 20,
                                     Vector(sx * bx, by, G['beam_bot'] - T - 10)), '1/2 in rod (forms a bolt hole)')
            for sx in (-1, 1) for bx in G['bolt_xs'] for by in G['bolt_ys']]
    on_floor = lambda p: p['shape'].BoundBox.YMax < G['beam_face'] + 8
    stages = [
        ('floor', B(b, ['Beam floor', 'Beam cleat']) + S('FrameBeam', keep=on_floor)),
        ('walls', B(b, ['Beam top wall', 'Beam bottom wall', 'Beam end wall']) + K(b, ['corner-bracket'])),
        ('tubes', S('FrameBeam', keep=lambda p: not on_floor(p)) + K(b, ['tube-locator', 'back-edge', 'dowel-stop']) + rods),
    ]
    steps(sc, 'step-beam', turn_beam, Vector(-0.45, -0.6, -0.65), stages)


# ------------------------------------------------------------------------------------------
# Gallery of the printed pieces
# ------------------------------------------------------------------------------------------
def gallery(sc, name, rows, cols=5, gap=40.0):
    sc.clear()
    cells = []
    for r in rows:
        shp = r['shape'][0] if isinstance(r['shape'], list) else r['shape']
        pose = moulds.print_pose(shp, r.get('up'), r['kind'] == 'core')
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
    for f in (fig_bayonet, fig_pins, fig_peg, fig_corner, fig_core, fig_socket, fig_toe, fig_locator):
        try:
            f(sc)
        except Exception as e:
            print('figure failed:', f.__name__, e)
    for f in (base_steps, upright_steps, beam_steps):
        try:
            f(sc)
        except Exception as e:
            print('steps failed:', f.__name__, e)
    kit_rows = [r for r in M.moulds if r['kind'] == 'kit']
    rest = [r for r in M.moulds if r['kind'] in ('former', 'filler', 'plug')]
    try:
        gallery(sc, 'gallery-kit', kit_rows)
        gallery(sc, 'gallery-pieces', rest)
    except Exception as e:
        print('gallery failed:', e)
    App.closeDocument(sc.doc.Name)


main()
QtCore.QTimer.singleShot(0, Gui.getMainWindow().close)
