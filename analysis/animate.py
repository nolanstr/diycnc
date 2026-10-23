"""Animated figures of the frame: its lowest vibration modes and its deflection under the cutting loads.

    python animate.py      # figs/modes.gif and figs/deflection.gif (about 4 min)

Needs pyvista and imageio (both in environment.yml). The motion is exaggerated so it shows; the
colors are the real relative motion (modes) or deflection in um at 1 kN (loads). Each loop starts
at the peak, so the first frame (all a PDF shows) is the deflected shape.
"""

import os
import warnings

import numpy as np
import pyvista as pv

from evaluate import FIGS
from loads import F0, cases, domain_mask, moduli, setup
from modal import mass_matrix, modes
from vfe import Voxels

N_FRAMES = 36
SHOW = 25.0          # mm of drawn motion at the peak
WINDOW = (560, 440)  # pixels per panel


def surface(mesh, el):
    """Outer surface of the elements `el`, with the mesh node of each surface point."""
    cells = np.hstack([np.full((el.sum(), 1), 8), mesh.enodes[el]]).ravel()
    grid = pv.UnstructuredGrid(cells, np.full(el.sum(), pv.CellType.HEXAHEDRON, np.uint8), mesh.xyz)
    surf = grid.extract_surface(pass_pointid=True, algorithm='dataset_surface')
    return surf, surf.point_data['vtkOriginalPointIds']


def panel(p, surf, title, clim, label):
    p.add_text(title, font_size=11, color='black')
    p.add_mesh(surf, scalars='u', cmap='turbo', clim=clim, show_edges=False,
               scalar_bar_args=dict(title=label, color='black', n_labels=3, fmt='%.0f',
                                    position_x=0.25, position_y=0.04, width=0.5, height=0.06))
    p.camera_position = [(1700, -1900, 1300), (0, 40, 230), (0, 0, 1)]
    p.camera.zoom(1.15)


def animate(path, shape, panels, clim, label, swing=True):
    """panels: (title, nodal motion (nn x 3, peak SHOW mm), nodal color). swing: back and forth
    (a vibration mode); otherwise between the peak and rest (a load put on and taken off)."""
    p = pv.Plotter(off_screen=True, shape=shape, window_size=(WINDOW[0] * shape[1], WINDOW[1] * shape[0]),
                   border=False)
    p.set_background('white')
    surfs = []
    for i, (title, u, c) in enumerate(panels):
        surf, ids = surface(*BODY)
        surf.point_data['u'] = c[ids]
        p.subplot(*divmod(i, shape[1]))
        panel(p, surf, title, clim, label)
        surfs.append((surf, surf.points.copy(), u[ids]))
    p.open_gif(path, fps=18)
    for t in range(N_FRAMES):
        s = np.cos(2 * np.pi * t / N_FRAMES)
        s = s if swing else 0.5 * (1 + s)
        for surf, x0, u in surfs:
            surf.points = x0 + s * u
        p.write_frame()
    p.close()
    print(f'{os.path.relpath(path)}: {os.path.getsize(path) / 1e6:.1f} MB', flush=True)


def main():
    global BODY
    warnings.filterwarnings('ignore', message='Matrix is nearly singular')
    os.makedirs(FIGS, exist_ok=True)
    vox = Voxels()
    mesh = setup(vox, domain_mask(vox))
    f = vox.f
    E = moduli(mesh, f, mesh.field(f['eg_base']))
    eg = sum(mesh.field(f[f'eg_{g}']) for g in ('base', 'up', 'beam'))
    st = sum(mesh.field(f[f'st_{g}']) for g in ('base', 'up', 'beam'))
    BODY = (mesh, (eg + st) > 0.3)

    M, _ = mass_matrix(mesh, vox, eg, st)
    fr, phi = modes(mesh, E, M, 4)
    panels = []
    for i in range(4):
        u = phi[:, i].reshape(-1, 3)
        mag = np.linalg.norm(u, axis=1)
        panels.append((f'Mode {i + 1}: {fr[i]:.0f} Hz', u * SHOW / mag.max(), 100 * mag / mag.max()))
    animate(os.path.join(FIGS, 'modes.gif'), (2, 2), panels, (0, 100), 'motion, % of peak')

    F, labels = cases(mesh, vox, yts=(0.0,))   # tool at the middle of X, table centered
    U = mesh.solve(E, F)
    k = F0 ** 2 / (F * U).sum(0) / 1e3
    panels = []
    for j, ax in enumerate('xyz'):
        u = U[:, j].reshape(-1, 3)
        mag = np.linalg.norm(u, axis=1)
        x = float(f'{SHOW / mag.max():.1g}')
        panels.append((f'{F0 / 1e3:.0f} kN in {ax.upper()}: {k[j]:.0f} N/um, motion x{x:,.0f}', u * x, 1e3 * mag))
    top = max(p_[2].max() for p_ in panels)
    animate(os.path.join(FIGS, 'deflection.gif'), (1, 3), panels, (0, top), 'deflection, um', swing=False)


if __name__ == '__main__':
    main()
