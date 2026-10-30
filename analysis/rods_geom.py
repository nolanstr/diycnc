"""Positions of the rods and studs the voxels leave out; writes analysis/rods.json for topopt_gantry.py,
which keeps material round the uprights' tie rods.

    python analysis/rods_geom.py
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
CAD = os.path.join(os.path.dirname(HERE), 'model')
src = open(os.path.join(CAD, 'build_cnc.py')).read()
src = src[:src.rstrip().rfind('\nmain()')]
ns = {'__file__': os.path.join(CAD, 'build_cnc.py'), '__name__': 'build_cnc'}
exec(compile(src, 'build_cnc.py', 'exec'), ns)
out = {}
for p in ns['build']().parts:
    if p['name'].startswith(('TieRod', 'DrawRod', 'CrossRod', 'BeamBolt')):
        bb = p['shape'].BoundBox
        out[p['name']] = [bb.XMin, bb.YMin, bb.ZMin, bb.XMax, bb.YMax, bb.ZMax]
json.dump(out, open(os.path.join(HERE, 'rods.json'), 'w'), indent=1)
print(len(out), 'rods ->', os.path.join(HERE, 'rods.json'))
