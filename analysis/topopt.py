"""Topology optimization of the base casting, inside the full frame model.

    python topopt.py pocket 21     # pockets open to the underside (removable cores), 21 L of EG
    python topopt.py free 21       # any shape (lost foam cores), 21 L of EG

Objective: the sum over the load cases of each case's compliance relative to the current
design, i.e. the frame's share of the tool-to-work deflection. The uprights, beam and all
cast-in steel stay as modeled; only the base's epoxy granite is redistributed.

Kept solid: a 20 mm top skin (the optimizer can thicken it), 10 mm of casting around all
cast-in steel and the sockets, the split face's gasket band and side walls, the floor under
the coolant trough and a column around the drain.

pocket: each underside column is solid from the top down to a depth D (>= the passive
        depth), so every void is a pocket open to the bottom. Filter radius 15 mm.
free:   3D SIMP (p = 3) with a 15 mm density filter and a Heaviside projection.
"""

import sys
import time
import warnings

import numpy as np
import scipy.ndimage as ndi
import scipy.sparse as sp

from loads import cases, domain_mask, moduli, setup
from vfe import E_EG, E_MIN, Voxels

SKIN = 20.0
R_FILTER = 15.0


def passive_solid(vox):
    f, h, d = vox.f, vox.h, vox.d
    X, Y, Z = np.meshgrid(vox.centers(0), vox.centers(1), vox.centers(2), indexing='ij')
    base = f['eg_base_solid'] > 0.01
    steel = (f['st_base'] > 0.02) | ((f['st_up'] > 0.02) & (Z < d['base_top']))
    near = ndi.binary_dilation(steel, np.ones((3, 3, 3), bool))
    top = d['base_top']
    half, y0 = d['base_half'], d['base_y0']
    split = (np.abs(Y) < 20.0) & ((Z > top - 25.0) | (np.abs(X) > half - 40.0))     # gasket band + draw-rod walls
    trough = (Y < y0 + 70.0) & (Z > top - 50.0)                                   # floor under the coolant trough
    drain = (X ** 2 + (Y - (y0 + 30.0)) ** 2) < 25.0 ** 2                          # around the drain, full depth
    p = (Z > top - SKIN) | near | split | trough | drain
    return p & base, base


def filter_matrix(coords, r):
    """Linear (cone) density filter over points `coords` (n x k), radius r, rows normalized."""
    from scipy.spatial import cKDTree
    t = cKDTree(coords)
    pairs = t.query_pairs(r, output_type='ndarray')
    i = np.r_[pairs[:, 0], pairs[:, 1], np.arange(len(coords))]
    j = np.r_[pairs[:, 1], pairs[:, 0], np.arange(len(coords))]
    w = r - np.linalg.norm(coords[i] - coords[j], axis=1)
    W = sp.csr_matrix((w, (i, j)), shape=(len(coords),) * 2)
    return sp.diags(1 / np.asarray(W.sum(1)).ravel()) @ W


def oc(x, dJ, dV, vol_fn, target, move, lo=0.0, hi=1.0):
    """Optimality-criteria update with bisection on the volume multiplier."""
    dJ = np.minimum(dJ, -1e-12)
    l1, l2 = 1e-12, 1e12
    while l2 / l1 > 1 + 1e-6:
        lm = np.sqrt(l1 * l2)
        xn = np.clip(x * np.sqrt(-dJ / (lm * np.maximum(dV, 1e-12))), np.maximum(lo, x - move), np.minimum(hi, x + move))
        if vol_fn(xn) > target:
            l1 = lm
        else:
            l2 = lm
    return xn


def main(mode, target_L, iters=None, tag=None):
    warnings.filterwarnings('ignore', message='Matrix is nearly singular')
    vox = Voxels()
    h, d, f = vox.h, vox.d, vox.f
    mesh = setup(vox, domain_mask(vox))
    F, labels = cases(mesh, vox)
    nlc = F.shape[1]
    passive3, base3 = passive_solid(vox)
    eg_solid = mesh.field(f['eg_base_solid'])
    in_base = mesh.field(base3)
    passive = mesh.field(passive3)
    design = in_base & ~passive
    v_el = eg_solid * h ** 3 / 1e6             # L of EG per element at full density
    v_fixed = v_el[passive].sum()
    print(f'{mode}: base EG max {v_el[in_base].sum():.1f} L, passive {v_fixed:.1f} L, target {target_L} L', flush=True)

    # reference compliances: the current design
    U0 = mesh.solve(moduli(mesh, f, mesh.field(f['eg_base'])), F)
    C0 = (F * U0).sum(0)

    de = np.nonzero(design)[0]
    ijk = mesh.ijk[de]
    if mode == 'pocket':
        H = d['base_top']
        # columns: all base columns; depth of the passive material in each
        cols, col_of = np.unique(ijk[:, 0] * 10000 + ijk[:, 1], return_inverse=True)
        top_k = int(round(H / h))
        pas = passive3 & base3
        lowest = np.where(pas.any(2), np.argmax(pas, axis=2), top_k)   # first passive layer from the bottom
        # everything above the lowest passive voxel must stay (closed voids are not allowed)
        ci, cj = cols // 10000, cols % 10000
        Dmin = np.minimum(H, H - lowest[ci, cj] * h)
        Dmin = np.maximum(Dmin, SKIN)
        # design elements above the lowest passive one are forced solid
        depth_top = H - (ijk[:, 2] + 1) * h          # depth of the element's top face
        Wf = filter_matrix(np.column_stack([ci, cj]) * h, R_FILTER)
        s = np.full(len(cols), 0.5)
        span = H - Dmin

        def rho_of(s):
            D = Dmin + (Wf @ s) * span
            return np.clip((D[col_of] - depth_top) / h, 0, 1), D

        def vol(s):
            return v_fixed + (rho_of(s)[0] * v_el[de]).sum()
        pen, move, x = 1.0, 0.05, s
        iters = iters or 80
    else:
        Wf = filter_matrix(ijk * h, R_FILTER)
        x = np.full(len(de), 0.5)
        beta, eta = 1.0, 0.5

        def proj(xt, beta):
            a, b = np.tanh(beta * eta), np.tanh(beta * (1 - eta))
            return (a + np.tanh(beta * (xt - eta))) / (a + b), beta * (1 - np.tanh(beta * (xt - eta)) ** 2) / (a + b)

        def vol(x):
            return v_fixed + (proj(Wf @ x, beta)[0] * v_el[de]).sum()
        pen, move = 3.0, 0.1
        iters = iters or 120

    hist = []
    rho_e = np.ones(mesh.ne)
    for it in range(iters):
        t = time.time()
        if mode == 'pocket':
            r, D = rho_of(x)
        else:
            if it and it % 25 == 0 and beta < 16:
                beta *= 2
            r, drdxt = proj(Wf @ x, beta)
        base_eg = np.where(in_base, eg_solid, 0.0)
        rho_e[:] = 1.0
        rho_e[de] = r
        Eb = base_eg * (E_MIN + (1 - E_MIN) * rho_e ** pen)
        U = mesh.solve(moduli(mesh, f, Eb), F)
        C = (F * U).sum(0)
        J = (C / C0).sum() / nlc
        en = mesh.energy(U)[de]                                   # ne_design x nlc
        dJdr = -(en / C0).sum(1) / nlc * E_EG * base_eg[de] * (1 - E_MIN) * pen * r ** (pen - 1)
        if mode == 'pocket':
            # d rho / d D = 1/h where the column's bottom face lies inside the element
            inside = (r > 0) & (r < 1)
            g_col = np.bincount(col_of, weights=np.where(inside, dJdr / h, 0.0), minlength=len(x))
            gv_col = np.bincount(col_of, weights=np.where(inside, v_el[de] / h, 0.0), minlength=len(x))
            dJ = Wf.T @ (g_col * span)
            dV = Wf.T @ (gv_col * span) + 1e-9
        else:
            dJ = Wf.T @ (dJdr * drdxt)
            dV = Wf.T @ (v_el[de] * drdxt)
        V = vol(x)
        k = 1e3 / C
        hist.append((J, V, *k))
        print(f'{it:3d} J {J:.4f} V {V:5.2f} L  k(x/y/z, table 0) {k[3]:5.1f} {k[4]:5.1f} {k[5]:5.1f}  {time.time() - t:4.1f} s',
              flush=True)
        if it > 10 and mode == 'pocket' and abs(hist[-1][0] - hist[-6][0]) < 1e-4:
            break
        x = oc(x, dJ, dV, vol, target_L, move)

    tag = tag or f'{mode}_{target_L:g}'
    rho3 = np.zeros(tuple(vox.n), np.float32)
    rho3[mesh.ijk[:, 0], mesh.ijk[:, 1], mesh.ijk[:, 2]] = np.where(in_base, rho_e, 0.0)
    out = dict(rho=rho3, hist=np.array(hist), labels=labels, k=k, C0=C0, passive=passive3)
    if mode == 'pocket':
        Dmap = np.zeros(tuple(vox.n[:2]), np.float32)
        Dmap[ci, cj] = D
        out['depth'] = Dmap
    np.savez_compressed(f'to_{tag}.npz', **out)
    print('saved', f'to_{tag}.npz')


if __name__ == '__main__':
    main(sys.argv[1], float(sys.argv[2]), int(sys.argv[3]) if len(sys.argv) > 3 else None)
