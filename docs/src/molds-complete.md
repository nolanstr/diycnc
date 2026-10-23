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

- **Thin pieces** (gasket-groove beads) have 3 mm pins that push into 1/8 in holes.

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
| Melamine board, 3/4 in | 1 sheet, 4 x 8 ft | layout in section 4 |
| 1x2 lumber (furring strip is fine) | 3 x 8 ft 1x2 (5.0 m) | the cleats: they lie on the floor outside the walls |
| XPS foam board, 2 in | 1 sheet, 2 x 8 ft | the cores |
| PETG | 1.69 kg | sliced; everything printed for the machine fits in two 1 kg rolls |
| Packing tape, double-sided carpet tape | 1 roll each | wrapping and holding the foam |
| Paste wax and PVA | 1 each | release |
| 3/8 in quarter-round PVC molding | about 6 m | the rounded outside edges |
| 2x4 offcut | 4 blocks per upright mold, about 50 mm | feet |

| Hardware | Qty |
|---|---|
| M3 nut | 20 |
| M3 washer | 20 |
| M3 x 25 bolt | 20 |
| M4 nut | 157 |
| M4 washer | 153 |
| M4 x 20 bolt (leg pinch screw) | 4 |
| M4 x 30 bolt | 90 |
| M4 x 35 bolt | 30 |
| M4 x 45 bolt | 33 |
| M5 x 20 screw, greased (holds an insert) | 19 |
| M5 x 30 screw, greased (holds a rail bar or the BK pad) | 12 |
| M5 x 50 screw, greased (holds the face plate) | 8 |
| M6 x 30 screw, greased (holds a support pad) | 8 |
| M6 x 50 screw, greased (holds the face plate) | 6 |
| 1/2 in plain steel rod, greased (forms a beam bolt hole), 204 mm | 8 |
| 1/2-13 x 1-1/2 in bolt + nut, greased (forms a dowel hole) | 2 |
| 3/8-16 x 3 in bolt, greased (holds the top plate, both layers) | 2 |
| the two column tie rods themselves, greased: up through the floor and the columns into the top plate, to center the columns while the casting goes off | 2 |

Add about 10 % spare small bolts, nuts and washers. **Tools:** drill and brad-point bits (sizes in section 5), a 2-1/2 in hole saw, a jigsaw for the side plates' slope, a square, clamps, a 7 mm nut driver, a 3 mm hex key, an awl, a fine saw or hot wire for the foam.

## 3. Print

111 prints, 1.69 kg, about 111 hours (sliced; settings in the print guide). Print one corner bracket and one saddle first
and check them on a board offcut. Press or slide the nuts in before the pieces go on the boards.

![The printed mold kit](../../renders/mold/gallery-kit.png)

![Formers, fillers and plugs](../../renders/mold/gallery-pieces.png)

| File | Qty | g | Time each |
|---|---|---|---|
| `base-box/kit-corner-bracket.stl` | 4 | 33 | 39m 23s |
| `base-box/kit-partition-bracket.stl` | 2 | 14 | 35m 28s |
| `base-box/kit-saddle.stl` | 6 | 58 | 46m 3s |
| `base-box/kit-leg-holder.stl` | 4 | 166 | 2h 30m 55s |
| `base-rear/former-gutter-L-part1of3.stl` | 1 | 8 | 35m 6s |
| `base-rear/former-gutter-L-part2of3.stl` | 1 | 8 | 33m 40s |
| `base-rear/former-gutter-L-part3of3.stl` | 1 | 7 | 31m 15s |
| `base-rear/former-gutter-R-part1of3.stl` | 1 | 8 | 35m 6s |
| `base-rear/former-gutter-R-part2of3.stl` | 1 | 8 | 33m 40s |
| `base-rear/former-gutter-R-part3of3.stl` | 1 | 7 | 31m 15s |
| `base-rear/filler-corner-L.stl` | 1 | 29 | 2h 10m 27s |
| `base-rear/filler-bevel-L-part1of2.stl` | 1 | 50 | 2h 39m 10s |
| `base-rear/filler-bevel-L-part2of2.stl` | 1 | 50 | 2h 39m 44s |
| `base-rear/filler-corner-R.stl` | 1 | 29 | 2h 9m 35s |
| `base-rear/filler-bevel-R-part1of2.stl` | 1 | 50 | 2h 34m 47s |
| `base-rear/filler-bevel-R-part2of2.stl` | 1 | 50 | 2h 35m 51s |
| `base-rear/filler-bevel-end-part1of3.stl` | 1 | 50 | 2h 36m 44s |
| `base-rear/filler-bevel-end-part2of3.stl` | 1 | 50 | 2h 37m 10s |
| `base-rear/filler-bevel-end-part3of3.stl` | 1 | 50 | 2h 36m 53s |
| `base-front/former-gutter-L-part1of2.stl` | 1 | 11 | 49m 24s |
| `base-front/former-gutter-L-part2of2.stl` | 1 | 10 | 43m 44s |
| `base-front/former-gutter-R-part1of2.stl` | 1 | 11 | 49m 24s |
| `base-front/former-gutter-R-part2of2.stl` | 1 | 10 | 43m 43s |
| `base-front/former-trough-part1of5.stl` | 1 | 19 | 1h 12m 26s |
| `base-front/former-trough-part2of5.stl` | 1 | 22 | 1h 21m 44s |
| `base-front/former-trough-part3of5.stl` | 1 | 24 | 1h 31m 38s |
| `base-front/former-trough-part4of5.stl` | 1 | 22 | 1h 21m 55s |
| `base-front/former-trough-part5of5.stl` | 1 | 20 | 1h 11m 51s |
| `base-front/filler-corner-L.stl` | 1 | 29 | 2h 10m 58s |
| `base-front/filler-bevel-L-part1of2.stl` | 1 | 46 | 2h 25m 12s |
| `base-front/filler-bevel-L-part2of2.stl` | 1 | 46 | 2h 25m 19s |
| `base-front/filler-corner-R.stl` | 1 | 29 | 2h 8m 15s |
| `base-front/filler-bevel-R-part1of2.stl` | 1 | 46 | 2h 21m 6s |
| `base-front/filler-bevel-R-part2of2.stl` | 1 | 46 | 2h 21m 45s |
| `base-front/filler-bevel-end-part1of3.stl` | 1 | 50 | 2h 32m 21s |
| `base-front/filler-bevel-end-part2of3.stl` | 1 | 50 | 2h 33m 43s |
| `base-front/filler-bevel-end-part3of3.stl` | 1 | 50 | 2h 33m 32s |
| `base-rear/former-split-gasket-groove-part1of4.stl` | 1 | 2 | 9m 41s |
| `base-rear/former-split-gasket-groove-part2of4.stl` | 1 | 1 | 8m 49s |
| `base-rear/former-split-gasket-groove-part3of4.stl` | 1 | 1 | 8m 49s |
| `base-rear/former-split-gasket-groove-part4of4.stl` | 1 | 2 | 9m 42s |
| `base-front/core-center-a-post.stl` | 1 | 5 | 44m 56s |
| `base-front/core-center-b-post.stl` | 1 | 5 | 44m 56s |
| `base-rear/core-center-post.stl` | 1 | 5 | 44m 56s |
| `base-front/core-outboard-L-post.stl` | 1 | 5 | 44m 53s |
| `base-rear/core-foot-b-L-post.stl` | 1 | 5 | 44m 53s |
| `base-rear/core-knee-L-post.stl` | 1 | 5 | 44m 53s |
| `base-front/core-outboard-R-post.stl` | 1 | 5 | 44m 53s |
| `base-rear/core-foot-b-R-post.stl` | 1 | 5 | 44m 53s |
| `base-rear/core-knee-R-post.stl` | 1 | 5 | 44m 53s |
| `base-front/plug-draw-pocket-L.stl` | 1 | 12 | 46m 16s |
| `base-front/plug-draw-pocket-R.stl` | 1 | 12 | 46m 16s |
| `base-rear/plug-draw-pocket-L.stl` | 1 | 5 | 21m 23s |
| `base-rear/plug-draw-pocket-R.stl` | 1 | 5 | 21m 23s |
| `upright/kit-back-bracket.stl` | 4 | 21 | 27m 31s |
| `upright/kit-front-bracket.stl` | 4 | 32 | 38m 26s |
| `upright/kit-saddle-flat.stl` | 4 | 18 | 22m 40s |
| `upright/filler-toe-filler.stl` | 1 | 26 | 1h 30m 59s |
| `upright/former-foot-gasket-groove-part1of4.stl` | 1 | 3 | 17m 31s |
| `upright/former-foot-gasket-groove-part2of4.stl` | 1 | 1 | 8m 54s |
| `upright/former-foot-gasket-groove-part3of4.stl` | 1 | 1 | 8m 54s |
| `upright/former-foot-gasket-groove-part4of4.stl` | 1 | 3 | 17m 27s |
| `upright/plug-toe-plug.stl` | 1 | 13 | 1h 3m 42s |
| `upright/kit-plate-spacer.stl` | 2 | 8 | 20m 9s |
| `beam/kit-corner-bracket.stl` | 4 | 33 | 40m 3s |
| `beam/filler-back-edge-part1of3.stl` | 1 | 17 | 1h 5m 47s |
| `beam/filler-back-edge-part2of3.stl` | 1 | 17 | 1h 6m 9s |
| `beam/filler-back-edge-part3of3.stl` | 1 | 17 | 1h 5m 50s |
| `beam/kit-dowel-stop.stl` | 2 | 1 | 4m 19s |
| `tools/kit-pour-gauge.stl` | 2 | 9 | 24m 33s |
| `tools/kit-screed-shoe.stl` | 2 | 20 | 44m 42s |
| `base-front/cast-in-leg-front-l-plug.stl` | 2 | 8 | 24m 14s |
| `base-rear/cast-in-leg-rear-l-plug.stl` | 2 | 8 | 24m 14s |
| `upright/cast-in-column-ring-l1a.stl` | 8 | 93 | 44m 23s |

## 4. Cut the boards

Have the store rip the strips; crosscut at home. Write each board's name on its outside face, and mark
the cast face (the melamine face the mix touches). The cleats are cut from 1x2 lumber, not the sheet;
the bridges and struts come out of the sheet's offcuts.

![Sheet 1](boards/sheet-1.svg)

| Board | Qty | Size (mm) | Notes |
|---|---|---|---|
| Base floor | 1 | 700 x 843 | both halves are cast on it |
| Base front wall | 1 | 620 x 135 |  |
| Base rear wall | 1 | 620 x 135 |  |
| Base side wall, left | 1 | 724 x 135 |  |
| Base side wall, right | 1 | 724 x 135 |  |
| Base partition | 1 | 582 x 135 | rear half only; comes out before the front half |
| Base partition strut | 2 | 326 x 60 | offcut, stands on edge; holds the partition foot (rear half only) |
| Base cleat, front | 1 | 620 x 38 | 1x2 lumber; flat on the floor |
| Base cleat, rear | 1 | 620 x 38 | 1x2 lumber; flat on the floor |
| Base cleat, left | 1 | 724 x 38 | 1x2 lumber; flat on the floor |
| Base cleat, right | 1 | 724 x 38 | 1x2 lumber; flat on the floor |
| Base bridge y=-230 | 1 | 633 x 60 |  |
| Base bridge y=-130 | 1 | 633 x 60 |  |
| Base bridge y=-60 | 1 | 633 x 60 |  |
| Base bridge y=100 | 1 | 633 x 60 |  |
| Base bridge y=170 | 1 | 633 x 60 |  |
| Base bridge y=280 | 1 | 633 x 60 |  |
| Base leg bridge y=-280 | 1 | 402 x 60 |  |
| Base leg bridge y=318 | 1 | 402 x 60 |  |
| Upright floor | 1 | 198 x 581 |  |
| Upright side plate, outer | 1 | 501 x 271 (profile) | cut to the profile |
| Upright side plate, inner | 1 | 501 x 271 (profile) | cut to the profile |
| Upright back board | 1 | 80 x 272 | ends cut square |
| Upright front board | 1 | 80 x 292 | ends cut square |
| Upright bridge | 1 | 131 x 138 |  |
| Upright cleat, outer | 1 | 411 x 38 | 1x2 lumber; flat on the floor |
| Upright cleat, inner | 1 | 411 x 38 | 1x2 lumber; flat on the floor |
| Upright cleat, back | 1 | 80 x 38 | 1x2 lumber; flat on the floor |
| Beam floor | 1 | 630 x 264 |  |
| Beam top wall | 1 | 550 x 165 |  |
| Beam bottom wall | 1 | 550 x 165 |  |
| Beam end wall, left | 1 | 146 x 165 |  |
| Beam end wall, right | 1 | 146 x 165 |  |
| Beam cleat, top | 1 | 550 x 38 | 1x2 lumber; flat on the floor |
| Beam cleat, bottom | 1 | 550 x 38 | 1x2 lumber; flat on the floor |
| Beam cleat, left | 1 | 146 x 38 | 1x2 lumber; flat on the floor |
| Beam cleat, right | 1 | 146 x 38 | 1x2 lumber; flat on the floor |

## 5. Mark and drill

1. Print the drilling templates (`templates/base-templates.pdf`, `templates/upright-templates.pdf`, `templates/beam-templates.pdf`) at **actual size** and check the 100 mm square.
2. Tape each board's pages onto it: printed edges on the board's edges, grid lines lined up.
3. Awl through every crosshair. Pencil the dashed **pour line** on the walls.
4. Drill from the marked face, at the size the color legend gives. Pilot the big ones; the 63.5 mm
   holes are a 2-1/2 in hole saw.

The appendix has every board as a drawing and a table, if you would rather measure.

| Hole | Drill | For |
|---|---|---|
| 3.2 mm | 1/8 in | foot-gasket-groove, split-gasket-groove |
| 3.4 mm | 9/64 in | corner-L, corner-R, gutter-L, gutter-R |
| 4.5 mm | 11/64 in | back-edge, bevel-L, bevel-R, bevel-end, cleat, core post, corner bracket, corner-L, corner-R, draw-pocket-L, draw-pocket-R, gutter-L, gutter-R, leg holder, saddle, toe-filler, toe-plug, trough |
| 5.5 mm | 7/32 in | M5 insert screw, M5 screw into the face plate, M5 screw into the steel |
| 6.5 mm | 17/64 in | M6 screw into a pad, M6 screw into the face plate |
| 9.6 mm | 25/64 in | 3/8 dowel, 3/8 dowel pin |
| 10 mm | 25/64 in | 3/8-16 bolt into the top plate |
| 13.1 mm | 33/64 in | 1/2 core rod, 1/2-13 bolt, base dowel hole |
| 13.5 mm | 17/32 in | column tie rod, from below |

## 6. Cut the foam

Fine saw, hot wire or a long knife. Stack and glue two layers of 2 in foam for the 90 mm cores. Wrap
each piece smooth in packing tape. Cut a snug 12 mm square hole 30 mm deep for each core's post and
glue the post in.

| Casting | Piece | Qty | Size and how |
|---|---|---|---|
| base-front | center-a | 1 | XPS block 100 x 73 x 90 mm, outline as the pocket (chamfered corners); taped, with its printed post glued in. |
| base-front | center-b | 1 | XPS block 100 x 72 x 90 mm, outline as the pocket (chamfered corners); taped, with its printed post glued in. |
| base-rear | center | 1 | XPS block 88 x 190 x 90 mm, outline as the pocket (chamfered corners); taped, with its printed post glued in. |
| base-front | outboard-L | 1 | XPS block 93 x 148 x 90 mm, outline as the pocket (chamfered corners); taped, with its printed post glued in. |
| base-rear | foot-b-L | 1 | XPS block 30 x 99 x 90 mm, outline as the pocket (chamfered corners); taped, with its printed post glued in. |
| base-rear | knee-L | 1 | XPS block 41 x 140 x 40 mm, outline as the pocket (chamfered corners); taped, with its printed post glued in. |
| base-front | outboard-R | 1 | XPS block 93 x 148 x 90 mm, outline as the pocket (chamfered corners); taped, with its printed post glued in. |
| base-rear | foot-b-R | 1 | XPS block 30 x 99 x 90 mm, outline as the pocket (chamfered corners); taped, with its printed post glued in. |
| base-rear | knee-R | 1 | XPS block 41 x 140 x 40 mm, outline as the pocket (chamfered corners); taped, with its printed post glued in. |
## 7. Wax

- 3-5 coats of paste wax on every face the mix touches, boards and removable printed pieces, then PVA.
  Don't wax pieces that stay in (core posts, cast-in parts): scuff and degrease them.
- Glue quarter-round into the floor-to-wall corners that make outside edges; silicone fillets elsewhere.
- Grease every screw, bolt and rod that comes out of the casting.

## 8. Assemble

### Base, rear half (first)

Cast upside down, top face on the floor; shown the right way up. New parts in color. Bolt each half's steel grid together first (the build guide, section 1), then it goes in as one piece.

![The base grids, both halves](../../renders/mold/skeleton-base.png)

1. Floor on three battens. Bolt the cleats down.

![Base rear, step 1](../../renders/mold/step-base-rear-1.png)

2. Walls against the cleats; corner brackets at the top. Diagonals equal within 2 mm, then tighten.

![Base rear, step 2](../../renders/mold/step-base-rear-2.png)

3. Partition between the side walls: two brackets, two struts to the front wall. Beads on its pins.

![Base rear, step 3](../../renders/mold/step-base-rear-3.png)

4. Gutter formers, corner fillers and the draw-rod pocket plugs on. Bevel strips on the side and rear walls, their 1-1/2 in face flush with the pour line.

![Base rear, step 4](../../renders/mold/step-base-rear-4.png)

5. The steel grid in, bolted up and upside down: its rail bars and the BK pad screwed to the floor (greased M5 and M6), its seats over the dowels, the split end plates against the partition with their dowel pins through it. Tape over the holes in the pedestals' bottom bars. Inserts; leg holders, legs set to height, pinch screws tight.

![Base rear, step 5](../../renders/mold/step-base-rear-5.png)

6. Pour the 20 mm skin. Foam cores on it between the steel, bridges into the saddles, each post bolted to its bridge. Fill to the pour line, packing the mix up under the bevel strips.

![Base rear, step 6](../../renders/mold/step-base-rear-6.png)

### Base, front half (against the rear half)

1. After the cure: bridges, partition and struts off. Pull the beads, tape the groove, and wax the rear half's split face, end plates and dowel pins.

![Base front, step 1](../../renders/mold/step-base-front-1.png)

2. Trough and gutter formers, corner fillers, bevel strips and pocket plugs on; the front grid in, its rail bars and BF pad screwed down and its split end plates onto the dowel pins; inserts and legs.

![Base front, step 2](../../renders/mold/step-base-front-2.png)

3. Skin, cores, bridges, fill (packed under the bevel strips). After the cure, take it apart and split the halves with wedges.

![Base front, step 3](../../renders/mold/step-base-front-3.png)

### Uprights (one mold, cast twice)

Cast foot down. The two uprights are the same part: cast one, take the mold apart after the cure, scrape and re-wax it and cast the other. The skeleton: the foot bar, two columns and the top plate (two flat bars), clamped later by the column tie rods.

![An upright skeleton](../../renders/mold/skeleton-upright.png)

1. Gasket bead pinned on; cleats bolted down.

![Upright, step 1](../../renders/mold/step-upright-1.png)

2. Side plates against their cleats, back board between them (it leans in, like the front board), two back brackets.

![Upright, step 2](../../renders/mold/step-upright-2.png)

3. Toe filler bolted down, the front board's foot in its lip, two front brackets at the top.

![Upright, step 3](../../renders/mold/step-upright-3.png)

4. Mold on its four 2x4 blocks. The foot bar on the floor; the two columns on beds of thickened epoxy on it, the top plate and bridge set on them while it goes off, then lifted away; the toe pocket plug on the foot bar; the two dowel-hole bolts from underneath.

![Upright, step 4](../../renders/mold/step-upright-4.png)

5. Fill to the line. Top plate (both bars) back on, hung from the bridge; bridge onto its saddles. Then the two column tie rods, greased, up from under the floor through the foot bar and the columns into the top plate: they center the columns while it cures.

![Upright, step 5](../../renders/mold/step-upright-5.png)

![The toe filler holds the front board's foot](../../renders/mold/detail-toe.png)

### Beam

Cast front (rail) face down, back open. Bolt the steel together on the bench: the three studs into the face bar, a pipe spacer on each, the back bar over them and a nut on each.

![The beam's steel box](../../renders/mold/skeleton-beam.png)

1. Cleats bolted down.

![Beam, step 1](../../renders/mold/step-beam-1.png)

2. Walls against the cleats; four corner brackets.

![Beam, step 2](../../renders/mold/step-beam-2.png)

3. The steel in, face bar down: greased M5 and M6 screws up through the floor into its tapped holes; the back bar on its pipe spacers and studs; greased 1/2 in rods through the top wall, the cap bars, the seat bars and the bottom wall; back-edge filler on the top wall between the uprights; dowels on their stops. Fill to the line.

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
| 1 | 80 | 21 | 4.5 | cleat |
| 2 | 260 | 21 | 4.5 | cleat |
| 3 | 440 | 21 | 4.5 | cleat |
| 4 | 620 | 21 | 4.5 | cleat |
| 5 | 71 | 64 | 3.4 | corner-R |
| 6 | 630 | 64 | 3.4 | corner-L |
| 7 | 150 | 69 | 5.5 | M5 insert screw |
| 8 | 350 | 69 | 5.5 | M5 insert screw |
| 9 | 550 | 69 | 5.5 | M5 insert screw |
| 10 | 269 | 89 | 4.5 | trough |
| 11 | 378 | 89 | 4.5 | trough |
| 12 | 486 | 89 | 4.5 | trough |
| 13 | 595 | 89 | 4.5 | trough |
| 14 | 133 | 97 | 4.5 | trough |
| 15 | 21 | 99 | 4.5 | cleat |
| 16 | 680 | 99 | 4.5 | cleat |
| 17 | 214 | 104 | 4.5 | trough |
| 18 | 323 | 104 | 4.5 | trough |
| 19 | 431 | 104 | 4.5 | trough |
| 20 | 540 | 104 | 4.5 | trough |
| 21 | 222 | 135 | 5.5 | M5 insert screw |
| 22 | 478 | 135 | 5.5 | M5 insert screw |
| 23 | 87 | 150 | 4.5 | gutter-R |
| 24 | 614 | 150 | 4.5 | gutter-L |
| 25 | 260 | 184 | 5.5 | M5 screw into the steel |
| 26 | 440 | 184 | 5.5 | M5 screw into the steel |
| 27 | 69 | 209 | 5.5 | M5 insert screw |
| 28 | 327 | 210 | 6.5 | M6 screw into a pad |
| 29 | 373 | 210 | 6.5 | M6 screw into a pad |
| 30 | 631 | 209 | 5.5 | M5 insert screw |
| 31 | 87 | 223 | 4.5 | gutter-R |
| 32 | 614 | 223 | 4.5 | gutter-L |
| 33 | 87 | 295 | 3.4 | gutter-R |
| 34 | 614 | 295 | 3.4 | gutter-L |
| 35 | 260 | 304 | 5.5 | M5 screw into the steel |
| 36 | 440 | 304 | 5.5 | M5 screw into the steel |
| 37 | 21 | 314 | 4.5 | cleat |
| 38 | 680 | 314 | 4.5 | cleat |
| 39 | 87 | 368 | 3.4 | gutter-R |
| 40 | 614 | 368 | 3.4 | gutter-L |
| 41 | 69 | 421 | 5.5 | M5 insert screw |
| 42 | 631 | 421 | 5.5 | M5 insert screw |
| 43 | 260 | 424 | 5.5 | M5 screw into the steel |
| 44 | 440 | 424 | 5.5 | M5 screw into the steel |
| 45 | 87 | 434 | 3.4 | gutter-R |
| 46 | 199 | 433 | 5.5 | M5 insert screw |
| 47 | 614 | 434 | 3.4 | gutter-L |
| 48 | 199 | 455 | 5.5 | M5 insert screw |
| 49 | 87 | 494 | 3.4 | gutter-R |
| 50 | 614 | 494 | 3.4 | gutter-L |
| 51 | 134 | 504 | 9.6 | 3/8 dowel |
| 52 | 566 | 504 | 9.6 | 3/8 dowel |
| 53 | 21 | 529 | 4.5 | cleat |
| 54 | 680 | 529 | 4.5 | cleat |
| 55 | 260 | 544 | 5.5 | M5 screw into the steel |
| 56 | 440 | 544 | 5.5 | M5 screw into the steel |
| 57 | 87 | 554 | 3.4 | gutter-R |
| 58 | 614 | 554 | 3.4 | gutter-L |
| 59 | 87 | 614 | 3.4 | gutter-R |
| 60 | 614 | 614 | 3.4 | gutter-L |
| 61 | 134 | 619 | 9.6 | 3/8 dowel |
| 62 | 566 | 619 | 9.6 | 3/8 dowel |
| 63 | 69 | 634 | 5.5 | M5 insert screw |
| 64 | 631 | 634 | 5.5 | M5 insert screw |
| 65 | 260 | 664 | 5.5 | M5 screw into the steel |
| 66 | 440 | 664 | 5.5 | M5 screw into the steel |
| 67 | 87 | 674 | 3.4 | gutter-R |
| 68 | 614 | 674 | 3.4 | gutter-L |
| 69 | 327 | 705 | 6.5 | M6 screw into a pad |
| 70 | 373 | 705 | 6.5 | M6 screw into a pad |
| 71 | 311 | 712 | 5.5 | M5 screw into the steel |
| 72 | 389 | 712 | 5.5 | M5 screw into the steel |
| 73 | 327 | 718 | 6.5 | M6 screw into a pad |
| 74 | 373 | 718 | 6.5 | M6 screw into a pad |
| 75 | 87 | 734 | 3.4 | gutter-R |
| 76 | 614 | 734 | 3.4 | gutter-L |
| 77 | 21 | 744 | 4.5 | cleat |
| 78 | 213 | 743 | 5.5 | M5 insert screw |
| 79 | 487 | 743 | 5.5 | M5 insert screw |
| 80 | 680 | 744 | 4.5 | cleat |
| 81 | 327 | 748 | 6.5 | M6 screw into a pad |
| 82 | 373 | 748 | 6.5 | M6 screw into a pad |
| 83 | 64 | 772 | 3.4 | corner-R |
| 84 | 637 | 772 | 3.4 | corner-L |
| 85 | 200 | 774 | 5.5 | M5 insert screw |
| 86 | 500 | 774 | 5.5 | M5 insert screw |
| 87 | 80 | 822 | 4.5 | cleat |
| 88 | 260 | 822 | 4.5 | cleat |
| 89 | 440 | 822 | 4.5 | cleat |
| 90 | 620 | 822 | 4.5 | cleat |

#### Base front wall

![Base front wall](boards/base-front-wall.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 220 | 39 | 4.5 | draw-pocket-L |
| 2 | 400 | 39 | 4.5 | draw-pocket-R |
| 3 | 34 | 57 | 4.5 | corner-L |
| 4 | 586 | 57 | 4.5 | corner-R |
| 5 | 146 | 78 | 4.5 | bevel-end |
| 6 | 310 | 78 | 4.5 | bevel-end |
| 7 | 474 | 78 | 4.5 | bevel-end |
| 8 | 33 | 124 | 4.5 | corner bracket |
| 9 | 588 | 124 | 4.5 | corner bracket |
| 10 | 84 | 129 | 4.5 | leg holder |
| 11 | 536 | 129 | 4.5 | leg holder |

#### Base rear wall

![Base rear wall](boards/base-rear-wall.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 220 | 39 | 4.5 | draw-pocket-R |
| 2 | 400 | 39 | 4.5 | draw-pocket-L |
| 3 | 34 | 57 | 4.5 | corner-R |
| 4 | 586 | 57 | 4.5 | corner-L |
| 5 | 146 | 78 | 4.5 | bevel-end |
| 6 | 310 | 78 | 4.5 | bevel-end |
| 7 | 474 | 78 | 4.5 | bevel-end |
| 8 | 33 | 124 | 4.5 | corner bracket |
| 9 | 588 | 124 | 4.5 | corner bracket |
| 10 | 84 | 129 | 4.5 | leg holder |
| 11 | 536 | 129 | 4.5 | leg holder |

#### Base side wall, left

![Base side wall, left](boards/base-side-wall-left.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 15 | 57 | 4.5 | corner-L |
| 2 | 709 | 57 | 4.5 | corner-L |
| 3 | 129 | 78 | 4.5 | bevel-L |
| 4 | 296 | 78 | 4.5 | bevel-L |
| 5 | 454 | 78 | 4.5 | bevel-L |
| 6 | 604 | 78 | 4.5 | bevel-L |
| 7 | 14 | 124 | 4.5 | corner bracket |
| 8 | 100 | 123 | 4.5 | saddle |
| 9 | 210 | 123 | 4.5 | saddle |
| 10 | 280 | 123 | 4.5 | saddle |
| 11 | 419 | 124 | 4.5 | corner bracket |
| 12 | 440 | 123 | 4.5 | saddle |
| 13 | 510 | 123 | 4.5 | saddle |
| 14 | 610 | 123 | 4.5 | saddle |
| 15 | 711 | 124 | 4.5 | corner bracket |
| 16 | 62 | 129 | 4.5 | leg holder |
| 17 | 660 | 129 | 4.5 | leg holder |

#### Base side wall, right

![Base side wall, right](boards/base-side-wall-right.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 15 | 57 | 4.5 | corner-R |
| 2 | 709 | 57 | 4.5 | corner-R |
| 3 | 120 | 78 | 4.5 | bevel-R |
| 4 | 270 | 78 | 4.5 | bevel-R |
| 5 | 429 | 78 | 4.5 | bevel-R |
| 6 | 596 | 78 | 4.5 | bevel-R |
| 7 | 14 | 124 | 4.5 | corner bracket |
| 8 | 115 | 123 | 4.5 | saddle |
| 9 | 215 | 123 | 4.5 | saddle |
| 10 | 285 | 123 | 4.5 | saddle |
| 11 | 306 | 124 | 4.5 | corner bracket |
| 12 | 445 | 123 | 4.5 | saddle |
| 13 | 515 | 123 | 4.5 | saddle |
| 14 | 625 | 123 | 4.5 | saddle |
| 15 | 711 | 124 | 4.5 | corner bracket |
| 16 | 65 | 129 | 4.5 | leg holder |
| 17 | 662 | 129 | 4.5 | leg holder |

#### Base partition

![Base partition](boards/base-partition.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 45 | 18 | 3.2 | split-gasket-groove |
| 2 | 115 | 18 | 3.2 | split-gasket-groove |
| 3 | 186 | 18 | 3.2 | split-gasket-groove |
| 4 | 256 | 18 | 3.2 | split-gasket-groove |
| 5 | 326 | 18 | 3.2 | split-gasket-groove |
| 6 | 397 | 18 | 3.2 | split-gasket-groove |
| 7 | 467 | 18 | 3.2 | split-gasket-groove |
| 8 | 537 | 18 | 3.2 | split-gasket-groove |
| 9 | 169 | 48 | 9.6 | 3/8 dowel pin (split) |
| 10 | 233 | 48 | 9.6 | 3/8 dowel pin (split) |
| 11 | 349 | 48 | 9.6 | 3/8 dowel pin (split) |
| 12 | 413 | 48 | 9.6 | 3/8 dowel pin (split) |
| 13 | 20 | 124 | 4.5 | corner bracket |
| 14 | 562 | 124 | 4.5 | corner bracket |

#### Base cleat, front

![Base cleat, front](boards/base-cleat-front.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 580 | 19 | 4.5 | cleat |
| 2 | 400 | 19 | 4.5 | cleat |
| 3 | 220 | 19 | 4.5 | cleat |
| 4 | 40 | 19 | 4.5 | cleat |

#### Base cleat, rear

![Base cleat, rear](boards/base-cleat-rear.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 580 | 19 | 4.5 | cleat |
| 2 | 400 | 19 | 4.5 | cleat |
| 3 | 220 | 19 | 4.5 | cleat |
| 4 | 40 | 19 | 4.5 | cleat |

#### Base cleat, left

![Base cleat, left](boards/base-cleat-left.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 684 | 19 | 4.5 | cleat |
| 2 | 470 | 19 | 4.5 | cleat |
| 3 | 255 | 19 | 4.5 | cleat |
| 4 | 40 | 19 | 4.5 | cleat |

#### Base cleat, right

![Base cleat, right](boards/base-cleat-right.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 684 | 19 | 4.5 | cleat |
| 2 | 470 | 19 | 4.5 | cleat |
| 3 | 255 | 19 | 4.5 | cleat |
| 4 | 40 | 19 | 4.5 | cleat |

#### Base bridge y=-230

![Base bridge y=-230](boards/base-bridge-y-230.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 618 | 11 | 4.5 | saddle |
| 2 | 317 | 12 | 4.5 | core post |
| 3 | 16 | 11 | 4.5 | saddle |

#### Base bridge y=-130

![Base bridge y=-130](boards/base-bridge-y-130.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 618 | 11 | 4.5 | saddle |
| 2 | 503 | 12 | 4.5 | core post |
| 3 | 317 | 12 | 4.5 | core post |
| 4 | 130 | 12 | 4.5 | core post |
| 5 | 16 | 11 | 4.5 | saddle |

#### Base bridge y=-60

![Base bridge y=-60](boards/base-bridge-y-60.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 618 | 11 | 4.5 | saddle |
| 2 | 16 | 11 | 4.5 | saddle |

#### Base bridge y=100

![Base bridge y=100](boards/base-bridge-y-100.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 618 | 11 | 4.5 | saddle |
| 2 | 468 | 12 | 4.5 | core post |
| 3 | 166 | 12 | 4.5 | core post |
| 4 | 16 | 11 | 4.5 | saddle |

#### Base bridge y=170

![Base bridge y=170](boards/base-bridge-y-170.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 618 | 11 | 4.5 | saddle |
| 2 | 467 | 12 | 4.5 | core post |
| 3 | 317 | 12 | 4.5 | core post |
| 4 | 166 | 12 | 4.5 | core post |
| 5 | 16 | 11 | 4.5 | saddle |

#### Base bridge y=280

![Base bridge y=280](boards/base-bridge-y-280.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 618 | 11 | 4.5 | saddle |
| 2 | 16 | 11 | 4.5 | saddle |

#### Base leg bridge y=-280

![Base leg bridge y=-280](boards/base-leg-bridge-y-280.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 396 | 11 | 4.5 | leg holder |
| 2 | 6 | 11 | 4.5 | leg holder |

#### Base leg bridge y=318

![Base leg bridge y=318](boards/base-leg-bridge-y-318.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 396 | 11 | 4.5 | leg holder |
| 2 | 6 | 11 | 4.5 | leg holder |

### Uprights

#### Upright floor

![Upright floor](boards/upright-floor.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 77 | 54 | 4.5 | toe-filler |
| 2 | 119 | 72 | 4.5 | toe-filler |
| 3 | 131 | 129 | 3.2 | foot-gasket-groove |
| 4 | 21 | 170 | 4.5 | cleat |
| 5 | 177 | 170 | 4.5 | cleat |
| 6 | 67 | 189 | 3.2 | foot-gasket-groove |
| 7 | 67 | 266 | 3.2 | foot-gasket-groove |
| 8 | 131 | 266 | 3.2 | foot-gasket-groove |
| 9 | 99 | 272 | 13.1 | 1/2-13 bolt, base dowel hole |
| 10 | 21 | 335 | 4.5 | cleat |
| 11 | 67 | 337 | 3.2 | foot-gasket-groove |
| 12 | 99 | 337 | 13.5 | column tie rod, from below |
| 13 | 131 | 337 | 3.2 | foot-gasket-groove |
| 14 | 177 | 335 | 4.5 | cleat |
| 15 | 99 | 387 | 13.1 | 1/2-13 bolt, base dowel hole |
| 16 | 131 | 414 | 3.2 | foot-gasket-groove |
| 17 | 99 | 437 | 13.5 | column tie rod, from below |
| 18 | 67 | 474 | 3.2 | foot-gasket-groove |
| 19 | 21 | 501 | 4.5 | cleat |
| 20 | 177 | 501 | 4.5 | cleat |
| 21 | 99 | 560 | 4.5 | cleat |

#### Upright side plate, outer

![Upright side plate, outer](boards/upright-side-plate-outer.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 246 | 241 | 4.5 | corner bracket |
| 2 | 437 | 256 | 4.5 | corner bracket |
| 3 | 356 | 259 | 4.5 | saddle |

Outline corners (x, y): (0, 0), (501, 0), (457, 271), (228, 271)

#### Upright side plate, inner

![Upright side plate, inner](boards/upright-side-plate-inner.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 255 | 241 | 4.5 | corner bracket |
| 2 | 64 | 256 | 4.5 | corner bracket |
| 3 | 145 | 259 | 4.5 | saddle |

Outline corners (x, y): (501, 0), (0, 0), (44, 271), (273, 271)

#### Upright back board

![Upright back board](boards/upright-back-board.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 3 | 260 | 4.5 | corner bracket |
| 2 | 77 | 260 | 4.5 | corner bracket |

#### Upright front board

![Upright front board](boards/upright-front-board.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 32 | 35 | 4.5 | toe-plug |
| 2 | 14 | 281 | 4.5 | corner bracket |
| 3 | 66 | 281 | 4.5 | corner bracket |

#### Upright bridge

![Upright bridge](boards/upright-bridge.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 87 | 40 | 10 | 3/8-16 bolt into the top plate |
| 2 | 43 | 130 | 10 | 3/8-16 bolt into the top plate |

#### Upright cleat, outer

![Upright cleat, outer](boards/upright-cleat-outer.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 371 | 19 | 4.5 | cleat |
| 2 | 205 | 19 | 4.5 | cleat |
| 3 | 40 | 19 | 4.5 | cleat |

#### Upright cleat, inner

![Upright cleat, inner](boards/upright-cleat-inner.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 371 | 19 | 4.5 | cleat |
| 2 | 205 | 19 | 4.5 | cleat |
| 3 | 40 | 19 | 4.5 | cleat |

#### Upright cleat, back

![Upright cleat, back](boards/upright-cleat-back.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 40 | 19 | 4.5 | cleat |

### Beam

#### Beam floor

![Beam floor](boards/beam-floor.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 80 | 21 | 4.5 | cleat |
| 2 | 315 | 21 | 4.5 | cleat |
| 3 | 550 | 21 | 4.5 | cleat |
| 4 | 165 | 82 | 5.5 | M5 screw into the face plate |
| 5 | 285 | 82 | 5.5 | M5 screw into the face plate |
| 6 | 345 | 82 | 5.5 | M5 screw into the face plate |
| 7 | 465 | 82 | 5.5 | M5 screw into the face plate |
| 8 | 21 | 99 | 4.5 | cleat |
| 9 | 610 | 99 | 4.5 | cleat |
| 10 | 85 | 109 | 6.5 | M6 screw into the face plate |
| 11 | 98 | 109 | 6.5 | M6 screw into the face plate |
| 12 | 443 | 109 | 6.5 | M6 screw into the face plate |
| 13 | 85 | 155 | 6.5 | M6 screw into the face plate |
| 14 | 98 | 155 | 6.5 | M6 screw into the face plate |
| 15 | 443 | 155 | 6.5 | M6 screw into the face plate |
| 16 | 21 | 165 | 4.5 | cleat |
| 17 | 610 | 165 | 4.5 | cleat |
| 18 | 165 | 182 | 5.5 | M5 screw into the face plate |
| 19 | 285 | 182 | 5.5 | M5 screw into the face plate |
| 20 | 345 | 182 | 5.5 | M5 screw into the face plate |
| 21 | 465 | 182 | 5.5 | M5 screw into the face plate |
| 22 | 80 | 243 | 4.5 | cleat |
| 23 | 315 | 243 | 4.5 | cleat |
| 24 | 550 | 243 | 4.5 | cleat |

#### Beam top wall

![Beam top wall](boards/beam-top-wall.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 37 | 25 | 13.1 | 1/2 core rod |
| 2 | 81 | 25 | 13.1 | 1/2 core rod |
| 3 | 469 | 25 | 13.1 | 1/2 core rod |
| 4 | 513 | 25 | 13.1 | 1/2 core rod |
| 5 | 398 | 49 | 5.5 | M5 insert screw |
| 6 | 398 | 71 | 5.5 | M5 insert screw |
| 7 | 37 | 115 | 13.1 | 1/2 core rod |
| 8 | 81 | 115 | 13.1 | 1/2 core rod |
| 9 | 469 | 115 | 13.1 | 1/2 core rod |
| 10 | 513 | 115 | 13.1 | 1/2 core rod |
| 11 | 162 | 133 | 4.5 | back-edge |
| 12 | 276 | 133 | 4.5 | back-edge |
| 13 | 390 | 133 | 4.5 | back-edge |
| 14 | 33 | 154 | 4.5 | corner bracket |
| 15 | 518 | 154 | 4.5 | corner bracket |

#### Beam bottom wall

![Beam bottom wall](boards/beam-bottom-wall.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 37 | 25 | 13.1 | 1/2 core rod |
| 2 | 81 | 25 | 13.1 | 1/2 core rod |
| 3 | 469 | 25 | 13.1 | 1/2 core rod |
| 4 | 513 | 25 | 13.1 | 1/2 core rod |
| 5 | 59 | 70 | 9.6 | 3/8 dowel |
| 6 | 491 | 70 | 9.6 | 3/8 dowel |
| 7 | 37 | 115 | 13.1 | 1/2 core rod |
| 8 | 81 | 115 | 13.1 | 1/2 core rod |
| 9 | 469 | 115 | 13.1 | 1/2 core rod |
| 10 | 513 | 115 | 13.1 | 1/2 core rod |
| 11 | 33 | 154 | 4.5 | corner bracket |
| 12 | 518 | 154 | 4.5 | corner bracket |

#### Beam end wall, left

![Beam end wall, left](boards/beam-end-wall-left.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 14 | 154 | 4.5 | corner bracket |
| 2 | 132 | 154 | 4.5 | corner bracket |

#### Beam end wall, right

![Beam end wall, right](boards/beam-end-wall-right.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 14 | 154 | 4.5 | corner bracket |
| 2 | 132 | 154 | 4.5 | corner bracket |

#### Beam cleat, top

![Beam cleat, top](boards/beam-cleat-top.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 510 | 19 | 4.5 | cleat |
| 2 | 275 | 19 | 4.5 | cleat |
| 3 | 40 | 19 | 4.5 | cleat |

#### Beam cleat, bottom

![Beam cleat, bottom](boards/beam-cleat-bottom.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 510 | 19 | 4.5 | cleat |
| 2 | 275 | 19 | 4.5 | cleat |
| 3 | 40 | 19 | 4.5 | cleat |

#### Beam cleat, left

![Beam cleat, left](boards/beam-cleat-left.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 106 | 19 | 4.5 | cleat |
| 2 | 40 | 19 | 4.5 | cleat |

#### Beam cleat, right

![Beam cleat, right](boards/beam-cleat-right.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 106 | 19 | 4.5 | cleat |
| 2 | 40 | 19 | 4.5 | cleat |
