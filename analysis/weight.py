"""Lighter base variants: frame stiffness against casting mass, with the alumina grits in the beam
and uprights (analysis/alumina.py).

    python weight.py vox_current vox_w_skin20 [...]

The variants are voxelized from build_cnc.py with parameter overrides, e.g.
    VOX_P='{"base_core_skin": 20}' VOX_OUT=analysis/vox_w_skin20 freecadcmd analysis/voxelize.py
"""

import sys
import warnings

from alumina import GRIT, MIX, dem
from loads import F0, cases, domain_mask, setup
from vfe import E_EG, E_MIN, E_ST, Voxels

RHO = 2.35                                   # kg/L, the sand mix
GRIT_GROUPS = ('up', 'beam')


def alumina_factors():
    """Stiffness and density ratios of the mix with both grits."""
    e0 = dem(MIX)
    mix, extra = dict(MIX), 0.0
    for k in ('coarse', 'fine'):
        w, rho, _, _ = MIX[k]
        rho_a, E_a, nu_a = GRIT[k]
        mix[k] = (w * rho_a / rho, rho_a, E_a, nu_a)
        extra += w / 100 * (rho_a / rho - 1)
    return dem(mix) / e0, 1 + extra


def main(names):
    warnings.filterwarnings('ignore', message='Matrix is nearly singular')
    r_e, r_m = alumina_factors()
    print(f'alumina in {", ".join(GRIT_GROUPS)}: E x{r_e:.2f}, density x{r_m:.2f}')
    ref = None
    for name in names:
        vox = Voxels(name)
        f, h = vox.f, vox.h
        mesh = setup(vox, domain_mask(vox))
        fld = mesh.field
        F, _ = cases(mesh, vox, xs=(0.0, 90.0))
        st = sum(fld(f[f'st_{g}']) for g in ('base', 'up', 'beam'))
        E = E_MIN * E_EG + E_ST * st + sum(E_EG * (r_e if g in GRIT_GROUPS else 1.0) * fld(f[f'eg_{g}'])
                                            for g in ('base', 'up', 'beam'))
        k = F0 ** 2 / (F * mesh.solve(E, F)).sum(0) / 1e3
        k = (k[0::3].mean(), k[1::3].mean(), k[2::3].mean())
        vol = {g: f[f'eg_{g}'].sum() * h ** 3 / 1e6 for g in ('base', 'up', 'beam')}
        kg = sum(v * RHO * (r_m if g in GRIT_GROUPS else 1.0) for g, v in vol.items())
        ref = ref or (k, kg)
        print(f'{name:18s} base {vol["base"]:5.1f} L  castings {kg:5.1f} kg ({kg - ref[1]:+5.1f})  '
              f'kx {k[0]:5.1f} ky {k[1]:5.1f} kz {k[2]:5.1f}  '
              f'({" ".join(f"{100 * (a / b - 1):+.1f}%" for a, b in zip(k, ref[0]))})', flush=True)


if __name__ == '__main__':
    main(sys.argv[1:])
