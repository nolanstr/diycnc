"""Figures for topopt_frame.py results.

    python plot_frame.py to_frame_34.6.npz [...]
"""

import os
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from evaluate import FIGS, plot_depth  # noqa: E402
from vfe import Voxels  # noqa: E402


def upright_views(vox, rho_up, title, path):
    """Left upright: side view (how much of its 80 mm width is solid) and slices across x."""
    d = vox.d
    xs = vox.centers(0)
    sel = (xs < -d['inner']) & (xs > -d['outer'])
    up = rho_up[sel] > 0.5                      # nx_sel x ny x nz
    frac = up.mean(0)
    ext = [vox.o[1], vox.o[1] + vox.n[1] * vox.h, vox.o[2], vox.o[2] + vox.n[2] * vox.h]
    cur = vox.f['eg_up'][sel].max(0) > 0.5
    fig = plt.figure(figsize=(12, 7.5))
    ax = fig.add_subplot(2, 1, 1)
    im = ax.imshow(frac.T, origin='lower', extent=ext, cmap='viridis', vmin=0, vmax=1, aspect='equal')
    ax.contour(np.linspace(ext[0], ext[1], vox.n[1]), np.linspace(ext[2], ext[3], vox.n[2]), cur.T.astype(float),
               levels=[0.5], colors='w', linewidths=1.2, linestyles='--')
    ax.axhline(d['base_top'], color='k', lw=0.8)
    ax.axhline(d['beam_bot'], color='k', lw=0.8)
    ax.axvline(d['beam_face'], color='k', lw=0.6, ls=':')
    ax.set_xlim(d['base_y0'], d['base_y1'])
    ax.set_ylim(d['base_top'] - 20, d['beam_bot'] + 20)
    ax.set_xlabel('y (mm), front at left')
    ax.set_ylabel('z (mm)')
    ax.set_title(title + ': side view, share of the 80 mm width that is solid (dashed: current upright)', fontsize=9)
    fig.colorbar(im, ax=ax, shrink=0.8)
    idx = np.nonzero(sel)[0]
    for k, i in enumerate(idx):
        a = fig.add_subplot(2, len(idx), len(idx) + k + 1)
        a.imshow((rho_up[i] > 0.5).T, origin='lower', extent=ext, cmap='Greys', vmin=0, vmax=1, aspect='auto')
        a.set_xlim(d['base_y0'], d['base_y1'])
        a.set_ylim(d['base_top'], d['beam_bot'])
        a.set_title(f'x {xs[i]:.0f}', fontsize=7)
        a.set_xticks([])
        a.set_yticks([])
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)


def main(paths):
    os.makedirs(FIGS, exist_ok=True)
    vox = Voxels('vox_current')
    for p in paths:
        r = np.load(p, allow_pickle=True)
        name = os.path.basename(p)[3:-4]
        hist = r['hist']
        vol_b = (vox.f['eg_base_solid'] * (r['rho'] > 0.5)).sum() * vox.h ** 3 / 1e6
        vol_u = (r['rho_up'] > 0.5).sum() * vox.h ** 3 / 1e6
        print(f'{name}: J {hist[-1, 0]:.3f}  base {vol_b:.1f} L, uprights {vol_u:.1f} L (both)  '
              f'k x/y/z {hist[-1, 2::3].mean():.1f} {hist[-1, 3::3].mean():.1f} {hist[-1, 4::3].mean():.1f}')
        plot_depth(vox, (r['rho'] > 0.5).astype(float), f'{name}: base, solid depth from the top',
                   os.path.join(FIGS, f'{name}_base.png'), vox.f['eg_base_solid'])
        upright_views(vox, r['rho_up'], name, os.path.join(FIGS, f'{name}_upright.png'))


if __name__ == '__main__':
    main(sys.argv[1:])
