"""The uprights' and beam's epoxy granite placed for damping: the castings optimized against the resonant
peaks at the tool, with the static stiffness weighted lightly, on a budget of epoxy granite (the cost).

    FEA_SYM=1 python topopt_damped.py 0.7 sym10            # keep 70 % of the uprights' and beam's epoxy granite
    FEA_SYM=1 python topopt_damped.py 0.7 sym10 --check    # the gradient against finite differences first
    FEA_SYM=1 python topopt_damped.py 0.7 sym10 --resume   # carry on from the last saved iteration

Stage 2 of the frame optimization (stage 1 is the steel, steel_opt.py). The design space and its rules are
topopt_gantry.py's (the same keep-solid regions, mirrored, free 3D, 25 mm filter), and so is the result:
vox_damped_<frac>_<voxels> for damping.py, lean_study.py, modal.py and chain.py.

Objective, with damping.py's loss factors (epoxy granite 0.02, steel 0.0005):

    J = W_STATIC * mean_c C_c / C_c0  +  W_DYN * || P_ic / P_0 ||_8

C_c is the static compliance in load case c (tool against work) and P_ic = (phi_i . F_c)^2 / (phi_i^T K_eta phi_i)
the resonant peak of mode i in case c (damping.py); the 8-norm over modes and cases is a smooth stand-in for the
worst peak. Epoxy granite raises a mode's damping where it carries strain energy, adds mass, and stiffens.

Sensitivities: the eigenvalues' are exact; the mode shapes' come from the other modes (Fox and Kapoor's modal
expansion over the K_MODES lowest) plus the static flexibility of the modes above them (one solve per objective
mode), the modified modal method; --check compares them with finite differences. SIMP p = 3 for the stiffness and the loss, mass linear in the density above 0.1 and
r^6 below (so near-empty voxels don't make spurious local modes). Optimality criteria, with the variables whose
gradient is positive (they cost the objective) pushed down by the move limit.
"""

import json
import os
import shutil
import sys
import time
import warnings

import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import LinearOperator, eigsh

from damping import ETA_EG, ETA_ST
from loads import F0, cases, domain_mask, setup
from modal import RHO_EG, RHO_ST, mass_matrix
from topopt_gantry import design_domain
from vfe import E_EG, E_MIN, E_ST, Voxels

HERE = os.path.dirname(os.path.abspath(__file__))
W_STATIC, W_DYN = float(os.environ.get('TO_W_STATIC', 0.25)), float(os.environ.get('TO_W_DYN', 0.75))
Q = 8.0                 # p-norm exponent over the peaks
K_MODES = 24            # modes in the basis
K_BLOCK = 16            # asked of each symmetry family (the lowest K_MODES of both are kept)
N_OBJ = 12              # the lowest modes the objective counts
PEN = 3.0


class Factored:
    """K factorized once per iteration (per symmetry block with FEA_SYM) and used for the static cases, the
    eigenvalues (shift-invert at 0) and the higher modes' flexibility. The eigen solve starts from the last
    iteration's modes."""

    def __init__(self, mesh, E, warm):
        K = mesh.assemble(E)
        self.blocks = []
        if mesh.sym:
            for key, T in mesh.T.items():
                Kr = (T.T @ K @ T).tocsc()
                self.blocks.append((key, T, Kr, mesh.factored(key, Kr)))
        else:
            from damping import _factor
            self.blocks.append(('all', None, K, _factor(mesh, K)))
        self.warm = warm

    def solve(self, B):
        out = 0
        for _, T, _, fac in self.blocks:
            out = out + (fac.solve(B) if T is None else T @ fac.solve(T.T @ B))
        return out

    def eigen(self, M, k):
        """Lowest k eigenpairs, mass-normalized; each block asked for K_BLOCK of them (more if one block
        supplies all it was asked for)."""
        out = []
        for key, T, Kr, fac in self.blocks:
            Mr = M if T is None else (T.T @ M @ T).tocsc()
            op = LinearOperator(Kr.shape, matvec=lambda v, fac=fac: fac.solve(v), dtype=float)
            nb = self.warm.get(('n', key), K_BLOCK if T is not None else k)
            v0 = self.warm.get(key)
            lam, q = eigsh(Kr, k=nb, M=Mr, sigma=0.0, which='LM', OPinv=op, v0=v0, tol=1e-9)
            self.warm[key] = q.sum(1)
            out += [(lam[i], q[:, i] if T is None else T @ q[:, i], key) for i in range(len(lam))]
        out.sort(key=lambda t: t[0])
        kept = out[:k]
        for key, T, _, _ in self.blocks:
            if T is not None and sum(1 for t in kept if t[2] == key) >= self.warm.get(('n', key), K_BLOCK):
                self.warm[('n', key)] = self.warm.get(('n', key), K_BLOCK) + 6     # one family ran out: ask more next time
        return np.array([t[0] for t in kept]), np.column_stack([t[1] for t in kept])


def matrix(mesh, E):
    """sum E_e k_e, without the supports' springs (for K_eta: the supports don't damp)."""
    data = np.bincount(mesh.scatter, weights=np.outer(E, mesh.ke.ravel()).ravel(), minlength=mesh.nnz)
    return sp.csc_matrix((data, mesh.indices, mesh.indptr), shape=(mesh.ndof, mesh.ndof))


def cross_energy(mesh, a, b):
    """u_a^T k_e u_b per element (unit E)."""
    ua, ub = a[mesh.edof], b[mesh.edof]
    return np.einsum('ea,ab,eb->e', ua, mesh.ke, ub)


def cross_mass(mesh, a, b):
    """Lumped per-unit-mass product per element: (1/8) sum over its nodes of a_n . b_n."""
    an, bn = a.reshape(-1, 3), b.reshape(-1, 3)
    nodal = (an * bn).sum(1)
    return nodal[mesh.enodes].sum(1) / 8


class Problem:
    def __init__(self, vox):
        self.vox = vox
        self.mesh = mesh = setup(vox, domain_mask(vox))
        self.F, self.labels = cases(mesh, vox, xs=(0.0, 90.0))
        dd = self.dd = design_domain(vox, mesh)
        self.de, self.col_of, self.W, self.eg_d = dd['de'], dd['col_of'], dd['W'], dd['eg_d']
        self.st, self.eg_base = dd['st'], dd['eg_base']
        h = vox.h
        # the attached masses (head, table) and the steel's and base's mass are fixed; the design's EG varies
        self.M_fixed, _ = mass_matrix(mesh, vox, self.eg_base, self.st)
        self.h3 = h ** 3
        self.beta = 1.0
        self.C0 = self.P0 = None
        self.warm = {}

    def proj(self, xt):
        b, eta = self.beta, 0.5
        a, c = np.tanh(b * eta), np.tanh(b * (1 - eta))
        return (a + np.tanh(b * (xt - eta))) / (a + c), b * (1 - np.tanh(b * (xt - eta)) ** 2) / (a + c)

    def densities(self, x):
        r, dr = self.proj(self.W @ x)
        rho = np.ones(self.mesh.ne)            # 1 outside the design elements
        rho[self.de] = r[self.col_of]
        return rho, r, dr

    def fields(self, rho):
        sE = E_MIN + (1 - E_MIN) * rho ** PEN
        dsE = (1 - E_MIN) * PEN * rho ** (PEN - 1)
        low = rho < 0.1
        sM = np.where(low, 1e5 * rho ** 6, rho)
        dsM = np.where(low, 6e5 * rho ** 5, 1.0)
        egd = self.eg_d * sE
        E = E_MIN * E_EG + E_EG * (self.eg_base + egd) + E_ST * self.st
        Ee = ETA_EG * E_EG * (self.eg_base + egd) + ETA_ST * E_ST * self.st
        me = RHO_EG * self.eg_d * sM * self.h3                  # the design EG's mass per element (t)
        return E, Ee, me, E_EG * self.eg_d * dsE, RHO_EG * self.eg_d * dsM * self.h3

    def mass(self, me):
        nodal = np.bincount(self.mesh.enodes.ravel(), weights=np.repeat(me / 8, 8), minlength=self.mesh.nn)
        return self.M_fixed + sp.diags(np.repeat(nodal, 3)).tocsc()

    def evaluate(self, x, grad=True):
        mesh, F = self.mesh, self.F
        rho, r, dr = self.densities(x)
        E, Ee, me, dE, dm = self.fields(rho)
        fk = Factored(mesh, E, self.warm)
        U = fk.solve(F)
        C = (F * U).sum(0)
        lam, phi = fk.eigen(self.mass(me), K_MODES)
        Keta = matrix(mesh, Ee)
        KePhi = Keta @ phi
        Qm = phi[:, :N_OBJ].T @ KePhi                          # N_OBJ x K_MODES, Q_ij = phi_i^T K_eta phi_j
        D = np.diag(Qm[:, :N_OBJ]).copy()
        a = phi.T @ F / F0                                      # K_MODES x cases
        P = a[:N_OBJ] ** 2 / D[:, None]
        if self.C0 is None:
            self.C0, self.P0 = C.copy(), P.max()
        nlc = F.shape[1]
        Js = (C / self.C0).mean()
        S = ((P / self.P0) ** Q).sum()
        Jd = S ** (1 / Q)
        J = W_STATIC * Js + W_DYN * Jd
        info = dict(J=J, Js=Js, Jd=Jd, C=C, P=P, lam=lam, eta=D / lam[:N_OBJ], rho=rho)
        if not grad:
            return J, None, info
        # static part
        g = W_STATIC * -(mesh.energy(U) / self.C0).sum(1) / nlc * dE
        # dynamic part, per objective mode. J depends on mode i's shape through b_i . d(phi_i), with
        # b_i = sum_c dJ/dP_ic (2 a_ic F_c / (D_i F0) - 2 a_ic^2 K_eta phi_i / D_i^2), and
        # d(phi_i) = sum_{j != i} phi_j phi_j^T (dK - lambda_i dM) phi_i / (lambda_i - lambda_j) - phi_i phi_i^T dM phi_i / 2
        # (the last term drops out: phi_i . b_i = 0). The kept modes give that sum directly; the rest, whose
        # lambda_j >> lambda_i, as their static flexibility: K^-1 b_i minus the kept modes' share of it.
        dJdP = W_DYN * S ** (1 / Q - 1) * (P / self.P0) ** (Q - 1) / self.P0     # N_OBJ x cases
        B = (F / F0) @ (dJdP * 2 * a[:N_OBJ] / D[:, None]).T - KePhi[:, :N_OBJ] * ((dJdP * 2 * a[:N_OBJ] ** 2).sum(1) / D ** 2)
        Zs = fk.solve(B)
        for i in range(N_OBJ):
            b = B[:, i]
            pb = phi.T @ b
            gap = lam[i] - lam
            ok = np.abs(gap) > 1e-6 * lam[i]
            ok[i] = False
            c1 = np.zeros(K_MODES)
            c1[ok] = pb[ok] / gap[ok]
            c3 = (dJdP[i] * -a[i] ** 2 / D[i] ** 2).sum()
            v = phi @ c1 - (Zs[:, i] - phi @ (pb / lam))
            pi = phi[:, i]
            g += dE * cross_energy(mesh, pi, v) - lam[i] * dm * cross_mass(mesh, pi, v)
            g += c3 * ETA_EG * dE * cross_energy(mesh, pi, pi)
        gcol = np.bincount(self.col_of, weights=g[self.de], minlength=len(r))
        dJ = self.W.T @ (gcol * dr)
        return J, dJ, info

    def volume(self, x):
        return self.dd['v_fix'] + (self.proj(self.W @ x)[0] * self.dd['vcol']).sum()


def check(pb, x, n=6, step=1e-3):
    """The gradient against central differences on the columns with the largest gradients."""
    J, dJ, _ = pb.evaluate(x)
    pick = np.argsort(-np.abs(dJ))[:n]
    print('  column   adjoint      finite diff   ratio', flush=True)
    for k in pick:
        xp, xm = x.copy(), x.copy()
        xp[k] += step
        xm[k] -= step
        fd = (pb.evaluate(xp, False)[0] - pb.evaluate(xm, False)[0]) / (2 * step)
        print(f'  {k:6d}  {dJ[k]: .4e}  {fd: .4e}  {dJ[k] / fd if fd else float("nan"):6.3f}', flush=True)


def main(frac, src='sym10', iters=int(os.environ.get('TO_ITERS', 60))):
    warnings.filterwarnings('ignore', message='Matrix is nearly singular')
    SRC = 'vox_' + src
    vox = Voxels(SRC)
    pb = Problem(vox)
    dd = pb.dd
    target = frac * dd['v_all']
    print(f'uprights + beam {dd["v_all"]:.2f} L, fixed {dd["v_fix"]:.2f} L, target {target:.2f} L, '
          f'{len(dd["cols"])} variables; weights static {W_STATIC:g}, peaks {W_DYN:g}', flush=True)
    x = np.full(len(dd['cols']), min(frac, 0.999))
    ckpt = os.path.join(HERE, f'vox_damped_{frac:g}_{src}_ckpt.npz')
    it0 = 0
    if '--resume' in sys.argv and os.path.exists(ckpt):
        c = np.load(ckpt)
        x, it0, pb.beta, pb.C0, pb.P0 = c['x'], int(c['it']) + 1, float(c['beta']), c['C0'], float(c['P0'])
        print(f'resuming after iteration {it0 - 1}', flush=True)
    if '--check' in sys.argv:
        pb.beta = 4.0
        check(pb, np.clip(x + 0.2 * (np.random.default_rng(0).random(len(x)) - 0.5), 0.05, 0.95), n=4)
        pb.beta, pb.C0, pb.P0 = 1.0, None, None
    hist = []
    for it in range(it0, iters):
        t = time.time()
        if it and it % 12 == 0 and pb.beta < 16:
            pb.beta *= 2
        J, dJ, info = pb.evaluate(x)
        dV = pb.W.T @ (dd['vcol'] * pb.proj(pb.W @ x)[1]) + 1e-12
        C, P = info['C'], info['P']
        ks = 1e3 / C
        kd = 1e-3 / P.max()
        fr = np.sqrt(info['lam'][:4]) / (2 * np.pi)
        hist.append((it, J, info['Js'], info['Jd'], pb.volume(x)))
        print(f'{it:3d} J {J:.4f} (static {info["Js"]:.3f}, peaks {info["Jd"]:.3f})  V {pb.volume(x):5.2f} L  '
              f'k x/y/z {ks[0::3].mean():5.1f} {ks[1::3].mean():5.1f} {ks[2::3].mean():5.1f}  worst peak {kd:5.2f} N/um  '
              f'modes {" ".join(f"{v:.0f}" for v in fr)} Hz  eta {info["eta"][:4].mean():.4f}  beta {pb.beta:g}  '
              f'{time.time() - t:4.0f} s', flush=True)
        B = np.maximum(-dJ, 1e-12 * np.abs(dJ).max())
        l1, l2 = 1e-12, 1e12
        while l2 / l1 > 1 + 1e-6:
            lm = np.sqrt(l1 * l2)
            xn = np.clip(x * np.sqrt(B / (lm * dV)), np.maximum(0, x - 0.1), np.minimum(1, x + 0.1))
            if pb.volume(xn) > target:
                l1 = lm
            else:
                l2 = lm
        x = xn
        np.savez(ckpt, x=x, it=it, beta=pb.beta, C0=pb.C0, P0=pb.P0)

    # threshold and write the frame with the cuts
    f = vox.f
    rho, _, _ = pb.densities(x)
    cut = np.zeros(pb.mesh.ne, bool)
    cut[pb.de] = rho[pb.de] < 0.5
    out = {k: v.copy() for k, v in f.items()}
    i, j, kk = pb.mesh.ijk[cut].T
    for g in ('up', 'beam'):
        out[f'eg_{g}'][i, j, kk] = 0.0
    name = f'vox_damped_{frac:g}_{src}'
    np.savez_compressed(os.path.join(HERE, name + '.npz'), **out)
    json.dump(json.load(open(os.path.join(HERE, SRC + '.json'))), open(os.path.join(HERE, name + '.json'), 'w'))
    if os.path.exists(os.path.join(HERE, SRC + '_parts.npz')):
        shutil.copy(os.path.join(HERE, SRC + '_parts.npz'), os.path.join(HERE, name + '_parts.npz'))
    np.save(os.path.join(HERE, name + '_x.npy'), x)
    left = sum(out[f'eg_{g}'].sum() for g in ('up', 'beam')) * vox.h ** 3 / 1e6
    print(f'saved {name}: uprights + beam {left:.2f} L of {dd["v_all"]:.2f}', flush=True)


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    main(float(args[0]), *args[1:2])
