"""Evaluate optimized (or other) base designs over all load cases, and plot them.

    FEA_VOX=vox_previous python evaluate.py to_*.npz    # stiffness table + figures in analysis/figs

The frame is FEA_VOX's; its own base is the reference ("current"). The base in COMPARE
(default vox_current, the model as now drawn) is added as "final (CAD)".
"""

import os
import sys
import warnings

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from loads import F0, cases, domain_mask, moduli, setup  # noqa: E402
from vfe import Voxels  # noqa: E402

FIGS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'figs')


def stiffness(mesh, vox, F, base_eg):
    U = mesh.solve(moduli(mesh, vox.f, base_eg), F)
    return F0 ** 2 / (F * U).sum(0) / 1e3


def summary(k, k0):
    """Mean stiffness per direction (N/um) and the worst-case ratio to the reference."""
    out = {}
    for i, ax in enumerate('xyz'):
        out[ax] = k[i::3].mean()
    out['worst'] = (k / k0).min()
    out['mean'] = (k / k0).mean()
    return out


def outline(ax, vox):
    """Rails, uprights, sockets, legs and the split line on a top view."""
    d, info = vox.d, vox.info
    half, y0, y1 = d['base_half'], d['base_y0'], d['base_y1']
    ax.plot([-half, half, half, -half, -half], [y0, y0, y1, y1, y0], 'k-', lw=0.8)
    s2 = info['P']['table_rail_spacing'] / 2
    for x in (-s2, s2):
        ax.plot([x, x], [-275, 275], color='w', lw=2.5)
        ax.plot([x, x], [-275, 275], color='k', lw=1, ls='--')
    for sx in (-1, 1):
        x0, x1 = sorted((sx * d['inner'], sx * d['outer']))
        ax.add_patch(plt.Rectangle((x0, d['up_y0']), x1 - x0, d['up_y1'] - d['up_y0'], fill=False, ec='k', lw=1.2))
        for py in info.get('post_ys', []):
            ax.add_patch(plt.Rectangle((sx * info['ux'] - 22, py - 22), 44, 44, fill=False, ec='k', lw=0.6))
    for lx, ly in info['legs']:
        ax.add_patch(plt.Rectangle((lx - 19, ly - 19), 38, 38, fill=False, ec='k', lw=0.6))
    ax.axhline(0, color='k', lw=0.6, ls=':')
    ax.set_aspect('equal')
    ax.set_xlim(-half - 5, half + 5)
    ax.set_ylim(y0 - 5, y1 + 5)
    ax.set_xlabel('x (mm)')
    ax.set_ylabel('y (mm), front at bottom')


def solid_depth(vox, rho):
    """Solid thickness from the top in each column of the base (mm)."""
    h = vox.h
    top = int(round(vox.d['base_top'] / h))
    return (rho[:, :, :top] > 0.5).sum(2) * h


def plot_depth(vox, rho, title, path, eg=None):
    D = solid_depth(vox, rho).astype(float)
    if eg is not None:
        D[eg[:, :, :int(round(vox.d['base_top'] / vox.h))].max(2) < 0.01] = np.nan
    fig, ax = plt.subplots(figsize=(6.2, 7))
    ext = [vox.o[0], vox.o[0] + vox.n[0] * vox.h, vox.o[1], vox.o[1] + vox.n[1] * vox.h]
    im = ax.imshow(D.T, origin='lower', extent=ext, cmap='viridis', vmin=0, vmax=vox.d['base_top'])
    outline(ax, vox)
    fig.colorbar(im, ax=ax, shrink=0.7, label='solid depth from the top (mm)')
    ax.set_title(title, fontsize=10)
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


def plot_layers(vox, rho, title, path):
    """Horizontal slices through the base, bottom to top."""
    top = int(round(vox.d['base_top'] / vox.h))
    fig, axs = plt.subplots(2, (top + 1) // 2, figsize=(2.3 * ((top + 1) // 2), 6.4))
    ext = [vox.o[0], vox.o[0] + vox.n[0] * vox.h, vox.o[1], vox.o[1] + vox.n[1] * vox.h]
    for k, ax in enumerate(axs.ravel()):
        if k >= top:
            ax.axis('off')
            continue
        ax.imshow(rho[:, :, k].T, origin='lower', extent=ext, cmap='Greys', vmin=0, vmax=1)
        ax.set_title(f'z {k * vox.h:.0f}-{(k + 1) * vox.h:.0f}', fontsize=8)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_aspect('equal')
    fig.suptitle(title, fontsize=10)
    fig.tight_layout()
    fig.savefig(path, dpi=110)
    plt.close(fig)


def main(paths):
    warnings.filterwarnings('ignore', message='Matrix is nearly singular')
    os.makedirs(FIGS, exist_ok=True)
    vox = Voxels()
    mesh = setup(vox, domain_mask(vox))
    F, labels = cases(mesh, vox, xs=(0.0, 90.0))
    f = vox.f
    in_base = mesh.field(f['eg_base_solid']) > 0.01
    k0 = stiffness(mesh, vox, F, mesh.field(f['eg_base']))
    rows = [('current', vox.info['vols']['Base front'] + vox.info['vols']['Base rear'], k0),
            ('solid (no pockets)', vox.info['solid_base_L'], stiffness(mesh, vox, F, mesh.field(f['eg_base_solid'])))]
    plot_depth(vox, f['eg_base'] > 0.5, 'Current base: solid depth from the top', os.path.join(FIGS, 'base_current.png'),
               f['eg_base_solid'])
    other = os.environ.get('COMPARE', 'vox_current')
    if other != os.environ.get('FEA_VOX', 'vox_current') and os.path.exists(os.path.join(os.path.dirname(FIGS), other + '.npz')):
        # another design's base (same grid) in this frame, e.g. the base now drawn in build_cnc.py
        fin = Voxels(other).f['eg_base']
        rows.append(('final (CAD)', fin.sum() * vox.h ** 3 / 1e6, stiffness(mesh, vox, F, mesh.field(fin))))
        plot_depth(vox, fin > 0.5, f"Final base (build_cnc.py): {rows[-1][1]:.1f} L, solid depth from the top",
                   os.path.join(FIGS, 'base_final.png'), f['eg_base_solid'])
    for p in paths:
        r = np.load(p, allow_pickle=True)
        rho = (r['rho'] > 0.5).astype(float)      # thresholded, as it would be cast
        eg = np.where(in_base, mesh.field(f['eg_base_solid']) * mesh.field(rho), 0.0)
        name = os.path.basename(p)[3:-4]
        vol = eg.sum() * vox.h ** 3 / 1e6
        rows.append((name, vol, stiffness(mesh, vox, F, eg)))
        title = f'{name}: {vol:.1f} L'
        plot_depth(vox, rho, title + ', solid depth from the top', os.path.join(FIGS, f'base_{name}_depth.png'),
                   f['eg_base_solid'])
        if name.startswith('free'):
            plot_layers(vox, rho, title + ', horizontal slices (black = casting)',
                        os.path.join(FIGS, f'base_{name}_layers.png'))
    print(f"{'design':22s} {'EG L':>6s} {'kx':>6s} {'ky':>6s} {'kz':>6s} {'mean':>6s} {'worst':>6s}  (N/um, ratio to current)")
    for name, vol, k in rows:
        s = summary(k, k0)
        print(f"{name:22s} {vol:6.1f} {s['x']:6.1f} {s['y']:6.1f} {s['z']:6.1f} {s['mean']:6.3f} {s['worst']:6.3f}")
    np.savez(os.path.join(os.path.dirname(FIGS), 'eval_result.npz'), names=[r[0] for r in rows], vols=[r[1] for r in rows], k=np.array([r[2] for r in rows]),
             labels=labels)

    fig, ax = plt.subplots(figsize=(6, 4))
    for name, vol, k in rows:
        s = summary(k, k0)
        kind = name.split('_')[0].split(' ')[0]
        mk, col = {'current': ('s', 'k'), 'solid': ('^', 'k'), 'final': ('*', 'r'), 'pocket': ('o', 'C0'),
                   'free': ('D', 'C1')}[kind]
        ax.plot(vol, s['mean'], mk, color=col, ms=12 if mk == '*' else 7)
        ax.annotate(name, (vol, s['mean']), textcoords='offset points', xytext=(5, -10), fontsize=7)
    ax.set_title('Base only (beam, uprights as before). o open pockets, D lost cores', fontsize=9)
    ax.set_xlabel('base epoxy granite (L)')
    ax.set_ylabel('frame stiffness at the tool / current (mean of 18 cases)')
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGS, 'tradeoff.png'), dpi=130)


if __name__ == '__main__':
    main(sys.argv[1:])
