"""Voxelize the frame for the stiffness study (run with freecadcmd).

    /Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd analysis/voxelize.py

Builds the model from build_cnc.py and writes analysis/vox_current.npz: per-voxel volume
fractions of epoxy granite and steel for each module group (base, uprights, beam),
plus the base with no underside pockets (the optimization's design space), and
analysis/vox_current.json with the positions the load cases need. VOX_P='{"beam_d": 140}' overrides
parameters, VOX_OUT names the output. VOX_PARTS=1 also writes <output>_parts.npz, each steel part's
own fractions (for steel_study.py).
"""

import json
import os
import sys

import numpy as np
from matplotlib.path import Path

import FreeCAD as App  # noqa: F401
from FreeCAD import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
CAD = os.path.join(os.path.dirname(HERE), 'model')
H = float(os.environ.get('VOX_H', '10'))     # voxel size, mm
SUB = int(os.environ.get('VOX_SUB', '4'))    # sample points per voxel edge
OUT = os.environ.get('VOX_OUT', os.path.join(HERE, 'vox_current'))
SKIP = [t for t in os.environ.get('VOX_SKIP', '').split(',') if t]   # part-name prefixes left out (unbonded rods)
PARTS = os.environ.get('VOX_PARTS') == '1'


def load_build():
    src = open(os.path.join(CAD, 'build_cnc.py')).read()
    src = src[:src.rstrip().rfind('\nmain()')]
    ns = {'__file__': os.path.join(CAD, 'build_cnc.py'), '__name__': 'build_cnc'}
    exec(compile(src, 'build_cnc.py', 'exec'), ns)
    return ns


class Grid:
    def __init__(self, x0, y0, z0, nx, ny, nz, h):
        self.o, self.n, self.h = np.array([x0, y0, z0]), np.array([nx, ny, nz]), h

    def sub(self, ax):
        k = np.arange(self.n[ax] * SUB)
        return self.o[ax] + (k + 0.5) * self.h / SUB


def fractions(shape, grid):
    """Volume fraction of shape in each voxel, by slicing at the sub-sample heights."""
    out = np.zeros(tuple(grid.n), np.float32)
    bb = shape.BoundBox
    xs, ys, zs = grid.sub(0), grid.sub(1), grid.sub(2)
    ix = np.nonzero((xs > bb.XMin) & (xs < bb.XMax))[0]
    iy = np.nonzero((ys > bb.YMin) & (ys < bb.YMax))[0]
    iz = np.nonzero((zs > bb.ZMin) & (zs < bb.ZMax))[0]
    if not len(ix) or not len(iy) or not len(iz):
        return out
    X, Y = np.meshgrid(xs[ix], ys[iy], indexing='ij')
    pts = np.column_stack([X.ravel(), Y.ravel()])
    acc = np.zeros((len(ix), len(iy), len(iz)), np.float32)
    for j, k in enumerate(iz):
        inside = np.zeros(len(pts), bool)
        for w in shape.slice(Vector(0, 0, 1), float(zs[k])):
            poly = np.array([(p.x, p.y) for p in w.discretize(Deflection=0.05)])
            if len(poly) > 2:
                inside ^= Path(poly).contains_points(pts)
        acc[:, :, j] = inside.reshape(len(ix), len(iy))
    # sum the sub-samples into voxels
    full = np.zeros((grid.n[0] * SUB, grid.n[1] * SUB, grid.n[2] * SUB), np.float32)
    full[np.ix_(ix, iy, iz)] = acc
    out = full.reshape(grid.n[0], SUB, grid.n[1], SUB, grid.n[2], SUB).mean(axis=(1, 3, 5))
    return out


GROUP = {'FrameBaseFront': 'base', 'FrameBaseRear': 'base', 'FrameUprightL': 'up', 'FrameUprightR': 'up',
         'FrameBeam': 'beam'}


def main():
    ns = load_build()
    P = ns['P']
    P.update(json.loads(os.environ.get('VOX_P', '{}')))   # parameter overrides for what-if runs
    m = ns['build']()
    d = m.dims
    half = d['base_half']
    nx = int(round(2 * half / H))
    ny = int(np.ceil((d['base_y1'] - d['base_y0']) / H))
    nz = int(np.ceil(d['beam_top'] / H))
    grid = Grid(-half, d['base_y0'], 0.0, nx, ny, nz, H)
    print('grid', nx, ny, nz, flush=True)

    risers = {'X_RiserL', 'X_RiserR', 'Y_RiserL', 'Y_RiserR'}
    fr = {f'{mat}_{g}': np.zeros(tuple(grid.n), np.float32) for mat in ('eg', 'st') for g in ('base', 'up', 'beam')}
    boxes, steel = {}, {}
    for p in m.parts:
        n = p['name']
        if any(n.startswith(t) for t in ('Y_BK12', 'Y_BF12', 'X_BK10', 'X_BF10', 'Y_Block', 'X_Block', 'Y_Screw', 'X_Screw')):
            bb = p['shape'].BoundBox
            boxes[n] = [bb.XMin, bb.YMin, bb.ZMin, bb.XMax, bb.YMax, bb.ZMax]
        if n not in m.structure and n not in risers and not n.endswith('Casting'):
            continue
        if p['look'] in ('printed', 'rubber') or any(n.startswith(t) for t in SKIP):
            continue
        mat = 'eg' if p['look'] == 'granite' else 'st'
        a = fractions(p['shape'], grid)
        fr[f"{mat}_{GROUP[p['container']]}"] += a
        if PARTS and mat == 'st':
            steel[n] = a
        print('  ', n, flush=True)

    # The base with no underside pockets: the optimization's design space.
    m2 = ns['Model']()
    g = ns['frame_layout'](d)
    st = ns['Steel'](m2)
    pockets = ns['base_pockets']
    ns['base_pockets'] = lambda g: []
    vols = [ns['base_half'](m2, g, st, front) for front in (True, False)]
    ns['base_pockets'] = pockets
    solid = np.zeros(tuple(grid.n), np.float32)
    for p in m2.parts:
        if p['name'].endswith('Casting'):
            solid += fractions(p['shape'], grid)
    print('solid base volume', sum(vols) / 1e6, 'L', flush=True)

    np.savez_compressed(OUT + '.npz', eg_base_solid=solid, **{k: np.clip(v, 0, 1) for k, v in fr.items()})
    if PARTS:
        np.savez_compressed(OUT + '_parts.npz', **steel)
    keys = ['base_top', 'table_top', 'beam_bot', 'beam_top', 'beam_face', 'inner', 'outer', 'up_y0', 'up_y1',
            'base_half', 'base_y0', 'base_y1', 'tip', 'nut_tip', 'y_bk', 'beam_cz', 'car_back']
    info = dict(h=H, origin=grid.o.tolist(), n=grid.n.tolist(), dims={k: float(d[k]) for k in keys}, boxes=boxes,
                legs=g['legs'], dowel_ys=list(g['dowel_ys']), ux=g['ux'],
                P={k: P[k] for k in ('table_rail_spacing', 'table_blk_pitch', 'beam_rail_spacing', 'beam_blk_pitch',
                                     'riser_w', 'table_riser_t', 'beam_riser_t', 'base_h', 'travel_x', 'travel_y',
                                     'travel_z', 'base_core_skin', 'table_len', 'table_w', 'table_t', 'carriage_w')},
                vols={k: v for k, v in d['casting_vols'].items()}, solid_base_L=sum(vols) / 1e6)
    json.dump(info, open(OUT + '.json', 'w'), indent=1)
    for k, v in fr.items():
        print(k, round(float(v.sum()) * H ** 3 / 1e6, 2), 'L')


main()
