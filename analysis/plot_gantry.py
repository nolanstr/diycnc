"""Where topopt_gantry.py takes the epoxy granite out: figs/gantry_<frac>.png.

    python plot_gantry.py 0.7 0.6
    python plot_gantry.py --ref sym10 gantry_0.7_sym10 damped_0.7_sym10     # any voxels, against --ref

Three views, each the share of the casting removed through its depth: an upright from the side (y, z,
through its width), the beam end-on (y, z, along its length between the uprights) and the beam from the
front (x, z, through its depth).
"""

import sys

import matplotlib
import numpy as np

matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402

from vfe import Voxels  # noqa: E402


def main(fracs, ref_name='lean0'):
    ref = Voxels('vox_' + ref_name, sym=False)
    h, o, n = ref.h, ref.o, ref.info['n']
    x = o[0] + (np.arange(n[0]) + 0.5) * h
    ext = lambda a, b: [o[a], o[a] + n[a] * h, o[b], o[b] + n[b] * h]
    fig, axs = plt.subplots(len(fracs), 3, figsize=(15, 4.2 * len(fracs)), squeeze=False,
                            gridspec_kw=dict(width_ratios=[1.2, 1.0, 2.2]))
    for row, frac in zip(axs, fracs):
        name = f'gantry_{frac:g}' if isinstance(frac, float) else frac
        v = Voxels('vox_' + name, sym=False)
        label = f'keep {frac:.0%}' if isinstance(frac, float) else name
        for ax, g, sel, (a, b), title in (
                (row[0], 'up', x < 0, (1, 2), 'left upright, from the side'),
                (row[1], 'beam', np.abs(x) < ref.d['inner'], (1, 2), 'beam, end-on'),
                (row[2], 'beam', slice(None), (0, 2), 'beam, from the front')):
            e0, e1 = ref.f[f'eg_{g}'][sel], v.f[f'eg_{g}'][sel]
            if b == 2 and a == 1:
                cast, cut = (e0 > 0.01).sum(0), ((e0 > 0.01) & (e1 < 0.01)).sum(0)
            else:
                cast, cut = (e0 > 0.01).sum(1), ((e0 > 0.01) & (e1 < 0.01)).sum(1)
            share = np.where(cast > 0, cut / np.maximum(cast, 1), np.nan)
            im = ax.imshow(share.T, origin='lower', extent=ext(a, b), cmap='magma_r', vmin=0, vmax=1)
            m = cast > 0
            idx = np.argwhere(m)
            lo, hi = idx.min(0), idx.max(0) + 1
            ax.set_xlim(o[a] + lo[0] * h - 10, o[a] + hi[0] * h + 10)
            ax.set_ylim(o[b] + lo[1] * h - 10, o[b] + hi[1] * h + 10)
            ax.set_aspect('equal')
            ax.set_title(f'{title}: {label}', fontsize=10)
            ax.set_xlabel('xyz'[a] + ' (mm)')
            ax.set_ylabel('z (mm)')
        fig.colorbar(im, ax=row[2], shrink=0.8, label='share removed through the depth')
    fig.tight_layout()
    out = f'figs/gantry_{"_".join(f"{f:g}" if isinstance(f, float) else f for f in fracs)}.png'
    fig.savefig(out, dpi=110)
    print('saved', out)


if __name__ == '__main__':
    args, ref = sys.argv[1:], 'lean0'
    if '--ref' in args:
        k = args.index('--ref')
        ref = args[k + 1]
        args = args[:k] + args[k + 2:]

    def arg(a):
        try:
            return float(a)
        except ValueError:
            return a
    main([arg(a) for a in args], ref)
