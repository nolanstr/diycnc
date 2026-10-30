# Base mold

How to make the base mold. Drilling templates: `templates/base-templates.pdf`. The sheet layout for the boards is
`docs/src/boards/sheet-1.svg`; `docs/src/make_pdfs.py` also makes `molds-complete.pdf`, all the molds in one
(not kept in the repo).

![The base mold (rear half), pulled apart](../../renders/mold/exploded-base.png)

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
| Melamine board, 3/4 in | about 1.3 m2 | all the molds come out of 1 sheet, 4 x 8 ft |
| 1x2 lumber (furring strip is fine) | 2 x 8 ft 1x2 (2.7 m) | the cleats: they lie on the floor outside the walls |
| XPS foam board, 2 in | 1 sheet, 2 x 8 ft | the cores |
| PETG | 1.80 kg | sliced; everything printed for the machine fits in two 1 kg rolls |
| Packing tape, double-sided carpet tape | 1 roll each | wrapping and holding the foam |
| Paste wax and PVA | 1 each | release |
| 3/8 in quarter-round PVC molding | a few meters | the rounded outside edges |

| Hardware | Qty |
|---|---|
| M3 nut | 20 |
| M3 washer | 20 |
| M3 x 25 bolt | 20 |
| M4 nut | 116 |
| M4 washer | 112 |
| M4 x 20 bolt (leg pinch screw) | 4 |
| M4 x 30 bolt | 68 |
| M4 x 35 bolt | 28 |
| M4 x 45 bolt | 16 |
| M5 x 20 screw, greased (holds an insert) | 17 |
| M5 x 30 screw, greased (holds a rail bar or the BK pad) | 12 |
| M6 x 30 screw, greased (holds a support pad) | 8 |

Add about 10 % spare small bolts, nuts and washers. **Tools:** drill and brad-point bits (sizes in section 5), a 2-1/2 in hole saw, a square, clamps, a 7 mm nut driver, a 3 mm hex key, an awl, a fine saw or hot wire for the foam.

## 3. Print

99 prints, 1.80 kg, about 116 hours (sliced; settings in the print guide). Print one corner bracket and one saddle first
and check them on a board offcut. Press or slide the nuts in before the pieces go on the boards.

| File | Qty | g | Time each |
|---|---|---|---|
| `base-box/kit-corner-bracket.stl` | 4 | 33 | 39m 22s |
| `base-box/kit-partition-bracket.stl` | 2 | 14 | 35m 31s |
| `base-box/kit-saddle.stl` | 6 | 58 | 46m 6s |
| `base-box/kit-leg-holder.stl` | 4 | 166 | 2h 31m 6s |
| `base-rear/former-gutter-L-part1of3.stl` | 1 | 8 | 35m 5s |
| `base-rear/former-gutter-L-part2of3.stl` | 1 | 8 | 33m 42s |
| `base-rear/former-gutter-L-part3of3.stl` | 1 | 7 | 31m 18s |
| `base-rear/former-gutter-R-part1of3.stl` | 1 | 8 | 35m 7s |
| `base-rear/former-gutter-R-part2of3.stl` | 1 | 8 | 33m 42s |
| `base-rear/former-gutter-R-part3of3.stl` | 1 | 7 | 31m 17s |
| `base-rear/former-floor-part1of9.stl` | 1 | 14 | 50m 49s |
| `base-rear/former-floor-part2of9.stl` | 1 | 31 | 1h 48m 52s |
| `base-rear/former-floor-part3of9.stl` | 1 | 13 | 50m 1s |
| `base-rear/former-floor-part4of9.stl` | 1 | 13 | 47m 47s |
| `base-rear/former-floor-part5of9.stl` | 1 | 29 | 1h 43m 13s |
| `base-rear/former-floor-part6of9.stl` | 1 | 13 | 47m 50s |
| `base-rear/former-floor-part7of9.stl` | 1 | 11 | 39m 30s |
| `base-rear/former-floor-part8of9.stl` | 1 | 11 | 42m 13s |
| `base-rear/former-floor-part9of9.stl` | 1 | 11 | 39m 27s |
| `base-rear/filler-corner-L.stl` | 1 | 29 | 2h 10m 25s |
| `base-rear/filler-bevel-L-part1of2.stl` | 1 | 50 | 2h 39m 10s |
| `base-rear/filler-bevel-L-part2of2.stl` | 1 | 50 | 2h 39m 43s |
| `base-rear/filler-corner-R.stl` | 1 | 29 | 2h 11m 15s |
| `base-rear/filler-bevel-R-part1of2.stl` | 1 | 50 | 2h 35m 0s |
| `base-rear/filler-bevel-R-part2of2.stl` | 1 | 50 | 2h 35m 59s |
| `base-rear/filler-bevel-end-part1of3.stl` | 1 | 50 | 2h 36m 46s |
| `base-rear/filler-bevel-end-part2of3.stl` | 1 | 50 | 2h 37m 13s |
| `base-rear/filler-bevel-end-part3of3.stl` | 1 | 50 | 2h 36m 47s |
| `base-front/former-gutter-L-part1of2.stl` | 1 | 11 | 49m 21s |
| `base-front/former-gutter-L-part2of2.stl` | 1 | 10 | 43m 43s |
| `base-front/former-gutter-R-part1of2.stl` | 1 | 11 | 49m 19s |
| `base-front/former-gutter-R-part2of2.stl` | 1 | 10 | 43m 45s |
| `base-front/former-floor-part1of12.stl` | 1 | 44 | 2h 24m 52s |
| `base-front/former-floor-part2of12.stl` | 1 | 23 | 1h 23m 35s |
| `base-front/former-floor-part3of12.stl` | 1 | 5 | 24m 55s |
| `base-front/former-floor-part4of12.stl` | 1 | 5 | 23m 14s |
| `base-front/former-floor-part5of12.stl` | 1 | 16 | 1h 1m 11s |
| `base-front/former-floor-part6of12.stl` | 1 | 21 | 1h 14m 46s |
| `base-front/former-floor-part7of12.stl` | 1 | 16 | 1h 1m 0s |
| `base-front/former-floor-part8of12.stl` | 1 | 21 | 1h 14m 46s |
| `base-front/former-floor-part9of12.stl` | 1 | 5 | 24m 47s |
| `base-front/former-floor-part10of12.stl` | 1 | 5 | 23m 14s |
| `base-front/former-floor-part11of12.stl` | 1 | 44 | 2h 24m 48s |
| `base-front/former-floor-part12of12.stl` | 1 | 23 | 1h 23m 37s |
| `base-front/former-trough-part1of5.stl` | 1 | 19 | 1h 12m 22s |
| `base-front/former-trough-part2of5.stl` | 1 | 22 | 1h 21m 40s |
| `base-front/former-trough-part3of5.stl` | 1 | 24 | 1h 31m 38s |
| `base-front/former-trough-part4of5.stl` | 1 | 22 | 1h 21m 54s |
| `base-front/former-trough-part5of5.stl` | 1 | 20 | 1h 11m 52s |
| `base-front/filler-corner-L.stl` | 1 | 29 | 2h 10m 54s |
| `base-front/filler-bevel-L-part1of2.stl` | 1 | 46 | 2h 25m 11s |
| `base-front/filler-bevel-L-part2of2.stl` | 1 | 46 | 2h 25m 26s |
| `base-front/filler-corner-R.stl` | 1 | 29 | 2h 8m 14s |
| `base-front/filler-bevel-R-part1of2.stl` | 1 | 46 | 2h 21m 16s |
| `base-front/filler-bevel-R-part2of2.stl` | 1 | 46 | 2h 21m 45s |
| `base-front/filler-bevel-end-part1of3.stl` | 1 | 50 | 2h 32m 31s |
| `base-front/filler-bevel-end-part2of3.stl` | 1 | 50 | 2h 33m 48s |
| `base-front/filler-bevel-end-part3of3.stl` | 1 | 50 | 2h 33m 22s |
| `base-rear/former-split-gasket-groove-part1of4.stl` | 1 | 2 | 9m 41s |
| `base-rear/former-split-gasket-groove-part2of4.stl` | 1 | 1 | 8m 49s |
| `base-rear/former-split-gasket-groove-part3of4.stl` | 1 | 1 | 8m 49s |
| `base-rear/former-split-gasket-groove-part4of4.stl` | 1 | 2 | 9m 44s |
| `base-front/core-center-a-post.stl` | 1 | 5 | 44m 53s |
| `base-front/core-center-b-post.stl` | 1 | 5 | 44m 53s |
| `base-rear/core-center-post.stl` | 1 | 5 | 44m 53s |
| `base-front/core-outboard-L-post.stl` | 1 | 5 | 44m 53s |
| `base-rear/core-foot-b-L-post.stl` | 1 | 5 | 44m 53s |
| `base-rear/core-knee-L-post.stl` | 1 | 5 | 44m 53s |
| `base-front/core-outboard-R-post.stl` | 1 | 5 | 44m 53s |
| `base-rear/core-foot-b-R-post.stl` | 1 | 5 | 44m 53s |
| `base-rear/core-knee-R-post.stl` | 1 | 5 | 44m 53s |
| `base-front/plug-draw-pocket-L.stl` | 1 | 12 | 46m 13s |
| `base-front/plug-draw-pocket-R.stl` | 1 | 12 | 46m 13s |
| `base-rear/plug-draw-pocket-L.stl` | 1 | 5 | 21m 23s |
| `base-rear/plug-draw-pocket-R.stl` | 1 | 5 | 21m 23s |
| `tools/kit-pour-gauge.stl` | 2 | 9 | 24m 41s |
| `tools/kit-screed-shoe.stl` | 2 | 20 | 47m 40s |
| `base-front/cast-in-leg-front-l-plug.stl` | 2 | 8 | 24m 42s |
| `base-front/cast-in-leg-front-l-foot-cup.stl` | 2 | 18 | 1h 0m 43s |
| `base-rear/cast-in-leg-rear-l-plug.stl` | 2 | 8 | 24m 42s |
| `base-rear/cast-in-leg-rear-l-foot-cup.stl` | 2 | 18 | 1h 0m 43s |

## 4. Cut the boards

Have the store rip the strips; crosscut at home. Write each board's name on its outside face, and mark
the cast face (the melamine face the mix touches). The cleats are cut from 1x2 lumber, not the sheet;
the bridges and struts come out of the sheet's offcuts.

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

## 5. Mark and drill

1. Print the drilling templates (`templates/base-templates.pdf`) at **actual size** and check the 100 mm square.
2. Tape each board's pages onto it: printed edges on the board's edges, grid lines lined up.
3. Awl through every crosshair. Pencil the dashed **pour line** on the walls.
4. Drill from the marked face, at the size the color legend gives. Pilot the big ones; the 63.5 mm
   holes are a 2-1/2 in hole saw.

The appendix has every board as a drawing and a table, if you would rather measure.

| Hole | Drill | For |
|---|---|---|
| 3.2 mm | 1/8 in | floor, split-gasket-groove |
| 3.4 mm | 9/64 in | corner-L, corner-R, gutter-L, gutter-R |
| 4.5 mm | 11/64 in | bevel-L, bevel-R, bevel-end, cleat, core post, corner bracket, corner-L, corner-R, draw-pocket-L, draw-pocket-R, gutter-L, gutter-R, leg holder, saddle, trough |
| 5.5 mm | 7/32 in | M5 insert screw, M5 screw into the steel |
| 6.5 mm | 17/64 in | M6 screw into a pad |
| 9.6 mm | 25/64 in | 3/8 dowel, 3/8 dowel pin |

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
| 24 | 192 | 152 | 3.2 | floor |
| 25 | 229 | 150 | 3.2 | floor |
| 26 | 338 | 152 | 3.2 | floor |
| 27 | 402 | 152 | 3.2 | floor |
| 28 | 472 | 150 | 3.2 | floor |
| 29 | 577 | 152 | 3.2 | floor |
| 30 | 614 | 150 | 4.5 | gutter-L |
| 31 | 260 | 184 | 5.5 | M5 screw into the steel |
| 32 | 440 | 184 | 5.5 | M5 screw into the steel |
| 33 | 69 | 209 | 5.5 | M5 insert screw |
| 34 | 327 | 210 | 6.5 | M6 screw into a pad |
| 35 | 373 | 210 | 6.5 | M6 screw into a pad |
| 36 | 631 | 209 | 5.5 | M5 insert screw |
| 37 | 124 | 221 | 3.2 | floor |
| 38 | 508 | 221 | 3.2 | floor |
| 39 | 87 | 223 | 4.5 | gutter-R |
| 40 | 229 | 223 | 3.2 | floor |
| 41 | 297 | 223 | 3.2 | floor |
| 42 | 472 | 223 | 3.2 | floor |
| 43 | 614 | 223 | 4.5 | gutter-L |
| 44 | 367 | 249 | 3.2 | floor |
| 45 | 145 | 276 | 3.2 | floor |
| 46 | 555 | 276 | 3.2 | floor |
| 47 | 87 | 295 | 3.4 | gutter-R |
| 48 | 229 | 295 | 3.2 | floor |
| 49 | 338 | 297 | 3.2 | floor |
| 50 | 402 | 297 | 3.2 | floor |
| 51 | 472 | 295 | 3.2 | floor |
| 52 | 614 | 295 | 3.4 | gutter-L |
| 53 | 260 | 304 | 5.5 | M5 screw into the steel |
| 54 | 440 | 304 | 5.5 | M5 screw into the steel |
| 55 | 21 | 314 | 4.5 | cleat |
| 56 | 680 | 314 | 4.5 | cleat |
| 57 | 214 | 344 | 3.2 | floor |
| 58 | 487 | 344 | 3.2 | floor |
| 59 | 298 | 366 | 3.2 | floor |
| 60 | 363 | 366 | 3.2 | floor |
| 61 | 87 | 368 | 3.4 | gutter-R |
| 62 | 229 | 368 | 3.2 | floor |
| 63 | 472 | 368 | 3.2 | floor |
| 64 | 614 | 368 | 3.4 | gutter-L |
| 65 | 69 | 421 | 5.5 | M5 insert screw |
| 66 | 631 | 421 | 5.5 | M5 insert screw |
| 67 | 260 | 424 | 5.5 | M5 screw into the steel |
| 68 | 440 | 424 | 5.5 | M5 screw into the steel |
| 69 | 381 | 432 | 3.2 | floor |
| 70 | 87 | 434 | 3.4 | gutter-R |
| 71 | 199 | 433 | 5.5 | M5 insert screw |
| 72 | 224 | 435 | 3.2 | floor |
| 73 | 509 | 435 | 3.2 | floor |
| 74 | 614 | 434 | 3.4 | gutter-L |
| 75 | 199 | 455 | 5.5 | M5 insert screw |
| 76 | 191 | 491 | 3.2 | floor |
| 77 | 477 | 491 | 3.2 | floor |
| 78 | 87 | 494 | 3.4 | gutter-R |
| 79 | 319 | 494 | 3.2 | floor |
| 80 | 614 | 494 | 3.4 | gutter-L |
| 81 | 134 | 504 | 9.6 | 3/8 dowel |
| 82 | 566 | 504 | 9.6 | 3/8 dowel |
| 83 | 21 | 529 | 4.5 | cleat |
| 84 | 680 | 529 | 4.5 | cleat |
| 85 | 260 | 544 | 5.5 | M5 screw into the steel |
| 86 | 440 | 544 | 5.5 | M5 screw into the steel |
| 87 | 224 | 552 | 3.2 | floor |
| 88 | 381 | 549 | 3.2 | floor |
| 89 | 509 | 552 | 3.2 | floor |
| 90 | 87 | 554 | 3.4 | gutter-R |
| 91 | 614 | 554 | 3.4 | gutter-L |
| 92 | 191 | 608 | 3.2 | floor |
| 93 | 319 | 611 | 3.2 | floor |
| 94 | 477 | 608 | 3.2 | floor |
| 95 | 87 | 614 | 3.4 | gutter-R |
| 96 | 614 | 614 | 3.4 | gutter-L |
| 97 | 134 | 619 | 9.6 | 3/8 dowel |
| 98 | 566 | 619 | 9.6 | 3/8 dowel |
| 99 | 69 | 634 | 5.5 | M5 insert screw |
| 100 | 631 | 634 | 5.5 | M5 insert screw |
| 101 | 260 | 664 | 5.5 | M5 screw into the steel |
| 102 | 385 | 663 | 3.2 | floor |
| 103 | 440 | 664 | 5.5 | M5 screw into the steel |
| 104 | 224 | 669 | 3.2 | floor |
| 105 | 509 | 669 | 3.2 | floor |
| 106 | 87 | 674 | 3.4 | gutter-R |
| 107 | 614 | 674 | 3.4 | gutter-L |
| 108 | 327 | 705 | 6.5 | M6 screw into a pad |
| 109 | 373 | 705 | 6.5 | M6 screw into a pad |
| 110 | 311 | 712 | 5.5 | M5 screw into the steel |
| 111 | 389 | 712 | 5.5 | M5 screw into the steel |
| 112 | 327 | 718 | 6.5 | M6 screw into a pad |
| 113 | 373 | 718 | 6.5 | M6 screw into a pad |
| 114 | 87 | 734 | 3.4 | gutter-R |
| 115 | 614 | 734 | 3.4 | gutter-L |
| 116 | 21 | 744 | 4.5 | cleat |
| 117 | 213 | 743 | 5.5 | M5 insert screw |
| 118 | 487 | 743 | 5.5 | M5 insert screw |
| 119 | 680 | 744 | 4.5 | cleat |
| 120 | 327 | 748 | 6.5 | M6 screw into a pad |
| 121 | 373 | 748 | 6.5 | M6 screw into a pad |
| 122 | 64 | 772 | 3.4 | corner-R |
| 123 | 637 | 772 | 3.4 | corner-L |
| 124 | 200 | 774 | 5.5 | M5 insert screw |
| 125 | 500 | 774 | 5.5 | M5 insert screw |
| 126 | 80 | 822 | 4.5 | cleat |
| 127 | 260 | 822 | 4.5 | cleat |
| 128 | 440 | 822 | 4.5 | cleat |
| 129 | 620 | 822 | 4.5 | cleat |

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
