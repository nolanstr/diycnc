"""Damping and vibration at the tool (voxel model): each mode's loss factor and the resonant peaks it gives
between the tool and the work.

    python damping.py                                   # FEA_VOX, FEA_SYM as everywhere (vox_sym10 + FEA_SYM=1 is quick)
    FEA_SYM=1 FEA_VOX=vox_sym10 python damping.py --frf # also the response curves, figs/frf_<vox>.png

Damping is structural: each material's stiffness is E(1 + i eta), so a mode's loss factor is the materials'
eta weighted by where it stores its strain energy (the modal strain energy method), and a mode that lives in
the steel has steel's eta. Near a resonance the tool-to-work deflection per newton of cutting force in case c
peaks at

    P = (phi . F_c)^2 / (lambda eta) = (phi . F_c)^2 / (phi^T K_eta phi)        (phi mass-normalized)

and its inverse is the dynamic stiffness at that resonance, the number chatter depends on. The static
stiffness is the same sum over all modes without the eta, so the dynamic stiffness is roughly the static one
times eta for the dominant mode. Cutting forces are the load cases of loads.py (the tool against the work,
1 kN along x, y or z, the table at its two ends and center, the carriage at center and right end).

Loss factors: epoxy granite ETA_EG (default 0.02: published polymer concrete runs 0.02-0.04, so check the
test bars), steel ETA_ST 0.0005 (the material alone; bolted joints add damping this model leaves out, so the
frame does somewhat better than this). FEA_ETA_EG and FEA_ETA_ST override them.
"""

import os
import sys
import time
import warnings

import numpy as np
from scipy.sparse.linalg import LinearOperator, eigsh

from loads import F0, EG_SCALE, cases, domain_mask, moduli, setup
from modal import mass_matrix
from vfe import E_EG, E_MIN, E_ST, Voxels

ETA_EG = float(os.environ.get('FEA_ETA_EG', 0.02))
ETA_ST = float(os.environ.get('FEA_ETA_ST', 0.0005))
HERE = os.path.dirname(os.path.abspath(__file__))


def loss_moduli(mesh, f, base_eg):
    """eta * E per element (the imaginary part of the complex modulus), as moduli() builds E."""
    Ee = np.zeros(mesh.ne)
    for g in ('base', 'up', 'beam'):
        eg = base_eg if g == 'base' else mesh.field(f[f'eg_{g}'])
        Ee += ETA_EG * E_EG * EG_SCALE[g] * eg + ETA_ST * E_ST * mesh.field(f[f'st_{g}'])
    return Ee


def eigen(mesh, E, M, k):
    """Lowest k eigenpairs (lambda = omega^2, mass-normalized shapes as columns). With FEA_SYM the lowest k of
    the symmetric and antisymmetric families together."""
    K = mesh.assemble(E)
    out = []
    blocks = mesh.T.items() if mesh.sym else [('all', None)]
    for key, T in blocks:
        Kr = (T.T @ K @ T).tocsc() if T is not None else K
        Mr = (T.T @ M @ T).tocsc() if T is not None else M
        fac = mesh.factored(key, Kr) if T is not None else _factor(mesh, Kr)
        op = LinearOperator(Kr.shape, matvec=lambda v, fac=fac: fac.solve(v), dtype=float)
        lam, q = eigsh(Kr, k=min(k, Kr.shape[0] - 2), M=Mr, sigma=0.0, which='LM', OPinv=op)
        out += [(lam[i], q[:, i] if T is None else T @ q[:, i]) for i in range(len(lam))]
    out.sort(key=lambda t: t[0])
    out = out[:k]
    return np.array([t[0] for t in out]), np.column_stack([t[1] for t in out])


def _factor(mesh, K):
    from vfe import CholeskyFactor
    if mesh.factor is None:
        mesh.factor = CholeskyFactor(K)
    num = mesh.factor.copy()
    num.factorize(K)
    return num


def modal_damping(mesh, phi, E, Ee):
    """Per mode: phi^T K phi, phi^T K_eta phi (from element energies) and the steel's share of the strain
    energy (with `st` the per-element steel modulus part)."""
    en = mesh.energy(phi)                         # ne x modes, for E = 1
    return (E[:, None] * en).sum(0), (Ee[:, None] * en).sum(0), en


def peaks(phi, D, F):
    """Peak tool-to-work compliance per mode and case (mm/N): (phi . F_c)^2 / D / F0^2."""
    a = phi.T @ F / F0                            # modes x cases
    return a ** 2 / D[:, None], a


def frf(lam, eta, a, Cstat, freqs):
    """Tool-to-work compliance (complex, mm/N) per case at freqs (Hz): the modes damped by their eta, plus the
    static share of the modes left out (Cstat: the static compliance per case, mm/N)."""
    w2 = (2 * np.pi * np.asarray(freqs)) ** 2
    resid = Cstat - (a ** 2 / lam[:, None]).sum(0)
    H = (a[:, None, :] ** 2 / (lam[:, None, None] * (1 + 1j * eta[:, None, None]) - w2[None, :, None])).sum(0)
    return H + resid[None, :]


def analyze(vox, k=16, f=None):
    f = f or vox.f
    mesh = setup(vox, domain_mask(vox))
    F, labels = cases(mesh, vox, xs=(0.0, 90.0))
    base = mesh.field(f['eg_base'])
    E = moduli(mesh, f, base)
    Ee = loss_moduli(mesh, f, base)
    eg = sum(mesh.field(f[f'eg_{g}']) for g in ('base', 'up', 'beam'))
    st = sum(mesh.field(f[f'st_{g}']) for g in ('base', 'up', 'beam'))
    M, _ = mass_matrix(mesh, vox, eg, st)
    U = mesh.solve(E, F)
    Cstat = (F * U).sum(0) / F0 ** 2
    lam, phi = eigen(mesh, E, M, k)
    Kd, D, en = modal_damping(mesh, phi, E, Ee)
    eta = D / Kd
    steel = (E_ST * st)[:, None] * en
    share_st = steel.sum(0) / Kd
    P, a = peaks(phi, D, F)
    return dict(mesh=mesh, F=F, labels=labels, E=E, Ee=Ee, M=M, lam=lam, phi=phi, eta=eta, share_st=share_st,
                P=P, a=a, Cstat=Cstat, freq=np.sqrt(np.abs(lam)) / (2 * np.pi))


def report(r, name=''):
    """Static and worst dynamic stiffness at the tool per direction, and each mode's damping."""
    P, Cs = r['P'], r['Cstat']
    dirs = np.array([lb.split()[0][1] for lb in r['labels']])
    print(f'{name}: loss factors epoxy granite {ETA_EG:g}, steel {ETA_ST:g}', flush=True)
    print('  mode    Hz    loss   steel share   worst case it rings in (dynamic stiffness N/um)')
    for j in range(len(r['lam'])):
        c = int(np.argmax(P[j]))
        print(f'  {j + 1:3d} {r["freq"][j]:6.0f}  {r["eta"][j]:.4f}  {r["share_st"][j]:10.0%}   '
              f'{r["labels"][c]:24s} {1e-3 / P[j, c]:8.2f}', flush=True)
    out = {}
    for ax in 'xyz':
        sel = dirs == ax
        ks = 1e-3 / Cs[sel].max()
        kd = 1e-3 / P[:, sel].max()
        out[ax] = (ks, kd)
        print(f'  {ax}: static {ks:6.1f} N/um (weakest case), dynamic {kd:6.2f} N/um at the worst resonance '
              f'({ks / kd:.0f}x amplification)', flush=True)
    return out


def main():
    warnings.filterwarnings('ignore', message='Matrix is nearly singular')
    t = time.time()
    vox = Voxels()
    name = os.environ.get('FEA_VOX', 'vox_current')
    r = analyze(vox)
    report(r, name)
    print(f'  ({time.time() - t:.0f} s)', flush=True)
    if '--frf' in sys.argv:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        freqs = np.linspace(20, 1.1 * r['freq'][-1], 1500)
        H = frf(r['lam'], r['eta'], r['a'], r['Cstat'], freqs)
        fig, ax = plt.subplots(figsize=(8, 4.5))
        for c, lb in enumerate(r['labels']):
            if 'x=+0' in lb and 'table=+0' in lb:
                ax.semilogy(freqs, np.abs(H[:, c]) * 1e3, label=lb.split()[0])
        ax.set_xlabel('Frequency (Hz)')
        ax.set_ylabel('Tool to work (um/N)')
        ax.set_title(f'{name}: frame response at the tool, eta EG {ETA_EG:g} / steel {ETA_ST:g}')
        ax.legend()
        ax.grid(alpha=0.3)
        os.makedirs(os.path.join(HERE, 'figs'), exist_ok=True)
        out = os.path.join(HERE, 'figs', f'frf_{name}.png')
        fig.savefig(out, dpi=130, bbox_inches='tight')
        print('  wrote', os.path.relpath(out))


if __name__ == '__main__':
    main()
