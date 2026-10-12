# DIY CNC: epoxy-granite desktop mill

A fixed-gantry desktop mill for cutting steel, sized like the Shariff DMC2 Mini:
180 x 300 x 140 mm travel, five bolt-together castings (laser-cut steel skeletons cast into epoxy granite), HGR15 rails,
ballscrews on all axes, a 2.2 kW water-cooled spindle, flood coolant and a full enclosure.
Everything is modeled in FreeCAD from one Python script.

![The machine](renders/machine_iso.png)

## Documents

The documents are in `docs/`, one folder per stage of the build, in the order you use them (index:
[docs/README.md](docs/README.md)).

| Folder | What's in it |
|---|---|
| [1-sourcing](docs/1-sourcing) | [Sourcing list](docs/1-sourcing/sourcing.pdf): parts to buy, with listings and prices (also as [CSV](docs/1-sourcing/sourcing.csv)) |
| [2-printing](docs/2-printing) | [Print guide](docs/2-printing/print-guide.pdf): every 3D-printed part, settings and sliced filament use |
| [3-molds](docs/3-molds) | [All the molds](docs/3-molds/molds-complete.pdf), or one guide per mold: [base](docs/3-molds/base-mold.pdf), [uprights](docs/3-molds/upright-molds.pdf), [beam](docs/3-molds/beam-mold.pdf); full-size [drilling templates](docs/3-molds/templates) to print and tape onto the boards |
| [4-build](docs/4-build) | [Build guide](docs/4-build/build-guide.pdf), and the same in five stages for the bench (steel, casting, frame, axes and electronics, enclosure) |
| [5-design](docs/5-design) | [Design notes](docs/5-design/design-notes.pdf) (the frame, joints, stiffness study, cost) and the [report](docs/5-design/report.txt) (dimensions, masses, BOM, collision check) |

The Markdown sources are in `docs/src/`.

## Repository layout

| Folder | Contents |
|---|---|
| `model/` | `build_cnc.py` (the whole machine; every dimension is in `P` at the top), `parts.py` (components from catalog drawings), `molds.py` (printed mold pieces, their bolts, pins and pegs, and STL export), `moldbox.py` (the mold boards, brackets and hole maps), `mold_figures.py` (the mold guide's illustrations; run it in the FreeCAD GUI), `slice_prints.py` (slices `print/` in Bambu Studio for real filament figures), and the generated `DIYCNC.FCStd` and `DIYCNC.step` |
| `print/` | STL files for every printed part, one folder per casting plus `machine/`, and `manifest.csv` |
| `renders/` | Images of the machine and its parts; `renders/build/` has the build-step pictures |
| `docs/` | The PDFs above, the report and the sourcing CSV; sources and generators in `docs/src/` |
| `analysis/` | Voxel finite-element model of the frame and the base topology optimization |

## Rebuilding

FreeCAD 1.1 is the only requirement for the model.

```sh
# collision check, docs/5-design/report.txt, the print/ STLs and the Markdown in docs/src/
/Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd model/build_cnc.py

# everything above plus DIYCNC.FCStd, DIYCNC.step and renders/ (opens and closes a FreeCAD window)
CNC_SNAPSHOTS=1 /Applications/FreeCAD.app/Contents/MacOS/FreeCAD "$PWD/model/build_cnc.py"

# the mold guide's illustrations (renders/mold/), and real filament figures from Bambu Studio
/Applications/FreeCAD.app/Contents/MacOS/FreeCAD "$PWD/model/mold_figures.py"
python3 model/slice_prints.py

# the sourcing list, then the PDFs (needs Python with the markdown package and Google Chrome)
python3 docs/src/make_sourcing.py
python3 docs/src/make_pdfs.py
```

In the FreeCAD file, edit `posX`, `posY`, `posZ` and `doorAngle` in the `Params` sheet to jog the
axes and open the door, `explode` to pull the frame apart and `sumpOut` to slide the coolant sump
out. The printed mold pieces are in the hidden `Molds` group.

The stiffness study needs Python with numpy, scipy, matplotlib and scikit-sparse 0.5 or later; see the
design notes.
