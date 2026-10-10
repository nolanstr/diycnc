"""Frame stiffness at the tool for voxelized what-if variants (current base).

    FEA_VOX=vox_beam_d140 python whatif.py
"""
import os
import warnings

from loads import F0, cases, domain_mask, moduli, setup
from vfe import Voxels

warnings.filterwarnings('ignore', message='Matrix is nearly singular')
vox = Voxels()
mesh = setup(vox, domain_mask(vox))
F, labels = cases(mesh, vox, xs=(0.0, 90.0))
U = mesh.solve(moduli(mesh, vox.f, mesh.field(vox.f['eg_base'])), F)
k = F0 ** 2 / (F * U).sum(0) / 1e3
eg = sum(vox.f[f'eg_{g}'].sum() for g in ('base', 'up', 'beam')) * vox.h ** 3 / 1e6
print(f"{os.environ.get('FEA_VOX', 'vox_current'):16s} EG {eg:5.1f} L  kx {k[0::3].mean():5.1f}  ky {k[1::3].mean():5.1f}  kz {k[2::3].mean():5.1f}")
