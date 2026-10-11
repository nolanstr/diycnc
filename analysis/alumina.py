"""Aluminium oxide grit in place of the sand: how much stiffer, and where it pays.

    python alumina.py

1. The epoxy granite's modulus from its ingredients (differential effective medium, spheres in
   epoxy), for the build guide's mix and with the coarse sand (0.6-3 mm) and/or the fine sand
   (0.1-0.6 mm) swapped for the same volume of alumina. The plain mix comes out near the 30 GPa
   the frame model assumes; only the ratios are used.
2. The frame stiffness with that ratio applied to the beam, the beam and uprights, or everything.
"""

import warnings

import numpy as np

from loads import F0, cases, domain_mask, setup
from vfe import E_EG, E_MIN, E_ST, Voxels

# (weight %, density, E GPa, Poisson) of the build guide's mix
MIX = dict(epoxy=(8.5, 1.15, 3.5, 0.35), whiting=(9.0, 2.71, 70.0, 0.30), fine=(15.0, 2.65, 70.0, 0.20),
           coarse=(27.5, 2.65, 70.0, 0.20), pea=(20.0, 2.65, 70.0, 0.20), gravel=(20.0, 2.65, 70.0, 0.20))
# (density, E GPa, Poisson): brown fused #16 for the coarse sand; black 70 grit (less pure, taken
# a little softer) for the fine sand
GRIT = dict(coarse=(3.95, 370.0, 0.23), fine=(3.75, 300.0, 0.23))


def kg(E, nu):
    return E / (3 * (1 - 2 * nu)), E / (2 * (1 + nu))


def dem(mix, steps=4000):
    """Differential effective medium: the fillers added little by little to the epoxy."""
    vol = {k: w / rho for k, (w, rho, _, _) in mix.items()}
    tot = sum(vol.values())
    fill = [(vol[k] / tot, *kg(E, nu)) for k, (_, _, E, nu) in mix.items() if k != 'epoxy']
    phi_end = sum(f for f, _, _ in fill)
    K, G = kg(*mix['epoxy'][2:])
    phi, dphi = 0.0, phi_end / steps
    for _ in range(steps):
        z = G * (9 * K + 8 * G) / (6 * (K + 2 * G))
        dK = sum(f / phi_end * (Ki - K) * (3 * K + 4 * G) / (3 * Ki + 4 * G) for f, Ki, Gi in fill)
        dG = sum(f / phi_end * (Gi - G) * (G + z) / (Gi + z) for f, Ki, Gi in fill)
        K, G, phi = K + dK * dphi / (1 - phi), G + dG * dphi / (1 - phi), phi + dphi
    return 9 * K * G / (3 * K + G)


def main():
    e0 = dem(MIX)
    print(f'mix modulus: plain {e0:.1f} GPa')
    ratios = {}
    for name, keys in (('coarse', ('coarse',)), ('fine', ('fine',)), ('both', ('coarse', 'fine'))):
        mix = dict(MIX)
        for k in keys:
            w, rho, _, _ = MIX[k]
            rho_a, E_a, nu_a = GRIT[k]
            mix[k] = (w * rho_a / rho, rho_a, E_a, nu_a)
        ratios[name] = dem(mix) / e0
        print(f'  alumina as the {name:6s} sand: x{ratios[name]:.2f}')

    warnings.filterwarnings('ignore', message='Matrix is nearly singular')
    vox = Voxels()
    f = vox.f
    mesh = setup(vox, domain_mask(vox))
    fld = mesh.field
    F, _ = cases(mesh, vox, xs=(0.0, 90.0))
    st = sum(fld(f[f'st_{g}']) for g in ('base', 'up', 'beam'))
    for name, r, groups in (('none', 1.0, ()), ('coarse, beam', ratios['coarse'], ('beam',)),
                            ('coarse, beam + uprights', ratios['coarse'], ('beam', 'up')),
                            ('fine, beam + uprights', ratios['fine'], ('beam', 'up')),
                            ('both, beam + uprights', ratios['both'], ('beam', 'up')),
                            ('both, everything', ratios['both'], ('beam', 'up', 'base'))):
        E = E_MIN * E_EG + E_ST * st + sum(E_EG * (r if g in groups else 1.0) * fld(f[f'eg_{g}'])
                                            for g in ('base', 'up', 'beam'))
        k = F0 ** 2 / (F * mesh.solve(E, F)).sum(0) / 1e3
        print(f'alumina {name:24s} kx {k[0::3].mean():5.1f} ky {k[1::3].mean():5.1f} kz {k[2::3].mean():5.1f}',
              flush=True)


if __name__ == '__main__':
    main()
