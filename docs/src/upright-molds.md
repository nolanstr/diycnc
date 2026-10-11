# Upright molds

How to make, put together and take apart the mold for the two uprights (two identical molds, cast together). The first section (how the molds
work) and the last three (pouring, taking it apart, fixes) are the same in every mold guide;
molds-complete.pdf has all the molds and the sheet layout for the boards.

The build guide covers the casting itself (mix, pour, cure); this guide is everything before and
after that. All the sizes and hole positions come from the model (`model/build_cnc.py`), so if you
change the design, re-run it and the guides, hole maps and printed parts all follow.

![An upright mold: boards see-through, printed kit in orange, foam in blue](../../renders/build/05-mold-upright.png)

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

**Fits** are 0.15 mm a side: snug, but they go together by hand. Board thickness matters: the
saddles and cradles are drawn for 19.05 mm board (Home Depot's 3/4 in white melamine is a true
0.750 in). Measure yours; if it differs, set `mold_board` in `model/build_cnc.py` and re-run it.

## 2. What you need

| Material | Amount | Notes |
|---|---|---|
| Melamine board, 19 mm (3/4 in) | about 1.0 m2 | all the molds come out of two 4 x 8 ft sheets (layout in molds-complete.pdf) |
| PETG | 0.31 kg | this mold's printed parts (sliced); all the molds and machine parts fit in two 1 kg rolls |
| Paste wax (Partall #2) and PVA | 1 each | release, 3-5 coats |
| 3/8 in quarter-round molding (PVC) | a few meters | the 10 mm outside edges of the castings |
| 2x4 offcut | 4 blocks per upright mold | 52 mm long |

**Hardware** (zinc-plated is fine; grease anything that touches the mix). Buy about 10 % spare of the
small bolts, nuts and washers.

| Item | Qty |
|---|---|
| M4 nut | 42 |
| M4 washer | 42 |
| M4 x 30 bolt | 24 |
| M4 x 35 bolt | 4 |
| M4 x 45 bolt | 14 |
| 1/2-13 x 1-1/2 in bolt + nut, greased (forms the dowel hole) | 2 |
| 3/8-16 x 2-1/2 in bolt, greased (holds the top plate) | 4 |
| 5/8 in plain steel rod, greased (forms a tie-rod hole), cut to 140 mm, 243 mm, 377 mm, 377 mm | 2 |

**Tools:** a drill with sharp brad-point bits (sizes in section 5) and a 2-1/2 in hole saw; a jigsaw or a circular saw for the upright side plates' sloped edge; a square and a long straightedge; a few clamps; a 7 mm nut driver and a 3 mm hex key; a marker that writes on melamine.

## 3. Print the parts

42 prints, 0.31 kg of PETG and about 24 hours of printing, sliced in Bambu Studio for an A1 mini (settings in the
print guide). Print one corner bracket and one saddle first and check them on an offcut of your
board: the saddle should drop over it with a little play.

| Folder | File | Qty | g (all) | Time each |
|---|---|---|---|---|
| upright | `kit-back-bracket.stl` | 4 | 21 | 27m 33s |
| upright | `kit-front-bracket.stl` | 4 | 32 | 38m 27s |
| upright | `kit-saddle-flat.stl` | 4 | 18 | 22m 40s |
| upright | `filler-toe-filler.stl` | 2 | 54 | 1h 33m 58s |
| upright | `former-foot-gasket-groove-part1of4.stl` | 2 | 7 | 17m 8s |
| upright | `former-foot-gasket-groove-part2of4.stl` | 2 | 3 | 8m 46s |
| upright | `former-foot-gasket-groove-part3of4.stl` | 2 | 3 | 8m 46s |
| upright | `former-foot-gasket-groove-part4of4.stl` | 2 | 7 | 17m 10s |
| upright | `plug-slope-plug-lower.stl` | 2 | 19 | 45m 49s |
| upright | `plug-slope-plug-upper.stl` | 2 | 19 | 45m 47s |
| upright | `plug-tie-rod-pocket.stl` | 4 | 33 | 39m 54s |
| upright | `kit-plate-spacer.stl` | 4 | 15 | 20m 9s |
| upright | `kit-post-bushing.stl` | 4 | 68 | 1h 11m 44s |
| upright | `cast-in-post-l1-plug.stl` | 4 | 14 | 15m 49s |

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
| Upright floor | 2 | 198 x 575 |  |
| Upright side plate, outer | 2 | 495 x 271 (profile) | cut to the profile |
| Upright side plate, inner | 2 | 495 x 271 (profile) | cut to the profile |
| Upright back board | 2 | 80 x 271 |  |
| Upright front board | 2 | 80 x 312 | ends cut square |
| Upright bridge | 2 | 131 x 108 |  |
| Upright cleat, outer | 2 | 405 x 40 | offcut strip, flat on the floor |
| Upright cleat, inner | 2 | 405 x 40 | offcut strip, flat on the floor |
| Upright cleat, back | 2 | 80 x 40 | offcut strip, flat on the floor |

The upright side plates are cut to a profile (their drawings give the corners): cut the rectangle,
then the sloped front edge. The front board's ends are square.

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
| 3.2 mm | 1/8 in | foot-gasket-groove |
| 4.5 mm | 11/64 in | cleat, corner bracket, saddle, slope-plug-lower, slope-plug-upper, toe-filler |
| 10 mm | 25/64 in | 3/8-16 bolt into the top plate |
| 13.1 mm | 33/64 in | 1/2-13 bolt, base dowel hole |
| 16.3 mm | 41/64 in | 5/8 core rod |
| 63.5 mm | 2-1/2 in hole saw | hole saw |

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

## 6. Prepare the surfaces

- Wax every face the mix touches, boards and removable printed pieces alike: 3-5 thin coats of paste
  wax, each buffed, then a coat of PVA. Don't wax the pieces that stay in (core posts, cast-in parts):
  scuff them and wipe them with acetone so the epoxy grips.
- The castings' outside edges are rounded 10 mm: glue 3/8 in quarter-round molding into the inside
  corners that form outside edges (floor to wall), and run a small silicone fillet into the others.
- Grease every screw, bolt and rod that will come out of the casting.

## 7. Put the mold together

### Uprights (two molds, cast together)

The uprights are cast foot down. Both are the same, so build two of everything.

1. Push the post bushings into the floor from below and pin the gasket-groove bead to it. Bolt the cleats down.

![Upright, step 1](../../renders/mold/step-upright-1.png)

2. Stand the side plates against their cleats and the back board between them; fit the two back brackets.

![Upright, step 2](../../renders/mold/step-upright-2.png)

3. Bolt the toe filler to the floor between the side plates, set the front board's foot in its lip and fit the two front brackets at the top.

![Upright, step 3](../../renders/mold/step-upright-3.png)

4. Stand the mold on its four 2x4 blocks. Push the posts up through the bushings onto the bench, and the greased 5/8 in rods up through the floor: the two short ones into the slope plugs (bolted to the front board), the two long ones on through the top. The dowel-hole bolt and nut go in from underneath.

![Upright, step 4](../../renders/mold/step-upright-4.png)

5. Fill to the line and vibrate. Then slide the top pocket plugs down the long rods, hang the top plate from the bridge on its greased 3/8 bolts and spacers, and drop the bridge onto its saddles.

![Upright, step 5](../../renders/mold/step-upright-5.png)

![The toe filler holds the front board's foot](../../renders/mold/detail-toe.png)

## 8. Pouring, and the pour line

- The pour line is 25 mm below the wall tops. Mark it inside each wall with a pencil line, and
  screed the top with a straight board that has two 25 mm feet riding on the wall tops.
- Vibrate each layer until it stops bubbling; the brackets and cleats hold the walls, so you can vibrate
  the floor board hard. Check the corner brackets and saddle bolts are still tight halfway through.
- Keep the mix off the bridges and saddles; scrape it off before it cures.

## 9. Taking it apart, and reuse

1. Leave it the full cure time (build guide). Unbolt the bridges and saddles, then the corner
   brackets, then the cleats; pull the walls straight off (a plastic wedge in the corner helps).
2. Unscrew every insert screw, coupler bolt and rod from outside, then lift the casting off the floor
   (or the floor off the casting).
3. Unbolt and pull the formers and fillers (the bolts come out from the board side first). A wooden
   dowel and a light tap frees a stuck one.
4. Scrape the boards, re-wax them, and store the kit pieces with their nuts in a box per mold. The
   same kit does the next casting; only the formers and pieces that stay in are per casting.

## 10. If something doesn't fit

| Problem | Fix |
|---|---|
| A nut won't slide under the hole | Clean the pocket with a nut on a bolt; a warm nut (hair dryer) pushes in |
| A bracket or saddle is loose on the board | Your board is thinner than set: shim with tape, or set `mold_board` and reprint |
| A pin won't go into its hole | Run a 1/8 in bit through the hole again; trim the pin tip with a knife |
| A foam core moves while pouring | Check its post bolt is tight and the post is glued; add carpet tape under it |
| Mix leaks at a corner | A silicone fillet inside the corner before waxing; check the diagonals and brackets |
| A former is stuck after curing | Bolts out first; then a dowel and a light tap from its thick end |
