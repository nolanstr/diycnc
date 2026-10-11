# Beam mold

How to make, put together and take apart the mold for the beam. The first section (how the molds
work) and the last three (pouring, taking it apart, fixes) are the same in every mold guide;
molds-complete.pdf has all the molds and the sheet layout for the boards.

The build guide covers the casting itself (mix, pour, cure); this guide is everything before and
after that. All the sizes and hole positions come from the model (`model/build_cnc.py`), so if you
change the design, re-run it and the guides, hole maps and printed parts all follow.

![The beam mold: boards see-through, printed kit in orange, foam in blue](../../renders/build/06-mold-beam.png)

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
| Melamine board, 19 mm (3/4 in) | about 0.5 m2 | all the molds come out of two 4 x 8 ft sheets (layout in molds-complete.pdf) |
| PETG | 0.15 kg | this mold's printed parts (sliced); all the molds and machine parts fit in two 1 kg rolls |
| Paste wax (Partall #2) and PVA | 1 each | release, 3-5 coats |
| 3/8 in quarter-round molding (PVC) | a few meters | the 10 mm outside edges of the castings |

**Hardware** (zinc-plated is fine; grease anything that touches the mix). Buy about 10 % spare of the
small bolts, nuts and washers.

| Item | Qty |
|---|---|
| M4 nut | 26 |
| M4 washer | 26 |
| M4 x 30 bolt | 12 |
| M4 x 45 bolt | 10 |
| M4 x 70 bolt | 4 |
| M5 x 20 screw, greased (holds an insert) | 8 |
| M6 x 20 screw, greased (holds a pad) | 6 |
| 1/2 in plain steel rod, greased (forms a beam bolt hole), 198 mm | 8 |

**Tools:** a drill with sharp brad-point bits (sizes in section 5); a square and a long straightedge; a few clamps; a 7 mm nut driver and a 3 mm hex key; a marker that writes on melamine.

## 3. Print the parts

14 prints, 0.15 kg of PETG and about 12 hours of printing, sliced in Bambu Studio for an A1 mini (settings in the
print guide). Print one corner bracket and one saddle first and check them on an offcut of your
board: the saddle should drop over it with a little play.

| Folder | File | Qty | g (all) | Time each |
|---|---|---|---|---|
| beam | `kit-corner-bracket.stl` | 4 | 33 | 40m 3s |
| beam | `filler-back-edge-part1of4.stl` | 1 | 19 | 1h 14m 46s |
| beam | `filler-back-edge-part2of4.stl` | 1 | 19 | 1h 14m 46s |
| beam | `filler-back-edge-part3of4.stl` | 1 | 19 | 1h 14m 46s |
| beam | `filler-back-edge-part4of4.stl` | 1 | 19 | 1h 15m 1s |
| beam | `kit-tube-locator.stl` | 4 | 39 | 55m 37s |
| beam | `kit-dowel-stop.stl` | 2 | 2 | 6m 51s |

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
| Beam floor | 1 | 648 x 258 |  |
| Beam top wall | 1 | 568 x 165 |  |
| Beam bottom wall | 1 | 568 x 165 |  |
| Beam end wall, left | 1 | 140 x 165 |  |
| Beam end wall, right | 1 | 140 x 165 |  |
| Beam cleat, top | 1 | 568 x 40 | offcut strip, flat on the floor |
| Beam cleat, bottom | 1 | 568 x 40 | offcut strip, flat on the floor |
| Beam cleat, left | 1 | 140 x 40 | offcut strip, flat on the floor |
| Beam cleat, right | 1 | 140 x 40 | offcut strip, flat on the floor |

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
| 4.5 mm | 11/64 in | back-edge, cleat, corner bracket, tube locator |
| 5.5 mm | 7/32 in | M5 insert screw |
| 6.5 mm | 17/64 in | M6 insert screw |
| 9.6 mm | 25/64 in | 3/8 dowel |
| 13.1 mm | 33/64 in | 1/2 core rod |

#### Beam floor

![Beam floor](boards/beam-floor.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 80 | 20 | 4.5 | cleat |
| 2 | 324 | 20 | 4.5 | cleat |
| 3 | 568 | 20 | 4.5 | cleat |
| 4 | 174 | 79 | 5.5 | M5 insert screw |
| 5 | 294 | 79 | 5.5 | M5 insert screw |
| 6 | 354 | 79 | 5.5 | M5 insert screw |
| 7 | 474 | 79 | 5.5 | M5 insert screw |
| 8 | 20 | 99 | 4.5 | cleat |
| 9 | 628 | 99 | 4.5 | cleat |
| 10 | 94 | 106 | 6.5 | M6 insert screw |
| 11 | 107 | 106 | 6.5 | M6 insert screw |
| 12 | 452 | 106 | 6.5 | M6 insert screw |
| 13 | 94 | 152 | 6.5 | M6 insert screw |
| 14 | 107 | 152 | 6.5 | M6 insert screw |
| 15 | 452 | 152 | 6.5 | M6 insert screw |
| 16 | 20 | 159 | 4.5 | cleat |
| 17 | 628 | 159 | 4.5 | cleat |
| 18 | 174 | 179 | 5.5 | M5 insert screw |
| 19 | 294 | 179 | 5.5 | M5 insert screw |
| 20 | 354 | 179 | 5.5 | M5 insert screw |
| 21 | 474 | 179 | 5.5 | M5 insert screw |
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
| 9 | 84 | 133 | 4.5 | back-edge |
| 10 | 219 | 133 | 4.5 | back-edge |
| 11 | 351 | 133 | 4.5 | back-edge |
| 12 | 484 | 133 | 4.5 | back-edge |
| 13 | 33 | 154 | 4.5 | corner bracket |
| 14 | 535 | 154 | 4.5 | corner bracket |

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
| 1 | 70 | 44 | 4.5 | tube locator |
| 2 | 70 | 96 | 4.5 | tube locator |
| 3 | 14 | 154 | 4.5 | corner bracket |
| 4 | 126 | 154 | 4.5 | corner bracket |

#### Beam end wall, right

![Beam end wall, right](boards/beam-end-wall-right.svg)

| # | x | y | Hole | For |
|---|---|---|---|---|
| 1 | 70 | 44 | 4.5 | tube locator |
| 2 | 70 | 96 | 4.5 | tube locator |
| 3 | 14 | 154 | 4.5 | corner bracket |
| 4 | 126 | 154 | 4.5 | corner bracket |

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

## 6. Prepare the surfaces

- Wax every face the mix touches, boards and removable printed pieces alike: 3-5 thin coats of paste
  wax, each buffed, then a coat of PVA. Don't wax the pieces that stay in (core posts, cast-in parts):
  scuff them and wipe them with acetone so the epoxy grips.
- The castings' outside edges are rounded 10 mm: glue 3/8 in quarter-round molding into the inside
  corners that form outside edges (floor to wall), and run a small silicone fillet into the others.
- Grease every screw, bolt and rod that will come out of the casting.

## 7. Put the mold together

### Beam

The beam is cast with its front (rail) face down on the floor and its back open.

1. Bolt the cleats down; screw the support pads and riser inserts to the floor on greased screws.

![Beam, step 1](../../renders/mold/step-beam-1.png)

2. Stand the walls against the cleats and fit the four corner brackets.

![Beam, step 2](../../renders/mold/step-beam-2.png)

3. Bolt the tube locators through the end walls (M4 x 70 into the nut in each cross) and hang the tubes between them. Bolt the back-edge filler to the top wall, push the dowels into the bottom wall onto their printed stops, and slide the greased 1/2 in rods through both walls for the eight bolt holes. Fill to the line.

![Beam, step 3](../../renders/mold/step-beam-3.png)

![A tube locator: a cross in the tube end, bolted through the end wall](../../renders/mold/detail-locator.png)

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
