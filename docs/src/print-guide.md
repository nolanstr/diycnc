# Print guide

Every printed part for the molds, the castings and the machine, cut to fit a Bambu A1 mini
(180 mm cube; no piece is over 170 mm). The STL files are in `print/`, one folder per
casting, with the list in `print/manifest.csv`. They are written by `model/build_cnc.py` on every run.
How the molds go together is in the mold guide.

**114 prints, 1.25 kg of PETG** (two 1 kg rolls). The filament figures are rough estimates; run `python3 model/slice_prints.py` for sliced figures.

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

The base pocket cores are XPS foam board (`foam=True`, the default in
`model/build_cnc.py`); only their posts are printed. They are hidden and
only need to be within a millimeter or two. The coolant trough, gutters and the beam's back edge print,
because they shape faces you see and drain coolant (`foam_formers=True` cuts those from foam too). The
mold guide lists the foam pieces with their sizes. `foam=False` prints the cores (about 1.4 kg more).


## Tools: pour-line gauge and screed shoes

Folder `print/tools/`, about 37 g.

| File | What | Qty | Size (mm) | g (all) | Notes |
|---|---|---|---|---|---|
| `kit-pour-gauge.stl` | Mold kit (reused) | 2 | 25 x 29 x 24 | 11 | Clips over a wall top; its inner leg ends 25 mm down, on the pour line. Pencil along it all round the mold, and check the fill against it. |
| `kit-screed-shoe.stl` | Mold kit (reused) | 2 | 49 x 27 x 32 | 26 | A pair: rest them on two facing wall tops and drop a straight board (on edge) into them; its bottom edge sits on the pour line. Slide it along to strike off. |

## Base mold kit (both halves)

Folder `print/base-box/`, about 235 g.

| File | What | Qty | Size (mm) | g (all) | Notes |
|---|---|---|---|---|---|
| `kit-corner-bracket.stl` | Mold kit (reused) | 4 | 50 x 50 x 23 | 40 |  |
| `kit-partition-bracket.stl` | Mold kit (reused) | 2 | 44 x 44 x 23 | 18 |  |
| `kit-saddle.stl` | Mold kit (reused) | 6 | 53 x 31 x 25 | 73 | The rear half needs six; four move over for the front half. |
| `kit-leg-holder.stl` | Mold kit (reused) | 4 | 72 x 72 x 40 | 104 | Set the leg 92 mm proud of the holder and tighten the pinch screw (M4 x 20). |

## Base, rear half (cast first)

Folder `print/base-rear/`, about 195 g.

| File | What | Qty | Size (mm) | g (all) | Notes |
|---|---|---|---|---|---|
| `former-gutter-L-part1of3.stl` | Former (removable) | 1 | 15 x 124 x 12 | 9 | Bolts to the floor from underneath (the base is cast top face down). |
| `former-gutter-L-part2of3.stl` | Former (removable) | 1 | 15 x 124 x 10 | 8 |  |
| `former-gutter-L-part3of3.stl` | Former (removable) | 1 | 15 x 120 x 9 | 8 |  |
| `former-gutter-R-part1of3.stl` | Former (removable) | 1 | 15 x 124 x 12 | 9 | Bolts to the floor from underneath (the base is cast top face down). |
| `former-gutter-R-part2of3.stl` | Former (removable) | 1 | 15 x 124 x 10 | 8 |  |
| `former-gutter-R-part3of3.stl` | Former (removable) | 1 | 15 x 120 x 9 | 8 |  |
| `former-motor-relief.stl` | Former (removable) | 1 | 72 x 60 x 14 | 14 | Bolts to the floor from underneath (the base is cast top face down). |
| `filler-corner-L.stl` | Filler (removable) | 1 | 40 x 40 x 110 | 21 | Rounded corner; bolts to the floor and both walls. |
| `filler-corner-R.stl` | Filler (removable) | 1 | 40 x 40 x 110 | 21 | Rounded corner; bolts to the floor and both walls. |
| `former-split-gasket-groove-part1of4.stl` | Former (removable) | 1 | 145 x 14 x 8 | 2 | Pins into the partition. |
| `former-split-gasket-groove-part2of4.stl` | Former (removable) | 1 | 145 x 4 x 8 | 2 |  |
| `former-split-gasket-groove-part3of4.stl` | Former (removable) | 1 | 145 x 4 x 8 | 2 |  |
| `former-split-gasket-groove-part4of4.stl` | Former (removable) | 1 | 145 x 14 x 8 | 2 |  |
| `core-center-post.stl` | Pocket core (shell, stays in) | 1 | 12 x 12 x 81 | 6 | Post for a foam core: push it 30 mm into a snug hole in the foam and glue it. |
| `core-foot-b-L-post.stl` | Pocket core (shell, stays in) | 1 | 12 x 12 x 81 | 6 | Post for a foam core: push it 30 mm into a snug hole in the foam and glue it. |
| `core-knee-L-post.stl` | Pocket core (shell, stays in) | 1 | 12 x 12 x 81 | 6 | Post for a foam core: push it 30 mm into a snug hole in the foam and glue it. |
| `core-outer-a-L-post.stl` | Pocket core (shell, stays in) | 1 | 12 x 12 x 81 | 6 | Post for a foam core: push it 30 mm into a snug hole in the foam and glue it. |
| `core-outer-b-L-post.stl` | Pocket core (shell, stays in) | 1 | 12 x 12 x 81 | 6 | Post for a foam core: push it 30 mm into a snug hole in the foam and glue it. |
| `core-rear-L-post.stl` | Pocket core (shell, stays in) | 1 | 12 x 12 x 81 | 6 | Post for a foam core: push it 30 mm into a snug hole in the foam and glue it. |
| `core-foot-b-R-post.stl` | Pocket core (shell, stays in) | 1 | 12 x 12 x 81 | 6 | Post for a foam core: push it 30 mm into a snug hole in the foam and glue it. |
| `core-knee-R-post.stl` | Pocket core (shell, stays in) | 1 | 12 x 12 x 81 | 6 | Post for a foam core: push it 30 mm into a snug hole in the foam and glue it. |
| `core-outer-a-R-post.stl` | Pocket core (shell, stays in) | 1 | 12 x 12 x 81 | 6 | Post for a foam core: push it 30 mm into a snug hole in the foam and glue it. |
| `core-outer-b-R-post.stl` | Pocket core (shell, stays in) | 1 | 12 x 12 x 81 | 6 | Post for a foam core: push it 30 mm into a snug hole in the foam and glue it. |
| `core-rear-R-post.stl` | Pocket core (shell, stays in) | 1 | 12 x 12 x 81 | 6 | Post for a foam core: push it 30 mm into a snug hole in the foam and glue it. |
| `plug-draw-pocket-L.stl` | Plug (removable) | 1 | 32 x 32 x 20 | 6 | Forms a draw-rod nut pocket down to the girder's end plate; bolts to the wall. |
| `plug-draw-pocket-R.stl` | Plug (removable) | 1 | 32 x 32 x 20 | 6 | Forms a draw-rod nut pocket down to the girder's end plate; bolts to the wall. |
| `cast-in-leg-rear-l-plug.stl` | Cast-in part (stays in) | 2 | 31 x 31 x 10 | 9 | Cast in, stays. |

## Base, front half

Folder `print/base-front/`, about 288 g.

| File | What | Qty | Size (mm) | g (all) | Notes |
|---|---|---|---|---|---|
| `former-gutter-L-part1of2.stl` | Former (removable) | 1 | 15 x 149 x 15 | 13 | Bolts to the floor from underneath (the base is cast top face down). |
| `former-gutter-L-part2of2.stl` | Former (removable) | 1 | 15 x 145 x 13 | 12 |  |
| `former-gutter-R-part1of2.stl` | Former (removable) | 1 | 15 x 149 x 15 | 13 | Bolts to the floor from underneath (the base is cast top face down). |
| `former-gutter-R-part2of2.stl` | Former (removable) | 1 | 15 x 145 x 13 | 12 |  |
| `former-trough-part1of5.stl` | Former (removable) | 1 | 116 x 35 x 19 | 21 | Bolts to the floor from underneath (the base is cast top face down). |
| `former-trough-part2of5.stl` | Former (removable) | 1 | 116 x 35 x 23 | 24 |  |
| `former-trough-part3of5.stl` | Former (removable) | 1 | 116 x 35 x 33 | 27 |  |
| `former-trough-part4of5.stl` | Former (removable) | 1 | 116 x 35 x 24 | 25 |  |
| `former-trough-part5of5.stl` | Former (removable) | 1 | 112 x 35 x 21 | 23 |  |
| `filler-corner-L.stl` | Filler (removable) | 1 | 40 x 40 x 110 | 21 | Rounded corner; bolts to the floor and both walls. |
| `filler-corner-R.stl` | Filler (removable) | 1 | 40 x 40 x 110 | 21 | Rounded corner; bolts to the floor and both walls. |
| `core-center-a-post.stl` | Pocket core (shell, stays in) | 1 | 12 x 12 x 81 | 6 | Post for a foam core: push it 30 mm into a snug hole in the foam and glue it. |
| `core-center-b-post.stl` | Pocket core (shell, stays in) | 1 | 12 x 12 x 81 | 6 | Post for a foam core: push it 30 mm into a snug hole in the foam and glue it. |
| `core-outboard-L-post.stl` | Pocket core (shell, stays in) | 1 | 12 x 12 x 81 | 6 | Post for a foam core: push it 30 mm into a snug hole in the foam and glue it. |
| `core-trough-band-L-post.stl` | Pocket core (shell, stays in) | 1 | 12 x 12 x 81 | 6 | Post for a foam core: push it 30 mm into a snug hole in the foam and glue it. |
| `core-draw-rod-L-post.stl` | Pocket core (shell, stays in) | 1 | 12 x 12 x 81 | 6 | Post for a foam core: push it 30 mm into a snug hole in the foam and glue it. |
| `core-outboard-R-post.stl` | Pocket core (shell, stays in) | 1 | 12 x 12 x 81 | 6 | Post for a foam core: push it 30 mm into a snug hole in the foam and glue it. |
| `core-trough-band-R-post.stl` | Pocket core (shell, stays in) | 1 | 12 x 12 x 81 | 6 | Post for a foam core: push it 30 mm into a snug hole in the foam and glue it. |
| `core-draw-rod-R-post.stl` | Pocket core (shell, stays in) | 1 | 12 x 12 x 81 | 6 | Post for a foam core: push it 30 mm into a snug hole in the foam and glue it. |
| `plug-draw-pocket-L.stl` | Plug (removable) | 1 | 32 x 32 x 56 | 13 | Forms a draw-rod nut pocket down to the girder's end plate; bolts to the wall. |
| `plug-draw-pocket-R.stl` | Plug (removable) | 1 | 32 x 32 x 56 | 13 | Forms a draw-rod nut pocket down to the girder's end plate; bolts to the wall. |
| `cast-in-leg-front-l-plug.stl` | Cast-in part (stays in) | 2 | 31 x 31 x 10 | 9 | Cast in, stays. |

## Uprights (one mold, cast twice: cast-in parts are for both)

Folder `print/upright/`, about 275 g.

| File | What | Qty | Size (mm) | g (all) | Notes |
|---|---|---|---|---|---|
| `kit-back-bracket.stl` | Mold kit (reused) | 4 | 33 x 33 x 23 | 26 |  |
| `kit-front-bracket.stl` | Mold kit (reused) | 4 | 50 x 50 x 22 | 39 | At the top of the front board; its foot sits in the toe filler's lip. |
| `kit-saddle-flat.stl` | Mold kit (reused) | 4 | 31 x 25 x 25 | 23 | The bridge rests on them; its rods locate it. |
| `filler-toe-filler.stl` | Filler (removable) | 1 | 80 x 55 x 48 | 27 | Rounds the nose into the slope; the front board's foot sits in its lip. Bolts to the floor. |
| `former-foot-gasket-groove-part1of4.stl` | Former (removable) | 1 | 68 x 129 x 8 | 4 | Pins into the floor. |
| `former-foot-gasket-groove-part2of4.stl` | Former (removable) | 1 | 4 x 129 x 8 | 2 |  |
| `former-foot-gasket-groove-part3of4.stl` | Former (removable) | 1 | 4 x 129 x 8 | 2 |  |
| `former-foot-gasket-groove-part4of4.stl` | Former (removable) | 1 | 68 x 129 x 8 | 4 |  |
| `plug-toe-plug.stl` | Plug (removable) | 1 | 32 x 76 x 46 | 13 | Forms a nut pocket in the slope; bolts to the front board; its rod stops inside it. |
| `kit-plate-spacer.stl` | Mold kit (reused) | 2 | 16 x 16 x 31 | 9 | Between the bridge and the top plate, on its greased 3/8 bolt. |
| `cast-in-column-ring-l1a.stl` | Cast-in part (stays in) | 8 | 43 x 43 x 12 | 127 | Cast in, stays. |

## Beam

Folder `print/beam/`, about 108 g.

| File | What | Qty | Size (mm) | g (all) | Notes |
|---|---|---|---|---|---|
| `kit-corner-bracket.stl` | Mold kit (reused) | 4 | 50 x 50 x 23 | 40 |  |
| `filler-back-edge-part1of3.stl` | Filler (removable) | 1 | 124 x 40 x 40 | 22 | Rounded back edge between the uprights; bolts to the top wall. |
| `filler-back-edge-part2of3.stl` | Filler (removable) | 1 | 124 x 40 x 40 | 22 |  |
| `filler-back-edge-part3of3.stl` | Filler (removable) | 1 | 120 x 40 x 40 | 22 |  |
| `kit-dowel-stop.stl` | Mold kit (reused) | 2 | 18 x 18 x 6 | 2 | Pushes into the dowel hole from outside so the dowel stands 15 mm proud. |

## Machine parts

Folder `print/machine/`, about 113 g.

| File | What | Qty | Size (mm) | g (all) | Notes |
|---|---|---|---|---|---|
| `part-pocket-cap-l3.stl` | Machine part | 2 | 32 x 65 x 37 | 27 |  |
| `part-chain-mount-fixed.stl` | Machine part | 1 | 25 x 38 x 21 | 10 |  |
| `part-chain-mount-moving.stl` | Machine part | 1 | 37 x 123 x 45 | 24 |  |
| `part-sump-filter-frame-part1of2.stl` | Machine part | 1 | 148 x 6 x 92 | 26 |  |
| `part-sump-filter-frame-part2of2.stl` | Machine part | 1 | 148 x 6 x 92 | 26 |  |
