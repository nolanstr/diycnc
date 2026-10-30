"""Stage 1 of the frame optimization: the cast-in steel sized from stock, for stiffness at the tool against cost.

    FEA_SYM=1 FEA_VOX=vox_sym10 python steel_opt.py           # both paths from the frame as drawn (~40 min)
    FEA_SYM=1 FEA_VOX=vox_sym10 python steel_opt.py --down    # just the cheaper path

The steel is bought, not shaped: every member is a stock flat bar or tube, so this is a search over catalog
sizes, not a topology optimization. Each member group steps through the thicknesses it comes in (a thinner
or thicker bar, a lighter or heavier tube wall), modeled as in lean_study.py by scaling the steel where the
part lies in the voxels. Two greedy paths start from the frame as drawn:

- cheaper: take the step that saves the most money per percent of stiffness at the tool lost, again and again;
- stiffer: take the step that buys the most stiffness at the tool per dollar.

Each line is a frame you could build. Stiffness at the tool is the frame in series with the moving parts
(chain.py, as drawn), so it shows what a change is worth where the cutting happens. Members whose threads need
the thickness (the beam's face bar, the top plates, the rail bars) have it as their minimum. The castings
(stage 2, topopt_damped.py) and the steel's own ringing (ring_check.py) come after.
"""

import os
import re
import sys
import time
import warnings

import numpy as np

from loads import F0, cases, domain_mask, moduli, setup
from vfe import Voxels

HERE = os.path.dirname(os.path.abspath(__file__))
KM = np.array((4.0, 3.9, 7.2))       # the moving parts alone at the tool, N/um (chain.py, as drawn)
LB = 2.2046
PRICE = dict(flat=2.0, tube=3.0)     # $/lb, as lean_study.py
IN = 25.4

# group: (part-name pattern, kind, drawn thickness (mm), the sizes it comes in, tube outside (w, h) mm)
GROUPS = {
    'beam face bar': (r'^BeamFacePlate$', 'flat', 12.7, (12.7, 15.875, 19.05), None),        # tapped M5/M6: 1/2 in min
    'beam back bar': (r'^BeamBackPlate$', 'flat', 9.525, (6.35, 9.525, 12.7, 15.875, 19.05), None),
    'beam seat + cap bars': (r'^Beam(Seat|Cap)', 'flat', 9.525, (9.525, 12.7), None),
    'upright columns': (r'^UprightColumn', 'tube', 3.175, (3.175, 4.7625, 6.35), (50.8, 50.8)),
    'upright feet': (r'^UprightFoot', 'flat', 9.525, (6.35, 9.525, 12.7), None),
    'pedestal columns': (r'^BasePedestalColumn', 'tube', 3.175, (3.175, 4.7625, 6.35), (50.8, 50.8)),
    'base girders': (r'^BaseGirder(Front|Rear)[LR]$', 'tube', 3.175, (3.175, 4.7625, 6.35), (50.8, 76.2)),
    'cross tubes': (r'^BaseCross', 'tube', 3.175, (3.175, 4.7625), (38.1, 38.1)),
    'rail bars': (r'^BaseRailBar', 'flat', 9.525, (9.525, 12.7, 15.875), None),              # tapped: 3/8 in min
    'seat + bottom bars': (r'^Base(Seat|PedestalBar)', 'flat', 9.525, (6.35, 9.525, 12.7), None),
}


def group_of(name):
    if name.startswith(('Beam', 'X_')):
        return 'beam'
    return 'up' if name.startswith(('Upright', 'TopPlate', 'TieRod')) else 'base'


def area(kind, t, wh):
    if kind == 'flat':
        return t
    w, h = wh
    return 2 * t * (w + h) - 4 * t * t


def fmt(t):
    """A thickness in inches, as stock is sold."""
    for d in (2, 4, 8, 16, 32):
        n = t / IN * d
        if abs(n - round(n)) < 1e-3:
            from math import gcd
            n = round(n)
            g = gcd(n, d)
            return f'{n // g}/{d // g} in' if d // g > 1 else f'{n // g} in'
    return f'{t:.2f} mm'


class Study:
    def __init__(self):
        name = os.environ.get('FEA_VOX', 'vox_current')
        self.vox = Voxels(name)
        self.parts = np.load(os.path.join(HERE, name + '_parts.npz'))
        self.mesh = setup(self.vox, domain_mask(self.vox))
        self.F, _ = cases(self.mesh, self.vox, xs=(0.0, 90.0))
        self.members = {g: [p for p in self.parts.files if re.match(spec[0], p)] for g, spec in GROUPS.items()}
        self.kg0 = {g: sum(self.parts[p].sum() for p in ps) * self.vox.h ** 3 * 7.85e-6 for g, ps in self.members.items()}
        self.cache = {}

    def evaluate(self, state):
        """state: index into each group's sizes. Returns (tool stiffness x/y/z, frame stiffness, steel kg, $)."""
        key = tuple(state[g] for g in GROUPS)
        if key in self.cache:
            return self.cache[key]
        f = {k: v.copy() for k, v in self.vox.f.items()}
        kg = cost = 0.0
        for g, (pat, kind, t0, sizes, wh) in GROUPS.items():
            s = area(kind, sizes[state[g]], wh) / area(kind, t0, wh)
            for p in self.members[g]:
                grp = group_of(p)
                a = np.minimum(self.parts[p], f[f'st_{grp}'])
                f[f'st_{grp}'] += (s - 1) * a
            kg_g = self.kg0[g] * s
            kg += kg_g
            cost += kg_g * LB * PRICE[kind]
        E = moduli(self.mesh, f, self.mesh.field(f['eg_base']))
        k = F0 ** 2 / (self.F * self.mesh.solve(E, self.F)).sum(0) / 1e3
        k = np.array([k[0::3].mean(), k[1::3].mean(), k[2::3].mean()])
        tool = 1 / (1 / KM + 1 / k)
        out = (tool, k, kg, cost)
        self.cache[key] = out
        return out


def walk(st, state, down, limit):
    """Greedy path of single catalog steps; returns [(move, state, result)]."""
    path = []
    base = st.evaluate(state)
    while True:
        t0 = time.time()
        cur = st.evaluate(state)
        best = None
        for g, spec in GROUPS.items():
            i = state[g] + (-1 if down else 1)
            if not 0 <= i < len(spec[3]):
                continue
            trial = dict(state, **{g: i})
            res = st.evaluate(trial)
            dk = (res[0] / cur[0] - 1).mean()             # relative stiffness at the tool, mean of x/y/z
            dc = res[3] - cur[3]
            score = (-dc) / max(-dk, 1e-6) if down else dk / max(dc, 1e-6)
            if best is None or score > best[0]:
                best = (score, g, trial, res)
        if best is None:
            return path
        _, g, state, res = best
        loss = (res[0] / base[0] - 1).mean()
        if (down and loss < -limit) or (not down and res[3] - base[3] > limit):
            return path
        path.append((f'{g} {fmt(GROUPS[g][3][state[g] + (1 if down else -1)])} -> {fmt(GROUPS[g][3][state[g]])}',
                     dict(state), res))
        print(f'  {path[-1][0]:44s} tool {res[0][0]:.3f} {res[0][1]:.3f} {res[0][2]:.3f} N/um '
              f'({100 * loss:+.2f} %)  steel {res[2]:5.1f} kg  ${res[3]:6.0f}  ({time.time() - t0:.0f} s)', flush=True)


def main():
    warnings.filterwarnings('ignore', message='Matrix is nearly singular')
    st = Study()
    drawn = {g: spec[3].index(spec[2]) for g, spec in GROUPS.items()}
    tool, k, kg, cost = st.evaluate(drawn)
    print(f'as drawn: tool {tool[0]:.3f} {tool[1]:.3f} {tool[2]:.3f} N/um, frame {k[0]:.1f} {k[1]:.1f} {k[2]:.1f} N/um, '
          f'these members {kg:.1f} kg, ${cost:.0f}', flush=True)
    for g, ps in st.members.items():
        print(f'  {g:22s} {len(ps):2d} parts  {st.kg0[g]:5.1f} kg  {fmt(GROUPS[g][2])}', flush=True)
    if '--up' not in sys.argv:
        print('cheaper (most $ saved per % of stiffness at the tool, until 2 % is gone):', flush=True)
        walk(st, drawn, True, 0.02)
    if '--down' not in sys.argv:
        print('stiffer (most stiffness at the tool per $, up to $150 more):', flush=True)
        walk(st, drawn, False, 150.0)


if __name__ == '__main__':
    main()
