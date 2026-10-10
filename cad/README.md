# DIY CNC model

Fixed-gantry, epoxy-granite desktop mill sized like the Shariff DMC2 Mini
(180 x 300 x 140 mm travel), with a 2020/ACM enclosure mounted on the base and a clear lift-up door.

| File | What it is |
|---|---|
| `build_cnc.py` | Layout, enclosure, collision check, report, document. All dimensions in `P`. |
| `parts.py` | Component geometry built from the reference drawings below. |
| `DIYCNC.FCStd` | Colored FreeCAD model. Edit `posX`, `posY`, `posZ`, `doorAngle` in the `Params` sheet to jog the axes and open the door; set `explode` (e.g. 180) to pull the frame apart, `sumpOut` (e.g. 300) to slide the coolant sump out. |
| `DIYCNC.step` | Same assembly for Fusion 360, Onshape, Blender, etc. |
| `report.txt` | Key dimensions, casting mass, BOM, enclosure cut list, collision results. |
| `BUILD.md` | Step-by-step build: steel prep, moulds, casting, frame assembly, bedding the risers, axes, electronics, enclosure, commissioning. |
| `fea/` | Frame stiffness model and the base topology optimization (see Stiffness study). |
| `sourcing.md`, `sourcing.csv` | Parts to buy, with Amazon (and a few other) listings and prices checked 2026-10-09. |
| `renders/` | Snapshots, including the coolant system, way covers, cable chain, nozzles, Z axis and table drive. `frame_bare*`, `frame_section_*` and `gasket_*` show the castings on their own, with the gaskets drawn in blue (the real cord is black) and the printed liners, sleeves and plugs in orange. |

## Frame

Five epoxy-granite castings that bolt together, each with cast-in steel:

| Module | Steel inside | Joins to |
|---|---|---|
| Base front | 2x 2x2x1/8 in tubes (12 in) under the table rails, hollow, sockets for the split spigots, 2x M12 draw rods, the coolant outlet, O-ring groove on the split face | Rear half: 1-1/2 in spigots slide inside the sockets (printed sleeves take up the clearance); the draw rods pull it tight from pockets in the front face |
| Base rear | 2x 2x2x1/8 in tubes (12 in), 2x 1-1/2 in spigots (6 in), 4 printed socket liners, M12 coupling nuts | - |
| Upright (x2) | 2x 1-1/2x1-1/2x1/8 in posts (12 in) that stick out the bottom, 3/8 in top plate, O-ring groove under the foot | Posts drop into the lined sockets, a dowel locates it, 2x M12 tie rods pull it down |
| Beam (140 deep x 140 high) | 2x 2x2x1/8 in tubes (18 in), drilled 14 mm where the inner cap screws pass | A dowel and 4x M10 cap screws per side into the upright top plates |

**Nothing you buy gets cut.** The rails (including the 600 mm Y pair), ballscrews and tube are
used at the lengths they're sold in: tube in 18, 12 and 6 in pieces of two US sizes (remnants
are fine, lengths +/- 1/4 in, 0.120 in wall works as well as 1/8 in). The risers, aluminium
plates and the upright top plates are ordered cut to size. The only cutting left is the M12
threaded rod. The only machining is drilling the beam tubes (4 holes each) and drilling and
tapping the risers, top plates and support pads. Use plain steel, not galvanized: epoxy bonds
poorly to zinc. Wire-brush off rust and loose scale and degrease just before casting; paint only the
part of each leg that hangs below the base.

**Keeping the epoxy down.** About 10.3 kg of epoxy (10 % of 103 kg of casting):
- The base sockets, posts and legs stay hollow. Printed plugs close their ends so no mix
  gets in; fill them with dry sand first if you want extra damping. The beam tubes are
  filled, because the cap screws pass through them.
- The base's underside pockets follow the stiffness study below: two full-depth girders
  (80 mm wide) under the table rails, a full-depth tie between them just behind the split,
  solid knees from the girders out to the upright sockets, and a 25 mm top skin almost
  everywhere else. The 70 mm front wall carries the coolant trough. Every pocket is open
  to the bottom, so the cores (printed shells or foam blocks) pull straight out; a few are
  shallow steps (40 or 65 mm deep) under the trough band, the draw rods, the knees and
  outboard of the sockets (`base_pockets` in `build_cnc.py`).
- The sockets are printed PETG liners cast into the base, not steel tube.
- The mix matters as much as the geometry. Use a well-graded aggregate (gravel up to about
  10 mm, sand, fine sand, and silica flour or fly ash) and vibrate it. A good mix gets to
  about 9 % epoxy, which saves roughly another 1 kg.

**What the rails and supports bolt to.** Nothing bolts to the cast-in tubes; they stiffen
the castings and form the joints. The rails screw into steel risers, and the risers are bedded
on the castings with a thin epoxy grout and held down by counterbored M5 screws (under the
rail, between its own screws) into cast-in inserts: 5 per riser on the base (Y), 4 on the beam
(X). The Y ballscrew supports (BK12/BF12) bolt into M6 inserts in the base top. The X supports
(BK10/BF10) sit over the front beam tube, where an insert won't fit, so they bolt to two
1/4 in steel pads cast flush into the beam face and bearing on the tube. The Z axis mounts on
the aluminium plates and needs no inserts. See `BUILD.md`.

The enclosure's 2020 frame bolts to the base top with angle brackets into cast-in
M5 inserts, so the base is the enclosure floor. Seal the top with an epoxy gel coat;
coolant runs to the two drains at the front. The door laps over the base front face.

Assembly: base halves (spigots in, tighten the draw rods), uprights (posts into
sockets, tighten the tie rods), beam (cap screws), axes, enclosure. To break it down,
take the X and Y motors off first (they pass through the enclosure panels), then
reverse the order. Heaviest piece: the rear base half.

## Stiffness study (`fea/`)

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
| **Now: + riser hold-downs, support pads, uncut 600 mm Y rails** | **43.7 L** | **55.7** | **96.8** | **68.9** |

- The beam is the biggest share of the deflection, then the base and the uprights about
  equally. Litre for litre, epoxy in the beam is worth roughly ten times as much as epoxy
  in the base, so the beam now fills the upright tops (140 deep instead of 120).
- In the new frame the beam is still the biggest share. Making the uprights rigid would add
  about 75 / 25 / 85 % in X / Y / Z, and making the base rigid about 70 / 70 / 35 %. The
  uprights are only 3.1 L each, so per litre they're the next place to add material (wider
  or deeper, which also grows the base and the enclosure).
- The optimization (`fea/topopt.py`, pockets open to the bottom) puts the base material
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

Figures in `fea/figs` (and `renders/frame_base_underside.png`): `base_current.png` (the
previous base), `base_final.png` (solid depth from the top
in each column), `base_pocket_*` and `base_free_*` (optimization results at 18-28.5 L), and
`tradeoff.png` (base stiffness against base volume).

Rerun it with a Python that has numpy, scipy, matplotlib and scikit-sparse 0.5 or later
(older scikit-sparse falls back to a much slower solver):

```sh
/Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd cad/fea/voxelize.py   # -> fea/vox_current.*
cd cad/fea
python baseline.py                                  # stiffness and each module's share (about 1 min)
FEA_VOX=vox_previous sh run_sweep.sh                # base optimizations (about 10 min each)
FEA_VOX=vox_previous python evaluate.py to_*.npz    # table + figures
FEA_VOX=vox_current python whatif.py                # stiffness of the model as drawn
```

`vox_current` is whatever `build_cnc.py` draws now (`voxelize.py` rewrites it);
`vox_previous` is the frame before these changes, which the optimizations and the
"previous design" numbers above use. `VOX_P='{"beam_d": 160}' VOX_OUT=fea/vox_test` on the
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

**Checked against real listings (2026-10-09, `sourcing.md`): about $2,730 for the priced items,
plus 17 unpriced ones, so roughly $3.1-3.4k at Amazon prices.** Buying the tube, plate and
risers from a local steel yard should take roughly another $100-150 off. The estimate below was made
before that check and is too low; it assumed AliExpress-level prices. It's kept here to show
what each cost-down change saves.

Rough estimates in USD at hobby-supplier prices (AliExpress/Amazon-type sources, late
2026). They're not quotes; check current listings. The cost-down column keeps the
machine's capability: same travel, rigidity, spindle, closed-loop X/Y, flood coolant
and enclosure.

| Item | Before | Cost-down | Change |
|---|---|---|---|
| Epoxy + aggregate | $240-315 | $200-255 | Hollow rear base, 10 % epoxy mix (well-graded aggregate + silica flour/fly ash), bulk kits |
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

## Rebuilding

```sh
# collision check + report only
/Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd cad/build_cnc.py

# full rebuild: model, STEP, renders (opens and closes a FreeCAD window)
CNC_SNAPSHOTS=1 /Applications/FreeCAD.app/Contents/MacOS/FreeCAD "$PWD/cad/build_cnc.py"
```

Or in FreeCAD: Macro > Macros... > `build_cnc.py` > Execute.

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
