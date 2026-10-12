# Mold guide

How to make the molds for the five castings. Each mold also has its own shorter guide in this folder
(base, uprights, beam), and its own printable drilling templates in `templates/`.

![The base mold (rear half), pulled apart](../../renders/mold/exploded-base.png)

![An upright mold, pulled apart](../../renders/mold/exploded-upright.png)

![The beam mold, pulled apart](../../renders/mold/exploded-beam.png)

**In short:** melamine boards bolt together with printed brackets. Every printed piece bolts or pins to
its board from outside. The walls stand 25 mm above the pour line, so no bolt goes through a face the
mix touches. Nothing is glued, and it all comes apart for the next casting.

**Order of work:** print &rarr; cut the boards &rarr; mark them with the templates and drill &rarr; cut the foam &rarr; wax &rarr; assemble &rarr; pour &rarr; take apart.

## 1. How it works

- **Walls** stand on the floor against bolted-down **cleats**; **corner brackets** square the tops. All the
  bolts go through the top 25 mm, above the pour line.

![A corner of the base mold](../../renders/mold/detail-corner.png)

- **Printed pieces** have a nut built in: it goes into a pocket on the board side and slides under the
  hole; an M4 bolt comes through the board from outside.

![The captive nut](../../renders/mold/fixing-nut.png)

- **Thin pieces** (gasket-groove beads, motor relief) have 3 mm pins that push into 1/8 in holes.

![Pins on a gasket-groove bead](../../renders/mold/fixing-pins.png)

- **Long pieces** are printed in parts that peg together; each part bolts down on its own.

![Peg and socket](../../renders/mold/fixing-peg.png)

- **Cores** are taped foam blocks with a printed post that bolts to a bridge across the mold.

![A foam core on its bridge](../../renders/mold/detail-core.png)

- **Fits** are 0.15 mm a side, and drawn for 19.05 mm board (Home Depot's 3/4 in melamine is a true
  0.750 in). Measure yours; if it differs, set `mold_board` in `model/build_cnc.py` and re-run it.

## 2. What you need

| Material | Amount | Notes |
|---|---|---|
| Melamine board, 3/4 in | 2 sheets, 4 x 8 ft | layout in section 4 |
| XPS foam board, 2 in | 1 sheet, 2 x 8 ft | the cores |
| PETG | 1.03 kg | sliced; everything printed for the machine fits in two 1 kg rolls |
| Packing tape, double-sided carpet tape | 1 roll each | wrapping and holding the foam |
| Paste wax and PVA | 1 each | release |
| 3/8 in quarter-round PVC molding | about 6 m | the rounded outside edges |
| 2x4 offcut | 4 blocks per upright mold, about 50 mm | feet |

| Hardware | Qty |
|---|---|
| M3 nut | 20 |
| M3 washer | 20 |
| M3 x 25 bolt | 20 |
| M4 nut | 172 |
| M4 washer | 168 |
| M4 x 20 bolt (leg pinch screw) | 4 |
| M4 x 30 bolt | 96 |
| M4 x 35 bolt | 32 |
| M4 x 45 bolt | 40 |
| M5 x 20 screw, greased (holds an insert) | 11 |
| M5 x 30 screw, greased (holds a rail bar) | 10 |
| M5 x 40 screw, greased (holds the face plate) | 8 |
| M6 x 30 screw, greased (holds a support pad) | 6 |
| M6 x 40 screw, greased (holds the face plate) | 6 |
| 1/2 in plain steel rod, greased (forms a beam bolt hole), 198 mm | 8 |
| 1/2 in rod (or a tie rod), greased, 355 mm: centers a top tie-rod sleeve | 4 |
| 1/2-13 x 1-1/2 in bolt + nut, greased (forms a dowel hole) | 4 |
| 3/8-16 x 3 in bolt, greased (holds the top plate, both layers) | 4 |
| 5/8 in plain steel rod, greased (forms a draw-rod hole), 803 mm | 2 |
| 5/8 in plain steel rod, greased (forms a slope tie-rod hole), cut to 89 mm | 2 |
| 5/8 in plain steel rod, greased (forms a tie-rod hole through the base), 169 mm | 4 |

Add about 10 % spare small bolts, nuts and washers. **Tools:** drill and brad-point bits (sizes in section 5), a 2-1/2 in hole saw, a jigsaw for the side plates' slope, a square, clamps, a 7 mm nut driver, a 3 mm hex key, an awl, a fine saw or hot wire for the foam.

## 3. Print

118 prints, 1.03 kg, about 86 hours (sliced; settings in the print guide). Print one corner bracket and one saddle first
and check them on a board offcut. Press or slide the nuts in before the pieces go on the boards.

![The printed mold kit](../../renders/mold/gallery-kit.png)

![Formers, fillers and plugs](../../renders/mold/gallery-pieces.png)

| File | Qty | g | Time each |
|---|---|---|---|
| `base-box/kit-corner-bracket.stl` | 4 | 33 | 39m 23s |
| `base-box/kit-partition-bracket.stl` | 2 | 14 | 35m 28s |
| `base-box/kit-saddle.stl` | 6 | 58 | 46m 3s |
| `base-box/kit-leg-holder.stl` | 4 | 82 | 1h 37m 0s |
| `base-rear/former-gutter-L-part1of3.stl` | 1 | 8 | 35m 5s |
| `base-rear/former-gutter-L-part2of3.stl` | 1 | 8 | 33m 40s |
| `base-rear/former-gutter-L-part3of3.stl` | 1 | 7 | 31m 15s |
| `base-rear/former-gutter-R-part1of3.stl` | 1 | 8 | 35m 6s |
| `base-rear/former-gutter-R-part2of3.stl` | 1 | 8 | 33m 40s |
| `base-rear/former-gutter-R-part3of3.stl` | 1 | 7 | 31m 15s |
| `base-rear/former-motor-relief.stl` | 1 | 12 | 40m 58s |
| `base-rear/filler-corner-L.stl` | 1 | 17 | 1h 44m 24s |
| `base-rear/filler-corner-R.stl` | 1 | 16 | 1h 42m 27s |
| `base-front/former-gutter-L-part1of2.stl` | 1 | 11 | 49m 23s |
| `base-front/former-gutter-L-part2of2.stl` | 1 | 10 | 43m 43s |
| `base-front/former-gutter-R-part1of2.stl` | 1 | 11 | 49m 24s |
| `base-front/former-gutter-R-part2of2.stl` | 1 | 10 | 43m 43s |
| `base-front/former-trough-part1of5.stl` | 1 | 20 | 1h 14m 18s |
| `base-front/former-trough-part2of5.stl` | 1 | 22 | 1h 23m 56s |
| `base-front/former-trough-part3of5.stl` | 1 | 25 | 1h 33m 33s |
| `base-front/former-trough-part4of5.stl` | 1 | 23 | 1h 24m 3s |
| `base-front/former-trough-part5of5.stl` | 1 | 21 | 1h 17m 36s |
| `base-front/filler-corner-L.stl` | 1 | 16 | 1h 43m 48s |
| `base-front/filler-corner-R.stl` | 1 | 17 | 1h 40m 33s |
| `base-rear/former-split-gasket-groove-part1of4.stl` | 1 | 2 | 9m 50s |
| `base-rear/former-split-gasket-groove-part2of4.stl` | 1 | 1 | 8m 58s |
| `base-rear/former-split-gasket-groove-part3of4.stl` | 1 | 1 | 8m 58s |
| `base-rear/former-split-gasket-groove-part4of4.stl` | 1 | 2 | 9m 53s |
| `base-front/core-center-a-post.stl` | 1 | 5 | 44m 56s |
| `base-front/core-center-b-post.stl` | 1 | 5 | 44m 56s |
| `base-rear/core-center-post.stl` | 1 | 5 | 44m 56s |
| `base-front/core-outboard-L-post.stl` | 1 | 5 | 44m 53s |
| `base-front/core-trough-band-L-post.stl` | 1 | 5 | 44m 54s |
| `base-front/core-draw-rod-L-post.stl` | 1 | 5 | 44m 53s |
| `base-front/core-foot-a-L-post.stl` | 1 | 5 | 44m 54s |
| `base-rear/core-foot-b-L-post.stl` | 1 | 5 | 44m 53s |
| `base-rear/core-knee-L-post.stl` | 1 | 5 | 44m 53s |
| `base-rear/core-outer-a-L-post.stl` | 1 | 5 | 44m 53s |
| `base-rear/core-outer-b-L-post.stl` | 1 | 5 | 44m 53s |
| `base-rear/core-rear-L-post.stl` | 1 | 5 | 44m 53s |
| `base-front/core-outboard-R-post.stl` | 1 | 5 | 44m 53s |
| `base-front/core-trough-band-R-post.stl` | 1 | 5 | 44m 54s |
| `base-front/core-draw-rod-R-post.stl` | 1 | 5 | 44m 53s |
| `base-front/core-foot-a-R-post.stl` | 1 | 5 | 44m 54s |
| `base-rear/core-foot-b-R-post.stl` | 1 | 5 | 44m 53s |
| `base-rear/core-knee-R-post.stl` | 1 | 5 | 44m 53s |
| `base-rear/core-outer-a-R-post.stl` | 1 | 5 | 44m 53s |
| `base-rear/core-outer-b-R-post.stl` | 1 | 5 | 44m 53s |
| `base-rear/core-rear-R-post.stl` | 1 | 5 | 44m 53s |
| `base-front/plug-draw-pocket-L.stl` | 1 | 12 | 59m 24s |
| `base-front/plug-draw-pocket-R.stl` | 1 | 12 | 59m 24s |
| `base-rear/plug-draw-pocket-L.stl` | 1 | 5 | 25m 9s |
| `base-rear/plug-draw-pocket-R.stl` | 1 | 5 | 25m 8s |
| `upright/kit-back-bracket.stl` | 4 | 21 | 27m 33s |
| `upright/kit-front-bracket.stl` | 4 | 32 | 38m 26s |
| `upright/kit-saddle-flat.stl` | 4 | 18 | 22m 40s |
| `upright/filler-toe-filler.stl` | 2 | 51 | 1h 30m 59s |
| `upright/former-foot-gasket-groove-part1of4.stl` | 2 | 6 | 16m 25s |
| `upright/former-foot-gasket-groove-part2of4.stl` | 2 | 2 | 8m 22s |
| `upright/former-foot-gasket-groove-part3of4.stl` | 2 | 2 | 8m 22s |
| `upright/former-foot-gasket-groove-part4of4.stl` | 2 | 6 | 16m 30s |
| `upright/plug-toe-plug.stl` | 2 | 26 | 1h 3m 42s |
| `upright/kit-plate-spacer.stl` | 4 | 15 | 20m 9s |
| `beam/kit-corner-bracket.stl` | 4 | 33 | 40m 3s |
| `beam/filler-back-edge-part1of3.stl` | 1 | 17 | 1h 8m 21s |
| `beam/filler-back-edge-part2of3.stl` | 1 | 18 | 1h 9m 13s |
| `beam/filler-back-edge-part3of3.stl` | 1 | 17 | 1h 8m 22s |
| `beam/kit-dowel-stop.stl` | 2 | 1 | 4m 19s |
| `tools/kit-pour-gauge.stl` | 2 | 9 | 24m 33s |
| `tools/kit-screed-shoe.stl` | 2 | 20 | 44m 42s |
| `base-front/cast-in-leg-front-l-plug.stl` | 2 | 8 | 24m 14s |
| `base-rear/cast-in-leg-rear-l-plug.stl` | 2 | 8 | 24m 14s |
| `upright/cast-in-column-ring-l1a.stl` | 8 | 109 | 49m 49s |

## 4. Cut the boards

Have the store rip the strips; crosscut at home. Write each board's name on its outside face, and mark
the cast face (the melamine face the mix touches).

![Sheet 1](boards/sheet-1.svg)

![Sheet 2](boards/sheet-2.svg)

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
| Base bridge y=-230 | 1 | 651 x 60 |  |
| Base bridge y=-130 | 1 | 651 x 60 |  |
| Base bridge y=-60 | 1 | 651 x 60 |  |
| Base bridge y=100 | 1 | 651 x 60 |  |
| Base bridge y=170 | 1 | 651 x 60 |  |
| Base bridge y=280 | 1 | 651 x 60 |  |
| Base leg bridge y=-310 | 1 | 480 x 60 |  |
| Base leg bridge y=344 | 1 | 480 x 60 |  |
| Upright floor | 2 | 198 x 541 |  |
| Upright side plate, outer | 2 | 461 x 271 (profile) | cut to the profile |
| Upright side plate, inner | 2 | 461 x 271 (profile) | cut to the profile |
| Upright back board | 2 | 80 x 271 |  |
| Upright front board | 2 | 80 x 292 | ends cut square |
| Upright bridge | 2 | 131 x 138 |  |
| Upright cleat, outer | 2 | 371 x 40 | offcut strip, flat on the floor |
| Upright cleat, inner | 2 | 371 x 40 | offcut strip, flat on the floor |
| Upright cleat, back | 2 | 80 x 40 | offcut strip, flat on the floor |
| Beam floor | 1 | 648 x 258 |  |
| Beam top wall | 1 | 568 x 165 |  |
| Beam bottom wall | 1 | 568 x 165 |  |
| Beam end wall, left | 1 | 140 x 165 |  |
| Beam end wall, right | 1 | 140 x 165 |  |
| Beam cleat, top | 1 | 568 x 40 | offcut strip, flat on the floor |
| Beam cleat, bottom | 1 | 568 x 40 | offcut strip, flat on the floor |
| Beam cleat, left | 1 | 140 x 40 | offcut strip, flat on the floor |
| Beam cleat, right | 1 | 140 x 40 | offcut strip, flat on the floor |

## 5. Mark and drill

1. Print the drilling templates (`templates/base-templates.pdf`, `templates/upright-templates.pdf`, `templates/beam-templates.pdf`) at **actual size** and check the 100 mm square.
2. Tape each board's pages onto it: printed edges on the board's edges, grid lines lined up.
3. Awl through every crosshair. Pencil the dashed **pour line** on the walls.
4. Drill from the marked face, at the size the color legend gives. Pilot the big ones; the 63.5 mm
   holes are a 2-1/2 in hole saw.

The appendix has every board as a drawing and a table, if you would rather measure.

| Hole | Drill | For |
|---|---|---|
| 3.2 mm | 1/8 in | draw-pocket-L, draw-pocket-R, foot-gasket-groove, motor-relief, split-gasket-groove |
| 3.4 mm | 9/64 in | corner-L, corner-R, gutter-L, gutter-R |
| 4.5 mm | 11/64 in | back-edge, cleat, core post, corner bracket, corner-L, corner-R, gutter-L, gutter-R, leg holder, saddle, toe-filler, toe-plug, trough |
| 5.5 mm | 7/32 in | M5 insert screw, M5 screw into a rail bar, M5 screw into the face plate |
| 6.5 mm | 17/64 in | M6 screw into a pad, M6 screw into the face plate |
| 9.6 mm | 25/64 in | 3/8 dowel, 3/8 dowel pin |
| 10 mm | 25/64 in | 3/8-16 bolt into the top plate |
| 13.1 mm | 33/64 in | 1/2 core rod, 1/2-13 bolt, base dowel hole |
| 13.5 mm | 17/32 in | 1/2 rod through a sleeve |
| 16.3 mm | 41/64 in | 5/8 core rod |

## 6. Cut the foam

Fine saw, hot wire or a long knife. Stack and glue two layers of 2 in foam for the 90 mm cores. Wrap
each piece smooth in packing tape. Cut a snug 12 mm square hole 30 mm deep for each core's post and
glue the post in.

| Casting | Piece | Qty | Size and how |
|---|---|---|---|
| base-front | center-a | 1 | XPS block 100 x 73 x 90 mm, outline as the pocket (chamfered corners); taped, with its printed post glued in. |
| base-front | center-b | 1 | XPS block 100 x 72 x 90 mm, outline as the pocket (chamfered corners); taped, with its printed post glued in. |
| base-rear | center | 1 | XPS block 100 x 190 x 90 mm, outline as the pocket (chamfered corners); taped, with its printed post glued in. |
| base-front | outboard-L | 1 | XPS block 130 x 194 x 90 mm, outline as the pocket (chamfered corners); taped, with its printed post glued in. |
| base-front | trough-band-L | 1 | XPS block 101 x 55 x 40 mm, outline as the pocket (chamfered corners); taped, with its printed post glued in. |
| base-front | draw-rod-L | 1 | XPS block 20 x 255 x 40 mm, outline as the pocket (chamfered corners); taped, with its printed post glued in. |
| base-front | foot-a-L | 1 | XPS block 45 x 36 x 90 mm, outline as the pocket (chamfered corners); taped, with its printed post glued in. |
| base-rear | foot-b-L | 1 | XPS block 45 x 99 x 90 mm, outline as the pocket (chamfered corners); taped, with its printed post glued in. |
| base-rear | knee-L | 1 | XPS block 50 x 140 x 40 mm, outline as the pocket (chamfered corners); taped, with its printed post glued in. |
| base-rear | outer-a-L | 1 | XPS block 20 x 44 x 65 mm, outline as the pocket (chamfered corners); taped, with its printed post glued in. |
| base-rear | outer-b-L | 1 | XPS block 20 x 60 x 65 mm, outline as the pocket (chamfered corners); taped, with its printed post glued in. |
| base-rear | rear-L | 1 | XPS block 85 x 52 x 90 mm, outline as the pocket (chamfered corners); taped, with its printed post glued in. |
| base-front | outboard-R | 1 | XPS block 130 x 194 x 90 mm, outline as the pocket (chamfered corners); taped, with its printed post glued in. |
| base-front | trough-band-R | 1 | XPS block 101 x 55 x 40 mm, outline as the pocket (chamfered corners); taped, with its printed post glued in. |
| base-front | draw-rod-R | 1 | XPS block 20 x 255 x 40 mm, outline as the pocket (chamfered corners); taped, with its printed post glued in. |
| base-front | foot-a-R | 1 | XPS block 45 x 36 x 90 mm, outline as the pocket (chamfered corners); taped, with its printed post glued in. |
| base-rear | foot-b-R | 1 | XPS block 45 x 99 x 90 mm, outline as the pocket (chamfered corners); taped, with its printed post glued in. |
| base-rear | knee-R | 1 | XPS block 50 x 140 x 40 mm, outline as the pocket (chamfered corners); taped, with its printed post glued in. |
| base-rear | outer-a-R | 1 | XPS block 20 x 44 x 65 mm, outline as the pocket (chamfered corners); taped, with its printed post glued in. |
| base-rear | outer-b-R | 1 | XPS block 20 x 60 x 65 mm, outline as the pocket (chamfered corners); taped, with its printed post glued in. |
| base-rear | rear-R | 1 | XPS block 85 x 52 x 90 mm, outline as the pocket (chamfered corners); taped, with its printed post glued in. |
## 7. Wax

- 3-5 coats of paste wax on every face the mix touches, boards and removable printed pieces, then PVA.
  Don't wax pieces that stay in (core posts, cast-in parts): scuff and degrease them.
- Glue quarter-round into the floor-to-wall corners that make outside edges; silicone fillets elsewhere.
- Grease every screw, bolt and rod that comes out of the casting.

## 8. Assemble

### Base, rear half (first)

Cast upside down, top face on the floor; shown the right way up. New parts in color. Slot each half's steel grid together first (the plates only fit one way), then it goes in as one piece.

![The base grids, both halves](../../renders/mold/skeleton-base.png)

1. Floor on three battens. Bolt the cleats down.

![Base rear, step 1](../../renders/mold/step-base-rear-1.png)

2. Walls against the cleats; corner brackets at the top. Diagonals equal within 2 mm, then tighten.

![Base rear, step 2](../../renders/mold/step-base-rear-2.png)

3. Partition between the side walls: two brackets, two struts to the front wall. Beads on its pins.

![Base rear, step 3](../../renders/mold/step-base-rear-3.png)

4. Gutter formers, motor relief, corner fillers and the draw-rod pocket plugs on.

![Base rear, step 4](../../renders/mold/step-base-rear-4.png)

5. The steel grid in, upside down: its rail bars and the BK pad screwed to the floor (greased M5 and M6), its seats over the dowels; the split end plates against the partition, dowel pins through it. Greased 5/8 in rods up through the floor for the tie-rod holes, and through the partition, the end plates and the pocket plugs for the draw rods. Inserts; leg holders, legs pushed up to their leg plates, pinch screws tight.

![Base rear, step 5](../../renders/mold/step-base-rear-5.png)

6. Pour the 20 mm skin. Foam cores on it between the grid plates, bridges into the saddles, each post bolted to its bridge. Fill to the pour line.

![Base rear, step 6](../../renders/mold/step-base-rear-6.png)

### Base, front half (against the rear half)

1. After the cure: bridges, partition and struts off. Pull the beads, tape the groove, and wax the rear half's split face, end plates and dowel pins.

![Base front, step 1](../../renders/mold/step-base-front-1.png)

2. Trough and gutter formers, corner fillers and pocket plugs on; the front grid in, its rail bars and BF pad screwed down and its split end plates onto the dowel pins; rods; inserts and legs.

![Base front, step 2](../../renders/mold/step-base-front-2.png)

3. Skin, cores, bridges, fill. After the cure, pull the rods, take it apart and split the halves with wedges.

![Base front, step 3](../../renders/mold/step-base-front-3.png)

### Uprights (two molds)

Cast foot down. Build two of everything. The skeleton: foot plate, two columns, the brace slotted into the foot plate, the top plate slotted onto the brace.

![An upright skeleton](../../renders/mold/skeleton-upright.png)

1. Gasket bead pinned on; cleats bolted down.

![Upright, step 1](../../renders/mold/step-upright-1.png)

2. Side plates against their cleats, back board between them, two back brackets.

![Upright, step 2](../../renders/mold/step-upright-2.png)

3. Toe filler bolted down, the front board's foot in its lip, two front brackets at the top.

![Upright, step 3](../../renders/mold/step-upright-3.png)

4. Mold on its four 2x4 blocks. The skeleton in: foot plate on the floor, greased 1/2 in rods up through the floor, the foot plate and the columns; the brace in its slot; the toe pocket plug on the foot plate; the two dowel-hole bolts from underneath. Columns on a bed of thickened epoxy, the top plate and bridge set on them while it goes off, then lifted away.

![Upright, step 4](../../renders/mold/step-upright-4.png)

5. Fill to the line. Top plate (both layers) back down over the rods and the brace tab, hung from the bridge; bridge onto its saddles.

![Upright, step 5](../../renders/mold/step-upright-5.png)

![The toe filler holds the front board's foot](../../renders/mold/detail-toe.png)

### Beam

Cast front (rail) face down, back open. Slot the steel box together on the bench: diaphragms into the face plate, the back plate over them, the end plates on the tabs.

![The beam's steel box](../../renders/mold/skeleton-beam.png)

1. Cleats bolted down.

![Beam, step 1](../../renders/mold/step-beam-1.png)

2. Walls against the cleats; four corner brackets.

![Beam, step 2](../../renders/mold/step-beam-2.png)

3. The steel box in, face plate down, greased M5 and M6 screws up through the floor into its tapped holes; greased 1/2 in rods through the top wall, the cap plates, the box, the seat plates and the bottom wall; back-edge filler on the top wall between the uprights; dowels on their stops. Fill to the line through the back plate's windows.

![Beam, step 3](../../renders/mold/step-beam-3.png)

## 9. Pour

- Fill to the **pour line**, 25 mm below the wall tops (pencilled from the templates, or with the
  printed pour-line gauge clipped over a wall).
- Vibrate each layer until it stops bubbling; check the brackets halfway through.
- Strike the top off with a straight board in the two printed **screed shoes**: they hang it from the wall
  tops with its bottom edge on the pour line.

![Pour-line gauge and screed shoes](../../renders/mold/detail-pour.png)

## 10. Take apart

1. After the full cure: bridges and saddles off, then corner brackets, then cleats; pull the walls off.
2. Screws, bolts and rods out from outside; lift the casting off the floor.
3. Unbolt and pull the formers and fillers.
4. Scrape and re-wax the boards; keep each mold's kit in a box. The kit is reused.

## 11. If something doesn't fit

| Problem | Fix |
|---|---|
| Nut won't slide under the hole | Clean the pocket with a nut on a bolt; warm the nut |
| Bracket or saddle loose on the board | Board thinner than set: tape shim, or set `mold_board` and reprint |
| Pin won't go in | Run the 1/8 in bit through again; trim the pin tip |
| Foam core moves | Tighten its post bolt; carpet tape under it |
| Printed part won't go on or into a steel tube | File the weld seam; sand the part. Several tight: caliper the tube, put its sizes in `frame_tube` / `post_tube`, re-run and reprint |
| Printed part loose on a tube | A wrap of tape round the part |
| Leak at a corner | Silicone fillet inside before waxing; check the brackets and diagonals |
| Former stuck after curing | Bolts out first, then a dowel and a light tap |

## Appendix: hole maps

Every board as seen from the face you mark: x from the left edge, y from the bottom edge (for a wall, the
edge on the floor). The templates carry the same holes at full size.

### Base

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
| 24 | 269 | 184 | 5.5 | M5 screw into a rail bar |
| 25 | 449 | 184 | 5.5 | M5 screw into a rail bar |
| 26 | 69 | 209 | 5.5 | M5 insert screw |
| 27 | 336 | 210 | 6.5 | M6 screw into a pad |
| 28 | 382 | 210 | 6.5 | M6 screw into a pad |
| 29 | 649 | 209 | 5.5 | M5 insert screw |
| 30 | 87 | 223 | 4.5 | gutter-R |
| 31 | 632 | 223 | 4.5 | gutter-L |
| 32 | 87 | 295 | 3.4 | gutter-R |
| 33 | 632 | 295 | 3.4 | gutter-L |
| 34 | 269 | 304 | 5.5 | M5 screw into a rail bar |
| 35 | 449 | 304 | 5.5 | M5 screw into a rail bar |
| 36 | 20 | 314 | 4.5 | cleat |
| 37 | 698 | 314 | 4.5 | cleat |
| 38 | 134 | 349 | 16.3 | 5/8 core rod |
| 39 | 584 | 349 | 16.3 | 5/8 core rod |
| 40 | 87 | 368 | 3.4 | gutter-R |
| 41 | 632 | 368 | 3.4 | gutter-L |
| 42 | 69 | 421 | 5.5 | M5 insert screw |
| 43 | 649 | 421 | 5.5 | M5 insert screw |
| 44 | 269 | 424 | 5.5 | M5 screw into a rail bar |
| 45 | 449 | 424 | 5.5 | M5 screw into a rail bar |
| 46 | 87 | 434 | 3.4 | gutter-R |
| 47 | 632 | 434 | 3.4 | gutter-L |
| 48 | 87 | 494 | 3.4 | gutter-R |
| 49 | 632 | 494 | 3.4 | gutter-L |
| 50 | 134 | 504 | 9.6 | 3/8 dowel |
| 51 | 584 | 504 | 9.6 | 3/8 dowel |
| 52 | 20 | 529 | 4.5 | cleat |
| 53 | 698 | 529 | 4.5 | cleat |
| 54 | 269 | 544 | 5.5 | M5 screw into a rail bar |
| 55 | 449 | 544 | 5.5 | M5 screw into a rail bar |
| 56 | 87 | 554 | 3.4 | gutter-R |
| 57 | 632 | 554 | 3.4 | gutter-L |
| 58 | 134 | 569 | 16.3 | 5/8 core rod |
| 59 | 584 | 569 | 16.3 | 5/8 core rod |
| 60 | 87 | 614 | 3.4 | gutter-R |
| 61 | 632 | 614 | 3.4 | gutter-L |
| 62 | 134 | 619 | 9.6 | 3/8 dowel |
| 63 | 584 | 619 | 9.6 | 3/8 dowel |
| 64 | 69 | 634 | 5.5 | M5 insert screw |
| 65 | 649 | 634 | 5.5 | M5 insert screw |
| 66 | 269 | 664 | 5.5 | M5 screw into a rail bar |
| 67 | 449 | 664 | 5.5 | M5 screw into a rail bar |
| 68 | 134 | 669 | 16.3 | 5/8 core rod |
| 69 | 584 | 669 | 16.3 | 5/8 core rod |
| 70 | 87 | 674 | 3.4 | gutter-R |
| 71 | 632 | 674 | 3.4 | gutter-L |
| 72 | 336 | 705 | 6.5 | M6 screw into a pad |
| 73 | 382 | 705 | 6.5 | M6 screw into a pad |
| 74 | 336 | 718 | 6.5 | M6 screw into a pad |
| 75 | 382 | 718 | 6.5 | M6 screw into a pad |
| 76 | 87 | 734 | 3.4 | gutter-R |
| 77 | 343 | 737 | 3.2 | motor-relief |
| 78 | 632 | 734 | 3.4 | gutter-L |
| 79 | 20 | 744 | 4.5 | cleat |
| 80 | 698 | 744 | 4.5 | cleat |
| 81 | 64 | 772 | 3.4 | corner-R |
| 82 | 375 | 770 | 3.2 | motor-relief |
| 83 | 654 | 772 | 3.4 | corner-L |
| 84 | 209 | 774 | 5.5 | M5 insert screw |
| 85 | 509 | 774 | 5.5 | M5 insert screw |
| 86 | 80 | 823 | 4.5 | cleat |
| 87 | 266 | 823 | 4.5 | cleat |
| 88 | 452 | 823 | 4.5 | cleat |
| 89 | 638 | 823 | 4.5 | cleat |

#### Base front wall

![Base front wall](boards/base-front-wall.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 247 | 45 | 3.2 | draw-pocket-L |
| 2 | 391 | 45 | 3.2 | draw-pocket-R |
| 3 | 26 | 56 | 4.5 | corner-L |
| 4 | 612 | 56 | 4.5 | corner-R |
| 5 | 252 | 64 | 3.2 | draw-pocket-L |
| 6 | 396 | 64 | 3.2 | draw-pocket-R |
| 7 | 33 | 124 | 4.5 | corner bracket |
| 8 | 605 | 124 | 4.5 | corner bracket |
| 9 | 54 | 129 | 4.5 | leg holder |
| 10 | 584 | 129 | 4.5 | leg holder |

#### Base rear wall

![Base rear wall](boards/base-rear-wall.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 247 | 41 | 3.2 | draw-pocket-R |
| 2 | 391 | 41 | 3.2 | draw-pocket-L |
| 3 | 26 | 56 | 4.5 | corner-R |
| 4 | 612 | 56 | 4.5 | corner-L |
| 5 | 247 | 65 | 3.2 | draw-pocket-R |
| 6 | 391 | 65 | 3.2 | draw-pocket-L |
| 7 | 33 | 124 | 4.5 | corner bracket |
| 8 | 605 | 124 | 4.5 | corner bracket |
| 9 | 54 | 129 | 4.5 | leg holder |
| 10 | 584 | 129 | 4.5 | leg holder |

#### Base side wall, left

![Base side wall, left](boards/base-side-wall-left.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 7 | 35 | 4.5 | corner-L |
| 2 | 718 | 46 | 4.5 | corner-L |
| 3 | 14 | 124 | 4.5 | corner bracket |
| 4 | 100 | 123 | 4.5 | saddle |
| 5 | 210 | 123 | 4.5 | saddle |
| 6 | 280 | 123 | 4.5 | saddle |
| 7 | 419 | 124 | 4.5 | corner bracket |
| 8 | 440 | 123 | 4.5 | saddle |
| 9 | 510 | 123 | 4.5 | saddle |
| 10 | 610 | 123 | 4.5 | saddle |
| 11 | 711 | 124 | 4.5 | corner bracket |
| 12 | 35 | 129 | 4.5 | leg holder |
| 13 | 690 | 129 | 4.5 | leg holder |

#### Base side wall, right

![Base side wall, right](boards/base-side-wall-right.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 7 | 35 | 4.5 | corner-R |
| 2 | 718 | 35 | 4.5 | corner-R |
| 3 | 14 | 124 | 4.5 | corner bracket |
| 4 | 115 | 123 | 4.5 | saddle |
| 5 | 215 | 123 | 4.5 | saddle |
| 6 | 285 | 123 | 4.5 | saddle |
| 7 | 306 | 124 | 4.5 | corner bracket |
| 8 | 445 | 123 | 4.5 | saddle |
| 9 | 515 | 123 | 4.5 | saddle |
| 10 | 625 | 123 | 4.5 | saddle |
| 11 | 711 | 124 | 4.5 | corner bracket |
| 12 | 35 | 129 | 4.5 | leg holder |
| 13 | 690 | 129 | 4.5 | leg holder |

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
| 9 | 176 | 40 | 9.6 | 3/8 dowel pin (split) |
| 10 | 424 | 40 | 9.6 | 3/8 dowel pin (split) |
| 11 | 228 | 55 | 16.3 | 5/8 core rod (draw rod) |
| 12 | 372 | 55 | 16.3 | 5/8 core rod (draw rod) |
| 13 | 176 | 85 | 9.6 | 3/8 dowel pin (split) |
| 14 | 424 | 85 | 9.6 | 3/8 dowel pin (split) |
| 15 | 20 | 124 | 4.5 | corner bracket |
| 16 | 580 | 124 | 4.5 | corner bracket |

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

#### Base bridge y=-230

![Base bridge y=-230](boards/base-bridge-y-230.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 635 | 11 | 4.5 | saddle |
| 2 | 325 | 12 | 4.5 | core post |
| 3 | 16 | 11 | 4.5 | saddle |

#### Base bridge y=-130

![Base bridge y=-130](boards/base-bridge-y-130.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 635 | 11 | 4.5 | saddle |
| 2 | 608 | 12 | 4.5 | core post |
| 3 | 520 | 12 | 4.5 | core post |
| 4 | 325 | 12 | 4.5 | core post |
| 5 | 130 | 12 | 4.5 | core post |
| 6 | 43 | 12 | 4.5 | core post |
| 7 | 16 | 11 | 4.5 | saddle |

#### Base bridge y=-60

![Base bridge y=-60](boards/base-bridge-y-60.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 635 | 11 | 4.5 | saddle |
| 2 | 478 | 12 | 4.5 | core post |
| 3 | 173 | 12 | 4.5 | core post |
| 4 | 16 | 11 | 4.5 | saddle |

#### Base bridge y=100

![Base bridge y=100](boards/base-bridge-y-100.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 635 | 11 | 4.5 | saddle |
| 2 | 478 | 12 | 4.5 | core post |
| 3 | 173 | 12 | 4.5 | core post |
| 4 | 16 | 11 | 4.5 | saddle |

#### Base bridge y=170

![Base bridge y=170](boards/base-bridge-y-170.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 635 | 11 | 4.5 | saddle |
| 2 | 608 | 12 | 4.5 | core post |
| 3 | 480 | 12 | 4.5 | core post |
| 4 | 325 | 12 | 4.5 | core post |
| 5 | 170 | 12 | 4.5 | core post |
| 6 | 43 | 12 | 4.5 | core post |
| 7 | 16 | 11 | 4.5 | saddle |

#### Base bridge y=280

![Base bridge y=280](boards/base-bridge-y-280.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 635 | 11 | 4.5 | saddle |
| 2 | 608 | 12 | 4.5 | core post |
| 3 | 43 | 12 | 4.5 | core post |
| 4 | 16 | 11 | 4.5 | saddle |

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
| 2 | 428 | 12 | 4.5 | core post |
| 3 | 52 | 12 | 4.5 | core post |
| 4 | 6 | 11 | 4.5 | leg holder |

### Uprights

#### Upright floor (x2)

![Upright floor](boards/upright-floor.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 77 | 54 | 4.5 | toe-filler |
| 2 | 119 | 72 | 4.5 | toe-filler |
| 3 | 99 | 117 | 16.3 | 5/8 core rod |
| 4 | 131 | 123 | 3.2 | foot-gasket-groove |
| 5 | 20 | 170 | 4.5 | cleat |
| 6 | 178 | 170 | 4.5 | cleat |
| 7 | 67 | 182 | 3.2 | foot-gasket-groove |
| 8 | 67 | 249 | 3.2 | foot-gasket-groove |
| 9 | 131 | 249 | 3.2 | foot-gasket-groove |
| 10 | 99 | 272 | 13.1 | 1/2-13 bolt, base dowel hole |
| 11 | 20 | 315 | 4.5 | cleat |
| 12 | 67 | 314 | 3.2 | foot-gasket-groove |
| 13 | 131 | 314 | 3.2 | foot-gasket-groove |
| 14 | 178 | 315 | 4.5 | cleat |
| 15 | 99 | 337 | 13.5 | 1/2 rod through a sleeve |
| 16 | 131 | 381 | 3.2 | foot-gasket-groove |
| 17 | 99 | 387 | 13.1 | 1/2-13 bolt, base dowel hole |
| 18 | 99 | 437 | 13.5 | 1/2 rod through a sleeve |
| 19 | 67 | 441 | 3.2 | foot-gasket-groove |
| 20 | 20 | 461 | 4.5 | cleat |
| 21 | 178 | 461 | 4.5 | cleat |
| 22 | 99 | 521 | 4.5 | cleat |

#### Upright side plate, outer (x2)

![Upright side plate, outer](boards/upright-side-plate-outer.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 246 | 241 | 4.5 | corner bracket |
| 2 | 356 | 259 | 4.5 | saddle |
| 3 | 438 | 260 | 4.5 | corner bracket |

Outline corners (x, y): (0, 0), (461, 0), (461, 271), (228, 271)

#### Upright side plate, inner (x2)

![Upright side plate, inner](boards/upright-side-plate-inner.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 215 | 241 | 4.5 | corner bracket |
| 2 | 22 | 260 | 4.5 | corner bracket |
| 3 | 105 | 259 | 4.5 | saddle |

Outline corners (x, y): (461, 0), (0, 0), (0, 271), (233, 271)

#### Upright back board (x2)

![Upright back board](boards/upright-back-board.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 3 | 260 | 4.5 | corner bracket |
| 2 | 77 | 260 | 4.5 | corner bracket |

#### Upright front board (x2)

![Upright front board](boards/upright-front-board.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 32 | 35 | 4.5 | toe-plug |
| 2 | 14 | 281 | 4.5 | corner bracket |
| 3 | 66 | 281 | 4.5 | corner bracket |

#### Upright bridge (x2)

![Upright bridge](boards/upright-bridge.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 65 | 10 | 13.5 | 1/2 rod through a sleeve |
| 2 | 87 | 40 | 10 | 3/8-16 bolt into the top plate |
| 3 | 65 | 110 | 13.5 | 1/2 rod through a sleeve |
| 4 | 43 | 130 | 10 | 3/8-16 bolt into the top plate |

#### Upright cleat, outer (x2)

![Upright cleat, outer](boards/upright-cleat-outer.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 331 | 20 | 4.5 | cleat |
| 2 | 185 | 20 | 4.5 | cleat |
| 3 | 40 | 20 | 4.5 | cleat |

#### Upright cleat, inner (x2)

![Upright cleat, inner](boards/upright-cleat-inner.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 331 | 20 | 4.5 | cleat |
| 2 | 185 | 20 | 4.5 | cleat |
| 3 | 40 | 20 | 4.5 | cleat |

#### Upright cleat, back (x2)

![Upright cleat, back](boards/upright-cleat-back.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 40 | 20 | 4.5 | cleat |

### Beam

#### Beam floor

![Beam floor](boards/beam-floor.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 80 | 20 | 4.5 | cleat |
| 2 | 324 | 20 | 4.5 | cleat |
| 3 | 568 | 20 | 4.5 | cleat |
| 4 | 174 | 79 | 5.5 | M5 screw into the face plate |
| 5 | 294 | 79 | 5.5 | M5 screw into the face plate |
| 6 | 354 | 79 | 5.5 | M5 screw into the face plate |
| 7 | 474 | 79 | 5.5 | M5 screw into the face plate |
| 8 | 20 | 99 | 4.5 | cleat |
| 9 | 628 | 99 | 4.5 | cleat |
| 10 | 94 | 106 | 6.5 | M6 screw into the face plate |
| 11 | 107 | 106 | 6.5 | M6 screw into the face plate |
| 12 | 452 | 106 | 6.5 | M6 screw into the face plate |
| 13 | 94 | 152 | 6.5 | M6 screw into the face plate |
| 14 | 107 | 152 | 6.5 | M6 screw into the face plate |
| 15 | 452 | 152 | 6.5 | M6 screw into the face plate |
| 16 | 20 | 159 | 4.5 | cleat |
| 17 | 628 | 159 | 4.5 | cleat |
| 18 | 174 | 179 | 5.5 | M5 screw into the face plate |
| 19 | 294 | 179 | 5.5 | M5 screw into the face plate |
| 20 | 354 | 179 | 5.5 | M5 screw into the face plate |
| 21 | 474 | 179 | 5.5 | M5 screw into the face plate |
| 22 | 80 | 238 | 4.5 | cleat |
| 23 | 324 | 238 | 4.5 | cleat |
| 24 | 568 | 238 | 4.5 | cleat |

#### Beam top wall

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
| 9 | 163 | 133 | 4.5 | back-edge |
| 10 | 285 | 133 | 4.5 | back-edge |
| 11 | 403 | 133 | 4.5 | back-edge |
| 12 | 33 | 154 | 4.5 | corner bracket |
| 13 | 535 | 154 | 4.5 | corner bracket |

#### Beam bottom wall

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

#### Beam end wall, left

![Beam end wall, left](boards/beam-end-wall-left.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 14 | 154 | 4.5 | corner bracket |
| 2 | 126 | 154 | 4.5 | corner bracket |

#### Beam end wall, right

![Beam end wall, right](boards/beam-end-wall-right.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 14 | 154 | 4.5 | corner bracket |
| 2 | 126 | 154 | 4.5 | corner bracket |

#### Beam cleat, top

![Beam cleat, top](boards/beam-cleat-top.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 528 | 20 | 4.5 | cleat |
| 2 | 284 | 20 | 4.5 | cleat |
| 3 | 40 | 20 | 4.5 | cleat |

#### Beam cleat, bottom

![Beam cleat, bottom](boards/beam-cleat-bottom.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 528 | 20 | 4.5 | cleat |
| 2 | 284 | 20 | 4.5 | cleat |
| 3 | 40 | 20 | 4.5 | cleat |

#### Beam cleat, left

![Beam cleat, left](boards/beam-cleat-left.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 100 | 20 | 4.5 | cleat |
| 2 | 40 | 20 | 4.5 | cleat |

#### Beam cleat, right

![Beam cleat, right](boards/beam-cleat-right.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 100 | 20 | 4.5 | cleat |
| 2 | 40 | 20 | 4.5 | cleat |
