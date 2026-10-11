"""Lightening holes in the uprights: topology optimization inside the current (raked) upright.

    python topopt_upright.py 0.75            # keep 75 % of the upright's epoxy granite, holes go right through
    python topopt_upright.py 0.75 web        # same, but a 20 mm web on the inner face stays solid
                                             # (pockets from the outer face instead of holes)

The base, the beam and all the steel stay as drawn; only the uprights' epoxy granite changes.
The design is a side profile (y, z) cut straight through the upright's width (or through
all but the inner web), so it casts with plain printed cores. Both uprights are the same
(mirrored). Kept solid: 10 mm around the posts and tie rods, the top 25 mm under the beam
and the bottom 15 mm on the base.
"""

import sys
import time
import warnings

import numpy as np
import scipy.ndimage as ndi

from loads import cases, domain_mask, setup
from topopt import filter_matrix
from vfe import E_EG, E_MIN, E_ST, Voxels

R_FILTER = 25.0
WEB = 20.0


def main(frac, web=False, iters=60, tag=None):
    warnings.filterwarnings('ignore', message='Matrix is nearly singular')
    vox = Voxels('vox_current')
    h, d, f = vox.h, vox.d, vox.f
    mesh = setup(vox, domain_mask(vox))
    F, labels = cases(mesh, vox, xs=(0.0, 90.0))
    nlc = F.shape[1]
    fld = mesh.field
    st = fld(f['st_base']) + fld(f['st_up']) + fld(f['st_beam'])
    eg_fix = fld(f['eg_base']) + fld(f['eg_beam'])
    eg_up = fld(f['eg_up'])

    X, Y, Z = np.meshgrid(vox.centers(0), vox.centers(1), vox.centers(2), indexing='ij')
    keep = ndi.binary_dilation(f['st_up'] > 0.02, np.ones((3, 3, 3), bool))
    keep |= (Z > d['beam_bot'] - 25.0) | (Z < d['base_top'] + 15.0)
    up = eg_up > 0.01
    # the elements that may be cut: all of the upright, or all but the inner web
    out = up & ~fld(np.abs(X) < d['inner'] + WEB) if web else up
    # a (y, z) column is fixed solid if any of it must be (a hole has to clear it all the way through)
    jk = mesh.ijk[:, 1] * 1000 + mesh.ijk[:, 2]
    de = np.nonzero(out & ~np.isin(jk, np.unique(jk[out & fld(keep)])))[0]
    cols, col_of = np.unique(jk[de], return_inverse=True)
    W = filter_matrix(np.column_stack([cols // 1000, cols % 1000]) * h, R_FILTER)
    v_e = eg_up * h ** 3 / 1e6
    v_up = v_e[up].sum()
    v_fix = v_up - v_e[de].sum()
    target = frac * v_up
    print(f'uprights {v_up:.2f} L (both), fixed {v_fix:.2f} L, target {target:.2f} L, {len(cols)} columns', flush=True)
    beta, eta, pen = 1.0, 0.5, 3.0

    def proj(xt):
        a, b = np.tanh(beta * eta), np.tanh(beta * (1 - eta))
        return (a + np.tanh(beta * (xt - eta))) / (a + b), beta * (1 - np.tanh(beta * (xt - eta)) ** 2) / (a + b)

    def field(r):
        e = eg_up.copy()
        e[de] = eg_up[de] * (E_MIN + (1 - E_MIN) * r[col_of] ** pen)
        return e

    E0 = E_MIN * E_EG + E_EG * (eg_fix + eg_up) + E_ST * st
    C0 = (F * mesh.solve(E0, F)).sum(0)
    vcol = np.bincount(col_of, weights=v_e[de], minlength=len(cols))

    def volume(x):
        return v_fix + (proj(W @ x)[0] * vcol).sum()

    x = np.full(len(cols), frac)
    hist = []
    for it in range(iters):
        t = time.time()
        if it and it % 15 == 0 and beta < 16:
            beta *= 2
        r, dr = proj(W @ x)
        up_e = field(r)
        U = mesh.solve(E_MIN * E_EG + E_EG * (eg_fix + up_e) + E_ST * st, F)
        C = (F * U).sum(0)
        J = (C / C0).mean()
        dJdE = -(mesh.energy(U) / C0).sum(1) / nlc
        g = dJdE[de] * E_EG * eg_up[de] * (1 - E_MIN) * pen * r[col_of] ** (pen - 1)
        dJ = np.minimum(W.T @ (np.bincount(col_of, weights=g, minlength=len(cols)) * dr), -1e-12)
        dV = W.T @ (vcol * dr) + 1e-12
        k = 1e3 / C
        V = volume(x)
        hist.append((J, V, *k))
        print(f'{it:3d} J {J:.4f} V {V:5.2f} L  k x/y/z {k[0::3].mean():5.1f} {k[1::3].mean():5.1f} '
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

    tag = tag or f'upright_{"web" if web else "thru"}_{frac:g}'
    r = proj(W @ x)[0]
    rho = np.zeros(tuple(vox.n), np.float32)
    full = np.where(up, 1.0, 0.0)
    full[de] = r[col_of]
    rho[mesh.ijk[:, 0], mesh.ijk[:, 1], mesh.ijk[:, 2]] = full
    np.savez_compressed(f'to_{tag}.npz', rho_up=rho, hist=np.array(hist), labels=labels, C0=C0)
    print('saved', f'to_{tag}.npz')


if __name__ == '__main__':
    main(float(sys.argv[1]), len(sys.argv) > 2 and sys.argv[2] == 'web')
