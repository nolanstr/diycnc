# Print guide

Every printed part for the molds, the castings and the machine, cut to fit a Bambu A1 mini
(180 mm cube; no piece is over 170 mm). The STL files are in `print/`, one folder per
casting, with the list in `print/manifest.csv`. They are written by `model/build_cnc.py` on every run.
How the molds go together is in the mold guide.

**144 prints, 1.29 kg of PETG** (two 1 kg rolls). The filament figures are sliced in Bambu Studio (A1 mini, 0.4 mm nozzle, 0.2 mm layers, PETG) with the settings below, by `model/slice_prints.py`.

## Settings

- **PETG for everything.** Thick sections of curing epoxy get warm, and PLA softens at about 55 °C.
- 0.4 mm nozzle, 0.2 mm layers, 4 top and 3 bottom layers. Every file is already turned the way it prints
  best, without supports.
- **Cores** (`core-*`): thin shells, 1.2 mm walls (three lines), so they print solid; the
  posts get 2 walls and 10 % infill. The sand inside holds the walls while casting.
- **Fillers, formers, plugs** (`filler-*`, `former-*`, `plug-*`): 2 walls, 10 % infill. They only have to
  hold their shape against the mix; the nut pockets have their own walls.
- **Mold kit** (`kit-*`: brackets, saddles, holders, bushings) and machine parts: 3 walls, 15 % infill. Print one,  check it over a 19 mm offcut of your board, then the rest.
- **Liners and cast-in parts** (`liner-*`, `cast-in-*`): 3 walls, 40 % infill.
- **Fits.** Slip fits are 0.15 mm a side, nut pockets 0.15 mm over the nut, pins 3.0 mm into a 1/8 in
  hole. If your printer runs tight, print a bracket and a former first and adjust the
  horizontal expansion (XY compensation) rather than the files.

## Joining the pieces

- **Nuts.** Every piece that bolts to a board has its nut built in. On cast faces the nut drops into a
  pocket in the face against the board and slides sideways under the bolt hole; on brackets it
  presses into a hex pocket. Fit the nuts before the piece goes on the board.
- **Parts cut to fit the bed** (`-partNofM`) have a peg on one cut face and a socket on the other:
  push them together, no glue. Each part has its own bolts or pins to the board.
- **Cores** cut in two have a bulkhead on each side of the cut with two M3 x 10 bolts through them.
- **Pins.** Thin formers (gasket-groove beads, the shallow end of a gutter) have 3 mm pins that push into
  1/8 in holes. Nothing else holds them; the casting presses them onto the board.
- **Removable pieces** (formers, fillers, plugs, kit): 3-5 coats of paste wax and PVA like the boards.
  **Pieces that stay in** (core posts, cast-in parts): no wax; scuff and degrease them so the
  epoxy grips.

![Base rear mold: boards, kit and cores (orange)](../../renders/build/02-mold-base-rear.png)

## Foam pieces

The base pocket cores and the socket cores are XPS foam board (`foam=True`, the default in
`model/build_cnc.py`); only the pocket cores' posts and the socket spikes are printed. They are hidden and
only need to be within a millimeter or two. The coolant trough, gutters and the beam's back edge print,
because they shape faces you see and drain coolant (`foam_formers=True` cuts those from foam too). The
mold guide lists the foam pieces with their sizes. `foam=False` prints the cores (about 1.4 kg more).


## Base mold kit (both halves)

Folder `print/base-box/`, about 188 g.

| File | What | Qty | Size (mm) | g (all) | Notes |
|---|---|---|---|---|---|
| `kit-corner-bracket.stl` | Mold kit (reused) | 4 | 50 x 50 x 23 | 33 |  |
| `kit-partition-bracket.stl` | Mold kit (reused) | 2 | 44 x 44 x 23 | 14 |  |
| `kit-saddle.stl` | Mold kit (reused) | 6 | 53 x 31 x 25 | 58 | The rear half needs six; four move over for the front half. |
| `kit-leg-holder.stl` | Mold kit (reused) | 4 | 72 x 72 x 40 | 83 | Set the leg 92 mm proud of the holder and tighten the pinch screw (M4 x 20). |

## Base, rear half (cast first)

Folder `print/base-rear/`, about 250 g.

| File | What | Qty | Size (mm) | g (all) | Notes |
|---|---|---|---|---|---|
| `former-gutter-L-part1of3.stl` | Former (removable) | 1 | 15 x 124 x 12 | 8 | Bolts to the floor from underneath (the base is cast top face down). |
| `former-gutter-L-part2of3.stl` | Former (removable) | 1 | 15 x 124 x 10 | 8 |  |
| `former-gutter-L-part3of3.stl` | Former (removable) | 1 | 15 x 120 x 9 | 7 |  |
| `former-gutter-R-part1of3.stl` | Former (removable) | 1 | 15 x 124 x 12 | 8 | Bolts to the floor from underneath (the base is cast top face down). |
| `former-gutter-R-part2of3.stl` | Former (removable) | 1 | 15 x 124 x 10 | 8 |  |
| `former-gutter-R-part3of3.stl` | Former (removable) | 1 | 15 x 120 x 9 | 7 |  |
| `former-motor-relief.stl` | Former (removable) | 1 | 72 x 60 x 14 | 12 | Bolts to the floor from underneath (the base is cast top face down). |
| `filler-corner-L.stl` | Filler (removable) | 1 | 40 x 40 x 110 | 17 | Rounded corner; bolts to the floor and both walls. |
| `filler-corner-R.stl` | Filler (removable) | 1 | 40 x 40 x 110 | 16 | Rounded corner; bolts to the floor and both walls. |
| `former-split-gasket-groove-part1of4.stl` | Former (removable) | 1 | 145 x 14 x 8 | 2 | Pins into the partition. |
| `former-split-gasket-groove-part2of4.stl` | Former (removable) | 1 | 145 x 4 x 8 | 1 |  |
| `former-split-gasket-groove-part3of4.stl` | Former (removable) | 1 | 145 x 4 x 8 | 1 |  |
| `former-split-gasket-groove-part4of4.stl` | Former (removable) | 1 | 145 x 14 x 8 | 2 |  |
| `core-center-post.stl` | Pocket core (shell, stays in) | 1 | 12 x 12 x 81 | 5 | Post for a foam core: push it 30 mm into a snug hole in the foam and glue it. |
| `core-foot-b-L-post.stl` | Pocket core (shell, stays in) | 1 | 12 x 12 x 81 | 5 | Post for a foam core: push it 30 mm into a snug hole in the foam and glue it. |
| `core-foot-c-L-post.stl` | Pocket core (shell, stays in) | 1 | 12 x 12 x 81 | 5 | Post for a foam core: push it 30 mm into a snug hole in the foam and glue it. |
| `core-knee-L-post.stl` | Pocket core (shell, stays in) | 1 | 12 x 12 x 81 | 5 | Post for a foam core: push it 30 mm into a snug hole in the foam and glue it. |
| `core-outer-a-L-post.stl` | Pocket core (shell, stays in) | 1 | 12 x 12 x 81 | 5 | Post for a foam core: push it 30 mm into a snug hole in the foam and glue it. |
| `core-outer-b-L-post.stl` | Pocket core (shell, stays in) | 1 | 12 x 12 x 81 | 5 | Post for a foam core: push it 30 mm into a snug hole in the foam and glue it. |
| `core-rear-L-post.stl` | Pocket core (shell, stays in) | 1 | 12 x 12 x 81 | 5 | Post for a foam core: push it 30 mm into a snug hole in the foam and glue it. |
| `core-foot-b-R-post.stl` | Pocket core (shell, stays in) | 1 | 12 x 12 x 81 | 5 | Post for a foam core: push it 30 mm into a snug hole in the foam and glue it. |
| `core-foot-c-R-post.stl` | Pocket core (shell, stays in) | 1 | 12 x 12 x 81 | 5 | Post for a foam core: push it 30 mm into a snug hole in the foam and glue it. |
| `core-knee-R-post.stl` | Pocket core (shell, stays in) | 1 | 12 x 12 x 81 | 5 | Post for a foam core: push it 30 mm into a snug hole in the foam and glue it. |
| `core-outer-a-R-post.stl` | Pocket core (shell, stays in) | 1 | 12 x 12 x 81 | 5 | Post for a foam core: push it 30 mm into a snug hole in the foam and glue it. |
| `core-outer-b-R-post.stl` | Pocket core (shell, stays in) | 1 | 12 x 12 x 81 | 5 | Post for a foam core: push it 30 mm into a snug hole in the foam and glue it. |
| `core-rear-R-post.stl` | Pocket core (shell, stays in) | 1 | 12 x 12 x 81 | 5 | Post for a foam core: push it 30 mm into a snug hole in the foam and glue it. |
| `plug-socket-spike.stl` | Plug (removable) | 4 | 14 x 14 x 20 | 8 | Bolts to the floor; the foam socket block pushes over it (cut a 14 mm square hole 20 deep in the block). |
| `kit-spigot-bushing.stl` | Mold kit (reused) | 2 | 80 x 80 x 22 | 34 | Push fit in a 2-1/2 in hole-saw hole; flange on the far side. |
| `cast-in-base-rear-tube-plug-l.stl` | Cast-in part (stays in) | 2 | 42 x 10 x 42 | 13 | Cast in, stays. |
| `cast-in-base-rear-spigot-sleeve-l.stl` | Cast-in part (stays in) | 2 | 44 x 69 x 44 | 29 | Cast in, stays. |
| `cast-in-leg-rear-l-plug.stl` | Cast-in part (stays in) | 2 | 30 x 30 x 10 | 7 | Cast in, stays. |

## Base, front half

Folder `print/base-front/`, about 289 g.

| File | What | Qty | Size (mm) | g (all) | Notes |
|---|---|---|---|---|---|
| `former-gutter-L-part1of2.stl` | Former (removable) | 1 | 15 x 149 x 15 | 11 | Bolts to the floor from underneath (the base is cast top face down). |
| `former-gutter-L-part2of2.stl` | Former (removable) | 1 | 15 x 145 x 13 | 10 |  |
| `former-gutter-R-part1of2.stl` | Former (removable) | 1 | 15 x 149 x 15 | 11 | Bolts to the floor from underneath (the base is cast top face down). |
| `former-gutter-R-part2of2.stl` | Former (removable) | 1 | 15 x 145 x 13 | 10 |  |
| `former-trough-part1of5.stl` | Former (removable) | 1 | 116 x 35 x 19 | 20 | Bolts to the floor from underneath (the base is cast top face down). |
| `former-trough-part2of5.stl` | Former (removable) | 1 | 116 x 35 x 23 | 22 |  |
| `former-trough-part3of5.stl` | Former (removable) | 1 | 116 x 35 x 33 | 25 |  |
| `former-trough-part4of5.stl` | Former (removable) | 1 | 116 x 35 x 24 | 23 |  |
| `former-trough-part5of5.stl` | Former (removable) | 1 | 112 x 35 x 21 | 21 |  |
| `filler-corner-L.stl` | Filler (removable) | 1 | 40 x 40 x 110 | 21 | Rounded corner, and the plug that forms the draw-rod nut pocket; bolts to the floor and both walls. |
| `filler-corner-R.stl` | Filler (removable) | 1 | 40 x 40 x 110 | 21 | Rounded corner, and the plug that forms the draw-rod nut pocket; bolts to the floor and both walls. |
| `core-center-post.stl` | Pocket core (shell, stays in) | 1 | 12 x 12 x 81 | 5 | Post for a foam core: push it 30 mm into a snug hole in the foam and glue it. |
| `core-outboard-L-post.stl` | Pocket core (shell, stays in) | 1 | 12 x 12 x 81 | 5 | Post for a foam core: push it 30 mm into a snug hole in the foam and glue it. |
| `core-trough-band-L-post.stl` | Pocket core (shell, stays in) | 1 | 12 x 12 x 81 | 5 | Post for a foam core: push it 30 mm into a snug hole in the foam and glue it. |
| `core-draw-rod-L-post.stl` | Pocket core (shell, stays in) | 1 | 12 x 12 x 81 | 5 | Post for a foam core: push it 30 mm into a snug hole in the foam and glue it. |
| `core-foot-a-L-post.stl` | Pocket core (shell, stays in) | 1 | 12 x 12 x 81 | 5 | Post for a foam core: push it 30 mm into a snug hole in the foam and glue it. |
| `core-outboard-R-post.stl` | Pocket core (shell, stays in) | 1 | 12 x 12 x 81 | 5 | Post for a foam core: push it 30 mm into a snug hole in the foam and glue it. |
| `core-trough-band-R-post.stl` | Pocket core (shell, stays in) | 1 | 12 x 12 x 81 | 5 | Post for a foam core: push it 30 mm into a snug hole in the foam and glue it. |
| `core-draw-rod-R-post.stl` | Pocket core (shell, stays in) | 1 | 12 x 12 x 81 | 5 | Post for a foam core: push it 30 mm into a snug hole in the foam and glue it. |
| `core-foot-a-R-post.stl` | Pocket core (shell, stays in) | 1 | 12 x 12 x 81 | 5 | Post for a foam core: push it 30 mm into a snug hole in the foam and glue it. |
| `cast-in-base-front-tube-plug-l.stl` | Cast-in part (stays in) | 2 | 42 x 10 x 42 | 13 | Cast in, stays. |
| `cast-in-base-front-spigot-sleeve-l.stl` | Cast-in part (stays in) | 2 | 44 x 69 x 44 | 29 | Cast in, stays. |
| `cast-in-leg-front-l-plug.stl` | Cast-in part (stays in) | 2 | 30 x 30 x 10 | 7 | Cast in, stays. |

## Uprights (two molds: print quantities are for both)

Folder `print/upright/`, about 312 g.

| File | What | Qty | Size (mm) | g (all) | Notes |
|---|---|---|---|---|---|
| `kit-back-bracket.stl` | Mold kit (reused) | 4 | 33 x 33 x 23 | 21 |  |
| `kit-front-bracket.stl` | Mold kit (reused) | 4 | 50 x 50 x 22 | 32 | At the top of the front board; its foot sits in the toe filler's lip. |
| `kit-saddle-flat.stl` | Mold kit (reused) | 4 | 31 x 25 x 25 | 18 | The bridge rests on them; its rods locate it. |
| `filler-toe-filler.stl` | Filler (removable) | 2 | 80 x 60 x 48 | 54 | Rounds the nose into the slope; the front board's foot sits in its lip. Bolts to the floor. |
| `former-foot-gasket-groove-part1of4.stl` | Former (removable) | 2 | 68 x 139 x 8 | 7 | Pins into the floor. |
| `former-foot-gasket-groove-part2of4.stl` | Former (removable) | 2 | 4 x 139 x 8 | 3 |  |
| `former-foot-gasket-groove-part3of4.stl` | Former (removable) | 2 | 4 x 139 x 8 | 3 |  |
| `former-foot-gasket-groove-part4of4.stl` | Former (removable) | 2 | 68 x 139 x 8 | 7 |  |
| `plug-slope-plug-lower.stl` | Plug (removable) | 2 | 32 x 61 x 38 | 19 | Forms a nut pocket in the slope; bolts to the front board; its rod stops inside it. |
| `plug-slope-plug-upper.stl` | Plug (removable) | 2 | 32 x 61 x 38 | 19 | Forms a nut pocket in the slope; bolts to the front board; its rod stops inside it. |
| `plug-tie-rod-pocket.stl` | Plug (removable) | 4 | 32 x 32 x 49 | 33 | Forms a top nut pocket: slides down its rod; the bridge holds it down. |
| `kit-plate-spacer.stl` | Mold kit (reused) | 4 | 16 x 16 x 31 | 15 | Between the bridge and the top plate, on its greased 3/8 bolt. |
| `kit-post-bushing.stl` | Mold kit (reused) | 4 | 80 x 80 x 22 | 68 | Push fit in a 2-1/2 in hole-saw hole in the floor, flange underneath. |
| `cast-in-post-l1-plug.stl` | Cast-in part (stays in) | 4 | 30 x 30 x 10 | 14 | Cast in, stays. |

## Beam

Folder `print/beam/`, about 150 g.

| File | What | Qty | Size (mm) | g (all) | Notes |
|---|---|---|---|---|---|
| `kit-corner-bracket.stl` | Mold kit (reused) | 4 | 50 x 50 x 23 | 33 |  |
| `filler-back-edge-part1of4.stl` | Filler (removable) | 1 | 136 x 40 x 40 | 19 | Rounded back edge; bolts to the top wall. |
| `filler-back-edge-part2of4.stl` | Filler (removable) | 1 | 136 x 40 x 40 | 19 |  |
| `filler-back-edge-part3of4.stl` | Filler (removable) | 1 | 136 x 40 x 40 | 19 |  |
| `filler-back-edge-part4of4.stl` | Filler (removable) | 1 | 132 x 40 x 40 | 19 |  |
| `kit-tube-locator.stl` | Mold kit (reused) | 4 | 44 x 44 x 51 | 39 | Square end into the tube, stem to the end wall, M4 x 70 through the wall into a nut slid in from inside the tube. Leaves a 16 mm hole in each beam end. |
| `kit-dowel-stop.stl` | Mold kit (reused) | 2 | 18 x 18 x 11 | 2 | Pushes into the dowel hole from outside so the dowel stands 10 mm proud. |

## Machine parts

Folder `print/machine/`, about 99 g.

| File | What | Qty | Size (mm) | g (all) | Notes |
|---|---|---|---|---|---|
| `part-pocket-cap-l3.stl` | Machine part | 4 | 32 x 52 x 29 | 32 |  |
| `part-chain-mount-fixed.stl` | Machine part | 1 | 25 x 38 x 21 | 8 |  |
| `part-chain-mount-moving.stl` | Machine part | 1 | 37 x 123 x 45 | 18 |  |
| `part-sump-filter-frame-part1of2.stl` | Machine part | 1 | 148 x 6 x 92 | 20 |  |
| `part-sump-filter-frame-part2of2.stl` | Machine part | 1 | 148 x 6 x 92 | 20 |  |
