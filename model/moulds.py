"""Printed mould parts for the epoxy-granite castings, and STL export split for a small printer.

The mould boxes themselves are melamine board: flat, cheap, and the reference for the
castings' important faces. Everything with shape is printed:
  core    pocket cores: thin closed-top shells, left in the casting (fill with sand while casting)
  former  recesses in a cast face (gutters, trough, motor relief, gasket grooves): stuck to the
          mould board, waxed, pulled after curing
  filler  rounded corners and the upright flare: fill the mould box corners, waxed, reused
  plug    removable pocket formers (upright tie-rod nut pockets), waxed
  liner   stays in the casting (drain liner)
Pieces larger than the bed are cut into parts to glue together.
"""

import csv
import math
import os

import Part
from FreeCAD import Vector

BED = 170.0       # Bambu A1 mini: 180 mm cube, less a margin
WALL = 1.6        # core shell wall: four 0.4 mm lines (the sand inside holds the shape)
PETG = 1.27       # g/cm^3


def prism(poly, z0, z1):
    face = Part.Face(Part.makePolygon([Vector(x, y, z0) for x, y in poly + poly[:1]]))
    return face.extrude(Vector(0, 0, z1 - z0))


def shell_core(poly, z_top, wall=WALL):
    """Pocket core: closed at the pocket's top (z_top), open at the casting's underside (z = 0)."""
    face = Part.Face(Part.makePolygon([Vector(x, y, -1.0) for x, y in poly + poly[:1]]))
    inner = face.makeOffset2D(-wall, join=2).extrude(Vector(0, 0, z_top - wall + 1.0))
    return prism(poly, 0.0, z_top).cut(inner)


def fillers(envelope, min_dim=15.0, min_vol=5e3):
    """What the casting's rounded corners and sloped faces leave empty in a square mould box.
    Thin edge-fillet slivers are left out (a wax or silicone fillet does those)."""
    bb = envelope.BoundBox
    box = Part.makeBox(bb.XLength, bb.YLength, bb.ZLength, Vector(bb.XMin, bb.YMin, bb.ZMin))
    rest = box.cut(envelope)
    return [s for s in rest.Solids
            if min(s.BoundBox.XLength, s.BoundBox.YLength, s.BoundBox.ZLength) >= min_dim and s.Volume > min_vol]


def split_bed(shape, lim=BED):
    """Cut a solid into equal slabs along its longest axes until every piece fits the bed."""
    bb = shape.BoundBox
    lens = (bb.XLength, bb.YLength, bb.ZLength)
    ax = max(range(3), key=lambda i: lens[i])
    if lens[ax] <= lim:
        return [shape]
    n = math.ceil(lens[ax] / lim)
    lo = (bb.XMin, bb.YMin, bb.ZMin)[ax]
    step = lens[ax] / n
    out = []
    for k in range(n):
        o = [bb.XMin - 1, bb.YMin - 1, bb.ZMin - 1]
        size = [bb.XLength + 2, bb.YLength + 2, bb.ZLength + 2]
        o[ax], size[ax] = lo + k * step, step
        slab = Part.makeBox(*size, Vector(*o))
        for s in shape.common(slab).Solids:
            if s.Volume > 1.0:
                out += split_bed(s, lim)
    return out


def print_pose(shape, flip):
    """Closed face of a core on the bed; everything else as modelled. Moved to the origin."""
    s = shape.copy()
    if flip:
        s.rotate(Vector(0, 0, 0), Vector(1, 0, 0), 180)
    bb = s.BoundBox
    s.translate(Vector(-bb.XMin, -bb.YMin, -bb.ZMin))
    return s


def grams(shape, kind):
    """Rough filament use: shells and liners print solid; the rest at ~3 walls + 15 % infill."""
    v = shape.Volume / 1000.0
    if kind in ('core', 'liner', 'cast-in'):
        return v * PETG
    area = shape.Area / 100.0
    return (min(v, area * 0.12) + 0.15 * v) * PETG


def export(pieces, root):
    """pieces: (folder, name, shape, kind, qty, note). Writes STLs under root, returns manifest rows."""
    import MeshPart
    rows = []
    for folder, name, shape, kind, qty, note in pieces:
        d = os.path.join(root, folder)
        os.makedirs(d, exist_ok=True)
        parts = split_bed(shape)
        for k, p in enumerate(parts):
            stem = f'{kind}-{name}' + (f'-part{k + 1}of{len(parts)}' if len(parts) > 1 else '')
            pose = print_pose(p, kind == 'core')
            mesh = MeshPart.meshFromShape(Shape=pose, LinearDeflection=0.05, AngularDeflection=0.25, Relative=False)
            mesh.write(os.path.join(d, stem + '.stl'))
            bb = pose.BoundBox
            rows.append(dict(folder=folder, file=stem + '.stl', kind=kind, qty=qty,
                             size=f'{bb.XLength:.0f} x {bb.YLength:.0f} x {bb.ZLength:.0f}',
                             grams=grams(p, kind) * qty, note=note if k == 0 else ''))
    with open(os.path.join(root, 'manifest.csv'), 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=['folder', 'file', 'kind', 'qty', 'size', 'grams', 'note'])
        w.writeheader()
        for r in rows:
            w.writerow({**r, 'grams': f"{r['grams']:.0f}"})
    return rows
