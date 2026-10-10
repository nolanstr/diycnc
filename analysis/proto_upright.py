"""Try castable versions of the optimized (raked-buttress) upright on the voxel model.

    python proto_upright.py

Each variant replaces the uprights' epoxy granite with a side profile (y, z) extruded over
part of the upright's width; the base, beam and all steel stay as in vox_current.
"""

import warnings

import numpy as np
from matplotlib.path import Path

from loads import F0, cases, domain_mask, setup
from topopt_frame import upright_domain
from vfe import E_EG, E_MIN, E_ST, Voxels

SUB = 4


def profile_field(vox, parts):
    """parts: list of (polygon [(y, z)], x_in, x_out, sign) with x measured outward from the upright's inner face;
    sign +1 adds material, -1 removes it. Returns the EG fraction for both uprights (mirrored)."""
    d, h, n, o = vox.d, vox.h, vox.n, vox.o
    xs = o[0] + (np.arange(n[0] * SUB) + 0.5) * h / SUB
    ys = o[1] + (np.arange(n[1] * SUB) + 0.5) * h / SUB
    zs = o[2] + (np.arange(n[2] * SUB) + 0.5) * h / SUB
    Yg, Zg = np.meshgrid(ys, zs, indexing='ij')
    pts = np.column_stack([Yg.ravel(), Zg.ravel()])
    field = np.zeros((len(xs), len(ys), len(zs)), bool)
    ax = np.abs(xs) - d['inner']                   # distance out from the inner face
    for poly, x0, x1, sign in parts:
        inside = Path(poly).contains_points(pts).reshape(len(ys), len(zs))
        sel = (ax >= x0) & (ax <= x1)
        if sign > 0:
            field[sel] |= inside[None]
        else:
            field[sel] &= ~inside[None]
    frac = field.reshape(n[0], SUB, n[1], SUB, n[2], SUB).mean(axis=(1, 3, 5))
    return np.clip(frac - vox.f['st_up'], 0, 1)


def main():
    warnings.filterwarnings('ignore', message='Matrix is nearly singular')
    vox = Voxels('vox_current')
    d, f, h = vox.d, vox.f, vox.h
    upL, upR = upright_domain(vox)
    mesh = setup(vox, domain_mask(vox) | upL | upR)
    F, _ = cases(mesh, vox, xs=(0.0, 90.0))
    fld = mesh.field
    st = fld(f['st_base']) + fld(f['st_up']) + fld(f['st_beam'])
    bt, bb = d['base_top'], d['beam_bot']
    W = d['outer'] - d['inner']

    def run(name, up_eg, base_eg=None):
        base_eg = fld(f['eg_base']) if base_eg is None else base_eg
        E = E_MIN * E_EG + E_EG * (base_eg + fld(up_eg) + fld(f['eg_beam'])) + E_ST * st
        U = mesh.solve(E, F)
        k = F0 ** 2 / (F * U).sum(0) / 1e3
        vol = up_eg.sum() * h ** 3 / 1e6 / 2
        print(f'{name:42s} upright {vol:4.1f} L each  kx {k[0::3].mean():5.1f} ky {k[1::3].mean():5.1f} '
              f'kz {k[2::3].mean():5.1f}', flush=True)

    run('current', f['eg_up'])
    back = 309.5                                   # back face (the beam's back)
    for yf, yt in ((-190.0, 100.0), (-120.0, 100.0), (-60.0, 129.5)):
        full = [(yf, bt), (yt, bb), (back, bb), (back, bt)]
        run(f'buttress full width, foot y {yf:.0f}', profile_field(vox, [(full, 0, W, 1)]))
        front = [(yf, bt), (yt, bb), (130.0, bb), (130.0, bt)]
        rear = [(130.0, bt), (130.0, bb), (back, bb), (back, bt)]
        run(f'  rear block + inner 40 mm gusset', profile_field(vox, [(rear, 0, W, 1), (front, 0, 40, 1)]))
        # outer-side window: the front triangle hollowed from the outer face, 40 mm deep, 35 mm inset
        tri = np.array([(yf, bt), (yt, bb), (130.0, bb), (130.0, bt)])
        c = tri.mean(0)
        inset = [tuple(c + (p - c) * 0.62) for p in tri]
        run(f'  full width, outer window', profile_field(vox, [(full, 0, W, 1), (inset, 40, W, -1)]))


if __name__ == '__main__':
    main()
