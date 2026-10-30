"""Geometry of the moving parts for the drive-chain stiffness study.

    python analysis/chain_geom.py

Builds the model from build_cnc.py and writes analysis/chain_geom.json: the bounding boxes of the
plates (and what they're made of), the carriage's angles, the risers, rails, blocks, nuts and screw
supports (Z at the top), plus the dimensions chain.py needs. VOX_P overrides parameters as in
voxelize.py; CHAIN_OUT names the output.
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
CAD = os.path.join(os.path.dirname(HERE), 'model')
OUT = os.environ.get('CHAIN_OUT', os.path.join(HERE, 'chain_geom.json'))
KEEP = ('Riser', 'Rail', 'Block', 'Nut', 'BK', 'BF', 'MotorBracket', 'Screw')


def load_build():
    src = open(os.path.join(CAD, 'build_cnc.py')).read()
    src = src[:src.rstrip().rfind('\nmain()')]
    ns = {'__file__': os.path.join(CAD, 'build_cnc.py'), '__name__': 'build_cnc'}
    exec(compile(src, 'build_cnc.py', 'exec'), ns)
    return ns


def main():
    ns = load_build()
    P = ns['P']
    P.update(json.loads(os.environ.get('VOX_P', '{}')))
    m = ns['build']()
    d = m.dims
    boxes, looks = {}, {}
    for p in m.parts:
        n = p['name']
        if n in ('Table', 'XCarriagePlate', 'ZPlate', 'SpindleClamp') or n.startswith('XCarriageAngle') or (
                n[:2] in ('X_', 'Y_', 'Z_') and any(k in n for k in KEEP) and not n.endswith(('Nipple', 'Seals'))):
            bb = p['shape'].BoundBox
            boxes[n] = [bb.XMin, bb.YMin, bb.ZMin, bb.XMax, bb.YMax, bb.ZMax]
            looks[n] = p['look']
    keys = ['base_top', 'table_top', 'table_bot', 'beam_face', 'beam_cz', 'tip', 'zp_bot', 'car_back', 'y_bk']
    json.dump(dict(boxes=boxes, looks=looks, dims={k: float(d[k]) for k in keys},
                   P={k: P[k] for k in ('travel_x', 'travel_y', 'travel_z', 'table_t', 'carriage_t', 'zplate_t',
                                        'bracket_y', 'car_angle')}),
              open(OUT, 'w'), indent=1)
    print(len(boxes), 'boxes ->', OUT)


main()
