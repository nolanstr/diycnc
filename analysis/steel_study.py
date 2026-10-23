"""Where steel pays: the frame with chosen skeleton parts made thicker (their steel scaled up in
the voxels they fill) or taken out (their voxels filled with epoxy granite). Plain sand unless
FEA_GRIT says otherwise.

    VOX_PARTS=1 VOX_SKIP=TieRod,DrawRod,CrossRod VOX_OUT=analysis/vox_grit freecadcmd analysis/voxelize.py
    FEA_VOX=vox_grit python steel_study.py                      # every variant (about 4 min each)
    FEA_VOX=vox_grit python steel_study.py beam34+cols316       # parts combined with +

vox_grit is the frame as it was with the #16 grit (3/8 in beam bars, 1/8 in column walls).
"""

import os
import sys
import warnings

import numpy as np

from loads import F0, cases, domain_mask, moduli, setup
from vfe import Voxels

# part-name prefix -> steel scale (0 = taken out)
VARIANTS = {
    'beam12': {'BeamFacePlate': 4 / 3, 'BeamBackPlate': 4 / 3},     # beam bars 3/8 -> 1/2 in
    'beam58': {'BeamFacePlate': 5 / 3, 'BeamBackPlate': 5 / 3},     # -> 5/8 in
    'beam34': {'BeamFacePlate': 2.0, 'BeamBackPlate': 2.0},         # -> 3/4 in
    'back34': {'BeamBackPlate': 2.0},
    'noback': {'BeamBackPlate': 0.0},
    'cols316': {'UprightColumn': 1.5},                              # 2x2 tube 1/8 -> 3/16 in wall
    'pedcols316': {'BasePedestalColumn': 1.5},
    'tops': {'TopPlate': 1.25, 'UprightFoot': 4 / 3},               # top plates 5/8 in bars, feet 1/2 in
    'girders316': {'BaseGirder': 1.5},                              # 2x3 tube 1/8 -> 3/16 in wall
    'basebars': {'BaseRailBar': 4 / 3, 'BaseSeat': 4 / 3, 'BasePedestalBar': 4 / 3},
    'nopedbars': {'BasePedestalBar': 0.0},
    'beamends': {'BeamSeat': 4 / 3, 'BeamCap': 4 / 3},
}


def group(name):
    if name.startswith(('Beam', 'X_')):
        return 'beam'
    return 'up' if name.startswith(('Upright', 'TopPlate', 'TieRod')) else 'base'


def main():
    warnings.filterwarnings('ignore', message='Matrix is nearly singular')
    vox = Voxels()
    parts = np.load(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 os.environ.get('FEA_VOX', 'vox_current') + '_parts.npz'))
    mesh = setup(vox, domain_mask(vox))
    F, _ = cases(mesh, vox, xs=(0.0, 90.0))
    for name in ['as drawn'] + (sys.argv[1:] or list(VARIANTS)):
        spec = {}
        for v in name.split('+') if name != 'as drawn' else ():
            spec.update(VARIANTS[v])
        f = {k: v.copy() for k, v in vox.f.items()}
        added = 0.0
        for prefix, s in spec.items():
            for p in parts.files:
                if p.startswith(prefix):
                    g = group(p)
                    a = np.minimum(parts[p], f[f'st_{g}'])
                    f[f'st_{g}'] += (s - 1) * a
                    if s == 0:
                        f[f'eg_{g}'] += a
                    added += (s - 1) * a.sum() * vox.h ** 3 * 7.85e-6
        U = mesh.solve(moduli(mesh, f, mesh.field(f['eg_base'])), F)
        k = F0 ** 2 / (F * U).sum(0) / 1e3
        print(f'{name:28s} {added:+5.1f} kg steel   X {k[0::3].mean():6.1f}  Y {k[1::3].mean():6.1f}  '
              f'Z {k[2::3].mean():6.1f} N/um', flush=True)


if __name__ == '__main__':
    main()
