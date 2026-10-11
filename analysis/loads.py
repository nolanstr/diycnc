"""Cutting-force load cases for the frame.

A force F on the tool goes into the frame twice: through the spindle, Z axis and X carriage
into the beam's rail blocks, and (reversed) through the work, table and Y blocks into the
base. The component along each moving axis goes through that axis' ballscrew to its fixed
(BK) bearing instead of the rails. Each side is applied as a rigid-body-equivalent spread
over the block (or BK) footprints, so the compliance F.u is the frame's share of the
tool-to-work deflection along F.
"""

import os

import numpy as np

from vfe import E_EG, E_MIN, E_ST, Mesh, Voxels, wrench_loads

F0 = 1000.0   # N
# Epoxy-granite stiffness factor per casting: FEA_GRIT=1.37 for the alumina grits in the uprights
# and beam (analysis/alumina.py); 1 = the plain sand mix everywhere.
EG_SCALE = {'base': 1.0, 'up': float(os.environ.get('FEA_GRIT', 1.0)), 'beam': float(os.environ.get('FEA_GRIT', 1.0))}


def union_box(boxes, prefix):
    bb = np.array([v for k, v in boxes.items() if k.startswith(prefix)])
    return np.r_[bb[:, :3].min(0), bb[:, 3:].max(0)]


def setup(vox, mask):
    mesh = Mesh(vox, mask)
    f = vox.f
    total = sum(mesh.field(f[k]) for k in f if k != 'eg_base_solid')
    mesh.solid = total > 0.3
    mesh.solid_or_base = mesh.solid | (mesh.field(f['eg_base_solid']) > 0.3)
    # Bench supports: the four leg positions on the underside (z only, plus 3 in-plane).
    fixed = []
    for i, (lx, ly) in enumerate(vox.info['legs']):
        n = mesh.nodes_in(np.r_[lx - 20, ly - 20, -1], np.r_[lx + 20, ly + 20, vox.h], mesh.solid_or_base)
        n = n[mesh.xyz[n, 2] < 1e-6]
        fixed += list(3 * n + 2)
        if i == 0:
            fixed += list(3 * n) + list(3 * n + 1)
        elif i == 1:
            fixed += list(3 * n + 1)
    mesh.fixed = np.array(sorted(set(fixed)))
    return mesh


def cases(mesh, vox, xs=(0.0,), yts=(-150.0, 0.0, 150.0), tip_above_table=50.0, dirs='xyz'):
    """Load matrix (ndof x nlc) and labels. yt = table centre position; the tool is always at y = 0."""
    d, b, Pp, h = vox.d, vox.info['boxes'], vox.info['P'], vox.h
    zt = d['table_top'] + tip_above_table
    bf, bt = d['beam_face'], d['base_top']
    Fs, labels = [], []
    # screw axes (a point on each) and fixed-bearing footprints
    bk_x = union_box(b, 'X_BK10')
    bk_y = union_box(b, 'Y_BK12')
    sx_pt = np.r_[0.5 * (bk_x[0] + bk_x[3]), bf - 22.0, d['beam_cz']]
    sy_pt = np.r_[0.0, 0.5 * (bk_y[1] + bk_y[4]), bt + 25.0]
    n_bkx = mesh.nodes_in(np.r_[bk_x[0], bf - 1, bk_x[2]], np.r_[bk_x[3], bf + h, bk_x[5]], mesh.solid)
    n_bky = mesh.nodes_in(np.r_[bk_y[0], bk_y[1], bt - h], np.r_[bk_y[3], bk_y[4], bt + 1], mesh.solid_or_base)
    for xc in xs:
        nx_rail = []
        for s in 'LR':
            for i in '12':
                bb = union_box(b, f'X_Block{s}{i}')
                nx_rail.append(mesh.nodes_in(np.r_[bb[0] + xc, bf - Pp['beam_riser_t'] - 1, bb[2]],
                                             np.r_[bb[3] + xc, bf + h, bb[5]], mesh.solid))
        nx_rail = np.unique(np.concatenate(nx_rail))
        for yt in yts:
            ny_rail = []
            for s in 'LR':
                for i in '12':
                    bb = union_box(b, f'Y_Block{s}{i}')
                    ny_rail.append(mesh.nodes_in(np.r_[bb[0], bb[1] + yt, bt - h],
                                                 np.r_[bb[3], bb[4] + yt, bt + Pp['table_riser_t'] + 1],
                                                 mesh.solid_or_base))
            ny_rail = np.unique(np.concatenate(ny_rail))
            rt = np.r_[xc, 0.0, zt]
            for ax in dirs:
                e = np.zeros(3)
                e['xyz'.index(ax)] = 1
                F = F0 * e
                f = np.zeros((mesh.nn, 3))
                # beam side: +F at the tool
                Fa = np.r_[F[0], 0, 0]
                f[n_bkx] += wrench_loads(mesh.xyz, n_bkx, Fa, np.cross(sx_pt, Fa), np.zeros(3))
                Fr = F - Fa
                f[nx_rail] += wrench_loads(mesh.xyz, nx_rail, Fr, np.cross(rt, F) - np.cross(sx_pt, Fa), np.zeros(3))
                # base side: -F at the work
                Fa = np.r_[0, -F[1], 0]
                f[n_bky] += wrench_loads(mesh.xyz, n_bky, Fa, np.cross(sy_pt, Fa), np.zeros(3))
                Fr = -F - Fa
                f[ny_rail] += wrench_loads(mesh.xyz, ny_rail, Fr, np.cross(rt, -F) - np.cross(sy_pt, Fa), np.zeros(3))
                Fs.append(f.ravel())
                labels.append(f'F{ax} x={xc:+.0f} table={yt:+.0f}')
    return np.column_stack(Fs), labels


def moduli(mesh, f, base_eg, rigid=()):
    """Element moduli. base_eg: per-element EG fraction for the base (design or current).
    rigid: groups ('base', 'up', 'beam') made 1000x stiffer, to see each one's share."""
    E = E_MIN * E_EG * np.ones(mesh.ne)
    for g in ('base', 'up', 'beam'):
        k = 1000.0 if g in rigid else 1.0
        eg = base_eg if g == 'base' else mesh.field(f[f'eg_{g}'])
        E += k * (E_EG * EG_SCALE[g] * eg + E_ST * mesh.field(f[f'st_{g}']))
    return E


def domain_mask(vox):
    f = vox.f
    total = sum(f[k] for k in f)
    return total > 0.01
