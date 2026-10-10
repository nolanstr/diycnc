"""Stiffness of the current frame at the tool, and each module's share of the deflection.

    python baseline.py      (FEA_VOX=vox_previous for the design before the optimization)
"""

import os
import time
import warnings

import numpy as np

from loads import F0, cases, domain_mask, moduli, setup
from vfe import Voxels


def run(mesh, E, F):
    t = time.time()
    U = mesh.solve(E, F)
    C = (F * U).sum(0)
    return F0 ** 2 / C / 1e3, U, time.time() - t     # N/um


def main():
    warnings.filterwarnings('ignore', message='Matrix is nearly singular')
    vox = Voxels()
    t = time.time()
    mesh = setup(vox, domain_mask(vox))
    print(f'{mesh.ne} elements, {mesh.ndof} dof, setup {time.time() - t:.1f} s')
    F, labels = cases(mesh, vox, xs=(0.0, 90.0))
    f = vox.f
    cur = mesh.field(f['eg_base'])
    solid = mesh.field(f['eg_base_solid'])
    rows = {}
    for name, E in [('current', moduli(mesh, f, cur)),
                    ('solid base (no pockets)', moduli(mesh, f, solid)),
                    ('base rigid', moduli(mesh, f, cur, ('base',))),
                    ('uprights rigid', moduli(mesh, f, cur, ('up',))),
                    ('beam rigid', moduli(mesh, f, cur, ('beam',)))]:
        k, U, dt = run(mesh, E, F)
        rows[name] = k
        print(f'{name:26s} mean kx {k[0::3].mean():6.1f}  ky {k[1::3].mean():6.1f}  kz {k[2::3].mean():6.1f}   ({dt:.0f} s)')
    print('cases:', labels)
    np.savez(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'baseline_result.npz'), labels=labels, **{k.replace(' ', '_'): v for k, v in rows.items()})


if __name__ == '__main__':
    main()
