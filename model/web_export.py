"""The machine as an interactive page for a web browser (cad-rust-app's web viewer): jog X, Y and Z within their
travel by slider, by dragging the table, carriage or spindle, or with the arrow keys; swing the door, pull the
coolant drawer and explode the frame. The ball screws turn with their axes, the way covers, cable chain and
coolant loop follow them, and the tool tip reads out (and traces) its position on the table. A demo program
cuts a pocket and drills four holes in a block on the table.

    python model/web_export.py            # writes model/DIYCNC.html (about 9 MB; open it in a browser)
"""

import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'DIYCNC.html')
SAMPLES = 13            # poses along an axis for the parts that change shape (the page blends between them)
DYN = dict(linear=0.5, angular=0.6)

# what the page's layers call the looks, and their densities (g/cm^3) for the part details
LAYER = {'granite': 'Epoxy granite castings', 'granite_hi': 'Epoxy granite castings', 'printed_dark': 'Epoxy granite castings',
         'steeltube': 'Steel skeleton', 'motor': 'Motors', 'spindle': 'Spindle', 'printed': 'Printed parts',
         'rubber': 'Rubber and gaskets', 'gasket_hi': 'Rubber and gaskets', 'sand': 'Steel skeleton',
         'vinyl': 'Steel skeleton'}
DENSITY = {'granite': 2.35, 'steeltube': 7.85, 'steel': 7.85, 'alu': 2.70, 'brass': 8.50, 'printed': 1.25,
           'printed_dark': 1.25, 'rubber': 1.20, 'wood': 0.60, 'shim': 7.85, 'sand': 1.60, 'vinyl': 1.30}
CONTAINER_LAYER = {'Enclosure': 'Enclosure', 'Door': 'Enclosure', 'Workbench': 'Workbench', 'CoolantSump': 'Coolant',
                   'CoolantLines': 'Coolant', 'WayCovers': 'Way covers and chain', 'CableChain': 'Way covers and chain'}


def load():
    src = open(os.path.join(HERE, 'build_cnc.py')).read()
    src = src[:src.rstrip().rfind('\nmain()')]
    ns = {'__file__': os.path.join(HERE, 'build_cnc.py'), '__name__': 'build_cnc'}
    sys.path.insert(0, HERE)
    exec(compile(src, 'build_cnc.py', 'exec'), ns)
    return ns


def layer_of(container, look):
    return CONTAINER_LAYER.get(container) or LAYER.get(look) or 'Motion hardware'


def main():
    from cadrust.freecad import Part, Vector
    from cadrust.web import Scene
    ns = load()
    m = ns['build']()
    P, LOOKS, d = ns['P'], ns['LOOKS'], m.dims
    objs, parent = ns['scene'](m)
    objs = [o for o in objs if not o['container'].startswith('Mold')]
    hx, hy, tz = P['travel_x'] / 2, P['travel_y'] / 2, P['travel_z']

    sc = Scene('DIYCNC', notes=f"Epoxy-granite CNC mill: {P['travel_x']:.0f} × {P['travel_y']:.0f} × {P['travel_z']:.0f} mm "
                               'travel. Y moves the table, X the carriage on the beam, Z the spindle. Machine '
                               'coordinates: +Y moves the tool back on the work, so the table comes forward.')
    nodes = {}

    def node(name, **kw):
        if name not in nodes:
            par = parent.get(name)
            nodes[name] = sc.node(name, parent=node(par) if par else None, **kw)
        return nodes[name]

    # the moving containers first, with their joints (positions and axes in the world frame, as drawn)
    node('Frame')
    for c, e in (('FrameUprightL', (-90, 0, 180)), ('FrameUprightR', (90, 0, 180)), ('FrameBeam', (0, 0, 360)),
                 ('FrameBaseFront', (0, -216, 0)), ('FrameBaseRear', None)):
        node(c, explode=e)
    parent['TableAxis'] = 'FrameBaseRear'
    node('TableAxis', slider=(0, -1, 0), limits=(-hy, hy), label='Y · table')
    parent['XCarriage'] = 'FrameBeam'          # so the carriage rides along when the beam explodes
    node('XCarriage', slider=(1, 0, 0), limits=(-hx, hx), label='X · carriage')
    node('ZAxis', slider=(0, 0, 1), limits=(-tz, 0.0), label='Z · spindle')
    h = d['hinge']
    node('Door', revolute=(0, 0, -1), origin=(h.x, h.y, h.z), limits=(0, 100), label='Door')
    node('CoolantSump', slider=(0, -1, 0), limits=(0, 450), label='Coolant drawer')
    Y, X, Z = nodes['TableAxis'], nodes['XCarriage'], nodes['ZAxis']

    # ball screws, couplers and motor shafts turn with their axes (deg per mm = 360 / lead)
    spin_parts = {'X': ('XCarriage', 'FrameBeam', (1, 0, 0), 4.0), 'Y': ('TableAxis', 'FrameBaseRear', (0, 1, 0), 5.0),
                  'Z': ('ZAxis', 'XCarriage', (0, 0, 1), 4.0)}
    by_name = {p['name']: p for p in m.parts}
    spin_node = {}
    for ax, (mover, on, dirn, lead) in spin_parts.items():
        bb = by_name[f'{ax}_Screw']['shape'].BoundBox
        c = (bb.XMin + bb.XMax) / 2, (bb.YMin + bb.YMax) / 2, (bb.ZMin + bb.ZMax) / 2
        spin_node[ax] = sc.node(f'{ax} screw', parent=node(on), revolute=dirn, origin=c, follows=nodes[mover],
                                ratio=360.0 / lead * (-1 if ax == 'Y' else 1))
    spinning = {f'{ax}_{n}': ax for ax in 'XYZ' for n in ('Screw', 'Coupler', 'MotorShaft', 'BK10LockNut', 'BK12LockNut')}

    # parts
    for o in objs:
        if 'shape' not in o:
            continue
        shape = o['shape']
        if shape is None or shape.isNull():
            continue
        rgb, shine, transp = LOOKS[o['look']]
        at = spin_node[spinning[o['name']]] if o['name'] in spinning else node(o['container'])
        vol = shape.Volume / 1000.0
        info = {'Container': o['container'], 'Volume': f'{vol:,.1f} cm³'}
        if o['look'] in DENSITY:
            info['Mass'] = f'{vol * DENSITY[o["look"]] / 1000:,.2f} kg'
        sc.part(shape, at, name=o['name'], color=rgb, opacity=1 - transp / 100, shine=shine,
                edges=o['look'] not in ns['SHADED'], layer=layer_of(o['container'], o['look']), info=info)

    # a block of stock on the table for the demo program
    tt = d['table_top']
    stock = (120.0, 80.0, 30.0)
    block = Part.makeBox(stock[0], stock[1], stock[2], Vector(-stock[0] / 2, -stock[1] / 2, tt))
    sc.part(block, Y, name='Stock (6061, demo)', color=(0.86, 0.80, 0.62), shine=0.2, layer='Stock',
            info={'Size': f'{stock[0]:.0f} × {stock[1]:.0f} × {stock[2]:.0f} mm'})

    # parts that change shape with the axes: sampled over their joints' travel
    travel = dict(x=(X, -hx, hx), y=(Y, -hy, hy), z=(Z, -tz, 0.0))
    for o in objs:
        if 'fn' not in o:
            continue
        fn = o['fn']

        def at(pose):
            # pose in joint values; the build's y is the table's travel, the opposite of the Y joint
            s = fn(pose.get('x', 0.0), -pose.get('y', 0.0), pose.get('z', 0.0))
            return None if s is None or s.isNull() else s

        def key(s):
            if s is None:
                return None
            b = s.BoundBox
            return tuple(round(v, 3) for v in (b.XMin, b.XMax, b.YMin, b.YMax, b.ZMin, b.ZMax))
        axes = [a for a in 'xyz' if key(at({a: travel[a][1]})) != key(at({a: travel[a][2]}))]
        n = SAMPLES if len(axes) == 1 else 7
        grid = [list(np.linspace(travel[a][1], travel[a][2], n)) for a in axes]
        shapes = [at({a: grid[k][i] for k, (a, i) in enumerate(zip(axes, idx))}) for idx in np.ndindex(*[n] * len(axes))]
        rgb, shine, transp = LOOKS[o['look']]
        sc.morph(o['name'], node(o['container']), [travel[a][0] for a in axes], grid, shapes, color=rgb,
                 opacity=1 - transp / 100, shine=shine, layer=layer_of(o['container'], o['look']), **DYN)
        print(f"  {o['name']}: follows {''.join(axes).upper() or '-'}, {len(shapes)} samples", flush=True)

    # the tool tip on the table, and the volume it can reach there
    tip = d['tip']
    sc.marker('Tool tip on the work (machine coordinates)', Z, (0.0, 0.0, tip), relative=Y, trail=True)
    sc.box('Work envelope', Y, (-hx, -hy, tip - tz), (hx, hy, tip))

    # demo program in machine coordinates: face the top, cut a pocket, drill four holes
    top = tt + stock[2] - tip               # Z where the tip touches the top of the block
    safe = top + 10.0
    rapid, cut, plunge = 60.0, 12.0, 4.0

    def go(x=None, y=None, z=None, feed=cut, note=None):
        v = {}
        if x is not None:
            v[X] = x
        if y is not None:
            v[Y] = y
        if z is not None:
            v[Z] = z
        return (v, feed, note)
    prog = [go(z=0.0, feed=rapid, note='Home'), go(-50, -30, feed=rapid, note='Rapid over the block'), go(z=safe, feed=rapid),
            go(z=top - 1.0, feed=plunge, note='Face the top, 1 mm deep')]
    rows = np.arange(-30.0, 30.1, 10.0)
    for i, y in enumerate(rows):
        prog.append(go(50 if i % 2 == 0 else -50, y))          # across the block
        if i + 1 < len(rows):
            prog.append(go(y=rows[i + 1]))                      # step over
    prog += [go(z=safe, feed=rapid), go(-25, -15, feed=rapid, note='Pocket 50 × 30 mm, 6 mm deep, in 2 mm steps')]
    for depth in (3.0, 5.0, 7.0):
        prog.append(go(z=top - depth, feed=plunge))
        for r in (0, 5, 10):
            prog += [go(25 - r, -15 + r), go(25 - r, 15 - r), go(-25 + r, 15 - r), go(-25 + r, -15 + r)]
        prog.append(go(-25, -15))
    prog.append(go(z=safe, feed=rapid, note='Drill four holes'))
    for x, y in ((-50, -32), (50, -32), (50, 32), (-50, 32)):
        prog += [go(x, y, feed=rapid), go(z=top - 12.0, feed=plunge), go(z=safe, feed=rapid)]
    prog += [go(z=0.0, feed=rapid, note='Back home'), go(0, 0, feed=rapid)]
    sc.tour('Demo: face, pocket, drill', prog)
    sc.tour('Corners of the travel', [go(0, 0, 0, rapid, 'Home'), go(-hx, -hy, feed=rapid, note='X− Y−'),
                                      go(hx, feed=rapid, note='X+'), go(y=hy, feed=rapid, note='Y+'),
                                      go(-hx, feed=rapid, note='X−'), go(z=-tz, feed=rapid / 2, note='Z all the way down'),
                                      go(z=0.0, feed=rapid / 2), go(0, 0, feed=rapid, note='Home')])

    for name in ('Enclosure', 'Workbench'):            # open on the machine itself; the panel brings them back
        sc.layer(name, 'hide')
    nbytes, nmesh, ntri = sc.write(OUT)
    print(f'{len(sc.parts)} parts, {len(sc.morphs)} that change shape, {nmesh} meshes, {ntri:,} triangles; '
          f'{os.path.relpath(OUT)} {nbytes / 1e6:.1f} MB')


main()
