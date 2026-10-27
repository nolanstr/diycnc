"""Natural frequencies of the frame (voxel model, bench-mounted on its four feet).

    python modal.py                      # current design
    FEA_VOX=vox_previous python modal.py

Lumped element masses (epoxy granite 2.35, steel 7.85 kg/L). The moving assemblies are added
as rigid masses tied to their rail blocks (RBE3 style, through the same rigid-body spread the
load cases use): the X carriage + Z axis + spindle on the beam blocks, the table + vise + work
on the Y blocks. Brick elements this coarse are a little stiff in bending, so the
frequencies are somewhat high; the comparison between variants is what counts.
"""

import warnings

import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import LinearOperator, eigsh

from loads import domain_mask, moduli, setup, union_box
from vfe import CholeskyFactor, Voxels, wrench_loads

RHO_EG, RHO_ST = 2.35e-9, 7.85e-9    # t/mm^3 (mm, N, t -> s)

# Moving assemblies: mass (kg), center of mass offset from (tool x, tool y, z), box size for inertia (mm)
HEAD = dict(m=18.5, at=(0.0, 30.0, 440.0), box=(170.0, 150.0, 300.0))      # steel X carriage + angles, Z axis, spindle
TABLE = dict(m=12.0, dz=60.0, box=(320.0, 260.0, 100.0))                   # table, vise, work


def rigid_mass(mesh, nodes, m, point, box):
    """Mass matrix (ndof x ndof) of a rigid body of mass m (kg) at `point`, tied to `nodes`."""
    W = np.zeros((3 * len(nodes), 6))
    for a in range(6):
        e = np.zeros(3)
        e[a % 3] = 1
        F, M = (e, np.zeros(3)) if a < 3 else (np.zeros(3), e)
        W[:, a] = wrench_loads(mesh.xyz, nodes, F, M, point).ravel()
    bx, by, bz = box
    mt = m * 1e-3
    Mp = np.diag([mt, mt, mt, mt * (by ** 2 + bz ** 2) / 12, mt * (bx ** 2 + bz ** 2) / 12, mt * (bx ** 2 + by ** 2) / 12])
    dofs = (3 * nodes[:, None] + np.arange(3)).ravel()
    blk = W @ Mp @ W.T
    r, c = np.meshgrid(dofs, dofs, indexing='ij')
    return sp.csc_matrix((blk.ravel(), (r.ravel(), c.ravel())), shape=(mesh.ndof, mesh.ndof))


def mass_matrix(mesh, vox, eg, st):
    """eg, st: per-element epoxy-granite and steel fractions. Returns (M, attached-mass matrix)."""
    d, b, Pp, h = vox.d, vox.info['boxes'], vox.info['P'], vox.h
    me = (RHO_EG * eg + RHO_ST * st) * h ** 3
    nodal = np.bincount(mesh.enodes.ravel(), weights=np.repeat(me / 8, 8), minlength=mesh.nn)
    M = sp.diags(np.repeat(nodal, 3)).tocsc()
    bf, bt = d['beam_face'], d['base_top']
    nx = np.unique(np.concatenate([
        mesh.nodes_in(np.r_[bb[0], bf - Pp['beam_riser_t'] - 1, bb[2]], np.r_[bb[3], bf + h, bb[5]], mesh.solid)
        for bb in (union_box(b, f'X_Block{s}{i}') for s in 'LR' for i in '12')]))
    ny = np.unique(np.concatenate([
        mesh.nodes_in(np.r_[bb[0], bb[1], bt - h], np.r_[bb[3], bb[4], bt + Pp['table_riser_t'] + 1], mesh.solid_or_base)
        for bb in (union_box(b, f'Y_Block{s}{i}') for s in 'LR' for i in '12')]))
    Ma = rigid_mass(mesh, nx, HEAD['m'], np.r_[HEAD['at']], HEAD['box'])
    Ma += rigid_mass(mesh, ny, TABLE['m'], np.r_[0.0, 0.0, d['table_top'] + TABLE['dz']], TABLE['box'])
    return M + Ma, Ma


def modes(mesh, E, M, k=6):
    """Lowest k natural frequencies (Hz) and mode shapes."""
    K = mesh.assemble(E)
    fac = CholeskyFactor(K)
    fac.factorize(K)
    op = LinearOperator(K.shape, matvec=lambda v: fac.solve(v), dtype=float)
    lam, phi = eigsh(K, k=k, M=M, sigma=0.0, which='LM', OPinv=op)
    o = np.argsort(lam)
    return np.sqrt(np.abs(lam[o])) / (2 * np.pi), phi[:, o]


def describe(mesh, vox, phi, M, groups):
    """Where each mode's kinetic energy sits (share per group) and the beam's main motion."""
    out = []
    for i in range(phi.shape[1]):
        v = phi[:, i]
        ke = v * (M @ v)
        tot = ke.sum()
        shares = {g: ke[np.repeat(sel, 3)].sum() / tot for g, sel in groups.items()}
        beam = np.repeat(groups['beam'], 3)
        u = np.abs(v[beam].reshape(-1, 3)).mean(0)
        out.append((shares, 'xyz'[int(np.argmax(u))]))
    return out


def node_groups(mesh, vox):
    f = vox.f
    sel = {}
    for g in ('base', 'up', 'beam'):
        el = (mesh.field(f[f'eg_{g}']) + mesh.field(f[f'st_{g}'])) > 0.3
        m = np.zeros(mesh.nn, bool)
        m[np.unique(mesh.enodes[el])] = True
        sel[g] = m
    sel['up'] &= ~sel['beam']
    sel['base'] &= ~sel['up']
    return sel


def report(mesh, vox, E, eg, st, name, k=6):
    M, Ma = mass_matrix(mesh, vox, eg, st)
    fr, phi = modes(mesh, E, M, k)
    mass = (RHO_EG * eg + RHO_ST * st).sum() * vox.h ** 3 * 1e3
    print(f'{name}: frame {mass:.0f} kg + {HEAD["m"] + TABLE["m"]:.0f} kg moving', flush=True)
    for i, (f_, (sh, ax)) in enumerate(zip(fr, describe(mesh, vox, phi, M, node_groups(mesh, vox)))):
        print(f'  mode {i + 1}: {f_:6.0f} Hz  beam moves mostly in {ax}   energy: base {sh["base"]:.0%}, '
              f'uprights {sh["up"]:.0%}, beam {sh["beam"]:.0%}', flush=True)
    return fr


def main():
    warnings.filterwarnings('ignore', message='Matrix is nearly singular')
    vox = Voxels()
    mesh = setup(vox, domain_mask(vox))
    f = vox.f
    eg = sum(mesh.field(f[f'eg_{g}']) for g in ('base', 'up', 'beam'))
    st = sum(mesh.field(f[f'st_{g}']) for g in ('base', 'up', 'beam'))
    report(mesh, vox, moduli(mesh, f, mesh.field(f['eg_base'])), eg, st, 'current')


if __name__ == '__main__':
    main()
