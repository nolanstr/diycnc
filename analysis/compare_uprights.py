"""Stiffness, natural frequencies and epoxy for upright variants (topopt_upright.py results).

    python compare_uprights.py to_upright_thru_0.9.npz [...]

Each result is thresholded at 0.5 (what you'd actually cast); figures go to figs/.
"""

import os
import sys
import warnings

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from evaluate import FIGS  # noqa: E402
from loads import F0, cases, domain_mask, setup  # noqa: E402
from modal import report  # noqa: E402
from vfe import E_EG, E_MIN, E_ST, Voxels  # noqa: E402

EPOXY = 0.085 * 2.35 * 13.8      # $ of epoxy per liter of casting (8.5 % mix, $13.8/kg)


def side_view(vox, rho, title, path):
    d = vox.d
    xs = vox.centers(0)
    sel = (xs < -d['inner']) & (xs > -d['outer'])
    frac = (rho[sel] > 0.5).mean(0)
    ext = [vox.o[1], vox.o[1] + vox.n[1] * vox.h, vox.o[2], vox.o[2] + vox.n[2] * vox.h]
    fig, ax = plt.subplots(figsize=(8, 3.6))
    ax.imshow(frac.T, origin='lower', extent=ext, cmap='Greys', vmin=0, vmax=1, aspect='equal')
    ax.set_xlim(d['base_y0'] + 200, d['base_y1'])
    ax.set_ylim(d['base_top'] - 10, d['beam_bot'] + 10)
    ax.set_xlabel('y (mm), front at left')
    ax.set_ylabel('z (mm)')
    ax.set_title(title, fontsize=9)
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)


def main(paths):
    warnings.filterwarnings('ignore', message='Matrix is nearly singular')
    vox = Voxels('vox_current')
    f, h = vox.f, vox.h
    mesh = setup(vox, domain_mask(vox))
    F, _ = cases(mesh, vox, xs=(0.0, 90.0))
    fld = mesh.field
    st = fld(f['st_base']) + fld(f['st_up']) + fld(f['st_beam'])
    eg_fix = fld(f['eg_base']) + fld(f['eg_beam'])
    v0 = fld(f['eg_up']).sum() * h ** 3 / 1e6
    variants = [('current', fld(f['eg_up']))]
    for p in paths:
        r = np.load(p)
        name = os.path.basename(p)[3:-4]
        variants.append((name, fld(f['eg_up']) * (fld(r['rho_up']) > 0.5)))
        side_view(vox, r['rho_up'], name, os.path.join(FIGS, f'{name}.png'))
    for name, up in variants:
        E = E_MIN * E_EG + E_EG * (eg_fix + up) + E_ST * st
        U = mesh.solve(E, F)
        k = F0 ** 2 / (F * U).sum(0) / 1e3
        v = up.sum() * h ** 3 / 1e6
        print(f'{name:22s} uprights {v:5.2f} L (-{v0 - v:4.2f} L, epoxy -${(v0 - v) * EPOXY:3.0f})  '
              f'kx {k[0::3].mean():5.1f} ky {k[1::3].mean():5.1f} kz {k[2::3].mean():5.1f}', flush=True)
        report(mesh, vox, E, eg_fix + up, st, name, k=4)


if __name__ == '__main__':
    main(sys.argv[1:])
