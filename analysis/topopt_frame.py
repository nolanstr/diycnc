"""Topology optimization of the base and the uprights together, in the current frame.

    python topopt_frame.py 34.6        # total epoxy granite for base + both uprights, litres

One epoxy-granite budget is shared by the base and the two uprights, so the optimizer can
also move material between them. The beam and all the cast-in steel stay as drawn.

Base: pockets open to the underside, as in topopt.py ("pocket" mode).
Uprights: free 3D SIMP inside a larger allowed region: the strip beside the table
(the uprights' x range), from near the front of the base to the back, from the base top to
the beam. Closed voids are allowed (printed shell cores stay in the casting). Both uprights
share one design (mirrored). Kept solid: 10 mm around the posts, tie rods and top plate,
the seat under the beam, and the current foot's contact layer.
"""

import sys
import time
import warnings

import numpy as np
import scipy.ndimage as ndi

from loads import cases, domain_mask, setup
from topopt import R_FILTER, SKIN, filter_matrix, passive_solid
from vfe import E_EG, E_MIN, E_ST, Voxels


def upright_domain(vox):
    d = vox.d
    X, Y, Z = np.meshgrid(vox.centres(0), vox.centres(1), vox.centres(2), indexing='ij')
    side = (np.abs(X) > d['inner']) & (np.abs(X) < d['outer'])
    span = (Y > d['base_y0'] + 40.0) & (Y < d['base_y1'] - 15.0)
    height = (Z > d['base_top']) & (Z < d['beam_bot'] - 5.0)
    dom = side & span & height
    return dom & (X < 0), dom & (X > 0)


def main(target_L, iters=100, tag=None):
    warnings.filterwarnings('ignore', message='Matrix is nearly singular')
    vox = Voxels('vox_current')
    h, d, f = vox.h, vox.d, vox.f
    upL3, upR3 = upright_domain(vox)
    mesh = setup(vox, domain_mask(vox) | upL3 | upR3)
    F, labels = cases(mesh, vox, xs=(0.0, 90.0))
    nlc = F.shape[1]
    fld = mesh.field
    st = fld(f['st_base']) + fld(f['st_up']) + fld(f['st_beam'])
    eg_beam = fld(f['eg_beam'])

    # ---- base (pocket columns) ------------------------------------------
    passive3, base3 = passive_solid(vox)
    eg_solid = fld(f['eg_base_solid'])
    in_base, passive_b = fld(base3), fld(passive3)
    de_b = np.nonzero(in_base & ~passive_b)[0]
    vb = eg_solid * h ** 3 / 1e6
    H = d['base_top']
    ijk = mesh.ijk[de_b]
    cols, col_of = np.unique(ijk[:, 0] * 10000 + ijk[:, 1], return_inverse=True)
    pas = passive3 & base3
    lowest = np.where(pas.any(2), np.argmax(pas, axis=2), int(round(H / h)))
    ci, cj = cols // 10000, cols % 10000
    Dmin = np.maximum(np.minimum(H, H - lowest[ci, cj] * h), SKIN)
    span = H - Dmin
    depth_top = H - (ijk[:, 2] + 1) * h
    Wb = filter_matrix(np.column_stack([ci, cj]) * h, R_FILTER)

    def rho_base(s):
        D = Dmin + (Wb @ s) * span
        return np.clip((D[col_of] - depth_top) / h, 0, 1)

    # ---- uprights (free 3D, mirrored) -----------------------------------
    eg_dom3 = np.clip(1.0 - f['st_up'], 0, 1)
    X, Y, Z = np.meshgrid(vox.centres(0), vox.centres(1), vox.centres(2), indexing='ij')
    cur = f['eg_up'] > 0.5
    keep = ndi.binary_dilation(f['st_up'] > 0.02, np.ones((3, 3, 3), bool))
    keep |= cur & (Z > d['beam_bot'] - 25.0)           # seat under the beam
    keep |= cur & (Z < d['base_top'] + 15.0)           # contact layer of the current foot
    in_up = fld(upL3 | upR3)
    eg_dom = np.where(in_up, fld(eg_dom3), 0.0)
    passive_u = in_up & fld(keep)
    vu = eg_dom * h ** 3 / 1e6
    # map right-side elements onto the left-side variables (x mirrored)
    nx = vox.n[0]
    idx = {tuple(t): e for e, t in enumerate(mesh.ijk)}
    de_uL = np.nonzero(fld(upL3) & ~passive_u)[0]
    de_uR = np.array([idx[(nx - 1 - i, j, k)] for i, j, k in mesh.ijk[de_uL]])
    Wu = filter_matrix(mesh.ijk[de_uL] * h, R_FILTER)
    beta, eta, pen = 1.0, 0.5, 3.0

    def proj(xt):
        a, b = np.tanh(beta * eta), np.tanh(beta * (1 - eta))
        return (a + np.tanh(beta * (xt - eta))) / (a + b), beta * (1 - np.tanh(beta * (xt - eta)) ** 2) / (a + b)

    v_fixed = vb[passive_b].sum() + vu[passive_u].sum()
    print(f'base max {vb[in_base].sum():.1f} L, upright domain {vu[in_up].sum():.1f} L (both), '
          f'fixed {v_fixed:.1f} L, target {target_L} L', flush=True)

    def moduli(rb, ru):
        base_eg = np.where(in_base, eg_solid, 0.0)
        base_eg[de_b] = eg_solid[de_b] * rb
        up_eg = np.where(passive_u, eg_dom, 0.0)
        up_eg[de_uL] = eg_dom[de_uL] * (E_MIN + (1 - E_MIN) * ru ** pen)
        up_eg[de_uR] = eg_dom[de_uR] * (E_MIN + (1 - E_MIN) * ru ** pen)
        return E_MIN * E_EG + E_EG * (base_eg + up_eg + eg_beam) + E_ST * st, base_eg, up_eg

    # reference: the current design
    E0 = E_MIN * E_EG + E_EG * (fld(f['eg_base']) + fld(f['eg_up']) + eg_beam) + E_ST * st
    C0 = (F * mesh.solve(E0, F)).sum(0)
    cur_L = (fld(f['eg_base']).sum() + fld(f['eg_up']).sum()) * h ** 3 / 1e6
    print(f'current base + uprights: {cur_L:.1f} L', flush=True)

    nb = len(cols)
    x = np.r_[np.full(nb, 0.5), np.full(len(de_uL), 0.3)]
    move = np.r_[np.full(nb, 0.05), np.full(len(de_uL), 0.1)]

    def volume(x):
        rb = rho_base(x[:nb])
        ru = proj(Wu @ x[nb:])[0]
        return v_fixed + (rb * vb[de_b]).sum() + (ru * (vu[de_uL] + vu[de_uR])).sum()

    hist = []
    for it in range(iters):
        t = time.time()
        if it and it % 20 == 0 and beta < 8:
            beta *= 2
        rb = rho_base(x[:nb])
        ru, dru = proj(Wu @ x[nb:])
        E, base_eg, up_eg = moduli(rb, ru)
        U = mesh.solve(E, F)
        C = (F * U).sum(0)
        J = (C / C0).mean()
        dJdE = -(mesh.energy(U) / C0).sum(1) / nlc
        # base: thickness sensitivities (d rho / d D = 1/h in the element holding the bottom face)
        inside = (rb > 0) & (rb < 1)
        g_e = np.where(inside, dJdE[de_b] * E_EG * eg_solid[de_b] / h, 0.0)
        gv_e = np.where(inside, vb[de_b] / h, 0.0)
        dJ_b = Wb.T @ (np.bincount(col_of, weights=g_e, minlength=nb) * span)
        dV_b = Wb.T @ (np.bincount(col_of, weights=gv_e, minlength=nb) * span) + 1e-9
        # uprights: both sides feed the shared variable
        dEdr = E_EG * (1 - E_MIN) * pen * ru ** (pen - 1)
        dJ_u = Wu.T @ ((dJdE[de_uL] * eg_dom[de_uL] + dJdE[de_uR] * eg_dom[de_uR]) * dEdr * dru)
        dV_u = Wu.T @ ((vu[de_uL] + vu[de_uR]) * dru) + 1e-9
        dJ, dV = np.minimum(np.r_[dJ_b, dJ_u], -1e-12), np.r_[dV_b, dV_u]
        V = volume(x)
        k = 1e3 / C
        hist.append((J, V, *k))
        vb_now = base_eg.sum() * h ** 3 / 1e6
        vu_now = (up_eg[in_up]).sum() * h ** 3 / 1e6
        print(f'{it:3d} J {J:.4f} V {V:5.2f} L (base {vb_now:4.1f}, uprights {vu_now:4.1f})  '
              f'k x/y/z {k[0::3].mean():5.1f} {k[1::3].mean():5.1f} {k[2::3].mean():5.1f}  {time.time() - t:4.1f} s',
              flush=True)
        l1, l2 = 1e-12, 1e12
        while l2 / l1 > 1 + 1e-6:
            lm = np.sqrt(l1 * l2)
            xn = np.clip(x * np.sqrt(-dJ / (lm * dV)), np.maximum(0, x - move), np.minimum(1, x + move))
            if volume(xn) > target_L:
                l1 = lm
            else:
                l2 = lm
        x = xn

    tag = tag or f'frame_{target_L:g}'
    rho_b3 = np.zeros(tuple(vox.n), np.float32)
    rho_u3 = np.zeros(tuple(vox.n), np.float32)
    rb = rho_base(x[:nb])
    ru = proj(Wu @ x[nb:])[0]
    full_b = np.where(in_base, 1.0, 0.0)
    full_b[de_b] = rb
    rho_b3[mesh.ijk[:, 0], mesh.ijk[:, 1], mesh.ijk[:, 2]] = np.where(in_base, full_b, 0.0)
    full_u = np.where(passive_u, 1.0, 0.0)
    full_u[de_uL] = ru
    full_u[de_uR] = ru
    rho_u3[mesh.ijk[:, 0], mesh.ijk[:, 1], mesh.ijk[:, 2]] = full_u
    np.savez_compressed(f'to_{tag}.npz', rho=rho_b3, rho_up=rho_u3, hist=np.array(hist), labels=labels, C0=C0)
    print('saved', f'to_{tag}.npz')


if __name__ == '__main__':
    main(float(sys.argv[1]), int(sys.argv[2]) if len(sys.argv) > 2 else 100)
