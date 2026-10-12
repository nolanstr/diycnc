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
| Melamine board, 3/4 in | about 1.0 m2 | all the molds come out of two 4 x 8 ft sheets |
| PETG | 0.34 kg | sliced; everything printed for the machine fits in two 1 kg rolls |
| Paste wax and PVA | 1 each | release |
| 3/8 in quarter-round PVC molding | a few meters | the rounded outside edges |
| 2x4 offcut | 4 blocks per upright mold, about 50 mm | feet |

| Hardware | Qty |
|---|---|
| M4 nut | 42 |
| M4 washer | 42 |
| M4 x 30 bolt | 24 |
| M4 x 35 bolt | 4 |
| M4 x 45 bolt | 14 |
| 1/2-13 x 1-1/2 in bolt + nut, greased (forms the dowel hole) | 2 |
| 3/8-16 x 2-1/2 in bolt, greased (holds the top plate) | 4 |
| 5/8 in plain steel rod, greased (forms a tie-rod hole), cut to 144 mm, 247 mm, 381 mm, 381 mm | 2 |

Add about 10 % spare small bolts, nuts and washers. **Tools:** drill and brad-point bits (sizes in section 5), a 2-1/2 in hole saw, a jigsaw for the side plates' slope, a square, clamps, a 7 mm nut driver, a 3 mm hex key, an awl.

## 3. Print

46 prints, 0.34 kg, about 27 hours (sliced; settings in the print guide). Print one corner bracket and one saddle first
and check them on a board offcut. Press or slide the nuts in before the pieces go on the boards.

| File | Qty | g | Time each |
|---|---|---|---|
| `upright/kit-back-bracket.stl` | 4 | 21 | 27m 33s |
| `upright/kit-front-bracket.stl` | 4 | 32 | 38m 27s |
| `upright/kit-saddle-flat.stl` | 4 | 18 | 22m 40s |
| `upright/filler-toe-filler.stl` | 2 | 54 | 1h 33m 58s |
| `upright/former-foot-gasket-groove-part1of4.stl` | 2 | 7 | 17m 8s |
| `upright/former-foot-gasket-groove-part2of4.stl` | 2 | 3 | 8m 46s |
| `upright/former-foot-gasket-groove-part3of4.stl` | 2 | 3 | 8m 46s |
| `upright/former-foot-gasket-groove-part4of4.stl` | 2 | 7 | 17m 10s |
| `upright/plug-slope-plug-lower.stl` | 2 | 19 | 45m 49s |
| `upright/plug-slope-plug-upper.stl` | 2 | 19 | 45m 47s |
| `upright/plug-tie-rod-pocket.stl` | 4 | 33 | 39m 54s |
| `upright/kit-plate-spacer.stl` | 4 | 15 | 20m 9s |
| `upright/kit-post-bushing.stl` | 4 | 67 | 1h 11m 51s |
| `tools/kit-pour-gauge.stl` | 2 | 9 | 24m 33s |
| `tools/kit-screed-shoe.stl` | 2 | 20 | 44m 42s |
| `upright/cast-in-post-l1-plug.stl` | 4 | 16 | 24m 37s |

## 4. Cut the boards

Have the store rip the strips; crosscut at home. Write each board's name on its outside face, and mark
the cast face (the melamine face the mix touches).

| Board | Qty | Size (mm) | Notes |
|---|---|---|---|
| Upright floor | 2 | 198 x 575 |  |
| Upright side plate, outer | 2 | 495 x 271 (profile) | cut to the profile |
| Upright side plate, inner | 2 | 495 x 271 (profile) | cut to the profile |
| Upright back board | 2 | 80 x 271 |  |
| Upright front board | 2 | 80 x 312 | ends cut square |
| Upright bridge | 2 | 131 x 108 |  |
| Upright cleat, outer | 2 | 405 x 40 | offcut strip, flat on the floor |
| Upright cleat, inner | 2 | 405 x 40 | offcut strip, flat on the floor |
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
| 4.5 mm | 11/64 in | cleat, corner bracket, saddle, slope-plug-lower, slope-plug-upper, toe-filler |
| 10 mm | 25/64 in | 3/8-16 bolt into the top plate |
| 13.1 mm | 33/64 in | 1/2-13 bolt, base dowel hole |
| 16.3 mm | 41/64 in | 5/8 core rod |
| 63.5 mm | 2-1/2 in hole saw | hole saw |

## 6. Wax

- 3-5 coats of paste wax on every face the mix touches, boards and removable printed pieces, then PVA.
  Don't wax pieces that stay in (core posts, cast-in parts): scuff and degrease them.
- Glue quarter-round into the floor-to-wall corners that make outside edges; silicone fillets elsewhere.
- Grease every screw, bolt and rod that comes out of the casting.

## 7. Assemble

### Uprights (two molds)

Cast foot down. Build two of everything.

1. Post bushings into the floor from below; gasket bead pinned on; cleats bolted down.

![Upright, step 1](../../renders/mold/step-upright-1.png)

2. Side plates against their cleats, back board between them, two back brackets.

![Upright, step 2](../../renders/mold/step-upright-2.png)

3. Toe filler bolted down, the front board's foot in its lip, two front brackets at the top.

![Upright, step 3](../../renders/mold/step-upright-3.png)

4. Mold on its four 2x4 blocks. Posts up through the bushings, standing on the bench (a long post just ends nearer the top plate: 6 mm room); greased 5/8 in rods up through the floor (short ones into the slope plugs, long ones to the top); dowel-hole bolt from underneath.

![Upright, step 4](../../renders/mold/step-upright-4.png)

5. Fill to the line. Top pocket plugs down the long rods, top plate hung from the bridge, bridge onto its saddles.

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
| 1 | 121 | 56 | 4.5 | toe-filler |
| 2 | 79 | 75 | 4.5 | toe-filler |
| 3 | 131 | 136 | 3.2 | foot-gasket-groove |
| 4 | 99 | 146 | 16.3 | 5/8 core rod |
| 5 | 20 | 170 | 4.5 | cleat |
| 6 | 178 | 170 | 4.5 | cleat |
| 7 | 67 | 197 | 3.2 | foot-gasket-groove |
| 8 | 99 | 246 | 16.3 | 5/8 core rod |
| 9 | 67 | 266 | 3.2 | foot-gasket-groove |
| 10 | 131 | 266 | 3.2 | foot-gasket-groove |
| 11 | 20 | 333 | 4.5 | cleat |
| 12 | 67 | 336 | 3.2 | foot-gasket-groove |
| 13 | 131 | 336 | 3.2 | foot-gasket-groove |
| 14 | 178 | 333 | 4.5 | cleat |
| 15 | 99 | 371 | 63.5 | hole saw |
| 16 | 131 | 414 | 3.2 | foot-gasket-groove |
| 17 | 79 | 426 | 16.3 | 5/8 core rod |
| 18 | 99 | 426 | 13.1 | 1/2-13 bolt, base dowel hole |
| 19 | 119 | 426 | 16.3 | 5/8 core rod |
| 20 | 67 | 461 | 3.2 | foot-gasket-groove |
| 21 | 99 | 481 | 63.5 | hole saw |
| 22 | 20 | 495 | 4.5 | cleat |
| 23 | 178 | 495 | 4.5 | cleat |
| 24 | 99 | 555 | 4.5 | cleat |

#### Upright side plate, outer (x2)

![Upright side plate, outer](boards/upright-side-plate-outer.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 280 | 240 | 4.5 | corner bracket |
| 2 | 406 | 259 | 4.5 | saddle |
| 3 | 473 | 260 | 4.5 | corner bracket |

Outline corners (x, y): (0, 0), (495, 0), (495, 271), (264, 271)

#### Upright side plate, inner (x2)

![Upright side plate, inner](boards/upright-side-plate-inner.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 215 | 240 | 4.5 | corner bracket |
| 2 | 22 | 260 | 4.5 | corner bracket |
| 3 | 90 | 259 | 4.5 | saddle |

Outline corners (x, y): (495, 0), (0, 0), (0, 271), (231, 271)

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
| 1 | 32 | 66 | 4.5 | slope-plug-lower |
| 2 | 32 | 209 | 4.5 | slope-plug-upper |
| 3 | 14 | 301 | 4.5 | corner bracket |
| 4 | 66 | 301 | 4.5 | corner bracket |

#### Upright bridge (x2)

![Upright bridge](boards/upright-bridge.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 87 | 10 | 10 | 3/8-16 bolt into the top plate |
| 2 | 85 | 34 | 16.3 | 5/8 core rod |
| 3 | 45 | 34 | 16.3 | 5/8 core rod |
| 4 | 43 | 100 | 10 | 3/8-16 bolt into the top plate |

#### Upright cleat, outer (x2)

![Upright cleat, outer](boards/upright-cleat-outer.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 365 | 20 | 4.5 | cleat |
| 2 | 203 | 20 | 4.5 | cleat |
| 3 | 40 | 20 | 4.5 | cleat |

#### Upright cleat, inner (x2)

![Upright cleat, inner](boards/upright-cleat-inner.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 365 | 20 | 4.5 | cleat |
| 2 | 203 | 20 | 4.5 | cleat |
| 3 | 40 | 20 | 4.5 | cleat |

#### Upright cleat, back (x2)

![Upright cleat, back](boards/upright-cleat-back.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 40 | 20 | 4.5 | cleat |
