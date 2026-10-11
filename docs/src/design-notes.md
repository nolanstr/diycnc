# Design notes

Fixed-gantry, epoxy-granite desktop mill sized like the Shariff DMC2 Mini
(180 x 300 x 140 mm travel), with a 2020/ACM enclosure mounted on the base and a clear lift-up door.

This document explains the design: the frame, the coolant system, the stiffness study and
the cost. The repository layout and the rebuild commands are in the top-level `README.md`.

## Frame

Five epoxy-granite castings that bolt together, each with cast-in steel:

| Module | Steel inside | Joins to |
|---|---|---|
| Base front | 2x 2x2x1/8 in tubes (12 in) under the table rails, hollow, sockets for the split spigots, 2x 1/2-13 draw rods, the coolant outlet | Rear half: 1-1/2 in spigots slide inside the sockets (printed sleeves take up the clearance); the draw rods pull it tight from pockets in the front face. Cast against the rear half, so the joint fits by construction |
| Base rear | 2x 2x2x1/8 in tubes (12 in), 2x 1-1/2 in spigots (6 in), 4 printed socket liners, 1/2-13 coupling nuts, O-ring groove on the split face | - |
| Upright (x2), a raked buttress | 2x 1-1/2x1-1/2x1/8 in posts (12 in) that stick out the bottom, 3/8 in top plate, O-ring groove under the foot | Posts are grouted into the oversize sockets at first assembly (waxed, so they lift out), a dowel locates it, 4x 1/2-13 tie rods pull it down (two from pockets at the top, two from pockets in the sloped front) |
| Beam (140 deep x 140 high) | 2x 2x2x1/8 in tubes (18 in), drilled 14 mm where the inner cap screws pass | A dowel (grouted into an oversize plate hole at first assembly) and 4x 3/8-16 bolts per side into the upright top plates |

**Nothing you buy gets cut.** The rails (including the 600 mm Y pair), ballscrews and tube are
used at the lengths they're sold in: tube in 18, 12 and 6 in pieces of two US sizes (remnants
are fine, lengths +/- 1/4 in, 0.120 in wall works as well as 1/8 in). The risers, aluminium
plates and the upright top plates are ordered cut to size. The only cutting left is the 1/2-13
threaded rod. The only machining is drilling the beam tubes (4 holes each) and drilling and
tapping the risers, top plates and support pads. Use plain steel, not galvanized: epoxy bonds
poorly to zinc. Wire-brush off rust and loose scale and degrease just before casting; paint only the
part of each leg that hangs below the base.

**Keeping the epoxy down.** About 9.9 kg of epoxy (8.5 % of the 116 kg the castings would weigh with sand; 126 kg with the alumina):
- The base sockets, posts and legs stay hollow. Printed plugs close their ends so no mix
  gets in; fill them with dry sand first if you want extra damping. The beam tubes are
  filled, because the cap screws pass through them.
- The base's underside pockets follow the stiffness study below: two full-depth girders
  (80 mm wide, the narrowest that still fills around the rail tubes) under the table rails, a
  full-depth tie between them across the split, a full-depth rib across the front of each
  upright foot and another along the split, and a 20 mm top skin almost everywhere else,
  including over pockets under the upright feet that keep clear of the tie-rod couplers and
  sockets. The 70 mm front wall carries the coolant trough. Every pocket is open to the
  bottom, so the cores (printed shells or foam blocks) pull straight out; a few are shallow
  steps (40 or 65 mm deep) under the trough band, the draw rods, the knees and outboard of
  the sockets (`base_pockets` in `model/build_cnc.py`).
- The sockets are cast on foam blocks (dug out after) and grouted to the posts at assembly, not steel tube.

**Moulds and fits.** The moulds are a kit (`model/mouldbox.py`, the mould guide): melamine boards
with every wall 25 mm above the pour line, held by printed brackets and saddles with M4 bolts
through that band, so no bolt passes through a cast face. Every printed piece bolts to its board
from outside into a captive nut (a bayonet pocket in the face against the board), or pins on if
it is too thin, and pieces cut to fit the printer are pegged together. The hidden pocket and socket
cores are XPS foam, which keeps the printing to about 1.5 kg of PETG. A clash check in the
model keeps the kit, the boards, the castings and the steel apart. Two joints are made to fit by
construction instead of by measuring: the front base half is cast against the rear half
(flush top faces, matching split faces, tubes straight onto the spigots), and the posts and
dowels are grouted into oversize holes at first assembly. Two independent moulds can't hold
the 0.2 mm a side the old printed socket liners needed.
- The mix matters as much as the geometry. Use a well-graded aggregate (gravel up to about
  10 mm, sand, fine sand, and whiting, i.e. calcium carbonate powder) and vibrate it. The
  split in the build guide follows a modified Fuller curve, P(d) = (d^q - d_min^q) / (D^q - d_min^q)
  with D = 10 mm and q about 0.45: q = 0.5 (classic Fuller) is a little coarse and needs more
  epoxy to wet, q = 0.37 (Andreasen) packs tighter but its extra powder soaks up epoxy.
- **Aluminium oxide in the beam and uprights.** Alumina grit (E about 370 GPa for brown fused,
  a little less for black, against about 70 for quartz and granite) replaces the sand, volume
  for volume, in those three castings only (`analysis/alumina.py`): brown #16 for the coarse
  sand, black 70 grit for the fine sand. A differential-effective-medium estimate of the mix
  (the plain mix comes out at 34 GPa, close to the 30 GPa the frame model uses) puts it
  22 % stiffer with the #16 alone, 10 % with the 70 grit alone and 37 % with both. On the
  frame, both come to about +17 / +16 / +21 % in X / Y / Z for $150 (a 50 lb and a 25 lb
  bag); the #16 alone is about +10 %. Doing the base as well would take about 60 kg more grit
  for another 8-11 %. It's an estimate, so the build guide's tap-tested bars check it, and
  sand is the fallback. Other options:
  **Graded industrial quartz** (Agsco and similar) is clean, dry and
  consistent but costs more and ships heavy; pool filter sand is the local equivalent.
  **Ceramic microspheres** (Zeeospheres) help the mix flow at low epoxy, but whiting does most
  of that for far less. **Epoxy grout** (Laticrete SpectraLock) is fine for a test bar or a
  repair, but it's fine-grained (about 15-20 % binder) and far too expensive for 126 kg. Whiting is
  used instead of silica flour because it has no crystalline silica: a plain dust mask is enough. A good mix gets to
  8.5 % epoxy, which fits a single 3 gal kit (10 % needs a second, small kit); the build guide's
  jar test and test bars check it before anything is cast.

**What the rails and supports bolt to.** Nothing bolts to the cast-in tubes; they stiffen
the castings and form the joints. The rails screw into steel risers, and the risers are bedded
on the castings with a thin epoxy grout and held down by counterbored M5 screws (under the
rail, between its own screws) into cast-in inserts: 5 per riser on the base (Y), 4 on the beam
(X). The Y ballscrew supports (BK12/BF12) bolt into M6 inserts in the base top. The X supports
(BK10/BF10) sit over the front beam tube, where an insert won't fit, so they bolt to two
1/4 in steel pads cast flush into the beam face and bearing on the tube. The Z axis mounts on
the aluminium plates and needs no inserts. See the build guide.

The enclosure's 2020 frame bolts to the base top with angle brackets into cast-in
M5 inserts, so the base is the enclosure floor. Seal the top with an epoxy gel coat;
coolant runs to the two drains at the front. The door laps over the base front face.

Assembly: base halves (spigots in, tighten the draw rods), uprights (posts grouted into the
sockets the first time, tighten the tie rods), beam (cap screws), axes, enclosure. To break it down,
take the X and Y motors off first (they pass through the enclosure panels), then
reverse the order. Heaviest piece: the rear base half (about 38 kg). The upright feet run
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
tool, tool against work, for X at the centre and end, the table at both ends and the
centre, and the tool 50 mm above the table. Rails, blocks, screws and the spindle are not
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
| **Now: lighter base (pockets under the upright feet, 20 mm skin), 9 kg less** | **49.5 L** | **84.3** | **124.5** | **111.1** |

- The beam is the biggest share of the deflection, then the base and the uprights about
  equally. Litre for litre, epoxy in the beam is worth roughly ten times as much as epoxy
  in the base, so the beam now fills the upright tops (140 deep instead of 120).
- In the new frame the beam is still the biggest share. Making the uprights rigid would add
  about 75 / 25 / 85 % in X / Y / Z, and making the base rigid about 70 / 70 / 35 %. The
  uprights are only 3.1 L each, so per litre they're the next place to add material (wider
  or deeper, which also grows the base and the enclosure).
- **Uprights.** Optimizing the base and the uprights together (`analysis/topopt_frame.py`,
  one shared budget, the uprights free to grow anywhere beside the table under the beam) moves
  about 3 L from the base into the uprights and turns each upright into a raked buttress: the
  foot runs about 300 mm forward along the base and the front face slopes up to just ahead of
  the beam (`analysis/figs/frame_34.6_upright.png`). That alone, at the same total material, is
  +15 / +7 / +24 % in X / Y / Z. With 4 L less material in total the frame ends up about 20 %
  less stiff than before, so cutting material isn't worth it.
- The castable version drawn now is a solid full-width buttress (one sloped board in the
  mould, no cores) with its foot 290 mm ahead of the beam face: 5.3 L per upright (5.5 L since
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

**Vibration** (`analysis/modal.py`, run with `FEA_GRIT=1.37` for the alumina). The frame as drawn
on its four feet, with 12 kg of X carriage, Z axis and spindle on the beam blocks and 12 kg of
table, vise and work on the Y blocks:

| Mode | Frequency | Motion |
|---|---|---|
| 1 | 135 Hz | gantry sways side to side (X); base twisting on its feet carries 39 % of it |
| 2 | 268 Hz | beam rocks front to back (Y) |
| 3 | 290 Hz | base bends, front to back |
| 4 | 359 Hz | gantry sway with the base, second form |

Bricks this coarse run a little stiff, so the real frequencies are probably 10-20 % lower.
Mode 1 is at the bottom of the tooth-pass band for steel (roughly 130-400 Hz: 4,000-8,000 rpm
with 2-3 flutes) and modes 2-4 are inside it. That's normal for a machine this size; the frame is still several times stiffer than
the spindle and tool (static X/Y/Z above), and chatter on a mill like this usually
comes from the spindle, Z axis and tool. If a frequency rings, change the spindle speed by
10-20 % rather than the frame. A solid bench (the base twisting on its feet is in every mode)
and sand in the hollow posts and sockets help more than geometry changes.

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

Rerun it with a Python that has numpy, scipy, matplotlib and scikit-sparse 0.5 or later
(older scikit-sparse falls back to a much slower solver):

```sh
/Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd analysis/voxelize.py   # -> analysis/vox_current.*
cd analysis
python baseline.py                                  # stiffness and each module's share (about 1 min)
FEA_VOX=vox_previous sh run_sweep.sh                # base optimizations (about 10 min each)
FEA_VOX=vox_previous python evaluate.py to_*.npz    # table + figures
FEA_VOX=vox_current python whatif.py                # stiffness of the model as drawn
python alumina.py                                   # alumina grit: mix modulus and frame stiffness
FEA_GRIT=1.37 python -c "import topopt; topopt.main('pocket', 24, tag='light_24')"   # lighter base
python weight.py vox_current [vox_...]              # castings mass against stiffness
python modal.py                                     # natural frequencies (about 30 s)
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

**Checked against real listings (2026-10-09/10, the sourcing list).** The list is in three parts:
**1, the frame** (castings, steel, rails, ballscrews, chip protection) about **$1,562** (including $150 of alumina grit for the beam and uprights, and about $200 for the
bolt-together mould kit: two sheets of melamine, its hardware, a sheet of XPS foam and the PETG); **2, the
electronics and spindle** about **$430** plus the spindle the builder picks ($250-375 for a 1.5 kW
110 V kit, $430-600 for the 2.2 kW kit with a 120 V step-up VFD); **3, the enclosure and flood
coolant** about $650-700. The steel and aluminium are priced as remnants and the joint hardware
from a hardware store; the remnant prices are estimates. The estimate below was made
before that check and is too low; it assumed AliExpress-level prices. It's kept here to show
what each cost-down change saves.

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
| DSG12H nut housing (24 mm bore) | zyltech / vxb listings | Centre height and holes estimated. |
| NEMA 23 motors | StepperOnline drawings 23HS45-4204D-E1000, 23HS30-5004D-E1000, 23HS30-3004S | |
| Motor bracket | No published drawing | Sized from kit listings: motor face ~47 mm from the BK. |
| D25 L30 coupler | Seller listings (5 N·m, 8x10 / 6.35x10 bores) | Hub depth estimated. |
| GDZ80-2.2 spindle | StepperOnline drawings GDZ80-2.2A/B | Some features scaled from the drawing (±1 mm). Body length varies by seller (213/230/240): measure yours. |
| 80 mm cast clamp | cnconline.co.za 80 mm spindle bracket drawing | 148 W x 80 D, 14 foot, bore centre 50 off the foot. |
| ER20 nut | DIN 6499 / spindle drawing | Chinese spindles ship a 30 AF hex nut. |
| 2020 extrusion | Misumi HFS5-2020 catalog p.2-511 | Owned V-slot is OpenBuilds profile (6.25 throat). |

Before casting anything, measure the parts you actually have, especially the
owned ANWOK rails, blocks and SFU1204 kit. Clone parts can differ from these
catalogs by a millimetre or two.
