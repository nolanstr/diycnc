# Base mold

How to make, put together and take apart the mold for the base: both halves, cast one after the other on one floor board. The first section (how the molds
work) and the last three (pouring, taking it apart, fixes) are the same in every mold guide;
molds-complete.pdf has all the molds and the sheet layout for the boards.

The build guide covers the casting itself (mix, pour, cure); this guide is everything before and
after that. All the sizes and hole positions come from the model (`model/build_cnc.py`), so if you
change the design, re-run it and the guides, hole maps and printed parts all follow.

![The rear base-half mold ready to pour: boards see-through, printed kit in orange, foam in blue](../../renders/build/02-mold-base-rear.png)

**The order of work:** print the kit (start first: it is days of printing) &rarr; cut and drill the
boards &rarr; cut the foam &rarr; wax &rarr; assemble the mold &rarr; cast &rarr; take it apart. The
castings go in this order: base rear half, base front half (against the rear half), the two uprights
together, the beam.

## 1. How the molds work

**Walls stand 25 mm above the pour line.** All the bolts that hold the box together go through
that band, so none passes through a face that gets cast against. Fill to the line, not to the top.
Strips of board (cleats) bolted down along the outside of each wall's foot keep the walls from moving
out; printed corner brackets hold the corners square at the top.

![A corner of the base mold, the right way up](../../renders/mold/detail-corner.png)

**Printed pieces bolt on from outside.** Each piece that forms part of the casting's surface (the
formers and fillers) has a nut built into it: the nut drops into a pocket in the face that sits
against the board, slides sideways under the bolt hole, and an M4 bolt (M3 on thin pieces) goes
through the board from outside into it. The pocket is on the board side, so nothing opens onto a
cast face, and the bolt comes out from outside after casting. Fit the nuts before the pieces go on.

![The captive nut: drop it in, slide it under the hole, bolt through the board](../../renders/mold/fixing-nut.png)

**Thin pieces have pins.** The gasket-groove beads and the motor relief are too thin for a nut; their
3 mm pins push into 1/8 in holes. The casting presses them onto the board.

![Pins on a gasket-groove bead](../../renders/mold/fixing-pins.png)

**Pieces longer than the printer bed** are printed in parts with a peg on one cut face and a socket
in the other. Push them together; each part has its own bolts to the board, so they need no glue.

![Peg and socket between the parts of a long former](../../renders/mold/fixing-peg.png)

**Cores** (the pockets in the base underside) are blocks of XPS foam wrapped in packing tape. Each
has a printed post glued into it; the post bolts to the side of a bridge (a board standing on edge
across the mold, in printed saddles on the wall tops), which sets its height and stops it floating.

![A foam core hanging from its bridge](../../renders/mold/detail-core.png)

**Fits** are 0.15 mm a side: snug, but they go together by hand. Board thickness matters: the
saddles and cradles are drawn for 19.05 mm board (Home Depot's 3/4 in white melamine is a true
0.750 in). Measure yours; if it differs, set `mold_board` in `model/build_cnc.py` and re-run it.

## 2. What you need

| Material | Amount | Notes |
|---|---|---|
| Melamine board, 19 mm (3/4 in) | about 1.5 m2 | all the molds come out of two 4 x 8 ft sheets (layout in molds-complete.pdf) |
| XPS foam board, 2 in | 1 sheet, 2 x 8 ft | the cores; stack two layers for the 90 mm ones |
| PETG | 0.73 kg | this mold's printed parts (sliced); all the molds and machine parts fit in two 1 kg rolls |
| Packing tape, double-sided carpet tape | 1 roll each | foam wrapping and holding |
| Paste wax (Partall #2) and PVA | 1 each | release, 3-5 coats |
| 3/8 in quarter-round molding (PVC) | a few meters | the 10 mm outside edges of the castings |

**Hardware** (zinc-plated is fine; grease anything that touches the mix). Buy about 10 % spare of the
small bolts, nuts and washers.

| Item | Qty |
|---|---|
| M3 nut | 20 |
| M3 washer | 20 |
| M3 x 25 bolt | 20 |
| M4 nut | 112 |
| M4 washer | 108 |
| M4 x 20 bolt (leg pinch screw) | 4 |
| M4 x 30 bolt | 68 |
| M4 x 35 bolt | 24 |
| M4 x 45 bolt | 16 |
| M5 x 20 screw, greased (holds an insert) | 21 |
| M6 x 20 screw, greased (holds an insert) | 6 |
| 1/2-13 x 1-1/2 in bolt, greased (holds a draw-rod coupler) | 2 |
| 1/2-13 x 2-1/2 in bolt, greased (holds a coupler) | 8 |

**Tools:** a drill with sharp brad-point bits (sizes in section 5) and a 2-1/2 in hole saw; a square and a long straightedge; a few clamps; a 7 mm nut driver and a 3 mm hex key; a fine saw or a hot-wire cutter and a sanding block for the foam; a marker that writes on melamine.

## 3. Print the parts

80 prints, 0.73 kg of PETG and about 65 hours of printing, sliced in Bambu Studio for an A1 mini (settings in the
print guide). Print one corner bracket and one saddle first and check them on an offcut of your
board: the saddle should drop over it with a little play.

| Folder | File | Qty | g (all) | Time each |
|---|---|---|---|---|
| base-box | `kit-corner-bracket.stl` | 4 | 33 | 39m 28s |
| base-box | `kit-partition-bracket.stl` | 2 | 14 | 35m 28s |
| base-box | `kit-saddle.stl` | 6 | 58 | 46m 3s |
| base-box | `kit-leg-holder.stl` | 4 | 83 | 1h 37m 19s |
| base-rear | `former-gutter-L-part1of3.stl` | 1 | 8 | 35m 5s |
| base-rear | `former-gutter-L-part2of3.stl` | 1 | 8 | 33m 40s |
| base-rear | `former-gutter-L-part3of3.stl` | 1 | 7 | 31m 15s |
| base-rear | `former-gutter-R-part1of3.stl` | 1 | 8 | 35m 6s |
| base-rear | `former-gutter-R-part2of3.stl` | 1 | 8 | 33m 40s |
| base-rear | `former-gutter-R-part3of3.stl` | 1 | 7 | 31m 15s |
| base-rear | `former-motor-relief.stl` | 1 | 12 | 40m 58s |
| base-rear | `filler-corner-L.stl` | 1 | 17 | 1h 44m 24s |
| base-rear | `filler-corner-R.stl` | 1 | 16 | 1h 42m 27s |
| base-front | `former-gutter-L-part1of2.stl` | 1 | 11 | 49m 23s |
| base-front | `former-gutter-L-part2of2.stl` | 1 | 10 | 43m 43s |
| base-front | `former-gutter-R-part1of2.stl` | 1 | 11 | 49m 24s |
| base-front | `former-gutter-R-part2of2.stl` | 1 | 10 | 43m 43s |
| base-front | `former-trough-part1of5.stl` | 1 | 20 | 1h 14m 18s |
| base-front | `former-trough-part2of5.stl` | 1 | 22 | 1h 23m 56s |
| base-front | `former-trough-part3of5.stl` | 1 | 25 | 1h 33m 33s |
| base-front | `former-trough-part4of5.stl` | 1 | 23 | 1h 24m 3s |
| base-front | `former-trough-part5of5.stl` | 1 | 21 | 1h 17m 36s |
| base-front | `filler-corner-L.stl` | 1 | 21 | 2h 0m 50s |
| base-front | `filler-corner-R.stl` | 1 | 21 | 1h 56m 31s |
| base-rear | `former-split-gasket-groove-part1of4.stl` | 1 | 2 | 9m 50s |
| base-rear | `former-split-gasket-groove-part2of4.stl` | 1 | 1 | 8m 58s |
| base-rear | `former-split-gasket-groove-part3of4.stl` | 1 | 1 | 8m 58s |
| base-rear | `former-split-gasket-groove-part4of4.stl` | 1 | 2 | 9m 53s |
| base-front | `core-center-post.stl` | 1 | 5 | 44m 56s |
| base-rear | `core-center-post.stl` | 1 | 5 | 44m 56s |
| base-front | `core-outboard-L-post.stl` | 1 | 5 | 44m 53s |
| base-front | `core-trough-band-L-post.stl` | 1 | 5 | 44m 54s |
| base-front | `core-draw-rod-L-post.stl` | 1 | 5 | 44m 53s |
| base-front | `core-foot-a-L-post.stl` | 1 | 5 | 44m 53s |
| base-rear | `core-foot-b-L-post.stl` | 1 | 5 | 44m 53s |
| base-rear | `core-foot-c-L-post.stl` | 1 | 5 | 44m 53s |
| base-rear | `core-knee-L-post.stl` | 1 | 5 | 44m 53s |
| base-rear | `core-outer-a-L-post.stl` | 1 | 5 | 44m 53s |
| base-rear | `core-outer-b-L-post.stl` | 1 | 5 | 44m 53s |
| base-rear | `core-rear-L-post.stl` | 1 | 5 | 44m 53s |
| base-front | `core-outboard-R-post.stl` | 1 | 5 | 44m 53s |
| base-front | `core-trough-band-R-post.stl` | 1 | 5 | 44m 54s |
| base-front | `core-draw-rod-R-post.stl` | 1 | 5 | 44m 53s |
| base-front | `core-foot-a-R-post.stl` | 1 | 5 | 44m 53s |
| base-rear | `core-foot-b-R-post.stl` | 1 | 5 | 44m 53s |
| base-rear | `core-foot-c-R-post.stl` | 1 | 5 | 44m 53s |
| base-rear | `core-knee-R-post.stl` | 1 | 5 | 44m 53s |
| base-rear | `core-outer-a-R-post.stl` | 1 | 5 | 44m 53s |
| base-rear | `core-outer-b-R-post.stl` | 1 | 5 | 44m 53s |
| base-rear | `core-rear-R-post.stl` | 1 | 5 | 44m 53s |
| base-rear | `plug-socket-spike.stl` | 4 | 8 | 13m 26s |
| base-rear | `kit-spigot-bushing.stl` | 2 | 34 | 1h 11m 51s |
| base-front | `cast-in-base-front-tube-plug-l.stl` | 2 | 13 | 29m 7s |
| base-front | `cast-in-base-front-spigot-sleeve-l.stl` | 2 | 29 | 1h 14m 40s |
| base-front | `cast-in-leg-front-l-plug.stl` | 2 | 7 | 15m 49s |
| base-rear | `cast-in-base-rear-tube-plug-l.stl` | 2 | 13 | 27m 49s |
| base-rear | `cast-in-base-rear-spigot-sleeve-l.stl` | 2 | 29 | 1h 14m 38s |
| base-rear | `cast-in-leg-rear-l-plug.stl` | 2 | 7 | 15m 49s |

- **Nuts:** press M4 nuts into the hex pockets of the brackets and saddles; slide the nuts into the
  pockets of the formers and fillers (a dab of grease keeps them from falling out). A nut on a bolt
  through the hole pulls a tight one into place.
- **Pegs:** test-fit the parts of each long former; a light pass with a file if a peg is tight.

## 4. Cut the boards

Most boards are strips, so the quickest way is to have the store rip each sheet into strips at the
widths below, and crosscut them at home. Label every board with its name on the outside face as you
cut it, and mark which face is the cast face (the melamine face that the mix touches).

| Board | Qty | Size (mm) | Notes |
|---|---|---|---|
| Base floor | 1 | 718 x 843 | both halves are cast on it |
| Base front wall | 1 | 638 x 135 |  |
| Base rear wall | 1 | 638 x 135 |  |
| Base side wall, left | 1 | 724 x 135 |  |
| Base side wall, right | 1 | 724 x 135 |  |
| Base partition | 1 | 600 x 135 | rear half only; comes out before the front half |
| Base partition strut | 2 | 326 x 60 | offcut, stands on edge; holds the partition foot (rear half only) |
| Base cleat, front | 1 | 638 x 40 | offcut strip, flat on the floor |
| Base cleat, rear | 1 | 638 x 40 | offcut strip, flat on the floor |
| Base cleat, left | 1 | 724 x 40 | offcut strip, flat on the floor |
| Base cleat, right | 1 | 724 x 40 | offcut strip, flat on the floor |
| Base bridge y=-190 | 1 | 651 x 60 |  |
| Base bridge y=-58 | 1 | 651 x 60 |  |
| Base bridge y=100 | 1 | 651 x 60 |  |
| Base bridge y=170 | 1 | 651 x 60 |  |
| Base bridge y=280 | 1 | 651 x 60 |  |
| Base leg bridge y=-310 | 1 | 480 x 60 |  |
| Base leg bridge y=344 | 1 | 480 x 60 |  |

## 5. Drill the boards

- Drill every hole from the **cast side**, so any tear-out is on the outside. Clamp a scrap under
  the board where the bit comes out.
- The drawings and tables are seen from the cast side: x from the left edge, y from the bottom edge.
  For a wall the bottom edge sits on the floor; for a floor, the bottom of the drawing is toward the
  front wall (the beam's bottom wall). Left and right are as you look at the cast face, so a floor is
  mirrored compared with the machine. Bridges and cleats are drawn from the top.
- The brackets and saddles are drill guides: clamp one in place and drill through its holes.
- A washer goes under every bolt head; countersink nothing.

| Hole | Drill | For |
|---|---|---|
| 3.2 mm | 1/8 in | motor-relief, split-gasket-groove |
| 3.4 mm | 9/64 in | corner-L, corner-R, gutter-L, gutter-R |
| 4.5 mm | 11/64 in | cleat, core post, corner bracket, corner-L, corner-R, gutter-L, gutter-R, leg holder, saddle, socket spike, trough |
| 5.5 mm | 7/32 in | M5 insert screw |
| 6.5 mm | 17/64 in | M6 insert screw |
| 9.6 mm | 25/64 in | 3/8 dowel |
| 13.5 mm | 17/32 in | 1/2-13 bolt into coupler |
| 63.5 mm | 2-1/2 in hole saw | hole saw |

#### Base floor

![Base floor](boards/base-floor.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 80 | 20 | 4.5 | cleat |
| 2 | 266 | 20 | 4.5 | cleat |
| 3 | 452 | 20 | 4.5 | cleat |
| 4 | 638 | 20 | 4.5 | cleat |
| 5 | 71 | 64 | 3.4 | corner-R |
| 6 | 647 | 64 | 3.4 | corner-L |
| 7 | 159 | 69 | 5.5 | M5 insert screw |
| 8 | 359 | 69 | 5.5 | M5 insert screw |
| 9 | 559 | 69 | 5.5 | M5 insert screw |
| 10 | 107 | 89 | 4.5 | trough |
| 11 | 275 | 89 | 4.5 | trough |
| 12 | 387 | 89 | 4.5 | trough |
| 13 | 499 | 89 | 4.5 | trough |
| 14 | 611 | 89 | 4.5 | trough |
| 15 | 20 | 99 | 4.5 | cleat |
| 16 | 698 | 99 | 4.5 | cleat |
| 17 | 163 | 104 | 4.5 | trough |
| 18 | 219 | 104 | 4.5 | trough |
| 19 | 331 | 104 | 4.5 | trough |
| 20 | 443 | 104 | 4.5 | trough |
| 21 | 555 | 104 | 4.5 | trough |
| 22 | 87 | 150 | 4.5 | gutter-R |
| 23 | 632 | 150 | 4.5 | gutter-L |
| 24 | 269 | 184 | 5.5 | M5 insert screw |
| 25 | 449 | 184 | 5.5 | M5 insert screw |
| 26 | 69 | 209 | 5.5 | M5 insert screw |
| 27 | 336 | 210 | 6.5 | M6 insert screw |
| 28 | 382 | 210 | 6.5 | M6 insert screw |
| 29 | 649 | 209 | 5.5 | M5 insert screw |
| 30 | 87 | 223 | 4.5 | gutter-R |
| 31 | 632 | 223 | 4.5 | gutter-L |
| 32 | 87 | 295 | 3.4 | gutter-R |
| 33 | 632 | 295 | 3.4 | gutter-L |
| 34 | 269 | 304 | 5.5 | M5 insert screw |
| 35 | 449 | 304 | 5.5 | M5 insert screw |
| 36 | 20 | 314 | 4.5 | cleat |
| 37 | 698 | 314 | 4.5 | cleat |
| 38 | 134 | 344 | 13.5 | 1/2-13 bolt into coupler |
| 39 | 584 | 344 | 13.5 | 1/2-13 bolt into coupler |
| 40 | 87 | 368 | 3.4 | gutter-R |
| 41 | 632 | 368 | 3.4 | gutter-L |
| 42 | 69 | 421 | 5.5 | M5 insert screw |
| 43 | 649 | 421 | 5.5 | M5 insert screw |
| 44 | 269 | 424 | 5.5 | M5 insert screw |
| 45 | 449 | 424 | 5.5 | M5 insert screw |
| 46 | 87 | 434 | 3.4 | gutter-R |
| 47 | 632 | 434 | 3.4 | gutter-L |
| 48 | 134 | 444 | 13.5 | 1/2-13 bolt into coupler |
| 49 | 584 | 444 | 13.5 | 1/2-13 bolt into coupler |
| 50 | 87 | 494 | 3.4 | gutter-R |
| 51 | 632 | 494 | 3.4 | gutter-L |
| 52 | 20 | 529 | 4.5 | cleat |
| 53 | 698 | 529 | 4.5 | cleat |
| 54 | 269 | 544 | 5.5 | M5 insert screw |
| 55 | 449 | 544 | 5.5 | M5 insert screw |
| 56 | 87 | 554 | 3.4 | gutter-R |
| 57 | 632 | 554 | 3.4 | gutter-L |
| 58 | 134 | 569 | 4.5 | socket spike |
| 59 | 584 | 569 | 4.5 | socket spike |
| 60 | 87 | 614 | 3.4 | gutter-R |
| 61 | 632 | 614 | 3.4 | gutter-L |
| 62 | 114 | 624 | 13.5 | 1/2-13 bolt into coupler |
| 63 | 134 | 624 | 9.6 | 3/8 dowel |
| 64 | 154 | 624 | 13.5 | 1/2-13 bolt into coupler |
| 65 | 564 | 624 | 13.5 | 1/2-13 bolt into coupler |
| 66 | 584 | 624 | 9.6 | 3/8 dowel |
| 67 | 604 | 624 | 13.5 | 1/2-13 bolt into coupler |
| 68 | 69 | 634 | 5.5 | M5 insert screw |
| 69 | 649 | 634 | 5.5 | M5 insert screw |
| 70 | 269 | 664 | 5.5 | M5 insert screw |
| 71 | 449 | 664 | 5.5 | M5 insert screw |
| 72 | 87 | 674 | 3.4 | gutter-R |
| 73 | 632 | 674 | 3.4 | gutter-L |
| 74 | 134 | 679 | 4.5 | socket spike |
| 75 | 584 | 679 | 4.5 | socket spike |
| 76 | 336 | 705 | 6.5 | M6 insert screw |
| 77 | 382 | 705 | 6.5 | M6 insert screw |
| 78 | 336 | 718 | 6.5 | M6 insert screw |
| 79 | 382 | 718 | 6.5 | M6 insert screw |
| 80 | 87 | 734 | 3.4 | gutter-R |
| 81 | 343 | 737 | 3.2 | motor-relief |
| 82 | 632 | 734 | 3.4 | gutter-L |
| 83 | 20 | 744 | 4.5 | cleat |
| 84 | 698 | 744 | 4.5 | cleat |
| 85 | 64 | 772 | 3.4 | corner-R |
| 86 | 375 | 770 | 3.2 | motor-relief |
| 87 | 654 | 772 | 3.4 | corner-L |
| 88 | 209 | 774 | 5.5 | M5 insert screw |
| 89 | 509 | 774 | 5.5 | M5 insert screw |
| 90 | 80 | 823 | 4.5 | cleat |
| 91 | 266 | 823 | 4.5 | cleat |
| 92 | 452 | 823 | 4.5 | cleat |
| 93 | 638 | 823 | 4.5 | cleat |

#### Base front wall

![Base front wall](boards/base-front-wall.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 39 | 55 | 4.5 | corner-L |
| 2 | 599 | 55 | 4.5 | corner-R |
| 3 | 33 | 124 | 4.5 | corner bracket |
| 4 | 605 | 124 | 4.5 | corner bracket |
| 5 | 54 | 129 | 4.5 | leg holder |
| 6 | 584 | 129 | 4.5 | leg holder |

#### Base rear wall

![Base rear wall](boards/base-rear-wall.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 26 | 56 | 4.5 | corner-R |
| 2 | 612 | 56 | 4.5 | corner-L |
| 3 | 33 | 124 | 4.5 | corner bracket |
| 4 | 605 | 124 | 4.5 | corner bracket |
| 5 | 54 | 129 | 4.5 | leg holder |
| 6 | 584 | 129 | 4.5 | leg holder |

#### Base side wall, left

![Base side wall, left](boards/base-side-wall-left.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 7 | 35 | 4.5 | corner-L |
| 2 | 707 | 54 | 4.5 | corner-L |
| 3 | 14 | 124 | 4.5 | corner bracket |
| 4 | 100 | 123 | 4.5 | saddle |
| 5 | 210 | 123 | 4.5 | saddle |
| 6 | 280 | 123 | 4.5 | saddle |
| 7 | 419 | 124 | 4.5 | corner bracket |
| 8 | 438 | 123 | 4.5 | saddle |
| 9 | 570 | 123 | 4.5 | saddle |
| 10 | 711 | 124 | 4.5 | corner bracket |
| 11 | 35 | 129 | 4.5 | leg holder |
| 12 | 690 | 129 | 4.5 | leg holder |

#### Base side wall, right

![Base side wall, right](boards/base-side-wall-right.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 718 | 35 | 4.5 | corner-R |
| 2 | 18 | 56 | 4.5 | corner-R |
| 3 | 14 | 124 | 4.5 | corner bracket |
| 4 | 155 | 123 | 4.5 | saddle |
| 5 | 287 | 123 | 4.5 | saddle |
| 6 | 306 | 124 | 4.5 | corner bracket |
| 7 | 445 | 123 | 4.5 | saddle |
| 8 | 515 | 123 | 4.5 | saddle |
| 9 | 625 | 123 | 4.5 | saddle |
| 10 | 711 | 124 | 4.5 | corner bracket |
| 11 | 35 | 129 | 4.5 | leg holder |
| 12 | 690 | 129 | 4.5 | leg holder |

#### Base partition

![Base partition](boards/base-partition.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 46 | 18 | 3.2 | split-gasket-groove |
| 2 | 119 | 18 | 3.2 | split-gasket-groove |
| 3 | 191 | 18 | 3.2 | split-gasket-groove |
| 4 | 264 | 18 | 3.2 | split-gasket-groove |
| 5 | 336 | 18 | 3.2 | split-gasket-groove |
| 6 | 409 | 18 | 3.2 | split-gasket-groove |
| 7 | 481 | 18 | 3.2 | split-gasket-groove |
| 8 | 554 | 18 | 3.2 | split-gasket-groove |
| 9 | 20 | 55 | 13.5 | 1/2-13 bolt into coupler |
| 10 | 580 | 55 | 13.5 | 1/2-13 bolt into coupler |
| 11 | 210 | 68 | 63.5 | hole saw |
| 12 | 390 | 68 | 63.5 | hole saw |
| 13 | 20 | 124 | 4.5 | corner bracket |
| 14 | 580 | 124 | 4.5 | corner bracket |

#### Base cleat, front

![Base cleat, front](boards/base-cleat-front.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 598 | 20 | 4.5 | cleat |
| 2 | 412 | 20 | 4.5 | cleat |
| 3 | 226 | 20 | 4.5 | cleat |
| 4 | 40 | 20 | 4.5 | cleat |

#### Base cleat, rear

![Base cleat, rear](boards/base-cleat-rear.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 598 | 20 | 4.5 | cleat |
| 2 | 412 | 20 | 4.5 | cleat |
| 3 | 226 | 20 | 4.5 | cleat |
| 4 | 40 | 20 | 4.5 | cleat |

#### Base cleat, left

![Base cleat, left](boards/base-cleat-left.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 684 | 20 | 4.5 | cleat |
| 2 | 470 | 20 | 4.5 | cleat |
| 3 | 255 | 20 | 4.5 | cleat |
| 4 | 40 | 20 | 4.5 | cleat |

#### Base cleat, right

![Base cleat, right](boards/base-cleat-right.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 684 | 20 | 4.5 | cleat |
| 2 | 470 | 20 | 4.5 | cleat |
| 3 | 255 | 20 | 4.5 | cleat |
| 4 | 40 | 20 | 4.5 | cleat |

#### Base bridge y=-190

![Base bridge y=-190](boards/base-bridge-y-190.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 635 | 11 | 4.5 | saddle |
| 2 | 599 | 12 | 4.5 | core post |
| 3 | 520 | 12 | 4.5 | core post |
| 4 | 325 | 12 | 4.5 | core post |
| 5 | 130 | 12 | 4.5 | core post |
| 6 | 52 | 12 | 4.5 | core post |
| 7 | 16 | 11 | 4.5 | saddle |

#### Base bridge y=-58

![Base bridge y=-58](boards/base-bridge-y-58.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 635 | 11 | 4.5 | saddle |
| 2 | 489 | 12 | 4.5 | core post |
| 3 | 161 | 12 | 4.5 | core post |
| 4 | 16 | 11 | 4.5 | saddle |

#### Base bridge y=100

![Base bridge y=100](boards/base-bridge-y-100.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 635 | 11 | 4.5 | saddle |
| 2 | 565 | 12 | 4.5 | core post |
| 3 | 489 | 12 | 4.5 | core post |
| 4 | 161 | 12 | 4.5 | core post |
| 5 | 85 | 12 | 4.5 | core post |
| 6 | 16 | 11 | 4.5 | saddle |

#### Base bridge y=170

![Base bridge y=170](boards/base-bridge-y-170.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 635 | 11 | 4.5 | saddle |
| 2 | 600 | 12 | 4.5 | core post |
| 3 | 325 | 12 | 4.5 | core post |
| 4 | 51 | 12 | 4.5 | core post |
| 5 | 16 | 11 | 4.5 | saddle |

#### Base bridge y=280

![Base bridge y=280](boards/base-bridge-y-280.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 635 | 11 | 4.5 | saddle |
| 2 | 600 | 12 | 4.5 | core post |
| 3 | 480 | 12 | 4.5 | core post |
| 4 | 170 | 12 | 4.5 | core post |
| 5 | 51 | 12 | 4.5 | core post |
| 6 | 16 | 11 | 4.5 | saddle |

#### Base leg bridge y=-310

![Base leg bridge y=-310](boards/base-leg-bridge-y-310.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 474 | 11 | 4.5 | leg holder |
| 2 | 426 | 12 | 4.5 | core post |
| 3 | 54 | 12 | 4.5 | core post |
| 4 | 6 | 11 | 4.5 | leg holder |

#### Base leg bridge y=344

![Base leg bridge y=344](boards/base-leg-bridge-y-344.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 474 | 11 | 4.5 | leg holder |
| 2 | 385 | 12 | 4.5 | core post |
| 3 | 95 | 12 | 4.5 | core post |
| 4 | 6 | 11 | 4.5 | leg holder |

## 6. Cut the foam

Cut with a fine saw, a hot wire, or a long sharp knife and a sanding block. Wrap each piece in packing
tape (smooth, no wrinkles: the tape is the cast face). For the 90 mm cores glue two layers of 2 in
foam with a foam-safe adhesive (not solvent cement) or double-sided tape, then trim. Make each pocket
core's post hole a snug 12 mm square, 30 mm deep, and glue the printed post in.

| Casting | Piece | Qty | Size and how |
|---|---|---|---|
| base-front | center | 1 | XPS block 100 x 185 x 90 mm, outline as the pocket (chamfered corners); taped, with its printed post glued in. |
| base-rear | center | 1 | XPS block 100 x 190 x 90 mm, outline as the pocket (chamfered corners); taped, with its printed post glued in. |
| base-front | outboard-L | 1 | XPS block 130 x 164 x 90 mm, outline as the pocket (chamfered corners); taped, with its printed post glued in. |
| base-front | trough-band-L | 1 | XPS block 101 x 55 x 40 mm, outline as the pocket (chamfered corners); taped, with its printed post glued in. |
| base-front | draw-rod-L | 1 | XPS block 37 x 255 x 40 mm, outline as the pocket (chamfered corners); taped, with its printed post glued in. |
| base-front | foot-a-L | 1 | XPS block 68 x 66 x 90 mm, outline as the pocket (chamfered corners); taped, with its printed post glued in. |
| base-rear | foot-b-L | 1 | XPS block 68 x 100 x 90 mm, outline as the pocket (chamfered corners); taped, with its printed post glued in. |
| base-rear | foot-c-L | 1 | XPS block 80 x 63 x 90 mm, outline as the pocket (chamfered corners); taped, with its printed post glued in. |
| base-rear | knee-L | 1 | XPS block 50 x 183 x 40 mm, outline as the pocket (chamfered corners); taped, with its printed post glued in. |
| base-rear | outer-a-L | 1 | XPS block 35 x 43 x 65 mm, outline as the pocket (chamfered corners); taped, with its printed post glued in. |
| base-rear | outer-b-L | 1 | XPS block 35 x 60 x 65 mm, outline as the pocket (chamfered corners); taped, with its printed post glued in. |
| base-rear | rear-L | 1 | XPS block 170 x 52 x 90 mm, outline as the pocket (chamfered corners); taped, with its printed post glued in. |
| base-front | outboard-R | 1 | XPS block 130 x 164 x 90 mm, outline as the pocket (chamfered corners); taped, with its printed post glued in. |
| base-front | trough-band-R | 1 | XPS block 101 x 55 x 40 mm, outline as the pocket (chamfered corners); taped, with its printed post glued in. |
| base-front | draw-rod-R | 1 | XPS block 37 x 255 x 40 mm, outline as the pocket (chamfered corners); taped, with its printed post glued in. |
| base-front | foot-a-R | 1 | XPS block 68 x 66 x 90 mm, outline as the pocket (chamfered corners); taped, with its printed post glued in. |
| base-rear | foot-b-R | 1 | XPS block 68 x 100 x 90 mm, outline as the pocket (chamfered corners); taped, with its printed post glued in. |
| base-rear | foot-c-R | 1 | XPS block 80 x 63 x 90 mm, outline as the pocket (chamfered corners); taped, with its printed post glued in. |
| base-rear | knee-R | 1 | XPS block 50 x 183 x 40 mm, outline as the pocket (chamfered corners); taped, with its printed post glued in. |
| base-rear | outer-a-R | 1 | XPS block 35 x 43 x 65 mm, outline as the pocket (chamfered corners); taped, with its printed post glued in. |
| base-rear | outer-b-R | 1 | XPS block 35 x 60 x 65 mm, outline as the pocket (chamfered corners); taped, with its printed post glued in. |
| base-rear | rear-R | 1 | XPS block 170 x 52 x 90 mm, outline as the pocket (chamfered corners); taped, with its printed post glued in. |
| base-rear | socket | 4 | XPS block 41 x 41 x 80 mm, taped; dig it out after curing (a little acetone dissolves the rest). |

![A socket core: printed spike bolted to the floor, the foam pushed over it](../../renders/mold/detail-socket.png)

## 7. Prepare the surfaces

- Wax every face the mix touches, boards and removable printed pieces alike: 3-5 thin coats of paste
  wax, each buffed, then a coat of PVA. Don't wax the pieces that stay in (core posts, cast-in parts):
  scuff them and wipe them with acetone so the epoxy grips.
- The castings' outside edges are rounded 10 mm: glue 3/8 in quarter-round molding into the inside
  corners that form outside edges (floor to wall), and run a small silicone fillet into the others.
- Grease every screw, bolt and rod that will come out of the casting.

## 8. Put the mold together

### Base, rear half (cast first)

Both base halves are cast on the same floor board. The rear half goes first, against a partition at
the split; then the partition comes out and the front half is cast against the rear half's waxed
split face. The two top faces come out flush, the split faces match, and the front tubes slide
straight onto the rear half's spigots. The base is cast upside down (its top face on the floor);
these pictures show the mold the right way up.

1. Stand the floor on three battens (the insert screws and floor bolts come up from underneath) and bolt the cleats down along its edges.

![Base rear, step 1](../../renders/mold/step-base-rear-1.png)

2. Stand the walls on the floor against the cleats and fit the four corner brackets at the top corners. Measure the diagonals before you tighten: they should match within 2 mm.

![Base rear, step 2](../../renders/mold/step-base-rear-2.png)

3. Fit the partition between the side walls with its two brackets on the front side, and the two struts from the front wall to its foot. Push the gasket-groove beads onto its pins and the spigot bushings into its holes from the front.

![Base rear, step 3](../../renders/mold/step-base-rear-3.png)

4. Bolt on the gutter formers, the motor relief (pins) and the rear corner fillers; bolt the socket spikes to the floor and push a taped foam block over each.

![Base rear, step 4](../../renders/mold/step-base-rear-4.png)

5. Screw the inserts to the floor and the tie-rod couplers onto their greased bolts; hold the draw-rod couplers on bolts through the partition. Slide the spigots through the bushings and put the rear tubes on them, with their sleeves and end plugs. Bolt the leg holders into the corners, drop the legs in, set each at its height and tighten its pinch screw.

![Base rear, step 5](../../renders/mold/step-base-rear-5.png)

6. Cast the 20 mm skin first. Then set the foam cores on it, drop the bridges into the saddles and bolt each core's post to its bridge. Fill to the pour line.

![Base rear, step 6](../../renders/mold/step-base-rear-6.png)

### Base, front half (against the rear half)

1. After the cure: unbolt the bridges, the partition and its struts, and leave the rest. Dig the foam out of the four sockets, pull the gasket-groove beads, tape over the groove, and wax and PVA the rear half's split face and spigots.

![Base front, step 1](../../renders/mold/step-base-front-1.png)

2. Bolt on the trough and gutter formers (the drain liner on the trough's spigot) and the front corner fillers; put the front tubes, sleeves and plugs onto the spigots; screw the draw rods into the rear half's couplers with their ends in the corner fillers; inserts, couplers and legs as before.

![Base front, step 2](../../renders/mold/step-base-front-2.png)

3. Skin, foam cores, bridges, fill. After the cure unbolt everything and split the halves with a few wedges at the split, gently.

![Base front, step 3](../../renders/mold/step-base-front-3.png)

## 9. Pouring, and the pour line

- The pour line is 25 mm below the wall tops. Mark it inside each wall with a pencil line, and
  screed the top with a straight board that has two 25 mm feet riding on the wall tops.
- Vibrate each layer until it stops bubbling; the brackets and cleats hold the walls, so you can vibrate
  the floor board hard. Check the corner brackets and saddle bolts are still tight halfway through.
- Keep the mix off the bridges and saddles; scrape it off before it cures.

## 10. Taking it apart, and reuse

1. Leave it the full cure time (build guide). Unbolt the bridges and saddles, then the corner
   brackets, then the cleats; pull the walls straight off (a plastic wedge in the corner helps).
2. Unscrew every insert screw, coupler bolt and rod from outside, then lift the casting off the floor
   (or the floor off the casting).
3. Unbolt and pull the formers and fillers (the bolts come out from the board side first). A wooden
   dowel and a light tap frees a stuck one. Dig out the socket foam; the pocket cores can stay.
4. Scrape the boards, re-wax them, and store the kit pieces with their nuts in a box per mold. The
   same kit does the next casting; only the formers and pieces that stay in are per casting.

## 11. If something doesn't fit

| Problem | Fix |
|---|---|
| A nut won't slide under the hole | Clean the pocket with a nut on a bolt; a warm nut (hair dryer) pushes in |
| A bracket or saddle is loose on the board | Your board is thinner than set: shim with tape, or set `mold_board` and reprint |
| A pin won't go into its hole | Run a 1/8 in bit through the hole again; trim the pin tip with a knife |
| A foam core moves while pouring | Check its post bolt is tight and the post is glued; add carpet tape under it |
| Mix leaks at a corner | A silicone fillet inside the corner before waxing; check the diagonals and brackets |
| A former is stuck after curing | Bolts out first; then a dowel and a light tap from its thick end |
