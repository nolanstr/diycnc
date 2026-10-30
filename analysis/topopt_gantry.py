"""Aggressive lightening of the gantry: the uprights and the beam optimized together on one budget.

    python topopt_gantry.py 0.6              # keep 60 % of the uprights' and the beam's epoxy granite
    python lean_study.py lean0: gantry_0.6:  # then judge it at the tool, by its modes and its mass
    python topopt_gantry.py 0.7 lean0_h7.5   # from other voxels (here 7.5 mm): writes vox_gantry_0.7_lean0_h7.5

Free 3D in both (closed voids are fine: printed or XPS cores left in the casting, as in topopt_frame.py), the
same on both sides of x = 0. Kept solid in both: 10 mm around
all the cast-in steel and 15 mm round the tie rods (rods.json), a 20 mm skin on the beam, the top 25 mm of each upright under the beam and its bottom
15 mm on the base. The base and all the steel stay as drawn. The objective is the frame's mean compliance over
the load cases; the result is thresholded and written as vox_gantry_<frac> (with vox_lean0's per-part steel).
"""

import json
import os
import shutil
import sys
import time
import warnings

import numpy as np
import scipy.ndimage as ndi

from loads import cases, domain_mask, setup
from topopt import filter_matrix
from vfe import E_EG, E_MIN, E_ST, Voxels

HERE = os.path.dirname(os.path.abspath(__file__))
R_FILTER = 25.0
SKIN = 20.0


def design_domain(vox, mesh):
    """The uprights' and beam's epoxy granite the optimizer may take out: design elements `de`, grouped in
    columns mirrored about x = 0 (`col_of`), their density filter `W`, and the volumes the budget counts."""
    h, d, f = vox.h, vox.d, vox.f
    fld = mesh.field
    st = fld(f['st_base']) + fld(f['st_up']) + fld(f['st_beam'])
    eg_base, eg_up, eg_beam = fld(f['eg_base']), fld(f['eg_up']), fld(f['eg_beam'])

    X, Y, Z = np.meshgrid(vox.centers(0), vox.centers(1), vox.centers(2), indexing='ij')
    near_steel = ndi.distance_transform_edt((f['st_up'] + f['st_beam']) <= 0.02) * h <= 10.0 + 1e-6
    beam_solid = (f['eg_beam'] + f['st_beam']) > 0.01
    skin = beam_solid & (ndi.distance_transform_edt(beam_solid) * h <= SKIN)
    keep = near_steel | skin | (Z > d['beam_bot'] - 25.0) & (f['eg_up'] > 0.01) | (Z < d['base_top'] + 15.0)
    # the uprights' tie rods aren't in the voxels (they're unbonded): keep 15 mm round each (rods.json, from the model)
    for n, bb in json.load(open(os.path.join(HERE, 'rods.json'))).items():
        if n.startswith('TieRod') and 'Nut' not in n:
            keep |= ((X > bb[0] - 15) & (X < bb[3] + 15) & (Y > bb[1] - 15) & (Y < bb[4] + 15) &
                     (Z > bb[2]) & (Z < bb[5]))
    keep = fld(keep)

    # design elements, free in 3D (closed voids are fine: printed or XPS cores stay in the casting) and the same
    # on both sides of x = 0 (the uprights mirrored, the beam symmetric)
    up = eg_up > 0.01
    region = (up | (eg_beam > 0.01)) & ~keep
    de = np.nonzero(region)[0]
    ax = np.abs(mesh.center[de, 0])
    key = np.column_stack([np.round(ax / h), mesh.ijk[de, 1], mesh.ijk[de, 2]]).astype(int)
    cols, col_of = np.unique(key, axis=0, return_inverse=True)
    col_of = col_of.ravel()
    W = filter_matrix(cols * h, R_FILTER)
    eg_d = eg_up + eg_beam
    v_e = eg_d * h ** 3 / 1e6
    v_all = v_e[up | (eg_beam > 0.01)].sum()
    v_fix = v_all - v_e[de].sum()
    vcol = np.bincount(col_of, weights=v_e[de], minlength=len(cols))
    return dict(de=de, cols=cols, col_of=col_of, W=W, eg_d=eg_d, v_all=v_all, v_fix=v_fix, vcol=vcol, st=st,
                eg_base=eg_base)


def main(frac, src='lean0', iters=80):
    warnings.filterwarnings('ignore', message='Matrix is nearly singular')
    SRC = 'vox_' + src
    vox = Voxels(SRC)
    h, f = vox.h, vox.f
    mesh = setup(vox, domain_mask(vox))
    F, labels = cases(mesh, vox, xs=(0.0, 90.0))
    nlc = F.shape[1]
    dd = design_domain(vox, mesh)
    de, cols, col_of, W, eg_d = dd['de'], dd['cols'], dd['col_of'], dd['W'], dd['eg_d']
    v_all, v_fix, vcol, st, eg_base = dd['v_all'], dd['v_fix'], dd['vcol'], dd['st'], dd['eg_base']
    target = frac * v_all
    print(f'uprights + beam {v_all:.2f} L, fixed {v_fix:.2f} L, target {target:.2f} L, {len(cols)} variables',
          flush=True)
    beta, eta, pen = 1.0, 0.5, 3.0

    def proj(xt):
        a, b = np.tanh(beta * eta), np.tanh(beta * (1 - eta))
        return (a + np.tanh(beta * (xt - eta))) / (a + b), beta * (1 - np.tanh(beta * (xt - eta)) ** 2) / (a + b)

    def field(r):
        e = eg_d.copy()
        e[de] = eg_d[de] * (E_MIN + (1 - E_MIN) * r[col_of] ** pen)
        return e

    E0 = E_MIN * E_EG + E_EG * (eg_base + eg_d) + E_ST * st
    C0 = (F * mesh.solve(E0, F)).sum(0)

    def volume(x):
        return v_fix + (proj(W @ x)[0] * vcol).sum()

    x = np.full(len(cols), frac)
    for it in range(iters):
        t = time.time()
        if it and it % 15 == 0 and beta < 16:
            beta *= 2
        r, dr = proj(W @ x)
        U = mesh.solve(E_MIN * E_EG + E_EG * (eg_base + field(r)) + E_ST * st, F)
        C = (F * U).sum(0)
        J = (C / C0).mean()
        dJdE = -(mesh.energy(U) / C0).sum(1) / nlc
        g = dJdE[de] * E_EG * eg_d[de] * (1 - E_MIN) * pen * r[col_of] ** (pen - 1)
        dJ = np.minimum(W.T @ (np.bincount(col_of, weights=g, minlength=len(cols)) * dr), -1e-12)
        dV = W.T @ (vcol * dr) + 1e-12
        k = 1e3 / C
        print(f'{it:3d} J {J:.4f} V {volume(x):5.2f} L  k x/y/z {k[0::3].mean():5.1f} {k[1::3].mean():5.1f} '
              f'{k[2::3].mean():5.1f}  beta {beta:g}  {time.time() - t:4.1f} s', flush=True)
        l1, l2 = 1e-12, 1e12
        while l2 / l1 > 1 + 1e-6:
            lm = np.sqrt(l1 * l2)
            xn = np.clip(x * np.sqrt(-dJ / (lm * dV)), np.maximum(0, x - 0.1), np.minimum(1, x + 0.1))
            if volume(xn) > target:
                l1 = lm
            else:
                l2 = lm
        x = xn

    # threshold and write the frame with the cuts, for lean_study.py, modal.py and chain.py
    cut = np.zeros(mesh.center.shape[0], bool)
    cut[de] = proj(W @ x)[0][col_of] < 0.5
    out = {k: v.copy() for k, v in f.items()}
    i, j, kk = mesh.ijk[cut].T
    for g in ('up', 'beam'):
        out[f'eg_{g}'][i, j, kk] = 0.0
    name = f'vox_gantry_{frac:g}' + ('' if src == 'lean0' else '_' + src)
    np.savez_compressed(os.path.join(HERE, name + '.npz'), **out)
    info = json.load(open(os.path.join(HERE, SRC + '.json')))
    json.dump(info, open(os.path.join(HERE, name + '.json'), 'w'))
    shutil.copy(os.path.join(HERE, SRC + '_parts.npz'), os.path.join(HERE, name + '_parts.npz'))
    left = sum(out[f'eg_{g}'].sum() for g in ('up', 'beam')) * h ** 3 / 1e6
    print(f'saved {name}: uprights + beam {left:.2f} L of {v_all:.2f}', flush=True)


if __name__ == '__main__':
    main(float(sys.argv[1]), *sys.argv[2:3])
