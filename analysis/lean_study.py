"""A leaner frame: less cast-in steel and smaller castings, judged at the tool and by the natural frequencies.

    VOX_PARTS=1 VOX_SKIP=TieRod,DrawRod,CrossRod VOX_OUT=analysis/vox_lean0 freecadcmd analysis/voxelize.py
    VOX_P='{"upright_t": 65}' VOX_PARTS=1 VOX_SKIP=... VOX_OUT=analysis/vox_lean_ut65 freecadcmd analysis/voxelize.py
    python lean_study.py lean0: lean0:beam12+cols18 lean_ut65:beam12      # <voxels>:<steel changes, + joined>

Each case is a voxelized frame (vox_<name>, with its per-part steel) and steel changes as in steel_study.py: a
part's steel scaled where it lies (a thinner bar or wall) or taken out (filled with epoxy granite). It prints the
frame's stiffness; the machine's at the tool, the moving parts (chain.py, as drawn) in series with the frame; the
four lowest modes (modal.py); the castings' and the steel's mass; and what changes in cost. --save writes
vox_<name>_<changes>.npz/json, so chain.py and modal.py can run on it (FEA_VOX=...).
"""

import os
import shutil
import sys
import warnings

import numpy as np

from loads import F0, cases, domain_mask, moduli, setup
from modal import mass_matrix, modes
from vfe import Voxels

HERE = os.path.dirname(os.path.abspath(__file__))
KM = (4.0, 3.9, 7.2)                     # the moving parts alone at the tool, N/um (chain.py, as drawn)
RHO_EG = 2.35                            # kg/L, the sand mix
EPOXY = 10.3 / 103.6 * 13.8              # $ of epoxy per kg of casting (10.3 kg in the drawn 103.6 kg, $13.8/kg)
LB = 2.2046
TUBE = ('UprightColumn', 'BasePedestalColumn', 'BaseGirder', 'BaseCross')     # $3/lb; flat bar $2/lb

# part-name prefix -> steel scale (0 = taken out)
VARIANTS = {
    'beam12': {'BeamFacePlate': 2 / 3, 'BeamBackPlate': 2 / 3},     # beam bars 3/4 -> 1/2 in
    'beam1238': {'BeamFacePlate': 2 / 3, 'BeamBackPlate': 1 / 2},   # face bar 1/2 in, back bar 3/8 in (3/8 in at
                                                                    # the face is too thin for the voxels at the BK)
    'back12': {'BeamBackPlate': 2 / 3},                             # the back bar alone 1/2 in
    'cols18': {'UprightColumn': 2 / 3, 'BasePedestalColumn': 2 / 3},  # 2x2 tube 3/16 -> 1/8 in wall
    'tops38': {'TopPlate': 3 / 4},                                  # top plates 3/8 in bars
    'girders316': {'BaseGirder': 1.5},                              # 2x3 tube 1/8 -> 3/16 in wall
}


def group(name):
    if name.startswith(('Beam', 'X_')):
        return 'beam'
    return 'up' if name.startswith(('Upright', 'TopPlate', 'TieRod')) else 'base'


def run(case, save=False, ref=None):
    base, _, changes = case.partition(':')
    vox = Voxels('vox_' + base)
    parts = np.load(os.path.join(HERE, f'vox_{base}_parts.npz'))
    spec = {}
    for v in filter(None, changes.split('+')):
        spec.update(VARIANTS[v])
    f = {k: v.copy() for k, v in vox.f.items()}
    dkg, dcost = 0.0, 0.0
    for prefix, s in spec.items():
        for p in parts.files:
            if p.startswith(prefix):
                g = group(p)
                a = np.minimum(parts[p], f[f'st_{g}'])
                f[f'st_{g}'] += (s - 1) * a
                if s == 0:
                    f[f'eg_{g}'] += a
                kg = (s - 1) * a.sum() * vox.h ** 3 * 7.85e-6
                dkg += kg
                dcost += kg * LB * (3.0 if p.startswith(TUBE) else 2.0)
    vox.f = f
    mesh = setup(vox, domain_mask(vox))
    F, _ = cases(mesh, vox, xs=(0.0, 90.0))
    E = moduli(mesh, f, mesh.field(f['eg_base']))
    k = F0 ** 2 / (F * mesh.solve(E, F)).sum(0) / 1e3
    k = np.array([k[0::3].mean(), k[1::3].mean(), k[2::3].mean()])
    tool = 1 / (1 / np.array(KM) + 1 / k)
    eg = sum(mesh.field(f[f'eg_{g}']) for g in ('base', 'up', 'beam'))
    st = sum(mesh.field(f[f'st_{g}']) for g in ('base', 'up', 'beam'))
    M, _ = mass_matrix(mesh, vox, eg, st)
    fr, _ = modes(mesh, E, M, 4)
    cast = sum(f[f'eg_{g}'].sum() for g in ('base', 'up', 'beam')) * vox.h ** 3 / 1e6 * RHO_EG
    steel = sum(f[f'st_{g}'].sum() for g in ('base', 'up', 'beam')) * vox.h ** 3 * 7.85e-6
    out = dict(k=k, tool=tool, fr=fr, cast=cast, steel=steel, dcost=dcost)
    if ref is None:
        ref = out
    epoxy = (cast - ref['cast']) * EPOXY
    print(f"{case:30s} frame {k[0]:6.1f} {k[1]:6.1f} {k[2]:6.1f}  tool {tool[0]:4.2f} {tool[1]:4.2f} {tool[2]:4.2f} "
          f"({' '.join(f'{100 * (a / b - 1):+5.1f}%' for a, b in zip(tool, ref['tool']))})  "
          f"modes {' '.join(f'{x:4.0f}' for x in fr)} Hz  castings {cast:5.1f} kg  steel {steel:4.1f} kg  "
          f"total {cast + steel - ref['cast'] - ref['steel']:+5.1f} kg  steel ${dcost:+4.0f} epoxy ${epoxy:+4.0f}",
          flush=True)
    if save and changes:
        name = f'vox_{base}_{changes.replace("+", "_")}'
        np.savez_compressed(os.path.join(HERE, name + '.npz'), **f)
        shutil.copy(os.path.join(HERE, f'vox_{base}.json'), os.path.join(HERE, name + '.json'))
    return out


def main():
    warnings.filterwarnings('ignore', message='Matrix is nearly singular')
    save = '--save' in sys.argv
    names = [a for a in sys.argv[1:] if not a.startswith('--')]
    ref = None
    for case in names:
        out = run(case, save, ref)
        ref = ref or out


if __name__ == '__main__':
    main()
