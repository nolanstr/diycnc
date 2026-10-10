# DIY CNC: epoxy-granite desktop mill

A fixed-gantry desktop mill for cutting steel, sized like the Shariff DMC2 Mini:
180 x 300 x 140 mm travel, five bolt-together epoxy-granite castings, HGR15 rails,
ballscrews on all axes, a 2.2 kW water-cooled spindle, flood coolant and a full enclosure.
Everything is modelled in FreeCAD from one Python script.

![The machine](renders/machine_iso.png)

## Documents

| PDF | What's in it |
|---|---|
| [Build guide](docs/build-guide.pdf) | Step by step, with pictures: steel prep, moulds, casting, frame, risers, axes, electronics, enclosure, commissioning |
| [Print guide](docs/print-guide.pdf) | Every 3D-printed part (mould cores, formers, fillers, liners), cut to fit a Bambu A1 mini |
| [Sourcing list](docs/sourcing.pdf) | Parts to buy, with listings and prices (also as [CSV](docs/sourcing.csv)) |
| [Design notes](docs/design-notes.pdf) | How the frame, coolant and joints work, the stiffness study and the cost |
| [Report](docs/report.txt) | Dimensions, casting volumes and masses, BOM, enclosure cut list, collision check |

The Markdown sources are in `docs/src/`.

## Repository layout

| Folder | Contents |
|---|---|
| `model/` | `build_cnc.py` (the whole machine; every dimension is in `P` at the top), `parts.py` (components from catalog drawings), `moulds.py` (printed mould pieces and STL export), and the generated `DIYCNC.FCStd` and `DIYCNC.step` |
| `print/` | STL files for every printed part, one folder per casting plus `machine/`, and `manifest.csv` |
| `renders/` | Images of the machine and its parts; `renders/build/` has the build-step pictures |
| `docs/` | The PDFs above, the report and the sourcing CSV; sources and generators in `docs/src/` |
| `analysis/` | Voxel finite-element model of the frame and the base topology optimization |

## Rebuilding

FreeCAD 1.1 is the only requirement for the model.

```sh
# collision check, docs/report.txt and the print/ STLs
/Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd model/build_cnc.py

# everything above plus DIYCNC.FCStd, DIYCNC.step and renders/ (opens and closes a FreeCAD window)
CNC_SNAPSHOTS=1 /Applications/FreeCAD.app/Contents/MacOS/FreeCAD "$PWD/model/build_cnc.py"

# the sourcing list, then the PDFs (needs Python with the markdown package and Google Chrome)
python3 docs/src/make_sourcing.py
python3 docs/src/make_pdfs.py
```

In the FreeCAD file, edit `posX`, `posY`, `posZ` and `doorAngle` in the `Params` sheet to jog the
axes and open the door, `explode` to pull the frame apart and `sumpOut` to slide the coolant sump
out. The printed mould pieces are in the hidden `Moulds` group.

The stiffness study needs Python with numpy, scipy, matplotlib and scikit-sparse 0.5 or later; see the
design notes.
