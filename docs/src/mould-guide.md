# Mould guide

The moulds are melamine boards that bolt together with printed brackets, and every printed piece
bolts or pins to its board from outside. Nothing is glued and nothing goes through a cast face,
so the moulds come apart cleanly and go back together the same way for the next casting.

## How it works

- **Walls stand 25 mm above the pour line.** The brackets, saddles and leg holders bolt through that
  band, so no bolt passes through a face that gets cast against. Fill to the line, not to the top.
- **Corner brackets** hold each outside corner square in that band; **floor brackets** hold each wall
  foot from outside and bolt down through the floor. Each bracket has its nut pressed into a hex pocket,
  and its holes are a drill guide: clamp it in place and drill through it.
- **Printed pieces bolt on from outside.** An M4 bolt (M3 on thin pieces) goes through the board into
  a nut built into the piece. The nut drops into a pocket in the face against the board and slides
  over under the hole, so nothing opens onto a cast face. Fit the nuts before the pieces go on.
- **Thin pieces have pins.** The gasket-groove beads and the shallow end of the gutters have 3 mm pins
  that push into 1/8 in holes. The casting presses them onto the board.
- **Pieces cut to fit the printer** have a peg and socket on the cut, and their own fixings.
- **Bridges** stand on edge in saddles that hook over the wall tops; each core has a post that bolts
  to the side of a bridge, which sets its height and stops it floating.
- **Fits** are 0.15 mm a side: snug, but they go together by hand. Waxed pieces come out after curing.

**Measure your board first.** The saddles, cradles and drawings are for 19.05 mm board (Home Depot's
3/4 in white melamine is a true 0.750 in; other "3/4 in" melamine can be 18 mm). If yours is different,
set `mould_board` in `model/build_cnc.py` and re-run it: the STLs, hole maps and this guide all update.

![Rear-half mould: walls see-through, kit and cores orange](../../renders/build/02-mould-base-rear.png)

![Corner of the base mould: corner bracket, leg holder and its sleeve, saddle and bridge, corner filler](../../renders/mould/base-corner.png)

## What to buy

- **Melamine board**, 19 mm (3/4 in): about 2.6 m2 of boards in all, so 2 sheets of 4 x 8 ft with room for mistakes. Have the store rip it into strips at the widths in the cut list.
- **Hardware** (zinc-plated is fine; grease anything that touches the mix):

| Item | Qty |
|---|---|
| M3 nut | 32 |
| M3 washer | 44 |
| M3 x 10 bolt | 12 |
| M3 x 25 bolt | 20 |
| M4 nut | 166 |
| M4 washer | 166 |
| M4 x 30 bolt | 134 |
| M4 x 35 bolt | 28 |
| M4 x 70 bolt | 4 |
| M5 x 20 screw, greased (holds an insert) | 29 |
| M6 x 20 screw, greased (holds a pad) | 6 |
| M6 x 20 screw, greased (holds an insert) | 6 |
| 1/2 in plain steel rod, greased (forms a beam bolt hole), 198 mm | 8 |
| 1/2-13 x 1-1/2 in bolt + nut, greased (forms the dowel hole) | 2 |
| 1/2-13 x 1-1/2 in bolt, greased (holds a draw-rod coupler) | 2 |
| 1/2-13 x 2-1/2 in bolt, greased (holds a coupler) | 8 |
| 3/8-16 x 2-1/2 in bolt, greased (holds the top plate) | 4 |
| 5/8 in plain steel rod, greased (forms a tie-rod hole), cut to 140 mm, 243 mm, 377 mm, 377 mm | 2 |
| Block of 2x4, 52 mm long: four under each upright mould (the posts stand on the bench) | 8 |

Buy about 10 % spare of the small bolts, nuts and washers.

## Cut list

Sizes are length x height (or width) of the face, in mm. Boards marked "profile" are cut to the outline in
their drawing.

| Mould | Board | Qty | Size (mm) | Notes |
|---|---|---|---|---|
| Base | Base floor | 1 | 718 x 843 | both halves are cast on it |
| Base | Base front wall | 1 | 638 x 135 |  |
| Base | Base rear wall | 1 | 638 x 135 |  |
| Base | Base side wall, left | 1 | 724 x 135 |  |
| Base | Base side wall, right | 1 | 724 x 135 |  |
| Base | Base partition | 1 | 600 x 135 | rear half only; comes out before the front half |
| Base | Base partition strut | 2 | 326 x 60 | offcut, stands on edge; holds the partition foot (rear half only) |
| Base | Base bridge y=-190 | 1 | 651 x 60 |  |
| Base | Base bridge y=-58 | 1 | 651 x 60 |  |
| Base | Base bridge y=100 | 1 | 651 x 60 |  |
| Base | Base bridge y=170 | 1 | 651 x 60 |  |
| Base | Base bridge y=280 | 1 | 651 x 60 |  |
| Base | Base leg bridge y=-310 | 1 | 480 x 60 |  |
| Base | Base leg bridge y=344 | 1 | 480 x 60 |  |
| Uprights | Upright floor | 2 | 198 x 575 |  |
| Uprights | Upright side plate, outer | 2 | 495 x 271 (profile) | cut to the profile |
| Uprights | Upright side plate, inner | 2 | 495 x 271 (profile) | cut to the profile |
| Uprights | Upright back board | 2 | 80 x 271 |  |
| Uprights | Upright front board | 2 | 80 x 312 | ends cut square |
| Uprights | Upright bridge | 2 | 131 x 108 |  |
| Beam | Beam floor | 1 | 648 x 258 |  |
| Beam | Beam top wall | 1 | 568 x 165 |  |
| Beam | Beam bottom wall | 1 | 568 x 165 |  |
| Beam | Beam end wall, left | 1 | 140 x 165 |  |
| Beam | Beam end wall, right | 1 | 140 x 165 |  |

## Drilling

- Drill every hole from the **cast side** (the face the mix touches), so any tear-out is on the outside.
  The drawings and tables are seen from that side: x from the left edge, y from the bottom edge. For a
  wall the bottom edge sits on the floor; for a floor, the bottom of the drawing is toward the front
  wall (or the beam's bottom wall). Left and right are as you look at the cast face, so a floor seen
  from above is mirrored compared with the machine.
- Bridges are drawn from the top (outside).
- Use the printed brackets as drill guides where they sit; the tables give every hole anyway.

| Hole | Drill | For |
|---|---|---|
| 3.2 mm | 1/8 in | foot-gasket-groove, motor-relief, split-gasket-groove |
| 3.4 mm | 9/64 in | corner-L, corner-R, gutter-L, gutter-R |
| 4.5 mm | 11/64 in | back-edge-1, core post, corner bracket, corner-L, corner-R, floor bracket, gutter-L, gutter-R, leg holder, saddle, slope-pocket--60, slope-pocket-40, socket plug, toe-filler, trough, tube locator |
| 5.5 mm | 7/32 in | M5 insert screw |
| 6.5 mm | 17/64 in | M6 insert screw |
| 9.6 mm | 25/64 in | 3/8 dowel |
| 10 mm | 25/64 in | 3/8-16 bolt into the top plate |
| 13.1 mm | 33/64 in | 1/2 core rod, 1/2-13 bolt, base dowel hole |
| 13.5 mm | 17/32 in | 1/2-13 bolt into coupler |
| 16.3 mm | 41/64 in | 5/8 core rod |
| 63.5 mm | 2-1/2 in hole saw | hole saw |

## Base: hole maps

### Base floor

![Base floor](boards/base-floor.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 209 | 21 | 4.5 | floor bracket |
| 2 | 509 | 21 | 4.5 | floor bracket |
| 3 | 71 | 64 | 3.4 | corner-R |
| 4 | 647 | 64 | 3.4 | corner-L |
| 5 | 159 | 69 | 5.5 | M5 insert screw |
| 6 | 359 | 69 | 5.5 | M5 insert screw |
| 7 | 559 | 69 | 5.5 | M5 insert screw |
| 8 | 107 | 89 | 4.5 | trough |
| 9 | 275 | 89 | 4.5 | trough |
| 10 | 387 | 89 | 4.5 | trough |
| 11 | 499 | 89 | 4.5 | trough |
| 12 | 611 | 89 | 4.5 | trough |
| 13 | 163 | 104 | 4.5 | trough |
| 14 | 219 | 104 | 4.5 | trough |
| 15 | 331 | 104 | 4.5 | trough |
| 16 | 443 | 104 | 4.5 | trough |
| 17 | 555 | 104 | 4.5 | trough |
| 18 | 87 | 150 | 4.5 | gutter-R |
| 19 | 632 | 150 | 4.5 | gutter-L |
| 20 | 21 | 174 | 4.5 | floor bracket |
| 21 | 697 | 174 | 4.5 | floor bracket |
| 22 | 269 | 184 | 5.5 | M5 insert screw |
| 23 | 449 | 184 | 5.5 | M5 insert screw |
| 24 | 69 | 209 | 5.5 | M5 insert screw |
| 25 | 336 | 210 | 6.5 | M6 insert screw |
| 26 | 382 | 210 | 6.5 | M6 insert screw |
| 27 | 649 | 209 | 5.5 | M5 insert screw |
| 28 | 87 | 223 | 4.5 | gutter-R |
| 29 | 632 | 223 | 4.5 | gutter-L |
| 30 | 87 | 295 | 3.4 | gutter-R |
| 31 | 632 | 295 | 3.4 | gutter-L |
| 32 | 269 | 304 | 5.5 | M5 insert screw |
| 33 | 449 | 304 | 5.5 | M5 insert screw |
| 34 | 134 | 344 | 13.5 | 1/2-13 bolt into coupler |
| 35 | 584 | 344 | 13.5 | 1/2-13 bolt into coupler |
| 36 | 87 | 368 | 3.4 | gutter-R |
| 37 | 632 | 368 | 3.4 | gutter-L |
| 38 | 69 | 421 | 5.5 | M5 insert screw |
| 39 | 649 | 421 | 5.5 | M5 insert screw |
| 40 | 21 | 424 | 4.5 | floor bracket |
| 41 | 269 | 424 | 5.5 | M5 insert screw |
| 42 | 449 | 424 | 5.5 | M5 insert screw |
| 43 | 697 | 424 | 4.5 | floor bracket |
| 44 | 87 | 434 | 3.4 | gutter-R |
| 45 | 632 | 434 | 3.4 | gutter-L |
| 46 | 134 | 444 | 13.5 | 1/2-13 bolt into coupler |
| 47 | 584 | 444 | 13.5 | 1/2-13 bolt into coupler |
| 48 | 87 | 494 | 3.4 | gutter-R |
| 49 | 632 | 494 | 3.4 | gutter-L |
| 50 | 269 | 544 | 5.5 | M5 insert screw |
| 51 | 449 | 544 | 5.5 | M5 insert screw |
| 52 | 87 | 554 | 3.4 | gutter-R |
| 53 | 632 | 554 | 3.4 | gutter-L |
| 54 | 134 | 569 | 4.5 | socket plug |
| 55 | 584 | 569 | 4.5 | socket plug |
| 56 | 87 | 614 | 3.4 | gutter-R |
| 57 | 632 | 614 | 3.4 | gutter-L |
| 58 | 114 | 624 | 13.5 | 1/2-13 bolt into coupler |
| 59 | 134 | 624 | 9.6 | 3/8 dowel |
| 60 | 154 | 624 | 13.5 | 1/2-13 bolt into coupler |
| 61 | 564 | 624 | 13.5 | 1/2-13 bolt into coupler |
| 62 | 584 | 624 | 9.6 | 3/8 dowel |
| 63 | 604 | 624 | 13.5 | 1/2-13 bolt into coupler |
| 64 | 69 | 634 | 5.5 | M5 insert screw |
| 65 | 649 | 634 | 5.5 | M5 insert screw |
| 66 | 269 | 664 | 5.5 | M5 insert screw |
| 67 | 449 | 664 | 5.5 | M5 insert screw |
| 68 | 21 | 674 | 4.5 | floor bracket |
| 69 | 87 | 674 | 3.4 | gutter-R |
| 70 | 632 | 674 | 3.4 | gutter-L |
| 71 | 697 | 674 | 4.5 | floor bracket |
| 72 | 134 | 679 | 4.5 | socket plug |
| 73 | 584 | 679 | 4.5 | socket plug |
| 74 | 336 | 705 | 6.5 | M6 insert screw |
| 75 | 382 | 705 | 6.5 | M6 insert screw |
| 76 | 336 | 718 | 6.5 | M6 insert screw |
| 77 | 382 | 718 | 6.5 | M6 insert screw |
| 78 | 87 | 734 | 3.4 | gutter-R |
| 79 | 343 | 737 | 3.2 | motor-relief |
| 80 | 632 | 734 | 3.4 | gutter-L |
| 81 | 64 | 772 | 3.4 | corner-R |
| 82 | 375 | 770 | 3.2 | motor-relief |
| 83 | 654 | 772 | 3.4 | corner-L |
| 84 | 209 | 774 | 5.5 | M5 insert screw |
| 85 | 509 | 774 | 5.5 | M5 insert screw |
| 86 | 209 | 822 | 4.5 | floor bracket |
| 87 | 509 | 822 | 4.5 | floor bracket |

### Base front wall

![Base front wall](boards/base-front-wall.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 39 | 55 | 4.5 | corner-L |
| 2 | 599 | 55 | 4.5 | corner-R |
| 3 | 33 | 124 | 4.5 | corner bracket |
| 4 | 54 | 124 | 4.5 | leg holder |
| 5 | 584 | 124 | 4.5 | leg holder |
| 6 | 605 | 124 | 4.5 | corner bracket |

### Base rear wall

![Base rear wall](boards/base-rear-wall.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 26 | 56 | 4.5 | corner-R |
| 2 | 612 | 56 | 4.5 | corner-L |
| 3 | 33 | 124 | 4.5 | corner bracket |
| 4 | 54 | 124 | 4.5 | leg holder |
| 5 | 584 | 124 | 4.5 | leg holder |
| 6 | 605 | 124 | 4.5 | corner bracket |

### Base side wall, left

![Base side wall, left](boards/base-side-wall-left.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 7 | 35 | 4.5 | corner-L |
| 2 | 707 | 54 | 4.5 | corner-L |
| 3 | 14 | 124 | 4.5 | corner bracket |
| 4 | 35 | 124 | 4.5 | leg holder |
| 5 | 100 | 123 | 4.5 | saddle |
| 6 | 210 | 123 | 4.5 | saddle |
| 7 | 280 | 123 | 4.5 | saddle |
| 8 | 419 | 124 | 4.5 | corner bracket |
| 9 | 438 | 123 | 4.5 | saddle |
| 10 | 570 | 123 | 4.5 | saddle |
| 11 | 690 | 124 | 4.5 | leg holder |
| 12 | 711 | 124 | 4.5 | corner bracket |

### Base side wall, right

![Base side wall, right](boards/base-side-wall-right.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 718 | 35 | 4.5 | corner-R |
| 2 | 18 | 56 | 4.5 | corner-R |
| 3 | 14 | 124 | 4.5 | corner bracket |
| 4 | 35 | 124 | 4.5 | leg holder |
| 5 | 155 | 123 | 4.5 | saddle |
| 6 | 287 | 123 | 4.5 | saddle |
| 7 | 306 | 124 | 4.5 | corner bracket |
| 8 | 445 | 123 | 4.5 | saddle |
| 9 | 515 | 123 | 4.5 | saddle |
| 10 | 625 | 123 | 4.5 | saddle |
| 11 | 690 | 124 | 4.5 | leg holder |
| 12 | 711 | 124 | 4.5 | corner bracket |

### Base partition

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

### Base bridge y=-190

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

### Base bridge y=-58

![Base bridge y=-58](boards/base-bridge-y-58.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 635 | 11 | 4.5 | saddle |
| 2 | 489 | 12 | 4.5 | core post |
| 3 | 161 | 12 | 4.5 | core post |
| 4 | 16 | 11 | 4.5 | saddle |

### Base bridge y=100

![Base bridge y=100](boards/base-bridge-y-100.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 635 | 11 | 4.5 | saddle |
| 2 | 565 | 12 | 4.5 | core post |
| 3 | 489 | 12 | 4.5 | core post |
| 4 | 161 | 12 | 4.5 | core post |
| 5 | 85 | 12 | 4.5 | core post |
| 6 | 16 | 11 | 4.5 | saddle |

### Base bridge y=170

![Base bridge y=170](boards/base-bridge-y-170.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 635 | 11 | 4.5 | saddle |
| 2 | 600 | 12 | 4.5 | core post |
| 3 | 325 | 12 | 4.5 | core post |
| 4 | 51 | 12 | 4.5 | core post |
| 5 | 16 | 11 | 4.5 | saddle |

### Base bridge y=280

![Base bridge y=280](boards/base-bridge-y-280.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 635 | 11 | 4.5 | saddle |
| 2 | 600 | 12 | 4.5 | core post |
| 3 | 480 | 12 | 4.5 | core post |
| 4 | 170 | 12 | 4.5 | core post |
| 5 | 51 | 12 | 4.5 | core post |
| 6 | 16 | 11 | 4.5 | saddle |

### Base leg bridge y=-310

![Base leg bridge y=-310](boards/base-leg-bridge-y-310.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 474 | 11 | 4.5 | leg holder |
| 2 | 426 | 12 | 4.5 | core post |
| 3 | 54 | 12 | 4.5 | core post |
| 4 | 6 | 11 | 4.5 | leg holder |

### Base leg bridge y=344

![Base leg bridge y=344](boards/base-leg-bridge-y-344.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 474 | 11 | 4.5 | leg holder |
| 2 | 385 | 12 | 4.5 | core post |
| 3 | 95 | 12 | 4.5 | core post |
| 4 | 6 | 11 | 4.5 | leg holder |

## Uprights: hole maps

### Upright floor (x2)

![Upright floor](boards/upright-floor.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 77 | 56 | 4.5 | toe-filler |
| 2 | 119 | 75 | 4.5 | toe-filler |
| 3 | 131 | 136 | 3.2 | foot-gasket-groove |
| 4 | 99 | 146 | 16.3 | 5/8 core rod |
| 5 | 21 | 167 | 4.5 | floor bracket |
| 6 | 177 | 167 | 4.5 | floor bracket |
| 7 | 67 | 197 | 3.2 | foot-gasket-groove |
| 8 | 99 | 246 | 16.3 | 5/8 core rod |
| 9 | 67 | 266 | 3.2 | foot-gasket-groove |
| 10 | 131 | 266 | 3.2 | foot-gasket-groove |
| 11 | 67 | 336 | 3.2 | foot-gasket-groove |
| 12 | 131 | 336 | 3.2 | foot-gasket-groove |
| 13 | 99 | 371 | 63.5 | hole saw |
| 14 | 131 | 414 | 3.2 | foot-gasket-groove |
| 15 | 79 | 426 | 16.3 | 5/8 core rod |
| 16 | 99 | 426 | 13.1 | 1/2-13 bolt, base dowel hole |
| 17 | 119 | 426 | 16.3 | 5/8 core rod |
| 18 | 21 | 437 | 4.5 | floor bracket |
| 19 | 177 | 437 | 4.5 | floor bracket |
| 20 | 67 | 461 | 3.2 | foot-gasket-groove |
| 21 | 99 | 481 | 63.5 | hole saw |
| 22 | 99 | 554 | 4.5 | floor bracket |

### Upright side plate, outer (x2)

![Upright side plate, outer](boards/upright-side-plate-outer.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 79 | 34 | 4.5 | corner bracket |
| 2 | 280 | 240 | 4.5 | corner bracket |
| 3 | 406 | 259 | 4.5 | saddle |
| 4 | 473 | 260 | 4.5 | corner bracket |

Outline corners (x, y): (0, 0), (495, 0), (495, 271), (264, 271)

### Upright side plate, inner (x2)

![Upright side plate, inner](boards/upright-side-plate-inner.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 416 | 34 | 4.5 | corner bracket |
| 2 | 215 | 240 | 4.5 | corner bracket |
| 3 | 22 | 260 | 4.5 | corner bracket |
| 4 | 90 | 259 | 4.5 | saddle |

Outline corners (x, y): (495, 0), (0, 0), (0, 271), (231, 271)

### Upright back board (x2)

![Upright back board](boards/upright-back-board.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 3 | 260 | 4.5 | corner bracket |
| 2 | 77 | 260 | 4.5 | corner bracket |

### Upright front board (x2)

![Upright front board](boards/upright-front-board.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 32 | 66 | 4.5 | slope-pocket--60 |
| 2 | 32 | 209 | 4.5 | slope-pocket-40 |
| 3 | 14 | 301 | 4.5 | corner bracket |
| 4 | 66 | 301 | 4.5 | corner bracket |

### Upright bridge (x2)

![Upright bridge](boards/upright-bridge.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 87 | 10 | 10 | 3/8-16 bolt into the top plate |
| 2 | 85 | 34 | 16.3 | 5/8 core rod |
| 3 | 45 | 34 | 16.3 | 5/8 core rod |
| 4 | 43 | 100 | 10 | 3/8-16 bolt into the top plate |

## Beam: hole maps

### Beam floor

![Beam floor](boards/beam-floor.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 174 | 21 | 4.5 | floor bracket |
| 2 | 474 | 21 | 4.5 | floor bracket |
| 3 | 174 | 79 | 5.5 | M5 insert screw |
| 4 | 294 | 79 | 5.5 | M5 insert screw |
| 5 | 354 | 79 | 5.5 | M5 insert screw |
| 6 | 474 | 79 | 5.5 | M5 insert screw |
| 7 | 94 | 106 | 6.5 | M6 insert screw |
| 8 | 107 | 106 | 6.5 | M6 insert screw |
| 9 | 452 | 106 | 6.5 | M6 insert screw |
| 10 | 21 | 129 | 4.5 | floor bracket |
| 11 | 627 | 129 | 4.5 | floor bracket |
| 12 | 94 | 152 | 6.5 | M6 insert screw |
| 13 | 107 | 152 | 6.5 | M6 insert screw |
| 14 | 452 | 152 | 6.5 | M6 insert screw |
| 15 | 174 | 179 | 5.5 | M5 insert screw |
| 16 | 294 | 179 | 5.5 | M5 insert screw |
| 17 | 354 | 179 | 5.5 | M5 insert screw |
| 18 | 474 | 179 | 5.5 | M5 insert screw |
| 19 | 174 | 237 | 4.5 | floor bracket |
| 20 | 474 | 237 | 4.5 | floor bracket |

### Beam top wall

![Beam top wall](boards/beam-top-wall.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 37 | 25 | 13.1 | 1/2 core rod |
| 2 | 81 | 25 | 13.1 | 1/2 core rod |
| 3 | 487 | 25 | 13.1 | 1/2 core rod |
| 4 | 531 | 25 | 13.1 | 1/2 core rod |
| 5 | 37 | 115 | 13.1 | 1/2 core rod |
| 6 | 81 | 115 | 13.1 | 1/2 core rod |
| 7 | 487 | 115 | 13.1 | 1/2 core rod |
| 8 | 531 | 115 | 13.1 | 1/2 core rod |
| 9 | 84 | 133 | 4.5 | back-edge-1 |
| 10 | 219 | 133 | 4.5 | back-edge-1 |
| 11 | 351 | 133 | 4.5 | back-edge-1 |
| 12 | 484 | 133 | 4.5 | back-edge-1 |
| 13 | 33 | 154 | 4.5 | corner bracket |
| 14 | 535 | 154 | 4.5 | corner bracket |

### Beam bottom wall

![Beam bottom wall](boards/beam-bottom-wall.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 37 | 25 | 13.1 | 1/2 core rod |
| 2 | 81 | 25 | 13.1 | 1/2 core rod |
| 3 | 487 | 25 | 13.1 | 1/2 core rod |
| 4 | 531 | 25 | 13.1 | 1/2 core rod |
| 5 | 59 | 70 | 9.6 | 3/8 dowel |
| 6 | 509 | 70 | 9.6 | 3/8 dowel |
| 7 | 37 | 115 | 13.1 | 1/2 core rod |
| 8 | 81 | 115 | 13.1 | 1/2 core rod |
| 9 | 487 | 115 | 13.1 | 1/2 core rod |
| 10 | 531 | 115 | 13.1 | 1/2 core rod |
| 11 | 33 | 154 | 4.5 | corner bracket |
| 12 | 535 | 154 | 4.5 | corner bracket |

### Beam end wall, left

![Beam end wall, left](boards/beam-end-wall-left.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 70 | 44 | 4.5 | tube locator |
| 2 | 70 | 96 | 4.5 | tube locator |
| 3 | 14 | 154 | 4.5 | corner bracket |
| 4 | 126 | 154 | 4.5 | corner bracket |

### Beam end wall, right

![Beam end wall, right](boards/beam-end-wall-right.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 70 | 44 | 4.5 | tube locator |
| 2 | 70 | 96 | 4.5 | tube locator |
| 3 | 14 | 154 | 4.5 | corner bracket |
| 4 | 126 | 154 | 4.5 | corner bracket |

## Putting the moulds together

### Base: both halves on one floor

The rear half is cast first, against a partition at the split. Then the partition comes out and the
front half is cast against the rear half's waxed split face, on the same floor. The two top faces come out
flush, the split faces match, and the front tubes slide straight onto the rear half's spigots.

1. Drill the floor, walls, partition and bridges. Wax and PVA every face that the mix touches.
2. Stand the floor on two or three battens (the insert screws and floor bolts come up from underneath).
3. Stand the walls on the floor. Fit the four corner brackets at the top corners, then the floor brackets
   along every wall foot. Square the box with a tape across the diagonals before tightening.
4. Fit the partition between the side walls with its two brackets on the front side, and the two struts
   from the front wall to its foot. Push the gasket-groove beads onto its pins; push the spigot bushings
   into its hole-saw holes from the front.
5. Bolt the rear-half pieces on: the gutter formers and the motor relief to the floor, the corner fillers
   to the floor and walls, the socket plugs to the floor (each with its liner over it), the inserts and
   the tie-rod couplers on their greased screws and bolts, the base dowels in their holes.
6. Hold the draw-rod couplers on greased 1/2-13 bolts through the partition. Slide the spigots through
   the bushings and put the rear tubes on them, with their sleeves and end plugs.
7. Bolt the leg holders into the rear corners, drop the legs through them and put a sleeve on each leg.
8. Cast the 20 mm skin, set the cores on it (sand in them), drop the bridges into the saddles and bolt each
   core's post to its bridge. Fill to the line.
9. After the cure: unbolt the bridges, partition and struts, leave the rest. Pull the gasket-groove beads,
   cover the groove with packing tape, and wax and PVA the rear half's split face and the spigots.
10. Front half the same way: formers, trough, corner fillers, couplers and inserts; front tubes onto the
    spigots; draw rods screwed into the rear half's couplers with their ends in the corner fillers; legs;
    skin, cores, bridges, fill.
11. After the cure, unbolt everything and split the halves (a few wedges at the split, gently).

![Front-half mould against the cured rear half](../../renders/build/04-mould-base-front.png)

### Uprights (two moulds, cast together)

1. Drill the boards; wax and PVA. Push the post bushings into the floor from below.
2. Stand each side plate on the floor with its floor brackets, the back board between them with its
   floor bracket, and the two back brackets at the top.
3. Bolt the toe filler to the floor between the side plates, set the front board on it and fit the
   front brackets: two at its top, two at its foot (those only bolt to the side plates).
4. Pin the gasket-groove bead to the floor. Set the mould on its four printed feet.
5. Posts up through the bushings onto the bench; greased 5/8 in rods up through the floor: the two
   short ones into the slope plugs (bolted to the front board), the two long ones on through the top.
   The dowel-hole bolt with its nut from underneath.
6. Fill to the line and vibrate. Then slide the top pocket plugs down the long rods, set the top plate
   (greased 3/8 bolts through the bridge and the spacers into it), drop the bridge into its saddles.

![Upright mould, front: toe filler, slope plug, front brackets](../../renders/mould/upright-front.png)

### Beam

1. Drill the boards; wax and PVA. Walls on the floor with the floor brackets, corner brackets at the top.
2. Screw the support pads and riser inserts to the floor on greased screws. Push the dowels into the
   bottom wall onto their printed stops.
3. Bolt the tube locators through the end walls (M4 x 70 into the nut in each square end) and hang the
   tubes between them. Bolt the back-edge fillers to the top wall.
4. Greased 1/2 in rods through the top and bottom walls for the eight bolt holes. Fill to the line.
5. The locators leave a 16 mm hole in each beam end; plug it with a dark printed cap or leave it.
