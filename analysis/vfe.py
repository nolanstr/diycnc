"""Voxel finite elements for the frame stiffness study (8-node bricks, CHOLMOD solve).

Units: mm, N, MPa. The voxel fractions come from voxelize.py. Each element's modulus is
the volume-weighted (Voigt) mix of epoxy granite and steel in it; the joints between
the castings are treated as bonded (preloaded, no gap opening).
"""

import json
import os

import numpy as np
import scipy.sparse as sp
try:    # scikit-sparse >= 0.5
    from sksparse.cholmod import CholeskyFactor
except ImportError:
    CholeskyFactor = None
    from sksparse.cholmod import analyze

HERE = os.path.dirname(os.path.abspath(__file__))
E_EG, E_ST, NU, E_MIN = 30e3, 200e3, 0.25, 1e-6


def brick_ke(h, nu=NU):
    """Stiffness of an h-cube 8-node brick with E = 1 (2x2x2 Gauss)."""
    lam, mu = nu / ((1 + nu) * (1 - 2 * nu)), 1 / (2 * (1 + nu))
    D = np.zeros((6, 6))
    D[:3, :3] = lam
    D[np.arange(3), np.arange(3)] += 2 * mu
    D[np.arange(3, 6), np.arange(3, 6)] = mu
    corners = np.array([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0], [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]], float)
    s = 2 * corners - 1
    g = 1 / np.sqrt(3)
    ke = np.zeros((24, 24))
    for gp in itertools_product((-g, g)):
        dN = np.zeros((8, 3))
        for a in range(8):
            for i in range(3):
                t = [1 + s[a, k] * gp[k] for k in range(3)]
                t[i] = s[a, i]
                dN[a, i] = t[0] * t[1] * t[2] / 8
        dN *= 2 / h   # d/dx = (2/h) d/dxi
        B = np.zeros((6, 24))
        for a in range(8):
            x, y, z = dN[a]
            B[0, 3 * a], B[1, 3 * a + 1], B[2, 3 * a + 2] = x, y, z
            B[3, 3 * a], B[3, 3 * a + 1] = y, x
            B[4, 3 * a + 1], B[4, 3 * a + 2] = z, y
            B[5, 3 * a], B[5, 3 * a + 2] = z, x
        ke += B.T @ D @ B * (h / 2) ** 3
    return ke


def itertools_product(v):
    return [(a, b, c) for a in v for b in v for c in v]


class Voxels:
    def __init__(self, name=os.environ.get('FEA_VOX', 'vox_current')):
        self.f = dict(np.load(os.path.join(HERE, name + '.npz')))
        self.info = json.load(open(os.path.join(HERE, name + '.json')))
        self.h = self.info['h']
        self.o = np.array(self.info['origin'])
        self.n = np.array(self.info['n'])
        self.d = self.info['dims']

    def centers(self, ax):
        return self.o[ax] + (np.arange(self.n[ax]) + 0.5) * self.h


class Mesh:
    """Elements = voxels in `mask`; nodes renumbered to those used."""

    def __init__(self, vox, mask):
        self.vox, self.h = vox, vox.h
        nx, ny, nz = vox.n
        ii, jj, kk = np.nonzero(mask)
        self.ijk = np.column_stack([ii, jj, kk])
        self.ne = len(ii)
        off = np.array([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0], [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]])
        gn = ((ii[:, None] + off[:, 0]) + (nx + 1) * ((jj[:, None] + off[:, 1]) + (ny + 1) * (kk[:, None] + off[:, 2])))
        used, enodes = np.unique(gn, return_inverse=True)
        self.enodes = enodes.reshape(self.ne, 8)
        self.nn = len(used)
        gi = used % (nx + 1)
        gj = (used // (nx + 1)) % (ny + 1)
        gk = used // ((nx + 1) * (ny + 1))
        self.xyz = vox.o + np.column_stack([gi, gj, gk]) * self.h
        self.ndof = 3 * self.nn
        self.edof = (3 * self.enodes[:, :, None] + np.arange(3)).reshape(self.ne, 24)
        self.ke = brick_ke(self.h)
        self.center = vox.o + (self.ijk + 0.5) * self.h
        # CSC pattern and scatter map, built once
        r = np.repeat(self.edof, 24, axis=1).ravel().astype(np.int64)
        c = np.tile(self.edof, (1, 24)).ravel().astype(np.int64)
        key, self.scatter = np.unique(c * self.ndof + r, return_inverse=True)
        self.indices = (key % self.ndof).astype(np.int32)
        self.indptr = np.searchsorted(key // self.ndof, np.arange(self.ndof + 1)).astype(np.int32)
        self.nnz = len(key)
        cols = np.repeat(np.arange(self.ndof), np.diff(self.indptr))
        self.diag = np.nonzero(self.indices == cols)[0]
        self.fixed = np.zeros(0, int)
        self.factor = None

    def field(self, a):
        return a[self.ijk[:, 0], self.ijk[:, 1], self.ijk[:, 2]]

    def assemble(self, E):
        data = np.bincount(self.scatter, weights=np.outer(E, self.ke.ravel()).ravel(), minlength=self.nnz)
        # supports as stiff springs on the diagonal; editing data in place keeps the sparsity
        # pattern fixed (adding matrices would drop exact zeros), so the symbolic factor stays valid
        data[self.diag[self.fixed]] += 1e4 * data[self.diag].max()
        return sp.csc_matrix((data, self.indices, self.indptr), shape=(self.ndof, self.ndof))

    def solve(self, E, F):
        K = self.assemble(E)
        if CholeskyFactor is not None:
            # keep the symbolic analysis; refactorizing a used factor drops it to the slow simplicial path
            if self.factor is None:
                self.factor = CholeskyFactor(K)
            num = self.factor.copy()
            num.factorize(K)
            return num.solve(F)
        # older scikit-sparse: its supernodal mode crashes with some BLAS builds
        if self.factor is None:
            self.factor = analyze(K, mode='simplicial')
        self.factor.cholesky_inplace(K)
        return self.factor(F)

    def energy(self, U):
        """u_e^T ke u_e per element and load case (for E = 1)."""
        ue = U[self.edof]                       # ne x 24 x nlc
        return np.einsum('eal,ab,ebl->el', ue, self.ke, ue)

    def nodes_in(self, lo, hi, solid=None):
        """Nodes of elements whose centers lie in the box [lo, hi] (and in `solid`, if given)."""
        sel = np.all((self.center >= lo) & (self.center <= hi), axis=1)
        if solid is not None:
            sel &= solid
        return np.unique(self.enodes[sel])


def wrench_loads(xyz, nodes, F, M_about, point):
    """Nodal forces on `nodes` statically equal to force F at `point` plus moment M_about,
    spread as a rigid body would (force evenly, moment by rotation about the centroid)."""
    r = xyz[nodes]
    c = r.mean(axis=0)
    dvec = r - c
    M = np.asarray(M_about, float) + np.cross(np.asarray(point) - c, F)
    I = (dvec ** 2).sum() * np.eye(3) - dvec.T @ dvec
    w = np.linalg.solve(I, M)
    return np.asarray(F, float) / len(nodes) + np.cross(w, dvec)
