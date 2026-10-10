# Sourcing list

Parts to buy for the machine in `DIYCNC.FCStd` / `report.txt`, sourced on Amazon (US) where it
makes sense. Prices and stock were checked on **2026-10-09**. "?" means the price was not visible
(Amazon blocks automated page reads); check the live listing. Shipping and tax are not included.
Off-Amazon picks are marked "not Amazon": they are there because Amazon doesn't carry the part or
is much dearer. Rows marked (opt) are optional and are left out of the totals.

The same list is in `sourcing.csv` for a spreadsheet.

## Totals

| Section | Priced | Unpriced items |
|---|---|---|
| Motion and drives | $522.50 | 0 |
| Spindle and electronics | $367.78 | 14 |
| Castings and frame | $1,267.80 | 0 |
| Enclosure, coolant and covers | $573.92 | 3 |
| **Total** | **$2,732.00** | **17** |

The unpriced items are mostly the 120 V VFD, the electrical parts, the ACM sheet, the sump pump
and the spiral cover. My rough estimate for them is another $450-750 (not checked), so the build comes to roughly $3.2-3.5k
before shipping.

**Where the money goes:** the frame section: casting materials ~$360, aluminium plate ~$240,
steel tube and plate ~$245, rods and fasteners ~$190, risers ~$110. Then the enclosure
and coolant ($574), the spindle and VFD, and the closed-loop motors ($162).

**Cheapest places to cut:** buy the tube, top-plate steel and risers from a local steel yard
(offcuts or full lengths you cut yourself; estimated ~$100-150 less than the listings here) and
the silica flour from a pottery supplier (~$40 less); skip the flood coolant and enclosure at
first (~$550, see the README cost section); AliExpress versions of the rails, ballscrews,
spindle and VFD (often 30-50 % less, slower shipping). Retail cut-to-size shops (e.g. Metal
Supermarkets) were checked and cost more than these listings, about $820 for the tube,
risers and aluminium.

## Motion and drives

| Item | Spec | Qty | Listing | Price | Line | Notes |
|---|---|---|---|---|---|---|
| Y rails + blocks | HGR15 x2 at 600 mm + 4x HGH15CA | 1 kit | [iMetrx HGR15 kit, 2x 600 mm + 4x HGH15CA](https://www.amazon.com/dp/B0GJZ7D9NG) | $55.99 | $55.99 | Used at full length, no cutting. The listing calls the blocks "aluminum", which is probably wrong: check them for play. |
| Z rails + blocks | HGR15 x2 at 300 mm + 4x HGH15CA | 1 kit | [BEVDICNC 2x HGR15-300 + 4x HGH15CA](https://www.amazon.com/dp/B0BYYJKBB5) | $35.69 | $35.69 | Alt: CNCMANS B09N73DY32 $34.98 |
| Y ballscrew kit | SFU1605-550, BK12/BF12, DSG16H | 1 | [Ballscrew kit DSG16H + SFU1605-550 + BK/BF12](https://www.amazon.com/dp/B088ZF8R91) | $39.39 | $39.39 | Ships with a 6.35x10 coupler: use the 8x10 below |
| Z ballscrew kit | SFU1204-300, BK10/BF10, DSG12H | 1 | [CNCYEAH SFU1204 300 mm kit](https://www.amazon.com/dp/B09MJ3T5JZ) | $32.69 | $32.69 | Ships with a 6.35x8 coupler: use the 8x8 below |
| Z motor bracket | NEMA 23 + BK10 (HM10-57) | 1 | [ANWOK NEMA 23 steel bracket, SFU1204](https://www.amazon.com/dp/B09S3HMB7S) | $32.02 | $32.02 | Same bracket as your X one |
| Y motor bracket | NEMA 23 + BK12 (HM12-57) | 1 | [ANWOK NEMA 23 steel bracket, SFU1605](https://www.amazon.com/dp/B09S39Q1RT) | $31.36 | $31.36 | Alt: CNCMANS HM12-57 B09QS2S3BT $28.98 |
| X/Y closed-loop kits | 23HS30-5004D-E1000 2.0 Nm + CL57T | 2 | [STEPPERONLINE closed-loop kit 2.0 Nm + CL57T](https://www.amazon.com/dp/B0C694KQQP) | $81.00 | $162.00 | Exact model. Low stock when checked. |
| Z driver (owned motor) | DM542T | 1 | [STEPPERONLINE DM542T](https://www.amazon.com/dp/B06Y5VPSFN) | $32.99 | $32.99 | Check that your motor is 4.2 A or less |
| Motor power supply | 48 V, 3 drivers | 1 | [Mean Well LRS-350-48 (7.3 A)](https://www.amazon.com/dp/B013EU4KNK) | $37.13 | $37.13 | Trim to about 46 V: CL57T max input is 48 V |
| Couplers, Y | 8x10 mm, D25 L30 | 1 (3-pack) | [CNCTOPBAOS 8x10 plum coupling, 3 pcs](https://www.amazon.com/dp/B082TT7B84) | $13.99 | $13.99 | Spares; check that D25 fits inside the bracket |
| Couplers, Z | 8x8 mm, D25 L30 | 1 (2-pack) | [Yeebyee 8x8 plum coupling, 2 pcs](https://www.amazon.com/dp/B0GTV7VMZB) | $12.89 | $12.89 | The spare covers X if your kit came with 6.35x8 |
| Grease gun | Mini, 3 oz cartridges | 1 | [Performance Tool W54205 mini grease gun kit](https://www.amazon.com/dp/B002V0AIWW) | $17.59 | $17.59 |  |
| Needle tip | For the blocks' M4 nipples | 1 | [LubriMatic 05-037 needle](https://www.amazon.com/dp/B000FMO6XU) | $6.98 | $6.98 |  |
| Grease | Lithium NLGI 2 | 1 (3x3 oz) | [LubriMatic 11312, 3x 3 oz](https://www.amazon.com/dp/B01JM4PCVG) | $11.79 | $11.79 |  |
| (opt) M4 grease nipples | M4x0.7 straight | 1 pack | [HARFINGTON 15 pcs M4x0.7](https://www.amazon.com/dp/B0CLP8NGRJ) | $13.94 | $13.94 | Only if the block nipples are missing or the coupler won't seat |

**Priced subtotal: $522.50**

## Spindle and electronics

| Item | Spec | Qty | Listing | Price | Line | Notes |
|---|---|---|---|---|---|---|
| Spindle kit | 2.2 kW 80 mm ER20 water-cooled + 220 V VFD + clamp | 1 | [RATTMMOTOR 2.2 kW ER20 kit with VFD, clamp, pump](https://www.amazon.com/dp/B073TRP92V) | $250.96 | $250.96 | Its VFD needs 220 V in: keep it for the 240 V upgrade. Its pump is 220 V too. Alt with 13 ER20 collets included: B07JB3TJKR (price not seen). |
| VFD for 120 V now | 110-120 V in, 220 V 3-phase out, 400 Hz | 1 | [Huanyang 1.5 kW step-up VFD (110 V in, 220 V out)](https://www.amazon.com/dp/B0D62J4G22) | ? | ? | Caps the spindle at ~1.5 kW until 240 V. Ask the seller to confirm 400 Hz. Alt: a 110 V-out HY02D211B (B0775F4G47) with the V/f curve set to 110 V at 200 Hz gives full torque up to 12k rpm. |
| ER20 collet set | 1-13 mm | 1 | [Chiloskit ER20 13 pcs](https://www.amazon.com/dp/B08B1H4RSR) | $25.21 | $25.21 | Skip if the kit includes a set |
| Spindle water pump | 110 V submersible, ~80 W | 1 | [110 V 80 W submersible pump for water-cooled spindles](https://www.amazon.com/dp/B0B7W31NBF) | ? | ? | Make sure it is the 110 V version; many are 220 V. Runs in a 10-20 L bucket. |
| Spindle coolant | Distilled water + 10-20 % RV antifreeze | 1 | Local store | ? | ? | Stops algae and corrosion |
| (opt) Radiator | 240 mm with fans | 1 | [ASHATA 240 mm radiator + 2 fans](https://www.amazon.com/dp/B07HK7GVZY) | ? | ? | Only if the bucket warms up on long jobs |
| Controller | FluidNC, 6 axes, external drivers, RS485, 0-10 V | 1 | [Elecrow Corgi ESP32 FluidNC controller (not Amazon)](https://www.elecrow.com/corgi-esp32-6-axis-cnc-controller-for-fluidnc.html) | $49.00 | $49.00 | Runs gSender or the web UI; no Windows license. Alt: DDCSV3.1 standalone B07SR854D1 (about $250-330 elsewhere). |
| 0-10 V spindle module | For the controller | 1 | [Elecrow FluidNC 0-10 V module](https://www.elecrow.com/6x-cnc-controller-for-fluidnc.html) | $11.00 | $11.00 | Check whether the Corgi already has 0-10 V built in |
| Spindle pump relay | SSR, DC in, 120 V AC out | 1 | [Aexit SSR-25DA](https://www.amazon.com/dp/B07L81H1LD) | ? | ? | Runs the 110 V spindle water pump whenever the spindle runs. Fuse the branch. |
| Homing sensors | Inductive NPN NO, M12 | 1 (5-pack) | [LJ12A3-4-Z/BX, 5 pcs](https://www.amazon.com/dp/B0D1R8RLMW) | ? | ? | Power them from 12 V, not 5 V |
| Tool setter | NC, magnetic base | 1 | [Z touch tool setter](https://www.amazon.com/dp/B0D42C32MR) | ~$31.61 | $31.61 | Price may belong to a neighbouring listing |
| E-stop | 22 mm mushroom, latching, in a box | 1 | [Shopcorp E-stop with box](https://www.amazon.com/dp/B0C8BGDVTH) | ? | ? | Wire it to cut drive enable and VFD run in hardware |
| Mains inlet, logic | IEC C14 with switch + fuse | 1 (4-pack) | [Oiyagai C14 inlet, switch, fuse](https://www.amazon.com/dp/B078N95379) | ? | ? | Logic, 48 V supply and pump only (6 A switch) |
| Mains inlet, VFD | IEC C20, 16/20 A | 1 | [Interpower 83030420](https://www.amazon.com/dp/B00917YXTW) | ? | ? | The VFD draws 15-20 A on 120 V: a 20 A circuit |
| Logic power supply | 24 V DIN rail | 1 | [Mean Well HDR-60-24](https://www.amazon.com/dp/B077BBD1K9) | ? | ? |  |
| Spindle cable | 14/4 shielded, 3 m | 1 (10 ft) | [LINKSQ 14/4 shielded](https://www.amazon.com/dp/B0DVQ61DS6) | ? | ? | Shield to earth at the VFD end |
| Stepper/sensor cable | 18/4 shielded | 1 (50 ft) | [Linear Motion Labs 18/4 shielded](https://www.amazon.com/dp/B01GZ50P7Q) | ? | ? |  |
| Electrical box | Steel, room for VFD + PSUs | 1 | [VEVOR 20x16x8 in enclosure](https://www.amazon.com/dp/B0924BN1P5) | ? | ? | 16x12x6 (B09247D9LH) is tight with the VFD inside. Add a filtered fan. |
| DIN rail + terminals | UK2.5B kit | 1 | [Erayco terminal block kit](https://www.amazon.com/dp/B07KRDJCYB) | ? | ? |  |
| Cable glands | PG7-PG19 | 1 (50 pcs) | [Bates nylon glands](https://www.amazon.com/dp/B09W9Q5HMH) | ? | ? |  |

**Priced subtotal: $367.78** + 14 unpriced: VFD for 120 V now, Spindle water pump, Spindle coolant, Spindle pump relay, Homing sensors, E-stop, Mains inlet, logic, Mains inlet, VFD, Logic power supply, Spindle cable, Stepper/sensor cable, Electrical box, DIN rail + terminals, Cable glands

## Castings and frame

| Item | Spec | Qty | Listing | Price | Line | Notes |
|---|---|---|---|---|---|---|
| Epoxy | ~10.6 kg low-viscosity laminating epoxy | 1 (3 gal) | [US Composites 635 Thin, 2 gal + 1 gal (not Amazon)](https://www.uscomposites.com/epoxy.html) | $185.30 | $185.30 | About $15/kg. Amazon alt: TotalBoat 2:1 Slow 3 gal B07N98VC3Z $354.99. Avoid deep-pour casting resins. |
| Fines | Silica flour 200-325 mesh, 10-15 kg | 1 (50 lb) | [Florock ground silica, 50 lb](https://www.amazon.com/dp/B00V7WOFAQ) | $94.37 | $94.37 | Mesh not stated. A pottery supplier sells 200 mesh for about half (e.g. $53 / 50 lb). Wear a respirator. |
| Aggregate | ~106 kg graded sand + pea gravel | ~5 bags | [Quikrete sand + Vigoro pea gravel (Home Depot)](https://www.homedepot.com/p/Vigoro-0-5-cu-ft-Bagged-Pea-Gravel-Pebble-Landscape-Rock-54255/202523000) | ~$7/bag | $40.00 | Buy locally. Wash and dry fully. |
| Mould release wax | Partall Paste #2 | 1 | [Partall Paste #2, 12 oz](https://www.amazon.com/dp/B0BQCZ8C3K) | $18.52 | $18.52 |  |
| Mould release PVA | Partall Film #10 | 1 qt | [Partall PVA, quart](https://www.amazon.com/dp/B09MY7PZ6D) | $22.99 | $22.99 |  |
| Square tube 2x2x1/8, 12 in | Base tubes (split sockets) | 4 | [Rocaris 2x2x1/8 steel square tube, 12 in](https://www.amazon.com/dp/B0FYPR4YJV) | $24.99 | $99.96 | Bought at length. Steel-yard remnants are cheaper (0.120 wall is fine). Plain steel, not galvanized. |
| Square tube 2x2x1/8, 18 in | Beam tubes | 2 | [2TwentyTwo 2x2x1/8 steel tube, 18 in](https://www.amazon.com/dp/B09KNXGQDM) | $18.42 | $36.84 | Drill 4x 14 mm holes per tube (drill press). Remnants are fine: 18 in +/- 1/4 in, any surface rust brushed off. |
| Square tube 1-1/2x1-1/2x1/8, 12 in | Upright posts | 4 | [1.5x1.5x1/8 mild steel tube (12)](https://www.amazon.com/dp/B0BYTFMLXV) | $13.73 | $54.92 |  |
| Square tube 1-1/2x1-1/2x1/8, 6 in | Base spigots (2) + legs (4) | 6 | [1.5x1.5x1/8 mild steel tube (6)](https://www.amazon.com/dp/B0BYTG6YTN) | $5.52 | $33.12 | Printed sleeves take up the spigot gap in the 2 in tube; file the inside weld seam. Leg feet: an M12 nut (from the 20-pack) bonded into a printed plug in each leg end. |
| Steel plate 3/8 in | Upright top plates 2x 68 x 168 mm (2-11/16 x 6-5/8 in) | 2 cut pieces | [A36 plate cut to size (Midwest Steel or a local yard)](https://www.midweststeelsupply.com/) | ~$15 | $15.00 | Order cut to size so nothing needs cutting; add it to the riser order. |
| Rail risers 3/4 x 1-1/4 CR | Y: 2x 600 mm | 2 | [Midwest Steel 1018 cold-rolled flat bar (not Amazon)](https://www.midweststeelsupply.com/store/1018coldrollsteelflatbar) | ~$4.50/lb | $58.00 | Not on Amazon. Cut to length by Midwest (cut fee not included). |
| Rail risers 5/8 x 1-1/4 CR | X: 2x 400, Z: 2x 300 mm | 4 | [Midwest Steel 1018 cold-rolled flat bar (not Amazon)](https://www.midweststeelsupply.com/store/1018coldrollsteelflatbar) | ~$4.50/lb | $56.00 | Same |
| Aluminium plates | Cast plate: table 3/4 x 10.5 x 13 in, X 5/8 x 7 x 16.5, Z 5/8 x 6.25 x 12.25 | 3 cut pieces | [Midwest ATP-5 / MIC-6 cast plate, cut to size (not Amazon)](https://www.midweststeelsupply.com/store/castaluminumplateatp5) | ~$242 | $242.00 | Amazon alt is about $458: 6061 3/4x12x18 B007B4XUFU $215.98 + 5/8x12x24 B0DYG69W17 $241.97 (12x12 is too small for the table). |
| M12 threaded rod | 4x 293 + 2x 358 mm | 2 (1 m) | [M12-1.75 x 1 m plain steel rod](https://www.amazon.com/dp/B076HB72TW) | $28.96 | $57.92 | Cut with a hacksaw. Confirm it is one rod per order. |
| M12 coupling nuts | 6 | 1 (8-pack) | [Hillman 44770 M12 coupling nut](https://www.amazon.com/dp/B00JDTZNXS) | $16.97 | $16.97 |  |
| M12 nuts | 12 | 1 (20-pack) | [Hillman 2468 M12 hex nut](https://www.amazon.com/dp/B00HYLYWDE) | $8.92 | $8.92 |  |
| M12 washers | 12 | 1 (25-pack) | [M12 flat washer, hardened](https://www.amazon.com/dp/B01GUEFWTS) | $11.84 | $11.84 |  |
| M10 x 150 cap screws | 8, 12.9 | 2 (5-pack) | [Aexit M10x150 12.9](https://www.amazon.com/dp/B07MQS53Y2) | $23.53 | $47.06 | M10 washers: buy locally |
| Dowel pins 10 x 30 | 4 (locating only) | 1 (14-pack) | [10 x 30 mm 304 stainless dowel / shelf pin, 14 pcs (Walmart)](https://www.walmart.com/ip/856431494) | $18.49 | $18.49 | They only locate the castings (the bolts and rods carry the load), so plain pins are fine. Was a $85 hardened 20-pack. |
| Leveling feet | M12, ~40 kg each | 1 (4-pack) | [Antrader M12 leg levelers D60](https://www.amazon.com/dp/B09NS87SYW) | $23.99 | $23.99 |  |
| O-ring cord | NBR 3 mm, 2.5 m | 1 (3 m) | [uxcell nitrile round strip 3 mm x 3 m](https://www.amazon.com/dp/B0CNKM7L8B) | $6.56 | $6.56 |  |
| Cord splice glue | Cyanoacrylate | 1 | [Loctite 406, 20 g](https://www.amazon.com/dp/B07H2YGBTJ) | $9.86 | $9.86 |  |
| M5 cast-in inserts | 29 (11 enclosure + 18 riser hold-downs) | 1 (30) | [uxcell knurled brass M5 x 16 mm](https://www.amazon.com/dp/B07R7LL1SG) | $11.08 | $11.08 | Screw each to the mould floor with a greased screw so it ends up flush. |
| M6 cast-in inserts | 6 (Y BK12/BF12 on the base) | 1 pack | Knurled brass M6 insert, ~15 mm long | ~$8 | $8.00 | Search "M6 knurled brass insert 15mm". |
| X support pads | 1/4 x 2-1/2 in flat bar, ~4 in | 1 offcut | Steel yard remnant | ~$5 | $5.00 | Two pads (49 and 36 mm), drilled and tapped M6, cast flush in the beam face. |
| Riser hold-down screws | DIN 7984 low-head M5 x 20 (8) and M5 x 25 (10) | 2 packs | Low-head socket cap screws | ~$12 | $12.00 | Low head (3.5 mm) so they sit below the rail in the 4.5 mm counterbores. |
| Support screws | M6 x 40 (6, Y); M6 x 35 + 12 DIN 433 small washers (6, X) | 2 packs + washers | M6 socket cap screws 12.9 | ~$10 | $10.00 | Two small washers (10 mm OD, fit the BK counterbore) under each X screw head so it stops short of the beam tube. |
| M5 x 35 cap screws | 11 | 1 (25) | [M5x35 12.9 SHCS](https://www.amazon.com/dp/B0CJV2ZW2C) | $8.99 | $8.99 |  |
| Cap screw assortment | M3-M6 | 1 | [Mywish 900 pcs 12.9 kit](https://www.amazon.com/dp/B0CS3797P1) | $21.99 | $21.99 |  |
| Rail screws | M4 x 16 | 1 (100) | [iexcell M4x16 12.9](https://www.amazon.com/dp/B08B1T9VM3) | $8.26 | $8.26 |  |
| Block screws | M4 x 20 | 1 (50) | [iexcell M4x20 12.9](https://www.amazon.com/dp/B08B1T7K14) | $7.86 | $7.86 | Check length against the plate thickness |
| PETG filament | 1 kg | 1 | [SUNLU PETG 1 kg](https://www.amazon.com/dp/B0FS1FJLCW) | $15.99 | $15.99 | Cable chain, socket liners, sleeves, plugs |

**Priced subtotal: $1,267.80**

## Enclosure, coolant and covers

| Item | Spec | Qty | Listing | Price | Line | Notes |
|---|---|---|---|---|---|---|
| 2020 extrusion | 4x766, 2x756, 4x684, 2x600, 3x560 mm | 2 (10x 1000 mm) | [KathyLiely 2020 T-slot 1000 mm, 10 pcs](https://www.amazon.com/dp/B0DQ7WTJHL) | $49.99 | $99.98 | One piece per stick; 5 sticks spare. Take the 2x 244 from your 400s. |
| ACM sheet | 3 mm, all four wall/roof panels | 1 (4x8 ft) | [Sign supply / Piedmont Plastics (not Amazon)](https://piedmontplastics.com/p/acm-sheet-3mm-x-30-x-48-black) | ? | ? | The 726x684 sides don't fit any in-stock Amazon sheet. One 4x8 covers all four panels and the drip shield. Amazon 24x36 2-pack (B0F18ZQ7DJ, $65.99) covers back + roof only. |
| Door | Clear polycarbonate 560x756 | 1 | [SIBE polycarbonate 1/8 in, 24x36](https://www.amazon.com/dp/B0772W49WL) | $24.63 | $24.63 |  |
| Corner brackets | ~30 | 1 | [JCSPBYL 30 sets 2020 corner brackets](https://www.amazon.com/dp/B0DQDT9K64) | $12.99 | $12.99 |  |
| T-nuts | M5 drop-in, 100 | 1 | [POLISI3D 100 M5 drop-in T-nuts](https://www.amazon.com/dp/B07TSM9XN7) | $7.65 | $7.65 |  |
| Button-head screws | M5 x 10, 100 | 1 | [uxcell M5x10 button head, 100](https://www.amazon.com/dp/B01AXUT6VA) | $13.99 | $13.99 |  |
| Hinges + handle | 2020, 6 mm slot | 1 kit | [KOOTANS 2020 hinge and handle kit](https://www.amazon.com/dp/B07NQ5WHW9) | $14.59 | $14.59 | M4 or M5 not stated |
| Gas struts | 2x ~50 N, 200 mm | 1 pair | [SBOTTON 200 mm gas struts, 50 N](https://www.amazon.com/dp/B0B2S4LNN2) | $38.76 | $38.76 | Check force against the door weight |
| Door catch | Magnetic | 1 (4-pack) | [Onarway cabinet magnets](https://www.amazon.com/dp/B07WQY14JR) | $13.99 | $13.99 |  |
| (opt) Door interlock | 2NC key switch | 1 | [CZ-93B safety switch](https://www.amazon.com/dp/B0D8Y4WK66) | $22.13 | $22.13 | Wire into the E-stop or feed-hold loop |
| Panel trim | U-strip for 3 mm panels | 1 | [BLCCLOY 2020 panel U-strip, 25x 420 mm](https://www.amazon.com/dp/B0FXWQ9941) | $17.99 | $17.99 | 10.5 m; just short of every edge |
| Brush seal | For 2x 72 mm motor cutouts | 1 m | [SLZ dust-shoe brush strip 50 mm](https://www.amazon.com/dp/B0GVHQQ699) | $20.00 | $20.00 |  |
| Bulkhead | 1/4 NPT, thin panel | 1 (2-pack) | [FloFlex 1/4 in bulkhead, short](https://www.amazon.com/dp/B0CSZ76G4K) | $9.99 | $9.99 | Measure the hole size first |
| Sump | Full-size steam-table pan, 4 in deep (~13 L) | 1 | [Winco SPJH-104, 22 ga stainless (not Amazon)](https://www.katom.com/080-SPJH104.html) | $22.16-26.81 | $26.81 | Not found on Amazon; restaurant-supply stores (KaTom, GoFoodservice $23.63) or a local one. Slides in under the base. |
| Chip basket | 1/3-size pan, 2-1/2 in deep | 1 | [CAC STPT-S25-2 1/3 pan (not Amazon)](https://www.gofoodservice.com/p/cac-stpt-s25-2) | $9.98 | $9.98 | Solid pan: drill 6 mm holes in the floor (or buy a perforated 1/3 x 2-1/2 in pan). Sits at the front, under the drain. |
| Sump filter mesh | 100 um | 1 | [100 micron filter sock (cut open)](https://www.amazon.com/dp/B082S88S92) | $10.59 | $10.59 | Cut open and clamp in the printed filter frame |
| Magnet bar | 100 x 25 mm | 1 | [ULIBERMAGNET 12000 Gs filter rod 100x25](https://www.amazon.com/dp/B0CWGNDRNL) | $29.99 | $29.99 | Lies on the sump floor and catches fine steel |
| Flood coolant pump | 24 V brushless submersible, ~800 L/h, 5 m head, <= 60 mm tall | 1 | Search Amazon: "24V brushless submersible pump 800L/H 5M" | ? | ? | Low enough for the 4 in sump and no mains voltage in the coolant. Runs from the 24 V supply via the controller's MOSFET output. Replaces the $113 120 V pump. |
| Return tubing | 8 mm OD PU | 1 (5.5 m) | [uxcell 8 mm PU tubing](https://www.amazon.com/dp/B00WW704BY) | $10.19 | $10.19 | +$1.21 shipping |
| Drain nipple | 1/2 NPT brass | 1 (2-pack) | [Legines brass barb 1/2 NPT x 5/8](https://www.amazon.com/dp/B077DMKGLB) | $10.99 | $10.99 | Cast into the base, pointing down into the chip basket. +$7.59 shipping. |
| Ball valve | 1/4 NPT | 1 | [Beduan brass mini ball valve](https://www.amazon.com/dp/B07PMPXC5X) | $7.99 | $7.99 |  |
| Manifold | 1/4 NPT Y | 1 | [FASPARTS brass Y block](https://www.amazon.com/dp/B01B5BY0BC) | $11.99 | $11.99 | One bullet says 1/2 in thread: check before ordering |
| Loc-Line nozzles | 1/4 in kit | 2 | [Loc-Line LP-40413 coolant hose kit](https://www.amazon.com/dp/B002QG4F8Y) | $15.15 | $30.30 |  |
| Push-to-connect fittings | 8 mm x 1/4 NPT | 1 (10) | [Qjaiune push fittings](https://www.amazon.com/dp/B098QMJHWP) | $7.49 | $7.49 | One at the pump outlet, so the return line unplugs and the sump slides out |
| Coolant concentrate | Semi-synthetic, 1 gal | 1 | [Fusion Cool 2240](https://www.amazon.com/dp/B09LSL9JS7) | $52.95 | $52.95 | Mix 5-10 % |
| Way cover strip | 0.1 mm 301 stainless | 1 | [SPCCGG 301 strip 0.1 x 300 x 1000 mm](https://www.amazon.com/dp/B0DNQVM7RB) | $54.10 | $54.10 | Gives all three strips. If it turns out soft, use 304 full-hard B09ZQQJ34Z for the 85 mm strips. |
| Way cover springs | Constant force, for printed rollers | 1 (5-pack) | [SUS301 constant-force springs, 5 pcs](https://www.amazon.com/dp/B0DMM8YSMM) | $35.99 | $35.99 | One per narrow strip, two for the wide one |
| Spiral screw cover | 20 mm ID, ~250-400 mm | 1 | [MISONONEIK spiral steel bellows cover](https://www.amazon.com/dp/B0GTDV8DZN) | ? | ? | Choose size 20-250-40-28 or 20-400-40-33; variants $47-116 |
| Drip shield | 510 x 57 mm | 0 | Cut from the ACM sheet offcut | $0 | $0.00 | Stainless was $57 (Speedy Metals 16 ga 12x24); ACM does the job |

**Priced subtotal: $573.92** + 3 unpriced: ACM sheet, Flood coolant pump, Spiral screw cover

## Already owned

- HGR15-400 rails x2 + 4 HGH15CA blocks (X)
- SFU1204-400 kit with BK10/BF10, DSG12H housing, coupler (X)
- NEMA 23 bracket for BK10 (X)
- Open-loop NEMA 23 (Z)
- Extrusion: 10x 2040 x 400, 4x 2020 x 400, 4x 2020 x 200
- Bambu A1 mini, taps, drill press

## Not included

- Cutting tools, a vise and clamps (workholding).
- The water hoses that come with the spindle kit (check the barb size before buying more).
- Wire, ferrules, fuses and breakers for the electrical box.

## Check before ordering

1. **Couplers.** Both ballscrew kits ship with 6.35 mm-bore couplers; your motors have 8 mm shafts.
   Also check your owned open-loop motor's shaft and current.
2. **VFD on 120 V.** No real 2.2 kW drive takes 120 V and outputs 220 V; the step-up drives stop
   at 1.5 kW. The spindle runs at up to ~1.5 kW now and gets its full 2.2 kW when you switch to
   the kit's 220 V VFD on 240 V. Use a dedicated 20 A circuit.
3. **No cutting.** Rails, ballscrews and tube are used at the lengths they are sold in; the risers,
   plates and top plates are ordered cut to size. Only the M12 threaded rod is cut (hacksaw).
4. **Tubes and rebar.** Buy plain (black) steel, not galvanized: epoxy bonds poorly to zinc.
   Wire-brush off rust and loose scale, degrease just before casting. Stock-length tube is
   +/-1/8 in on length, with an internal weld seam: file the seam where the spigots and printed
   sleeves go. 0.120 in wall (11 ga) works as well as 1/8 in.
5. **Imperial sizes.** The plates and risers are already inch sizes in the model. The 3/8 in
   top plates are 0.5 mm thinner than the modelled 10 mm, which doesn't matter.
6. **Low stock.** Several picks showed "only N left", including the closed-loop kits.
