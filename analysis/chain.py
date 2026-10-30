"""Stiffness at the tool through the whole chain: the frame (the voxel FEA in loads.py) in series with
the moving parts. The head (X carriage, Z plate with its risers and rails) and the table are voxel
models of their own at 1/8 in; the rail blocks and ballscrews are springs at their catalog stiffness,
each tied to the plate over its footprint as a rigid patch (RBE3 style, like the frame's loads). The
spindle and its clamp are rigid: the tool force goes into the Z plate over the clamp's foot.

    python analysis/chain_geom.py            # the moving parts' geometry -> chain_geom.json
    python chain.py                          # as drawn and every variant
    python chain.py yff car1 car1+yff        # chosen variants, combined with +
    python chain.py --no-frame ...           # the moving parts only

The load cases are the frame's (loads.cases: 1 kN at the tool 50 mm above the table, X at the center
and 90 mm off, the table at both ends and the center), so the compliances add: tool against work =
frame + head + table. The frame's share is cached in chain_frame_<FEA_VOX>.npz (it takes minutes) until
the voxels change; variant geometries in chain_geom_<params>.json.
Each part's share of the deflection is its share of the strain energy.
"""

import json
import os
import subprocess
import sys
import warnings
from types import SimpleNamespace

import numpy as np
import scipy.sparse as sp

from vfe import CholeskyFactor, Mesh

HERE = os.path.dirname(os.path.abspath(__file__))
F0 = 1000.0
H = 3.175                      # voxel, mm: 5 layers in a 5/8 in plate, 6 in a 3/4 in one
E_AL, E_ST = 69e3, 200e3
XS, YTS, DIRS = (0.0, 90.0), (-150.0, 0.0, 150.0), 'xyz'

# Springs, N/um. Blocks: HIWIN HG15C radial rigidity at light preload (Z0) from the HG catalog's table 3.5;
# the four-row 45 degree design is taken as stiff in reverse radial and lateral as in radial. The rest are
# estimates: an unpreloaded single nut at about 1 kN, a light-preload angular-contact pair in the BK.
SPRINGS = dict(block=196.0, nut={'SFU1204': 100.0, 'SFU1605': 150.0}, bearing={'BK10': 80.0, 'BK12': 100.0})
ROOT_D = {'SFU1204': 9.6, 'SFU1605': 12.9}    # thread root, mm: the shaft's area in tension
# What-if variants: name -> (description, changes). P: model parameters, rebuilt by chain_geom.py.
VARIANTS = {
    'yff': ('Y screw fixed at both ends (the spare BK12 in place of the BF12)', dict(y_fixed_fixed=True)),
    'za': ('Blocks at medium preload (ZA, 365 N/um: genuine HIWIN)', dict(block=365.0)),
    'soft': ('Blocks at half the catalog Z0 (a loose clone)', dict(block=98.0)),
    'bearings2x': ('Screw bearings twice as stiff', dict(bearing_scale=2.0)),
    'nuts2x': ('Preloaded nuts (twice as stiff)', dict(nut_scale=2.0)),
    'car34': ('3/4 in X carriage', dict(P=dict(carriage_t=19.05))),
    'car1': ('1 in X carriage', dict(P=dict(carriage_t=25.4))),
    'caralu': ('5/8 in aluminum X carriage (as it was)', dict(car_alu=True)),
    'zp34': ('3/4 in Z plate', dict(P=dict(zplate_t=19.05))),
    'zp1': ('1 in Z plate', dict(P=dict(zplate_t=25.4))),
    'table1': ('1 in table', dict(P=dict(table_t=25.4))),
    'zpitch': ('Z blocks 88 mm apart (as far as the travel allows)', dict(P=dict(z_blk_pitch=88.0))),
    'noangles': ('No angles up the carriage back', dict(no_angles=True)),
    'zpalu': ('5/8 in aluminum Z plate (as it was)', dict(zp_alu=True)),
    'tablesteel': ('Steel table', dict(table_steel=True)),
}

def frac1(o, n, lo, hi):
    """Overlap of [lo, hi] with each of n voxels of size H starting at o, as a fraction."""
    a = o + np.arange(n) * H
    return np.clip(np.minimum(a + H, hi) - np.maximum(a, lo), 0, None) / H


class Body:
    def __init__(self, name, box, E):
        self.name, self.box, self.E = name, np.array(box, float), E


class Part:
    """A voxel model of rigidly joined bodies, plus springs between patches on it and the ground."""

    def __init__(self, bodies, align):
        lo = np.min([b.box[:3] for b in bodies], 0)
        hi = np.max([b.box[3:] for b in bodies], 0)
        o = align - np.ceil((align - lo) / H) * H          # a voxel boundary on the aligning body's faces
        n = np.ceil((hi - o) / H).astype(int)
        frac = np.zeros((len(bodies),) + tuple(n))
        for i, b in enumerate(bodies):
            f = [frac1(o[a], n[a], b.box[a], b.box[a + 3]) for a in range(3)]
            frac[i] = f[0][:, None, None] * f[1][None, :, None] * f[2][None, None, :]
        total = frac.sum(0)
        self.vox = SimpleNamespace(o=o, n=n, h=H)
        self.mesh = Mesh(self.vox, total > 0.3)
        fe = np.array([self.mesh.field(fr) for fr in frac])
        self.E = (fe * np.array([b.E for b in bodies])[:, None]).sum(0)
        self.group = np.array([bodies[i].name for i in fe.argmax(0)], dtype=object)
        self.names = sorted({b.name for b in bodies})

    def patch(self, lo, hi):
        nodes = self.mesh.nodes_in(np.asarray(lo, float), np.asarray(hi, float))
        if len(nodes) < 3:
            raise ValueError(f'empty patch {lo} {hi}')
        r = self.mesh.xyz[nodes]
        c = r.mean(0)
        d = r - c
        Ir = (d ** 2).sum() * np.eye(3) - d.T @ d
        return SimpleNamespace(nodes=nodes, c=c, d=d, Iinv=np.linalg.inv(Ir))

    def row(self, pt, p, e):
        """Dofs and weights of e . (the patch's rigid motion at point p)."""
        n = len(pt.nodes)
        # u_p = mean(u) + theta x (p - c), theta = Iinv sum(d_i x u_i)
        a = np.cross(np.asarray(p, float) - pt.c, e)               # e . (theta x r) = theta . (r x e)
        w = np.tile(np.asarray(e, float) / n, (n, 1))
        b = pt.Iinv @ a                                            # theta . a = sum (d_i x u_i) . b = sum u_i . (b x d_i)
        w += np.cross(b, pt.d)
        dofs = (3 * pt.nodes[:, None] + np.arange(3)).ravel()
        return dofs, w.ravel()


def spring_matrix(ndof, springs):
    rows, cols, vals = [], [], []
    for parts, k in springs:
        dofs = np.concatenate([p[0] for p in parts])
        w = np.concatenate([s * p[1] for s, p in zip((1, -1), parts)])
        rows.append(np.repeat(dofs, len(dofs)))
        cols.append(np.tile(dofs, len(dofs)))
        vals.append(k * np.outer(w, w).ravel())
    return sp.csc_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(ndof, ndof))


def solve(K, f):
    fac = CholeskyFactor(K)
    fac.factorize(K)
    return fac.solve(f)


def screw_k(kind, support, lengths, opt):
    """Axial stiffness (N/mm) of a ballscrew: nut, shaft from each fixed bearing to the nut, bearings."""
    A = np.pi / 4 * ROOT_D[kind] ** 2
    shaft = sum(E_ST * A / L for L in lengths)
    bearing = SPRINGS['bearing'][support] * 1e3 * opt.get('bearing_scale', 1.0) * len(lengths)
    nut = SPRINGS['nut'][kind] * 1e3 * opt.get('nut_scale', 1.0)
    return 1 / (1 / nut + 1 / shaft + 1 / bearing)


def box(g, name, dz=0.0):
    b = np.array(g['boxes'][name], float)
    b[[2, 5]] -= dz
    return b


def energies(part, u, springs):
    """Strain energy x 2 per body and per spring set, for a unit load (mm/N)."""
    ee = part.E * part.mesh.energy(u[:, None])[:, 0]
    out = {n: ee[part.group == n].sum() for n in part.names}
    for (parts, k), tag in zip(springs, part.tags):
        dofs = [p[0] for p in parts]
        delta = sum(s * (u[d] @ p[1]) for s, d, p in zip((1, -1), dofs, parts))
        out[tag] = out.get(tag, 0.0) + k * delta ** 2
    return {k: v / F0 ** 2 for k, v in out.items()}


def head(g, opt, dz):
    """X carriage + Z plate, Z lowered dz from the top. Returns {(xc, dir): (compliance, energies)}."""
    zp, car = box(g, 'ZPlate', dz), box(g, 'XCarriagePlate')
    steel = g['looks']['XCarriagePlate'].startswith('steel') and not opt.get('car_alu')
    zp_steel = g['looks']['ZPlate'].startswith('steel') and not opt.get('zp_alu')
    bodies = [Body('Z plate', zp, E_ST if zp_steel else E_AL), Body('X carriage', car, E_ST if steel else E_AL)]
    bodies += [Body('Z plate', box(g, f'Z_{p}{s}', dz), E_ST) for p in ('Riser', 'Rail') for s in 'LR']
    a, t = g['P']['car_angle']
    for side in ('L', 'R') if not opt.get('no_angles') else ():
        # each angle as its two legs: the flat one on the carriage's back, the other standing at its outer edge
        b = box(g, f'XCarriageAngle{side}')
        xs = b[0] if side == 'L' else b[3] - t
        bodies += [Body('Carriage angles', [b[0], b[1], b[2], b[3], b[1] + t, b[5]], E_ST),
                   Body('Carriage angles', [xs, b[1] + t, b[2], xs + t, b[4], b[5]], E_ST)]
    part = Part(bodies, zp[:3])
    m, h = part.mesh, H
    # the carriage above its upper X blocks (it cantilevers up to the Z screw's BK10) on its own
    top = max(box(g, f'X_Block{s}{i}')[5] for s in 'LR' for i in '12')
    part.group[(part.group == 'X carriage') & (m.center[:, 2] > top)] = 'X carriage, upper'
    part.names = sorted(set(part.group))
    car_front, car_back = car[1], car[4]
    springs, tags = [], []
    kb = opt.get('block', SPRINGS['block']) * 1e3
    # Z blocks: fixed to the carriage, riding the Z rails (radial y, lateral x; z is the screw's)
    for s in 'LR':
        rail = box(g, f'Z_Rail{s}', dz)
        for i in '12':
            b = box(g, f'Z_Block{s}{i}')
            pr = part.patch([rail[0], rail[4] - h, b[2]], [rail[3], rail[4], b[5]])
            pc = part.patch([b[0], car_front, b[2]], [b[3], car_front + h, b[5]])
            p = [(b[0] + b[3]) / 2, (rail[4] + car_front) / 2, (b[2] + b[5]) / 2]
            for e in ((0, 1, 0), (1, 0, 0)):
                springs.append(((part.row(pc, p, e), part.row(pr, p, e)), kb))
                tags.append('Z blocks')
    # X blocks: the carriage's back face to the beam (radial y, lateral z)
    for s in 'LR':
        for i in '12':
            b = box(g, f'X_Block{s}{i}')
            pc = part.patch([b[0], car_back - h, b[2]], [b[3], car_back, b[5]])
            p = [(b[0] + b[3]) / 2, b[4], (b[2] + b[5]) / 2]
            for e in ((0, 1, 0), (0, 0, 1)):
                springs.append(((part.row(pc, p, e),), kb))
                tags.append('X blocks')
    # Z screw: the nut housing on the Z plate's back to the BK10 on the carriage's front, along z
    sh, bk, sc = box(g, 'Z_NutHousingShim', dz), box(g, 'Z_BK10'), box(g, 'Z_Screw', dz)
    pn = part.patch([sh[0], zp[4] - h, sh[2]], [sh[3], zp[4], sh[5]])
    pb = part.patch([bk[0], car_front, bk[2]], [bk[3], car_front + h, bk[5]])
    axis = [0.0, (sc[1] + sc[4]) / 2, (sh[2] + sh[5]) / 2]
    Lz = (bk[2] + bk[5]) / 2 - axis[2]
    springs.append(((part.row(pb, axis, (0, 0, 1)), part.row(pn, axis, (0, 0, 1))),
                    screw_k('SFU1204', 'BK10', [Lz], opt)))
    tags.append('Z screw')
    # X screw: the nut housing on the carriage's back to the beam, along x (its stiffness set per case)
    sh, sc, bk = box(g, 'X_NutHousingShim'), box(g, 'X_Screw'), box(g, 'X_BK10')
    px = part.patch([sh[0], car_back - h, sh[2]], [sh[3], car_back, sh[5]])
    xaxis = [0.0, (sc[1] + sc[4]) / 2, (sc[2] + sc[5]) / 2]
    springs.append(((part.row(px, xaxis, (1, 0, 0)),), None))
    tags.append('X screw')
    part.tags = tags
    # the tool force goes in over the spindle clamp's foot on the Z plate's front
    cl = box(g, 'SpindleClamp', dz)
    pl = part.patch([cl[0], zp[1], cl[2]], [cl[3], zp[1] + h, cl[5]])
    tool = [0.0, 0.0, g['dims']['table_top'] + 50.0]
    Kp = m.assemble(part.E)
    fixed = [s for s, t in zip(springs, tags) if t != 'X screw']
    Kf = Kp + spring_matrix(m.ndof, fixed)
    out = {}
    for xc in XS:
        sx = screw_k('SFU1204', 'BK10', [(bk[0] + bk[3]) / 2 - xc], opt)
        sprs = fixed + [(springs[-1][0], sx)]
        K = Kf + spring_matrix(m.ndof, [(springs[-1][0], sx)])
        rw = [part.row(pl, tool, e) for e in np.eye(3)]
        f = np.zeros((m.ndof, 3))
        for j, (dofs, w) in enumerate(rw):
            np.add.at(f[:, j], dofs, F0 * w)
        U = solve(K, f)
        for j, ax in enumerate(DIRS):
            dofs, w = rw[j]
            out[(xc, ax)] = (U[dofs, j] @ w / F0, energies(part, U[:, j], sprs))
    return out


def table(g, opt):
    """Table on its blocks and the Y screw. Returns {(xc, yt, dir): (compliance, energies)}."""
    tb = box(g, 'Table')
    part = Part([Body('Table', tb, E_ST if opt.get('table_steel') else E_AL)], tb[:3])
    m, h = part.mesh, H
    springs, tags = [], []
    kb = opt.get('block', SPRINGS['block']) * 1e3
    for s in 'LR':
        for i in '12':
            b = box(g, f'Y_Block{s}{i}')
            pt = part.patch([b[0], b[1], tb[2]], [b[3], b[4], tb[2] + h])
            p = [(b[0] + b[3]) / 2, (b[1] + b[4]) / 2, b[2]]
            for e in ((0, 0, 1), (1, 0, 0)):
                springs.append(((part.row(pt, p, e),), kb))
                tags.append('Y blocks')
    sh, sc, nut = box(g, 'Y_NutHousingShim'), box(g, 'Y_Screw'), box(g, 'Y_Nut')
    pn = part.patch([sh[0], sh[1], tb[2]], [sh[3], sh[4], tb[2] + h])
    yaxis = [0.0, (nut[1] + nut[4]) / 2, (sc[2] + sc[5]) / 2]
    tags.append('Y screw')
    part.tags = tags
    y_fixed = g['dims']['y_bk'] - 12.5                    # the HM12-57's bearings (where a BK12's would be)
    y_far = box(g, 'Y_BF12')[[1, 4]].mean()
    Kf = m.assemble(part.E) + spring_matrix(m.ndof, springs)
    top = tb[5]
    out = {}
    for yt in YTS:
        ny = yaxis[1] + yt
        L = [y_fixed - ny] + ([ny - y_far] if opt.get('y_fixed_fixed') else [])
        sy = (((part.row(pn, yaxis, (0, 1, 0)),), screw_k('SFU1605', 'BK12', L, opt)),)
        K = Kf + spring_matrix(m.ndof, sy)
        rw, f = [], []
        for xc in XS:
            # the work load goes in over a 100 mm square under the tool (a vise's footprint), on the table
            lo = [max(xc - 50, tb[0]), max(-yt - 50, tb[1]), top - h]
            hi = [min(xc + 50, tb[3]), min(-yt + 50, tb[4]), top]
            pw = part.patch(lo, hi)
            work = [xc, -yt, g['dims']['table_top'] + 50.0]
            for e in np.eye(3):
                rw.append(part.row(pw, work, e))
                f.append(np.zeros(m.ndof))
                np.add.at(f[-1], rw[-1][0], -F0 * rw[-1][1])
        U = solve(K, np.column_stack(f))
        j = 0
        for xc in XS:
            for ax in DIRS:
                dofs, w = rw[j]
                out[(xc, yt, ax)] = (-(U[dofs, j] @ w) / F0, energies(part, U[:, j], springs + list(sy)))
                j += 1
    return out


def geometry(P=None):
    """The moving parts' geometry, as drawn or rebuilt with parameter overrides (cached)."""
    if not P:
        return json.load(open(os.path.join(HERE, os.environ.get('CHAIN_GEOM', 'chain_geom.json'))))
    tag = '_'.join(f'{k}{v:g}' for k, v in sorted(P.items()))
    path = os.path.join(HERE, f'chain_geom_{tag}.json')
    if not os.path.exists(path):
        subprocess.run([sys.executable, os.path.join(HERE, 'chain_geom.py')], check=True, capture_output=True,
                       env=dict(os.environ, VOX_P=json.dumps(P), CHAIN_OUT=path))
    return json.load(open(path))


def frame_compliance():
    """The frame's compliance per load case (mm/N), in loads.cases order, cached."""
    name = os.environ.get('FEA_VOX', 'vox_current')
    path = os.path.join(HERE, f'chain_frame_{name}.npz')
    src = os.path.getmtime(os.path.join(HERE, name + '.npz'))      # rebuilt when the voxels are
    if os.path.exists(path):
        cached = np.load(path)
        if float(cached['src']) == src:
            return cached['c']
    from loads import cases, domain_mask, moduli, setup
    from vfe import Voxels
    vox = Voxels()
    mesh = setup(vox, domain_mask(vox))
    F, _ = cases(mesh, vox, xs=XS, yts=YTS)
    U = mesh.solve(moduli(mesh, vox.f, mesh.field(vox.f['eg_base'])), F)
    c = (F * U).sum(0) / F0 ** 2
    np.savez(path, c=c, src=src)
    return c


def evaluate(g, opt, cf, dz):
    hd, tb = head(g, opt, dz), table(g, opt)
    rows = {ax: [] for ax in DIRS}
    i = 0
    for xc in XS:
        for yt in YTS:
            for ax in DIRS:
                ch, eh = hd[(xc, ax)]
                ct, et = tb[(xc, yt, ax)]
                en = {'Frame': cf[i] if cf is not None else 0.0}
                for d_ in (eh, et):
                    for k, v in d_.items():
                        en[k] = en.get(k, 0.0) + v
                rows[ax].append((en['Frame'] + ch + ct, ch + ct, en))
                i += 1
    return rows


def summary(rows):
    k = {ax: np.mean([1 / r[0] for r in rows[ax]]) / 1e3 for ax in DIRS}
    km = {ax: np.mean([1 / r[1] for r in rows[ax]]) / 1e3 for ax in DIRS}
    share = {}
    for ax in DIRS:
        tot = sum(r[0] for r in rows[ax])
        for name in rows[ax][0][2]:
            share.setdefault(name, {})[ax] = sum(r[2][name] for r in rows[ax]) / tot
    return k, km, share


def main():
    warnings.filterwarnings('ignore', message='Matrix is nearly singular')
    g = geometry()
    no_frame = '--no-frame' in sys.argv
    names = [a for a in sys.argv[1:] if not a.startswith('--')]
    cf = None if no_frame else frame_compliance()
    if cf is not None:
        kf = {ax: np.mean(1 / cf[i::3]) / 1e3 for i, ax in enumerate(DIRS)}
        print(f"frame alone          kx {kf['x']:6.1f}  ky {kf['y']:6.1f}  kz {kf['z']:6.1f} N/um")
    tz = g['dims']['tip'] - g['dims']['table_top'] - 50.0     # Z lowered so the tool is 50 mm above the table
    base = None
    for name in ['as drawn'] + (names or list(VARIANTS)):
        opt = {}
        for v in name.split('+') if name != 'as drawn' else ():     # variants combined with +
            for key, val in VARIANTS[v][1].items():
                opt[key] = {**opt.get(key, {}), **val} if key == 'P' else val
        gv = geometry(opt.get('P'))
        tv = gv['dims']['tip'] - gv['dims']['table_top'] - 50.0
        k, km, share = summary(evaluate(gv, opt, cf, tv))
        rel = '' if base is None else '  ' + ' '.join(f'{100 * (k[a] / base[a] - 1):+5.1f}%' for a in DIRS)
        print(f"{name:12s} at the tool kx {k['x']:6.1f}  ky {k['y']:6.1f}  kz {k['z']:6.1f}   "
              f"moving parts alone {km['x']:6.1f} {km['y']:6.1f} {km['z']:6.1f}{rel}", flush=True)
        if base is None:
            base = k
            print('  share of the deflection at the tool (x / y / z):')
            for n, s in sorted(share.items(), key=lambda t: -sum(t[1].values())):
                print(f"    {n:12s} {100 * s['x']:5.1f} {100 * s['y']:5.1f} {100 * s['z']:5.1f} %")
    # the Z axis all the way down (the tool 140 mm below its top): the head only, X centered
    hd = head(g, {}, g['P']['travel_z'])
    hm = head(g, {}, tz)
    print('head alone, Z at 50 mm above the table / all the way down: ' +
          '  '.join(f"{a} {1 / hm[(0.0, a)][0] / 1e3:5.1f} / {1 / hd[(0.0, a)][0] / 1e3:5.1f}" for a in DIRS))


if __name__ == '__main__':
    main()
