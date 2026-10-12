# Documents

Everything to build the machine, one folder per stage, in the order you need them. Each folder has
PDFs to print or read on a tablet; the Markdown they come from is in `src/`, and most of it is
written by the model (`model/build_cnc.py`), so it stays in step with the design.

## 1. Sourcing: what to buy

- [sourcing.pdf](1-sourcing/sourcing.pdf): every part with a listing, price and notes, in three parts (frame,
  electronics, enclosure and coolant), with totals. [sourcing.csv](1-sourcing/sourcing.csv) is the same list
  for a spreadsheet.
- [laser/](1-sourcing/laser/README.md): DXFs of the steel to order laser cut: the upright top plates (two
  layers each) and the base anchor bars the tie rods pull against.

## 2. Printing: start this first

- [print-guide.pdf](2-printing/print-guide.pdf): every printed part (STLs in `print/`), the slicer settings,
  how the pieces join, and the filament each takes, sliced in Bambu Studio. About 1.4 kg of PETG and a
  hundred-odd hours of printing, so start it while the rest is on order.

## 3. Molds: making the molds

- [molds-complete.pdf](3-molds/molds-complete.pdf): all the molds, with the sheet layout for the boards.
- One guide per mold, each complete on its own (how the molds work, that mold's parts, hardware, boards,
  foam and steps): [base-mold.pdf](3-molds/base-mold.pdf) (both base halves),
  [upright-molds.pdf](3-molds/upright-molds.pdf), [beam-mold.pdf](3-molds/beam-mold.pdf).
- Full-size drilling templates to print on Letter paper and tape onto the boards, with the pour line on every
  wall: [base](3-molds/templates/base-templates.pdf), [uprights](3-molds/templates/upright-templates.pdf),
  [beam](3-molds/templates/beam-templates.pdf). The first page of each says how to print and use them.

## 4. Build: casting and assembly

- [build-guide.pdf](4-build/build-guide.pdf): the whole build. The same in stages, for the bench:
  1. [1-steel.pdf](4-build/1-steel.pdf): tools, space and safety; buying and preparing the steel.
  2. [2-casting.pdf](4-build/2-casting.pdf): the molds (summary) and the mix, test bars and casting.
  3. [3-frame.pdf](4-build/3-frame.pdf): joining the castings (grouting the dowels, the tie rods) and bedding the rail risers.
  4. [4-axes-electronics.pdf](4-build/4-axes-electronics.pdf): rails, ballscrews, motors, wiring, spindle.
  5. [5-enclosure-commissioning.pdf](4-build/5-enclosure-commissioning.pdf): enclosure, flood coolant, first cuts.

## 5. Design: how it works and why

- [design-notes.pdf](5-design/design-notes.pdf): the frame and its joints, the stiffness and vibration
  study, chips and coolant, cost, and reference dimensions.
- [report.txt](5-design/report.txt): the model's numbers: dimensions, casting volumes and masses, the BOM,
  the enclosure cut list and the collision check.
