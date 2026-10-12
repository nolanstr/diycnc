# Upright molds

How to make the upright molds. Drilling templates: `templates/upright-templates.pdf`. The complete guide (all the molds and the
sheet layout for the boards) is `molds-complete.pdf`.

![An upright mold, pulled apart](../../renders/mold/exploded-upright.png)

**In short:** melamine boards bolt together with printed brackets. Every printed piece bolts or pins to
its board from outside. The walls stand 25 mm above the pour line, so no bolt goes through a face the
mix touches. Nothing is glued, and it all comes apart for the next casting.

**Order of work:** print &rarr; cut the boards &rarr; mark them with the templates and drill &rarr; wax &rarr; assemble &rarr; pour &rarr; take apart.

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

- **Fits** are 0.15 mm a side, and drawn for 19.05 mm board (Home Depot's 3/4 in melamine is a true
  0.750 in). Measure yours; if it differs, set `mold_board` in `model/build_cnc.py` and re-run it.

## 2. What you need

| Material | Amount | Notes |
|---|---|---|
| Melamine board, 3/4 in | about 0.9 m2 | all the molds come out of two 4 x 8 ft sheets |
| PETG | 0.32 kg | sliced; everything printed for the machine fits in two 1 kg rolls |
| Paste wax and PVA | 1 each | release |
| 3/8 in quarter-round PVC molding | a few meters | the rounded outside edges |
| 2x4 offcut | 4 blocks per upright mold, about 50 mm | feet |

| Hardware | Qty |
|---|---|
| M4 nut | 40 |
| M4 washer | 40 |
| M4 x 30 bolt | 22 |
| M4 x 35 bolt | 4 |
| M4 x 45 bolt | 14 |
| 1/2 in rod (or a tie rod), greased, 355 mm: centers a top tie-rod sleeve | 4 |
| 1/2-13 x 1-1/2 in bolt + nut, greased (forms a dowel hole) | 4 |
| 3/8-16 x 3 in bolt, greased (holds the top plate, both layers) | 4 |
| 5/8 in plain steel rod, greased (forms a slope tie-rod hole), cut to 89 mm | 2 |

Add about 10 % spare small bolts, nuts and washers. **Tools:** drill and brad-point bits (sizes in section 5), a 2-1/2 in hole saw, a jigsaw for the side plates' slope, a square, clamps, a 7 mm nut driver, a 3 mm hex key, an awl.

## 3. Print

40 prints, 0.32 kg, about 23 hours (sliced; settings in the print guide). Print one corner bracket and one saddle first
and check them on a board offcut. Press or slide the nuts in before the pieces go on the boards.

| File | Qty | g | Time each |
|---|---|---|---|
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
| `tools/kit-pour-gauge.stl` | 2 | 9 | 24m 33s |
| `tools/kit-screed-shoe.stl` | 2 | 20 | 44m 42s |
| `upright/cast-in-column-ring-l1a.stl` | 8 | 109 | 49m 49s |

## 4. Cut the boards

Have the store rip the strips; crosscut at home. Write each board's name on its outside face, and mark
the cast face (the melamine face the mix touches).

| Board | Qty | Size (mm) | Notes |
|---|---|---|---|
| Upright floor | 2 | 198 x 541 |  |
| Upright side plate, outer | 2 | 461 x 271 (profile) | cut to the profile |
| Upright side plate, inner | 2 | 461 x 271 (profile) | cut to the profile |
| Upright back board | 2 | 80 x 271 |  |
| Upright front board | 2 | 80 x 292 | ends cut square |
| Upright bridge | 2 | 131 x 138 |  |
| Upright cleat, outer | 2 | 371 x 40 | offcut strip, flat on the floor |
| Upright cleat, inner | 2 | 371 x 40 | offcut strip, flat on the floor |
| Upright cleat, back | 2 | 80 x 40 | offcut strip, flat on the floor |

## 5. Mark and drill

1. Print the drilling templates (`templates/upright-templates.pdf`) at **actual size** and check the 100 mm square.
2. Tape each board's pages onto it: printed edges on the board's edges, grid lines lined up.
3. Awl through every crosshair. Pencil the dashed **pour line** on the walls.
4. Drill from the marked face, at the size the color legend gives. Pilot the big ones; the 63.5 mm
   holes are a 2-1/2 in hole saw.

The appendix has every board as a drawing and a table, if you would rather measure.

| Hole | Drill | For |
|---|---|---|
| 3.2 mm | 1/8 in | foot-gasket-groove |
| 4.5 mm | 11/64 in | cleat, corner bracket, saddle, toe-filler, toe-plug |
| 10 mm | 25/64 in | 3/8-16 bolt into the top plate |
| 13.1 mm | 33/64 in | 1/2-13 bolt, base dowel hole |
| 13.5 mm | 17/32 in | 1/2 rod through a sleeve |
| 16.3 mm | 41/64 in | 5/8 core rod |

## 6. Wax

- 3-5 coats of paste wax on every face the mix touches, boards and removable printed pieces, then PVA.
  Don't wax pieces that stay in (core posts, cast-in parts): scuff and degrease them.
- Glue quarter-round into the floor-to-wall corners that make outside edges; silicone fillets elsewhere.
- Grease every screw, bolt and rod that comes out of the casting.

## 7. Assemble

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

## 8. Pour

- Fill to the **pour line**, 25 mm below the wall tops (pencilled from the templates, or with the
  printed pour-line gauge clipped over a wall).
- Vibrate each layer until it stops bubbling; check the brackets halfway through.
- Strike the top off with a straight board in the two printed **screed shoes**: they hang it from the wall
  tops with its bottom edge on the pour line.

![Pour-line gauge and screed shoes](../../renders/mold/detail-pour.png)

## 9. Take apart

1. After the full cure: bridges and saddles off, then corner brackets, then cleats; pull the walls off.
2. Screws, bolts and rods out from outside; lift the casting off the floor.
3. Unbolt and pull the formers and fillers.
4. Scrape and re-wax the boards; keep each mold's kit in a box. The kit is reused.

## 10. If something doesn't fit

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
