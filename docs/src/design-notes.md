# Design notes

Fixed-gantry, epoxy-granite desktop mill sized like the Shariff DMC2 Mini
(180 x 300 x 140 mm travel), with a 2020/ACM enclosure mounted on the base and a clear lift-up door.

This document explains the design: the frame, the coolant system, the stiffness study and
the cost. The repository layout and the rebuild commands are in the top-level `README.md`.

## Frame

Five castings that bolt together. Each is a **steel skeleton** of stock flat bar and tube, cut to length,
drilled from printed templates and clamped with threaded rod, cast into **epoxy granite**, which damps it
and adds stiffness. The steel is the frame: every joint between castings, and every rail, riser and
ballscrew support, bolts steel to steel. Nothing is welded, nothing is custom-cut, and nothing is
threaded into the epoxy granite (17 M5 inserts hold only the add-ons: the enclosure, the way-cover rollers
and the cable-chain mount).

| Module | Steel skeleton (all stock) | Joins to |
|---|---|---|
| Base, two halves | Per half: a 2x3 tube girder under each Y rail with a tapped 3/8 x 1-1/2 in rail bar bolted on top and a 3/8 x 2-1/2 in end plate at each end; a pedestal under each upright (3/8 x 2-1/2 in seat and bottom bars, a 2x2 tube spacer round each tie rod); 1-1/2 in cross tubes from girder to girder (at the split and under the Y ballscrew supports, with tapped pads bolted on) and from each girder to its pedestal, each clamped by a 1/2-13 rod | The halves meet end plate to end plate on four dowel pins, clamped by two 1/2-13 draw rods that run inside the girders from a front pocket to a back pocket. The front half is cast against the rear, so the joint fits by construction |
| Upright (x2), a raked buttress | A 3/8 x 2 in flat-bar foot, two 2x2 tube columns, a top plate of two 1/2 x 2-1/2 in flat bars (the lower one tapped); O-ring groove under the foot | Its foot bar bears on the base pedestal's seat bar. Three 1/2-13 tie rods (two inside the columns, screwed into the top plate; one from the toe, onto the foot bar) run right through the pedestal to its bottom bar. Two dowels, grouted into the foot at first assembly, locate it |
| Beam (140 deep x 146 high) | A 3/8 x 5 in face bar (the rail face, tapped) and back bar, held apart by three pipe nipples on studs; a 3/8 x 2-1/2 in seat and cap bar at each end | The seat bars bear on the upright top plates; at each end four 3/8-16 grade B7 studs, screwed into the top plate, clamp cap bar, face and back bars and seat bar down; a dowel (grouted at first assembly) locates it |

**Nothing is made to order.** The rails (including the 600 mm Y pair) and ballscrews are used at the
lengths they're sold in; the skeletons are about 54 pieces of stock flat bar and tube (46 kg) cut to
length (`docs/1-sourcing/steel/` has the cut list and the drilling templates); the risers and aluminum
plates are ordered cut to size. The cutting left is the threaded rod; the machining is drilling and
tapping (from the templates) and the risers. Use plain steel, not galvanized: epoxy bonds poorly to zinc.
Wire-brush off rust and loose scale and degrease just before casting; paint only the part of each leg
that hangs below the base.

**Keeping the epoxy down.** About 9.1 kg of epoxy (8.5 % of the 107 kg the castings would weigh with sand; 113 kg with the #16 grit):
- The tubes stay hollow (girders, columns, cross tubes, legs): their ends are closed by the plates and bars
  they're clamped between, or by printed rings and plugs, so no mix gets in.
- The base's underside pockets follow the stiffness study below, with the steel grid in the ribs
  between them: two full-depth girders (80 mm wide) under the table rails, a
  full-depth tie between them across the split, a full-depth rib across the front of each
  upright foot and another along the split, and a 20 mm top skin almost everywhere else,
  including over pockets under the upright feet that keep clear of the band under each upright
  where the pedestal runs. The 70 mm front wall carries the coolant trough. Every pocket is open to the
  bottom, so the cores (printed shells or foam blocks) pull straight out; a few are shallow
  steps (40 or 65 mm deep) under the trough band, the draw rods, the knees and outboard of
  the pedestals (`base_pockets` in `model/build_cnc.py`).

**Molds and fits.** The molds are a kit (`model/moldbox.py`, the mold guide): melamine boards, all from
one 4 x 8 ft sheet (a three-stage cut: the bridges and struts come out of the strips the walls leave), and
1x2 cleats, with every wall 25 mm above the pour line, held by printed brackets and saddles with M4 bolts
through that band, so no bolt passes through a cast face. Every printed piece bolts to its board
from outside into a captive nut (a bayonet pocket in the face against the board), or pins on if
it is too thin, and pieces cut to fit the printer are pegged together. The hidden pocket
cores are XPS foam, which keeps the printing to about 1 kg of PETG (sliced in Bambu Studio). A clash check in the
model keeps the kit, the boards, the castings and the steel apart. Two joints are made to fit by
construction instead of by measuring: the front base half is cast against the rear half
(flush top faces, matching split faces, end plates straight onto the dowel pins), and the dowels
are grouted into oversize holes at first assembly, so two independent molds don't have to agree.
The two uprights are the same part, so one mold casts both, one after the other.
- The mix matters as much as the geometry. Use a well-graded aggregate (gravel up to about
  10 mm, sand, fine sand, and whiting, i.e. calcium carbonate powder) and vibrate it. The
  split in the build guide follows a modified Fuller curve, P(d) = (d^q - d_min^q) / (D^q - d_min^q)
  with D = 10 mm and q about 0.45: q = 0.5 (classic Fuller) is a little coarse and needs more
  epoxy to wet, q = 0.37 (Andreasen) packs tighter but its extra powder soaks up epoxy.
- **Aluminum oxide in the beam and uprights.** Alumina grit (E about 370 GPa for brown fused,
  a little less for black, against about 70 for quartz and granite) replaces the coarse sand,
  volume for volume, in those three castings only (`analysis/alumina.py`): brown #16, one 50 lb
  bag. A differential-effective-medium estimate of the mix (the plain mix comes out at 34 GPa,
  close to the 30 GPa the frame model uses) puts it 22 % stiffer with the #16 alone, 10 % with
  black 70 grit alone (for the fine sand) and 37 % with both. On the frame as drawn now, where
  the steel skeleton carries most of the load, that is worth much less than it was on the
  all-epoxy-granite frame (+17 %):

  | Grit in the beam and uprights | X | Y | Z | Grit |
  |---|---|---|---|---|
  | None (sand) | 89.2 | 137.8 | 117.0 | |
  | #16 in the beam only | 92.8 | 147.5 | 124.1 | ~$70 (two 12 lb bags) |
  | Both grits, beam only | 95.0 | 153.1 | 128.4 | ~$105 |
  | **#16, beam and uprights (drawn)** | **96.5** | **150.2** | **128.8** | **$110** |
  | Both grits, beam and uprights | 101.0 | 157.8 | 136.3 | $150 |

  So the #16 is about +5 % for $110 and the 70 grit another +5 % for $40: the 70 grit is an
  option (decided before the pour). Even with plain sand the frame is more than twice as stiff as
  the ballscrews. It's an estimate, so the build guide's tap-tested bars check it, and sand is
  the fallback. Other options:
  **Graded industrial quartz** (Agsco and similar) is clean, dry and
  consistent but costs more and ships heavy; pool filter sand is the local equivalent.
  **Ceramic microspheres** (Zeeospheres) help the mix flow at low epoxy, but whiting does most
  of that for far less. **Epoxy grout** (Laticrete SpectraLock) is fine for a test bar or a
  repair, but it's fine-grained (about 15-20 % binder) and far too expensive for 130 kg. Whiting is
  used instead of silica flour because it has no crystalline silica: a plain dust mask is enough. A good mix gets to
  8.5 % epoxy, which fits a single 3 gal kit (10 % needs a second, small kit); the build guide's
  jar test and test bars check it before anything is cast.

**What the rails and supports bolt to.** Steel. The rails screw into steel risers, and the risers
are bedded on the castings with a thin epoxy grout and held down by counterbored M5 screws (under
the rail, between its own screws) into the skeleton: the base's tapped rail bars (Y) and the beam's
tapped face bar (X). The Y ballscrew supports (BK12/BF12) bolt into tapped pads on the base grid's
cross tubes; the X supports (BK10/BF10) into the beam's face bar. Behind every tapped hole there's room
(the casting is relieved where the greased mold screw stood, or a relief hole is drilled in the tube
below). The Z axis mounts on the aluminum plates.

**Load path.** A cutting force goes spindle, Z plate, Z and X blocks, X rails, steel risers, the beam's
face bar and the steel behind it; at each end the seat bar bears on the upright's top plate, clamped by
four 3/8-16 studs; down the upright's columns to its foot bar, which bears on the base pedestal's seat
bar; the three tie rods clamp that whole stack (top plate, columns, foot bar, seat bar, pedestal
spacers, bottom bar) from the top plate to the nuts under the base; across the base grid (the cross
tubes and their rods, the girders, the split end plates on their dowel pins, clamped by the draw
rods); and back up through the Y rail bars, risers, rails and blocks to the table. Steel all the way,
and every nut in that chain can be reached and retightened: the tie-rod nuts under the base and in
the toe pockets, the draw-rod nuts in the front and back pockets, the stud nuts on the beam top. The
epoxy granite fills round and between the steel, in compression where the rods clamp; it damps the
frame and adds stiffness. The stiffness study treats it as bonded to the steel.

The steel is bolted, not welded. A welded skeleton would have to be welded before casting (and pulls
out of square doing it) or after (the heat ruins the epoxy next to it), and it would make the frame
one piece. Bolted from stock and drilled from templates, it goes together without a jig, the mold
screws and dowels put every tapped face where the templates say, and the five castings still come
apart.

**Steel tolerances.** A supplier's saw cut is good to about 1/8 in, and A500 tube is about 0.5 mm off
nominal with a weld seam inside. Each piece is set from one end and its other end has room
(`tube_cut_tol`, checked in the report). Each upright column is clamped up against its top plate, its
foot in a 4.8 mm epoxy bed on the foot bar; each girder is clamped between its end plates by the draw
rod, set from the split; the pedestal spacers set where the bottom bar sits, which only moves it a
little against the underside; the rods are screwed up to a stop at one end and have a 6 mm tail past
the far nut. The printed rings that center the columns on their rods have 0.5 mm a side (`tube_fit`)
and grooves for the seam. If the tube that arrives is further off, put its calipered sizes in
`frame_tube` / `post_tube` and re-run before printing.

The enclosure's 2020 frame bolts to the base top with angle brackets into cast-in
M5 inserts, so the base is the enclosure floor. Seal the top with an epoxy gel coat;
coolant runs to the two drains at the front. The door laps over the base front face.

Assembly: base halves (end plates onto the dowel pins, tighten the draw rods), uprights (dowels grouted into the
feet the first time, tighten the tie rods), beam (cap screws), axes, enclosure. To break it down,
take the X and Y motors off first (they pass through the enclosure panels), then
reverse the order. Heaviest piece: the rear base half (about 42 kg). The upright feet run
forward across the base split, so the base halves have to be joined before the uprights go on.

## Stiffness study (`analysis/`)

A finite-element model of the frame was used to see where the epoxy granite does the most
good, and a topology optimization was run on the base.

**Model.** The castings and cast-in steel are voxelized from this model at 10 mm (66k brick
elements). Each voxel's stiffness is its mix of epoxy granite (E = 30 GPa) and steel; the
joints between castings are treated as bonded, which is what the preload is for. A
1 kN force on the tool goes into the beam through the X blocks (the X component through
the X ballscrew to its BK bearing) and, reversed, into the base through the Y blocks (the Y
component through the Y screw to its BK). The result is the frame's own stiffness at the
tool, tool against work, for X at the center and end, the table at both ends and the
center, and the tool 50 mm above the table. Rails, blocks, screws and the spindle are not
in it; the screws alone are roughly 30-50 N/um, so the frame should stay well above that.

**Findings** (frame only, N/um at the tool, mean over the load cases):

| Frame | Epoxy granite | X | Y | Z |
|---|---|---|---|---|
| Previous design | 42.4 L | 48.9 | 80.7 | 57.9 |
| Same, base made rigid | | 87.2 | 130.9 | 80.2 |
| Same, uprights rigid | | 83.3 | 103.9 | 102.6 |
| Same, beam rigid | | 122.9 | 175.7 | 125.9 |
| Base with no pockets at all (+14 L) | 56.8 L | 61.5 | 90.1 | 67.0 |
| Beam 120 -> 140 mm deep only (+1.5 L) | 43.9 L | 51.1 | 90.9 | 63.8 |
| Optimized base + 140 mm beam | 43.7 L | 54.0 | 94.5 | 68.0 |
| + riser hold-downs, support pads, uncut 600 mm Y rails | 43.7 L | 55.7 | 96.8 | 68.9 |
| Base + uprights optimized together, same material (free-form uprights) | 43.7 L | 63.9 | 103.3 | 85.2 |
| Raked-buttress uprights, base re-laid around them | 52.6 L | 77.5 | 107.5 | 93.0 |
| + blunt upright toe, rounded edges, deeper slope pockets | 53.0 L | 78.2 | 110.1 | 95.5 |
| + alumina grit in the beam and uprights (estimate) | 53.0 L | 91.3 | 127.3 | 115.7 |
| Lighter base (pockets under the upright feet, 20 mm skin), 9 kg less | 49.5 L | 84.3 | 124.5 | 111.1 |
| Same, tie rods not counted as glued in (they sit in clearance holes; the rows below do the same; `vox_before_chain`) | 49.3 L | 81.6 | 121.9 | 107.6 |
| + tie rods right through the base to steel anchor bars, two-layer top plates | 50.5 L | 86.8 | 124.7 | 111.6 |
| + posts and sockets taken out, a second dowel per foot | 52.4 L | 86.3 | 124.2 | 110.1 |
| + upright feet 260 mm ahead of the beam (from 290) | 51.3 L | 84.2 | 123.0 | 109.3 |
| + steel skeletons in the uprights and a steel box in the beam (all 3/8 in) | 47.9 L | 96.0 | 132.7 | 130.9 |
| + steel grids in the base (all 3/8 in) | 45.8 L | 107.1 | 153.5 | 138.1 |
| Slimmed: webs, cross plates and braces 1/4 in with windows, 3/8 in foot plates (64 laser-cut plates) | 48.5 L | 99.7 | 146.9 | 124.7 |
| All stock flat bar and tube, bolted (no custom parts), beam 146 mm high | 44.8 L | 101.0 | 157.8 | 136.3 |
| **Now: the same with the #16 grit only (the 70 grit is an option)** | **44.8 L** | **96.5** | **150.2** | **128.8** |

- **Steel skeletons.** Making the steel the frame (epoxy granite cast round it) makes the frame stiffer
  than the last all-epoxy-granite design. The first version was 64 custom laser-cut plates slotted
  together (+18 / +19 / +14 %); the one drawn now is all stock flat bar and tube, cut to length, drilled
  from templates and bolted, and comes out stiffer still: +20 / +28 / +25 % (101.0 / 157.8 / 136.3 N/um
  with both grits; 96.5 / 150.2 / 128.8 with the #16 only, as drawn now), with modes 132 / 262 / 299 Hz
  (133 / 265 / 300 with both grits), about 60 kg of steel and hardware and 113 kg of castings (the hollow
  girder tubes take some epoxy granite out of the base). It loses the laser version's upright brace and
  beam diaphragms but gains the base girders' and the beam bars' depth.

- **The steel chain** (tie rods from the top plates to anchor bars under the base) is worth
  +6 / +2 / +4 % (the bars, the thicker top plates and the solid band left under each foot
  together). It also makes the
  posts redundant: with the feet clamped through steel they were worth under 1.5 %, so they're
  gone, and with them the sockets, the post bushings and the post grouting (a second grouted dowel
  per foot locates it instead). The stiffness left over paid for 30 mm off each upright foot.
  The frame ends up +3 / +1 / +2 % stiffer than before the chain, with modes 136 / 268 / 303 Hz
  (from 132 / 265 / 282), and about 6 kg heavier (the bars and the thicker top plates). A 250 mm
  foot keeps the static stiffness but drops mode 2 below the old frame; shorter than that the
  front foot pockets run past their mold bridges. Thinner uprights and a thinner front wall
  didn't pay.

- The beam is the biggest share of the deflection, then the base and the uprights about
  equally. Liter for liter, epoxy in the beam is worth roughly ten times as much as epoxy
  in the base, so the beam now fills the upright tops (140 deep instead of 120).
- In the new frame the beam is still the biggest share. Making the uprights rigid would add
  about 75 / 25 / 85 % in X / Y / Z, and making the base rigid about 70 / 70 / 35 %. The
  uprights are only 3.1 L each, so per liter they're the next place to add material (wider
  or deeper, which also grows the base and the enclosure).
- **Uprights.** Optimizing the base and the uprights together (`analysis/topopt_frame.py`,
  one shared budget, the uprights free to grow anywhere beside the table under the beam) moves
  about 3 L from the base into the uprights and turns each upright into a raked buttress: the
  foot runs about 300 mm forward along the base and the front face slopes up to just ahead of
  the beam (`analysis/figs/frame_34.6_upright.png`). That alone, at the same total material, is
  +15 / +7 / +24 % in X / Y / Z. With 4 L less material in total the frame ends up about 20 %
  less stiff than before, so cutting material isn't worth it.
- The castable version drawn now is a solid full-width buttress (one sloped board in the
  mold, no cores) with its foot 290 mm ahead of the beam face: 5.3 L per upright (5.5 L since
  the toe got a 20 mm nose). The base
  was then re-optimized around the longer feet (`analysis/figs/frame2_base_*.png`): it wants
  full depth under the feet and a wider tie across the split. Total +8.9 L of epoxy granite
  (about $75) for +39 / +11 / +35 %.
- The base optimization (`analysis/topopt.py`, pockets open to the bottom) puts the base material
  into girders under the rails, a tie between them behind the split and knees to the
  sockets, and takes it out of the perimeter walls, the cross rib at the split and the
  skin. The castable version drawn here has the same volume as before (28.4 L) and is 5 %
  stiffer on average (at least 3 % in every load case); the beam change adds the rest.
- The cast-in steel is mostly there for the joints. Replacing the base tubes with solid
  casting would cost only about 1 %; the beam tubes are worth 6-7 %. Six #6 rebars instead of
  the beam tubes would be about 3 % less stiff, so the tubes stay.
- Cutting epoxy from the base is cheap in money but expensive in stiffness. At the
  optimized layout's best: 24.5 L matches the old base, 21 L loses 11 %, and below about
  18.5 L (the minimum skin, walls and cover around the steel) it falls off fast. Epoxy
  granite costs about $8.50/L, so even the best case saves about $35. A free-form base
  with closed box sections (lost foam cores) is only about 8 % stiffer than open pockets
  at the same volume, which isn't worth the trouble.
- **Weight** (`analysis/weight.py`, `to_light_*`). With the alumina grit in the beam and
  uprights there was stiffness to spare, so the base was optimized again at smaller budgets.
  Free-form (ideal) pockets: 27 L of base is 14 kg lighter for -7 / -1 / -2 %, 24 L is 21 kg
  lighter and still at the sand-only frame's stiffness, 21 L drops below it. Nearly all of
  it comes out from under the upright feet, which the earlier, larger budget had filled. The
  castable version keeps a rib across the front of each foot and along the split and leaves
  room around the tie-rod couplers and the sockets: base 32.8 -> 29.1 L, castings 9 kg
  lighter, frame -8 / -2 / -4 % against the alumina frame and still +8 / +13 / +16 % over
  the sand-only one. The simple trims don't pay: 60 mm girders leave under 5 mm of casting
  beside the rail tubes, and a 55 mm front wall runs the pockets into the legs.

**Material and the 8.5 % mix.** The model uses E = 30 GPa for the epoxy granite. Published
values for well-graded 7-10 % mixes are 25-45 GPa (one commercial mineral casting lists
25 GPa); the university studies use 15-30 % resin with powder fillers and aren't comparable.
Granite is about 70 GPa and the epoxy about 3 GPa, so a lower epoxy fraction is as stiff or
stiffer as long as every stone is wetted and there are no voids; what it gives up is a little
damping (the resin does the damping) and some margin against dry spots. The frame's stiffness
scales almost directly with E:

| E of the epoxy granite | X | Y | Z |
|---|---|---|---|
| 20 GPa | 58.0 | 80.3 | 72.3 |
| 25 GPa | 68.3 | 95.5 | 84.1 |
| **30 GPa (assumed)** | **78.2** | **110.1** | **95.5** |
| 35 GPa | 87.9 | 124.4 | 106.6 |
| 40 GPa | 97.3 | 138.4 | 117.4 |

So the packing of the mix matters more than the last percent of epoxy. The build guide's jar
test and tap-tested bars check both before anything is cast.

**Vibration** (`analysis/modal.py`). The frame on its four feet, with 12 kg of X carriage, Z axis
and spindle on the beam blocks and 12 kg of table, vise and work on the Y blocks, with the #16 grit
only as drawn now (`FEA_GRIT=1.22`) and with the 70 grit too (`FEA_GRIT=1.37`). The 70 grit
raises them by 1-2 %:

| Mode | #16 only (drawn) | Both grits | Motion |
|---|---|---|---|
| 1 | **132 Hz** | 133 Hz | gantry sways side to side (X); base twisting on its feet carries 40 % of it |
| 2 | **262 Hz** | 265 Hz | beam rocks front to back (Y) |
| 3 | **299 Hz** | 300 Hz | base bends, front to back |
| 4 | **353 Hz** | 360 Hz | gantry sway with the base, second form |

Bricks this coarse run a little stiff, so the real frequencies are probably 10-20 % lower.
Mode 1 is at the bottom of the tooth-pass band for steel (roughly 130-400 Hz: 4,000-8,000 rpm
with 2-3 flutes) and modes 2-4 are inside it. That's normal for a machine this size; the frame is still several times stiffer than
the spindle and tool (static X/Y/Z above), and chatter on a mill like this usually
comes from the spindle, Z axis and tool. If a frequency rings, change the spindle speed by
10-20 % rather than the frame. A solid bench (the base twisting on its feet is in every mode)
and sand in the hollow tubes and legs help more than geometry changes.

**Lightening holes in the uprights** (`analysis/topopt_upright.py`, `compare_uprights.py`).
The uprights were optimized again on their own, with the cuts forced to go straight through
(windows) or to stop at a 20 mm web on the inner face (pockets from the outside), keeping 90 %
and 80 % of their material (run on the frame before the toe and edge cleanup, which added
1-3 %):

| Uprights (both) | Removed | X | Y | Z | Mode 1 / 2 | Epoxy saved |
|---|---|---|---|---|---|---|
| Solid, as drawn | | 77.5 | 107.5 | 93.0 | 135 / 264 Hz | |
| One window each, 90 % | 1.05 L, 2.5 kg | 75.0 | 106.5 | 91.2 | 136 / 263 Hz | ~$3 |
| One outer pocket each, 90 % | 1.05 L | 75.6 | 106.8 | 92.0 | 136 / 261 Hz | ~$3 |
| Two windows each, 80 % | 2.1 L, 4.9 kg | 71.7 | 104.8 | 88.9 | 136 / 255 Hz | ~$6 |
| Two outer pockets each, 80 % | 2.1 L | 73.1 | 105.6 | 90.3 | 135 / 254 Hz | ~$6 |

The holes land where you'd expect, in the low-stress middle of the buttress just ahead of
the front post (`analysis/figs/upright_*.png`), but they don't pay: 10 % of the upright costs
1-3 % of the frame's stiffness and saves about $3 of epoxy (the 3 gal kit is bought either
way), and the natural frequencies don't move because the mass that matters is the beam and
the head on top. Each window would also need a printed liner. The uprights stay solid; the
frame optimization above already moved material into them, not out.

Figures in `analysis/figs` (and `renders/frame_base_underside.png`): `frame_34.6_*` (base and
uprights optimized together), `frame2_base_*` (base around the new uprights), `base_current.png` (the
previous base), `base_final.png` (solid depth from the top
in each column), `base_pocket_*` and `base_free_*` (optimization results at 18-28.5 L), and
`tradeoff.png` (base stiffness against base volume), `upright_*` (lightening holes, at 90 and
80 % of the upright).

Rerun it in the `diycnc` conda env (`environment.yml`: numpy, scipy, matplotlib and
scikit-sparse 0.5 or later; older scikit-sparse falls back to a much slower solver):

```sh
/Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd analysis/voxelize.py   # -> analysis/vox_current.*
conda env create -f environment.yml                 # once
conda activate diycnc
cd analysis
python baseline.py                                  # stiffness and each module's share (about 1 min)
FEA_VOX=vox_previous sh run_sweep.sh                # base optimizations (about 10 min each)
FEA_VOX=vox_previous python evaluate.py to_*.npz    # table + figures
FEA_VOX=vox_current python whatif.py                # stiffness of the model as drawn
# voxelize with VOX_SKIP=TieRod,DrawRod,CrossRod so the rods in their clearance holes don't count as glued in
python alumina.py                                   # alumina grit: mix modulus and frame stiffness
FEA_GRIT=1.37 python -c "import topopt; topopt.main('pocket', 24, tag='light_24')"   # lighter base
python weight.py vox_current [vox_...]              # castings mass against stiffness
FEA_GRIT=1.22 python modal.py                       # natural frequencies (about 30 s)
python topopt_upright.py 0.9 [web]                  # upright holes (about 10 min each)
python compare_uprights.py to_upright_*.npz         # their stiffness and frequencies
```

`vox_current` is whatever `build_cnc.py` draws now (`voxelize.py` rewrites it);
`vox_previous` is the frame before these changes, which the optimizations and the
"previous design" numbers above use. `VOX_P='{"beam_d": 160}' VOX_OUT=analysis/vox_test` on the
voxelize command tries a parameter change.

## Chips and coolant

| Stage | What | Where in the model |
|---|---|---|
| Collect | Sealed base top; gutters between the uprights and the enclosure walls fall toward a trough across the front, which falls to one outlet | `BaseFrontCasting`, `BaseRearCasting` |
| Protect | Roll-up 0.1 mm stainless strips in front of and behind the table, a spiral spring cover on the rear screw, a drip shield over the beam rails, brush seals where the motors pass through the panels | `WayCovers`, `CoverRoller*`, `DripShield`, `BrushSeal*` |
| Drain | The trough drops straight down through the front wall to a cast-in brass nipple over the chip basket | `DrainOutlet` |
| Clean | Slide-out sump under the base, between four 6 in steel legs cast into the corners: a full-size 4 in stainless steam-table pan (~13 L, ~9 L working). Front to back: 1/3-size perforated pan as the chip basket, magnet bar, printed underflow baffle, 100 um screen in a printed frame, pump | `Sump*`, `Leg*` |
| Return | 24 V brushless submersible pump (switched by the controller's M8 output; no mains in the coolant), push-to-connect at the pump, hose under the base and up the back to a bulkhead in the back panel, along the printed cable chain, a loop down to a manifold on the spindle clamp, two Loc-Line nozzles | `ReturnHose`, `Bulkhead`, `CoolantLines`, `CoolantNozzle*` |

To empty or clean the sump, pop the hose off the pump and slide the pan out the front (set
`sumpOut` in the `Params` sheet to see it pulled out). The legs raise the machine 117 mm and
it still sits on four M12 leveling feet, now in the leg ends. Use a water-soluble coolant
and keep it topped up; skim tramp oil off the clean end now and then.

**Add later, fixed now.** The covers, the sump and the enclosure can come later, but whatever they fix
to is in the castings already, so nothing is recast:

| Add-on | Fixing | Where in the model |
|---|---|---|
| Way-cover rollers | Front: an M5 insert behind the coolant trough for each end bracket's foot. Rear: an insert outboard of each roller, and an M5 hole tapped in the BK12 pad beside the support for each inner foot | `roller_layout`, `CoverRoller*` |
| Spiral screw cover | None: it clamps between the nut housing and the BK12 | `CoverScrewRear` |
| Drip shield | The four front beam studs: its back edge goes under their washers (the studs are 190 mm, long enough for the 3 mm ACM) | `DripShield` |
| Cable-chain mount | Two M5 inserts in the beam top | `ChainMountFixed` |
| Enclosure | 11 M5 inserts in the base top | `rail_bolts` |
| Flood coolant | The trough, gutters and cast-in drain; room for the sump between the legs | `base_top_formers`, `DrainOutlet` |
| Homing switches | None: Y on the Y motor bracket, X and Z on the X carriage | |

**Cable chain.** One printed chain on top of the beam carries the coolant line, Z motor,
spindle power and spindle water hoses to the carriage (17 links, 38 x 21 outer, 20 mm
pitch, R38). Print it in PETG, not PLA. The model shows a simplified link; for the
real parts, start from a proven printable parametric chain sized to about 30 x 15 inside
and print three links to check the fit before printing the rest. The table and Z axes
don't need chains: the table carries no cables and Z uses a short service loop.

**Parts that change shape with the axes.** The way-cover strips, the screw cover, the
cable chain and the nozzle hose are drawn for the home position. The collision check
and the renders rebuild them at every pose, but jogging `posX` / `posY` / `posZ` in the
GUI won't redraw them; re-run the macro to see them elsewhere.

## Cost

**Checked against real listings (2026-10-09/12, the sourcing list).** The list is in three parts:
**1, the frame** (castings, steel, rails, ballscrews) about **$1,603**, plus about **$183 of add-later
niceties** (way covers, screw cover, stainless sump and chip basket, grease gun) that bolt on whenever
they're bought; **2, the electronics and spindle** about **$430** plus the spindle the builder picks
($250-375 for a 1.5 kW 110 V kit, $430-600 for the 2.2 kW kit with a 120 V step-up VFD); **3, the
enclosure and flood coolant** about $650-700. The steel and aluminum are priced as remnants and the joint
hardware from a hardware store; the remnant prices are estimates.

**Frame cost-down (2026-10-12).** The frame was $1,839 with everything in it. The changes, none of
which gives up travel, rigidity to speak of, chip protection or the coolant system:

| Change | Frame |
|---|---|
| Before | $1,839 |
| Missing or low lines added: a third B7 rod, the PVA film, the quarter-round and silicone | +$47 |
| Add-later niceties out of the frame total (they bolt to fixings cast in now, below; $183 with cheaper springs and screw cover) | -$210 |
| Their stand-ins for the first chips: a grease syringe, a bin under the drain | +$20 |
| #16 grit only; the 70 grit is an option (96.5 / 150.2 / 128.8 N/um against 101.0 / 157.8 / 136.3) | -$40 |
| One melamine sheet (one upright mold for both, three-stage cut) and 1x2 cleats | -$36 |
| Mold hardware and rods to the real counts; low-head screws by the piece | -$24 |
| More fine sand (it replaces the 70 grit) | +$7 |
| **Now** | **$1,603** |

What would take it further, all on the builder's side of the list: a steel-yard quote for the cut list
(about $220 at $2/lb, against the $300 estimate), AliExpress motor brackets and couplers (about $50 less,
2-4 weeks), and the #16 in the beam only (about $40 less for -3 to -4 %; plain sand everywhere is about
$100 less for -8 to -9 % against the drawn frame). The aluminum plates are the risk the other way: without
drops, cut plate is about $120-190 against the $85 estimate.

The estimate below was made before the listings were checked and is too low; it assumed
AliExpress-level prices. It's kept here to show what each earlier cost-down change saves.

Rough estimates in USD at hobby-supplier prices (AliExpress/Amazon-type sources, late
2026). They're not quotes; check current listings. The cost-down column keeps the
machine's capability: same travel, rigidity, spindle, closed-loop X/Y, flood coolant
and enclosure.

| Item | Before | Cost-down | Change |
|---|---|---|---|
| Epoxy + aggregate | $240-315 | $200-255 | Hollow rear base, 8.5 % epoxy mix (well-graded aggregate + whiting fines), bulk kits |
| Cast-in steel, rods, dowels, fasteners | $90-140 | $90-140 | |
| Rail risers | $60-90 | $25-40 | Cold-rolled flat bar bedded in epoxy and replicated, instead of MIC6 strips |
| MIC6 table, carriage, Z plate | $120-180 | $120-180 | Remnant/drop plate is often much cheaper |
| Rails + blocks (table, Z) | $110-160 | $110-160 | Beam rails owned |
| Ballscrew kits (table, Z) | $70-100 | $70-100 | Beam kit owned |
| X/Y closed-loop motors + drivers | $170-220 | $140-180 | 2 Nm 23HS30-E1000: lower inductance, holds torque better at speed, 37 mm shorter |
| Brackets, couplers | $20-30 | $20-30 | One bracket owned |
| Spindle, VFD, clamp, cooling loop | $280-370 | $280-370 | |
| Electronics | $150-200 | $150-200 | |
| Enclosure | $220-300 | $145-210 | 3 mm ACM walls and roof; polycarbonate only in the door |
| Coolant system | $105-180 | $105-180 | |
| Way covers, seals | $65-105 | $65-105 | |
| Lubrication | $40-60 | $10-15 | Grease gun on the blocks' grease nipples instead of a central pump |
| Gaskets, inserts, feet | $30-45 | $30-45 | |
| Printed cable chain | $3 | $3 | PETG |
| **Total** | **~$1,780-2,500** | **~$1,560-2,210** | |

Bigger savings mean giving something up. Options, roughly in order of impact:

- **Phase it.** Build without the enclosure and flood coolant first (mist or air
  blast). That saves about $250-400 up front. The base still has the gutters and
  mounting inserts, so both can be added later.
- **Polyester instead of epoxy** for the castings: about half the resin cost, but it
  shrinks more, so you rely more on the epoxy-replicated mounting surfaces.
- **1.5 kW 110 V spindle** instead of the 2.2 kW you can upgrade to 240 V later:
  about $40-70 cheaper, less power for steel.
- **Open-loop motors** on X/Y: about $60-80 cheaper, but you lose stall and crash detection.

## Reference dimensions

| Component | Source | Notes |
|---|---|---|
| HGR15 rail, HGH15CA block | HIWIN Linear Guideway catalog G99TE23-2203, HG series (p.38) | Ball-groove positions are not published; estimated. |
| SFU1204 / SFU1605 nuts, screw end machining | TBI Motion SFU sheet L010974 (via Anaheim Automation) | |
| BK10/BK12, BF10/BF12 supports | TBI Motion sheets L011175 (BK), L011178 (BF) | BK locknut size estimated. BK12 counterbore depth (1.5) is as printed; worth checking. |
| DSG16H nut housing | makerstore.cc drawing TR-BS-DSG16-00 | |
| DSG12H nut housing (24 mm bore) | zyltech / vxb listings | Center height and holes estimated. |
| NEMA 23 motors | StepperOnline drawings 23HS45-4204D-E1000, 23HS30-5004D-E1000, 23HS30-3004S | |
| Motor bracket | No published drawing | Sized from kit listings: motor face ~47 mm from the BK. |
| D25 L30 coupler | Seller listings (5 N·m, 8x10 / 6.35x10 bores) | Hub depth estimated. |
| GDZ80-2.2 spindle | StepperOnline drawings GDZ80-2.2A/B | Some features scaled from the drawing (±1 mm). Body length varies by seller (213/230/240): measure yours. |
| 80 mm cast clamp | cnconline.co.za 80 mm spindle bracket drawing | 148 W x 80 D, 14 foot, bore center 50 off the foot. |
| ER20 nut | DIN 6499 / spindle drawing | Chinese spindles ship a 30 AF hex nut. |
| 2020 extrusion | Misumi HFS5-2020 catalog p.2-511 | Owned V-slot is OpenBuilds profile (6.25 throat). |

Before casting anything, measure the parts you actually have, especially the
owned ANWOK rails, blocks and SFU1204 kit. Clone parts can differ from these
catalogs by a millimeter or two.
