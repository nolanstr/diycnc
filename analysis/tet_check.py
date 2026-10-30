"""How stiff is the voxel model? One upright with its cast-in steel, solved with the voxel bricks (vfe.py) and with
cad-rust-app's 10-node tetrahedra, each part meshed at its own size and tied where it touches the next.

    python analysis/tet_check.py                 # tets at two refinements; voxels at 10, 7.5 and 5 mm

Both models are cut to the same slab of the upright, between the grid planes every voxel size shares
(multiples of 30 mm), so neither has thin partial layers at its ends: the bottom section is held and 1 kN in x,
y or z is spread over the top section as a uniform traction. The stiffness is the force over the top section's
average displacement. The voxels are the frame's (vox_sym10, vox_sym7.5, vox_sym5;
VOX_SKIP=TieRod,DrawRod,CrossRod) cut down to the left upright; the tet model leaves out the same rods, the
printed rings and the gaskets.
"""

import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CAD = os.path.join(os.path.dirname(HERE), 'model')
sys.path.insert(0, HERE)
from vfe import E_EG, E_ST, NU, Mesh, Voxels  # noqa: E402

F0 = 1000.0
SKIP = ('TieRod', 'DrawRod', 'CrossRod')
# element sizes (mm): casting, tube walls, flat bar
LEVELS = [(16.0, 3.2, 6.35), (12.0, 2.5, 4.8)]     # 425,000 elements and 8 minutes at the finer one


def upright_parts():
    src = open(os.path.join(CAD, 'build_cnc.py')).read()
    src = src[:src.rstrip().rfind('\nmain()')]
    ns = {'__file__': os.path.join(CAD, 'build_cnc.py'), '__name__': 'build_cnc'}
    exec(compile(src, 'build_cnc.py', 'exec'), ns)
    m = ns['build']()
    out = []
    for p in m.parts:
        if p['container'] != 'FrameUprightL' or (p['name'] not in m.structure and not p['name'].endswith('Casting')):
            continue
        if p['look'] in ('printed', 'rubber') or p['name'].startswith(SKIP):
            continue
        out.append(p)
    return out


def slab(parts):
    """The z range both models are cut to: grid planes of all three voxel sizes."""
    z0 = min(p['shape'].BoundBox.ZMin for p in parts)
    z1 = max(p['shape'].BoundBox.ZMax for p in parts)
    return 30.0 * np.ceil(z0 / 30.0), 30.0 * np.floor(z1 / 30.0)


def tets(parts, sizes, za, zb):
    from cadrust import _core as C
    from cadrust.freecad import Part, Vector
    hc, ht, hb = sizes
    fm = C.FeModel()
    big = 1e4
    keep = Part.makeBox(2 * big, 2 * big, zb - za, Vector(-big, -big, za))
    for p in parts:
        s = p['shape'].common(keep)
        if s.isNull() or s.Volume < 1.0:
            continue
        if p['name'].endswith('Casting'):
            fm.add_body(s._s, E_EG, NU, 2.35, hc, p['name'])
        else:
            tube = p['look'] == 'steeltube' and 'Column' in p['name']
            fm.add_body(s._s, E_ST, NU, 7.85, ht if tube else hb, p['name'])
    t = time.time()
    nodes, els, ties = fm.mesh(tol=0.3)
    bottom = fm.patch((-big, -big, za - 0.5, big, big, za + 0.5), None, (0, 0, -1))
    top = fm.patch((-big, -big, zb - 0.5, big, big, zb + 0.5), None, (0, 0, 1))
    fm.fix(bottom)
    fm.solve([[(top, tuple(F0 * e for e in d))] for d in np.eye(3)])
    k = [F0 / abs(fm.displacement(i, top)[i]) / 1e3 for i in range(3)]
    return k, nodes, els, time.time() - t


def voxels(name, za, zb):
    vox = Voxels(name, sym=False)
    f = vox.f
    eg, st = f['eg_up'], f['st_up']
    x, z = vox.centers(0), vox.centers(2)
    mask = ((eg + st) > 0.01) & (x[:, None, None] < 0) & (z[None, None, :] > za) & (z[None, None, :] < zb)
    mesh = Mesh(vox, mask)
    zn = mesh.xyz[:, 2]
    bottom = np.nonzero(np.abs(zn - za) < 1e-6)[0]
    mesh.fixed = np.sort(np.concatenate([3 * bottom + c for c in range(3)]))
    # a uniform traction on the top section: each element face there puts a quarter on each of its nodes
    w = np.zeros(mesh.nn)
    top_el = np.abs(mesh.center[:, 2] + vox.h / 2 - zb) < 1e-6
    np.add.at(w, mesh.enodes[top_el][:, 4:].ravel(), 0.25)
    w /= w.sum()
    E = E_EG * mesh.field(eg) + E_ST * mesh.field(st) + 1e-6 * E_EG
    F = np.zeros((mesh.ndof, 3))
    for c in range(3):
        F[c::3, c] = F0 * w
    t = time.time()
    U = mesh.solve(E, F)
    k = [F0 / abs((w * U[c::3, c]).sum()) / 1e3 for c in range(3)]
    return k, mesh.ne, time.time() - t


def main():
    parts = upright_parts()
    za, zb = slab(parts)
    print('upright L:', ', '.join(p['name'] for p in parts))
    print(f'cut to z = {za:g} .. {zb:g} mm')
    print(f"{'model':38s} {'kx':>7s} {'ky':>7s} {'kz':>7s}  (N/um)")
    for name in ('vox_sym10', 'vox_sym7.5', 'vox_sym5'):
        k, ne, dt = voxels(name, za, zb)
        print(f'voxels {name[7:]:>4s} mm ({ne:7d} bricks)        {k[0]:7.1f} {k[1]:7.1f} {k[2]:7.1f}   {dt:5.0f} s', flush=True)
    for sizes in LEVELS:
        k, nodes, els, dt = tets(parts, sizes, za, zb)
        print(f'tets {sizes[0]:g}/{sizes[1]:g}/{sizes[2]:g} mm ({els:7d} el, {nodes:7d} nodes) {k[0]:7.1f} {k[1]:7.1f} {k[2]:7.1f}   {dt:5.0f} s',
              flush=True)


if __name__ == '__main__':
    main()
