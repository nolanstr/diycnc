"""Writes docs/src/sourcing.md and docs/sourcing.csv from the sourcing results (checked 2026-10-09).

    python3 docs/src/make_sourcing.py
"""
import csv
import os

SRC = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.dirname(SRC)
A = 'https://www.amazon.com/dp/'

# (item, spec, qty, listing, url, unit, line, notes, price source)
# line None = price not seen. Rows whose item starts with "(opt)" are left out of the totals.
SECTIONS = [
    ('Part 1 - Frame: castings and hardware', [
        ('Epoxy', '~10.6 kg low-viscosity laminating epoxy (8.5 % mix), plus ~10 % waste', '1 (3 gal)', 'Raka Standard 2:1 Epoxy Laminating Kit: 127 Thin resin + 606 Slow hardener, 3 gal (not Amazon)', 'https://www.raka.com/collections/epoxy-kits/products/standard-epoxy-kits-1',
         '$172.99', 172.99, 'About 12.5 kg, $13.8/kg; free shipping (Raka: orders over $100). Cast the test bars first; if the mix needs more than 8.5 %, add the 1.5 qt kit ($32.99). Alt: US Composites 635, 4 gal $245. Avoid deep-pour casting resins and 1:1 tabletop epoxies.', 'vendor page'),
        ('Fines', 'Whiting (calcium carbonate) 325 mesh, ~11 kg', '1 (50 lb)', 'Clay-King calcium carbonate whiting, 50 lb (not Amazon)', 'https://www.clay-king.com/product/calcium-carbonate-whiting/',
         '$0.84/lb', 42.00, 'No crystalline silica (check the SDS), so a basic N95 is enough. A local pottery supplier saves the heavy shipping. Avoid garden lime and talc.', 'vendor page'),
        ('Aggregate', '~105 kg: fine sand 19, coarse sand 34, pea gravel 25, 3/8 in gravel 25 kg', '~6 bags', 'Pool filter sand + Quikrete all-purpose sand + Vigoro pea gravel + 3/8 in stone (Home Depot)', 'https://www.homedepot.com/p/Vigoro-0-5-cu-ft-Bagged-Pea-Gravel-Pebble-Landscape-Rock-54255/202523000',
         '~$7/bag', 48.00, 'Buy locally. Wash and dry fully.', 'search snippets (est.)'),
        ('Mould release wax', 'Partall Paste #2', '1', 'Partall Paste #2, 12 oz (Fiberglass Supply)', 'https://www.fiberglasssupply.com/partall/',
         '$20.96', 20.96, '3-5 coats. PVA film is optional (Partall #10, $8.36/pint).', 'vendor page'),
        ('Square tube', '2x2x0.120 A500: 4x 12 in, 2x 18 in; 1-1/2x1-1/2x0.120: 4x 12 in, 6x 6 in', '~7 ft of each', 'Steel-yard remnants (local)', '',
         '~$40', 40.00, 'About 37 lb at $0.75-1.25/lb. Online cut lengths: Speedy Metals $106 + shipping. Plain steel, not galvanized.', 'estimate (forum/yard prices)'),
        ('Steel plate and pads', '3/8 in: 2x 68x168 mm; 1/4 x 2-1/2 in: ~4 in', 'offcuts', 'Steel-yard offcuts (local)', '',
         '~$15', 15.00, 'Upright top plates and the X support pads', 'estimate'),
        ('Rail risers', 'Cold-rolled 1018 x 1-1/4 in: 3/4 thick 2x 600 mm; 5/8 thick 2x 400 + 2x 300 mm', '~4 + 5 ft', 'Steel yard (local)', '',
         '~$40', 40.00, 'About 26 lb at $1-2/lb. Online: Speedy Metals $60 + shipping. Pieced bars are fine (two rail screws per piece).', 'estimate'),
        ('Aluminium plates', '6061 drops: table 3/4 x 10.5 x 13 in, X 5/8 x 7 x 16.5, Z 5/8 x 6.25 x 12.25', '~22 lb', 'eBay "6061 aluminum plate remnant" / local drops', '',
         '~$85', 85.00, 'About $2.3-4.5/lb delivered. Midwest MIC-6 cut pieces are $242 if you would rather not hunt. Check flatness; face the table on the machine.', 'estimate (eBay listings)'),
        ('Threaded rod', '1/2-13, cut to 4x 293, 2x 211, 2x 108, 2x 358 mm', '1x 6 ft + 1x 3 ft', 'Everbilt 1/2-13 zinc threaded rod (Home Depot)', 'https://www.homedepot.com/p/332733421',
         '$14.93 + $7.93', 22.86, '6 ft: 358, 358, 293, 293, 293, 102, 102; 3 ft: 293, 213, 213 (hacksaw).', 'search snippet'),
        ('Coupling nuts', '1/2-13, 10', '10', 'Everbilt 1/2-13 coupling nut (Home Depot)', 'https://www.homedepot.com/p/204337404',
         '$2.47', 24.70, 'Tractor Supply 3-packs $5.99 are a bit cheaper', 'search snippet'),
        ('Nuts and washers', '1/2-13 nuts x16, 1/2 in grade 8 washers x16, 3/8 grade 8 washers x8', '4 packs', 'Everbilt packs (Home Depot)', 'https://www.homedepot.com/p/204284519',
         '~$20', 19.86, 'Nuts 15-pack $4.89 + 4-pack $1.38; 1/2 washers 25-pack $9.75; 3/8 washers 25-pack $3.84', 'search snippets'),
        ('Beam bolts', '3/8-16 x 6 in grade 8 hex bolt', '8', 'Bolt Depot, grade 8 yellow zinc', 'https://www.boltdepot.com/Hex_bolts_Zinc_plated_grade_8_steel_yellow_3_8-16.aspx',
         '$1.96', 15.68, 'Shipping extra; a local fastener supplier may have them', 'search snippet'),
        ('Dowel pins', '3/8 x 1-1/4 in', '1 (10-pack)', 'Steel dowel pins (Zoro)', 'https://www.zoro.com/i/G410073219/',
         '$5.79', 5.79, 'They only locate the castings', 'search snippet'),
        ('Feet', '1/2-13 x 2 in hex bolt + jam nut + rubber pad, per leg', '4', 'Hardware store bolts + rubber anti-vibration pads', '',
         '~$12', 12.00, 'The bolt screws into the nut in each leg end; turn it to level, lock with the jam nut. Leveling mounts (S&W NYL B24, $9.49 each) if you prefer.', 'estimate'),
        ('O-ring cord', 'NBR 3 mm, 2.5 m', '1 (3 m)', 'uxcell nitrile round strip 3 mm x 3 m', A + 'B0CNKM7L8B',
         '$6.56', 6.56, '', 'product page'),
        ('Cord splice glue', 'Cyanoacrylate', '1', 'Loctite 406, 20 g', A + 'B07H2YGBTJ',
         '$9.86', 9.86, '', 'product page'),
        ('M5 cast-in inserts', '18 riser hold-downs (+11 for the part 3 enclosure)', '1 (30)', 'uxcell knurled brass M5 x 16 mm', A + 'B07R7LL1SG',
         '$11.08', 11.08, 'Screw each to the mould floor with a greased screw so it ends up flush. Cast the enclosure inserts now too.', 'product page'),
        ('M6 cast-in inserts', '6 (Y BK12/BF12 on the base)', '1 (20)', 'Knurled brass M6 inserts (eBay)', 'https://www.ebay.com/itm/156778660033',
         '~$16', 16.11, 'Length not confirmed; 12-16 mm is fine', 'search snippet'),
        ('Low-head screws', 'DIN 7984 M5 x 20 (8, X risers) and M5 x 25 (10, Y risers)', '2 (100)', 'Zoro Select DIN 7984 low-head, class 8.8', 'https://www.zoro.com/i/G2652426/',
         '$9.99 + $14.29', 24.28, 'Head 3.5 mm tall, sits below the rail in the 4.5 mm counterbore', 'search snippet'),
        ('Support screws', 'M6 x 40 (6, Y BK/BF); M6 x 35 (6, X) + 12 DIN 433 small washers', '1 (100) + 3 (2-pack)', 'Zoro M6x40 100-pack; Home Depot M6x35 2-packs', 'https://www.zoro.com/i/G2650606/',
         '$10.15 + 3x $3.75', 21.40, 'Two small washers under each X screw head so it stops short of the beam tube (washers from the hardware store)', 'search snippets'),
        ('Rail screws', 'M4 x 16', '1 (100)', 'iexcell M4x16 12.9', A + 'B08B1T9VM3',
         '$8.26', 8.26, '', 'product page'),
        ('Block screws', 'M4 x 20', '1 (50)', 'iexcell M4x20 12.9', A + 'B08B1T7K14',
         '$7.86', 7.86, 'Check length against the plate thickness', 'product page'),
        ('PETG filament', '~2.7 kg for the mould parts and liners', '3 (1 kg)', 'SUNLU PETG 1 kg', A + 'B0FS1FJLCW',
         '$15.99', 47.97, 'About 1.5 kg less if the pocket cores are cut from XPS foam instead', 'product page'),
    ]),
    ('Part 1 - Frame: rails, screws and mechanics', [
        ('Y rails + blocks', 'HGR15 x2 at 600 mm + 4x HGH15CA', '1 kit', 'iMetrx HGR15 kit, 2x 600 mm + 4x HGH15CA', A + 'B0GJZ7D9NG',
         '$55.99', 55.99, 'Used at full length, no cutting. The listing calls the blocks "aluminum", which is probably wrong: check them for play. JLCMC alt: 2x E-BHH15C-2-L600-ZA-C-E30 $27.40 + 55 % US duty prepaid + shipping.', 'product page'),
        ('Z rails + blocks', 'HGR15 x2 at 300 mm + 4x HGH15CA', '1 kit', 'BEVDICNC 2x HGR15-300 + 4x HGH15CA', A + 'B0BYYJKBB5',
         '$35.69', 35.69, 'Alt: CNCMANS B09N73DY32 $34.98', 'product page'),
        ('Y ballscrew kit', 'SFU1605-550, BK12/BF12, DSG16H', '1', 'Ballscrew kit DSG16H + SFU1605-550 + BK/BF12', A + 'B088ZF8R91',
         '$39.39', 39.39, 'Ships with a 6.35x10 coupler: use the 8x10 below', 'product page'),
        ('Z ballscrew kit', 'SFU1204-300, BK10/BF10, DSG12H', '1', 'CNCYEAH SFU1204 300 mm kit', A + 'B09MJ3T5JZ',
         '$32.69', 32.69, 'Ships with a 6.35x8 coupler: use the 8x8 below', 'product page'),
        ('Z motor bracket', 'NEMA 23 + BK10 (HM10-57)', '1', 'ANWOK NEMA 23 steel bracket, SFU1204', A + 'B09S3HMB7S',
         '$32.02', 32.02, 'Same bracket as your X one', 'product page'),
        ('Y motor bracket', 'NEMA 23 + BK12 (HM12-57)', '1', 'ANWOK NEMA 23 steel bracket, SFU1605', A + 'B09S39Q1RT',
         '$31.36', 31.36, 'Alt: CNCMANS HM12-57 B09QS2S3BT $28.98', 'product page'),
        ('Couplers, Y', '8x10 mm, D25 L30', '1 (3-pack)', 'CNCTOPBAOS 8x10 plum coupling, 3 pcs', A + 'B082TT7B84',
         '$13.99', 13.99, 'Spares; check that D25 fits inside the bracket', 'product page'),
        ('Couplers, Z', '8x8 mm, D25 L30', '1 (2-pack)', 'Yeebyee 8x8 plum coupling, 2 pcs', A + 'B0GTV7VMZB',
         '$12.89', 12.89, 'The spare covers X if your kit came with 6.35x8', 'product page'),
        ('Grease gun', 'Mini, 3 oz cartridges', '1', 'Performance Tool W54205 mini grease gun kit', A + 'B002V0AIWW',
         '$17.59', 17.59, '', 'product page'),
        ('Needle tip', 'For the blocks\' M4 nipples', '1', 'LubriMatic 05-037 needle', A + 'B000FMO6XU',
         '$6.98', 6.98, '', 'product page'),
        ('Grease', 'Lithium NLGI 2', '1 (3x3 oz)', 'LubriMatic 11312, 3x 3 oz', A + 'B01JM4PCVG',
         '$11.79', 11.79, '', 'product page'),
        ('(opt) M4 grease nipples', 'M4x0.7 straight', '1 pack', 'HARFINGTON 15 pcs M4x0.7', A + 'B0CLP8NGRJ',
         '$13.94', 13.94, 'Only if the block nipples are missing or the coupler won\'t seat', 'product page'),
    ]),
    ('Part 1 - Frame: chip protection', [
        ('Sump', 'Full-size steam-table pan, 4 in deep (~13 L)', '1', 'Winco SPJH-104, 22 ga stainless (not Amazon)', 'https://www.katom.com/080-SPJH104.html',
         '$22.16-26.81', 26.81, 'Not found on Amazon; restaurant-supply stores (KaTom, GoFoodservice $23.63) or a local one. Slides in under the base.', 'search result'),
        ('Chip basket', '1/3-size pan, 2-1/2 in deep', '1', 'CAC STPT-S25-2 1/3 pan (not Amazon)', 'https://www.gofoodservice.com/p/cac-stpt-s25-2',
         '$9.98', 9.98, 'Solid pan: drill 6 mm holes in the floor (or buy a perforated 1/3 x 2-1/2 in pan). Sits at the front, under the drain.', 'search result'),
        ('Drain nipple', '1/2 NPT brass', '1 (2-pack)', 'Legines brass barb 1/2 NPT x 5/8', A + 'B077DMKGLB',
         '$10.99', 10.99, 'Cast into the base, pointing down into the chip basket. +$7.59 shipping.', 'product page'),
        ('Way cover strip', '0.1 mm 301 stainless', '1', 'SPCCGG 301 strip 0.1 x 300 x 1000 mm', A + 'B0DNQVM7RB',
         '$54.10', 54.10, 'Gives all three strips. If it turns out soft, use 304 full-hard B09ZQQJ34Z for the 85 mm strips.', 'product page'),
        ('Way cover springs', 'Constant force, for printed rollers', '1 (5-pack)', 'SUS301 constant-force springs, 5 pcs', A + 'B0DMM8YSMM',
         '$35.99', 35.99, 'One per narrow strip, two for the wide one', 'product page'),
        ('Spiral screw cover', '20 mm ID, ~250-400 mm', '1', 'MISONONEIK spiral steel bellows cover', A + 'B0GTDV8DZN',
         '~$47', 47.00, 'Choose size 20-250-40-28 (the cheapest variant, about $47) or 20-400-40-33; variants $47-116', 'product page (variant range)'),
        ('Drip shield', '510 x 57 mm', '0', 'Cut from the ACM sheet offcut', '',
         '$0', 0.00, 'Stainless was $57 (Speedy Metals 16 ga 12x24); ACM does the job', 'design change'),
        ('Cutting fluid', 'Brush-on / drip, until flood coolant (part 3)', '1', 'Tap Magic or similar cutting fluid', '',
         '~$12', 12.00, 'Brush or drip it on; the base gutters and drain still carry it to the pan', 'estimate'),
    ]),
    ('Part 2 - Electronics: motors and drivers', [
        ('X/Y closed-loop kits', '23HS30-5004D-E1000 2.0 Nm + CL57T', '2', 'STEPPERONLINE closed-loop kit 2.0 Nm + CL57T', A + 'B0C694KQQP',
         '$81.00', 162.00, 'Exact model. Low stock when checked.', 'product page'),
        ('Z driver (owned motor)', 'DM542T', '1', 'STEPPERONLINE DM542T', A + 'B06Y5VPSFN',
         '$32.99', 32.99, 'Check that your motor is 4.2 A or less', 'product page'),
        ('Motor power supply', '48 V, 3 drivers', '1', 'Mean Well LRS-350-48 (7.3 A)', A + 'B013EU4KNK',
         '$37.13', 37.13, 'Trim to about 46 V: CL57T max input is 48 V', 'product page'),
    ]),
    ('Part 2 - Electronics: controller and wiring', [
        ('Controller', 'FluidNC, 6 axes, external drivers, RS485, 0-10 V', '1', 'Elecrow Corgi ESP32 FluidNC controller (not Amazon)',
         'https://www.elecrow.com/corgi-esp32-6-axis-cnc-controller-for-fluidnc.html',
         '$49.00', 49.00, 'Runs gSender or the web UI. Drives an RS485 VFD directly, so no 0-10 V module is needed for one.', 'Elecrow page'),
        ('Limit switches', 'Roller lever, 4 needed', '1 (5-pack)', 'Yusheng ME-8108 limit switch set of 5', 'https://www.cncproshop.com/products/yusheng-me-8108-limit-switch-set-of-5',
         '$16.99', 16.99, 'Inductive LJ12A3-4-Z/BX (about $4.50 each) also work; power them from 12 V.', 'search snippet'),
        ('E-stop', '22 mm mushroom, latching, NC, in a box', '1', 'Generic 22 mm E-stop station (eBay)', 'https://www.ebay.com/itm/144182671837',
         '$22.39', 22.39, 'Wire it to cut drive enable and VFD run in hardware. Check it has an NC contact.', 'search snippet'),
        ('Mains inlet', 'IEC C14 with switch + fuse', '1', 'IEC C14 inlet module (Walmart)', 'https://www.walmart.com/ip/115677799',
         '$7.99', 7.99, 'Often ships without the fuse: buy 5x20 mm fuses.', 'search snippet'),
        ('Logic power supply', '24 V, 6.5 A', '1', 'Mean Well LRS-150-24 (TRC Electronics)', 'https://www.trcelectronics.com/products/mean-well-lrs-150-24',
         '$20.39', 20.39, 'Jameco about $18.80', 'vendor page'),
        ('Electrical box', 'ABS IP65, 11.8 x 9.8 x 4.7 in', '1', 'LeMotech ABS IP65 junction box 11.8x9.8x4.7', 'https://thrumsvet.co.uk/products/lemotech-abs-plastic-dustproof-waterproof-ip65-junction-box/223105279/',
         '$25.99', 25.99, 'Holds the controller, three drivers and both supplies on a plywood or aluminium backplate; the VFD mounts outside. Steel alt: VEVOR 12x10x6 $48.90.', 'reseller snapshot (LeMotech is sold on Amazon)'),
        ('Motor, sensor and spindle cable', '4-conductor shielded, ~45 ft', '45 ft', 'BuildYourCNC 4-conductor shielded cable', 'https://buildyourcnc.com/',
         '$0.49/ft', 22.05, 'One spool for the steppers, switches and spindle: 18/4 shielded is enough for a 1.5-2.2 kW spindle (BuildYourCNC). Shield to earth at the VFD end. Check the gauge and that it is stranded for the cable chain.', 'vendor page (unit unclear)'),
        ('DIN rail + terminals', 'UK2.5B kit', '1', 'Erayco 20x UK2.5B + rail', A + 'B0BX2W42S4',
         '$19.99', 19.99, 'May need more rail', 'search snippet'),
        ('Cable glands', 'PG7-PG16', '1 (25 pcs)', 'Nylon cable gland kit (eBay)', 'https://www.ebay.com/itm/406955179899',
         '$13.80', 13.80, '', 'search snippet'),
        ('(opt) Tool setter', 'NC, magnetic base', '1', 'Z touch tool setter', A + 'B0D42C32MR',
         '~$31.61', 31.61, 'Nice to have; add later', 'search summary'),
    ]),
    ('Part 2 - Electronics: spindle (pick one)', [
        ('(choice A) 1.5 kW 110 V water-cooled kit', 'Spindle + 110 V VFD + 80 mm clamp + pump, ER11/ER16', '1', 'SainSmart / VXB / Huanyang-type kits', 'https://www.sainsmart.com/products/water-cooled-spindle-motor-kit',
         '$250-375', 300.00, 'Runs on a normal 120 V outlet. SainSmart $349 (sold out; open-box $249), VXB $374.88, eBay import ~$341 shipped. Check Amazon kits by hand.', 'vendor pages / snippets'),
        ('(choice B) 2.2 kW 220 V kit + 120 V step-up VFD', 'ER20 kit + 110-120 V in / 220 V out VFD', '1 + 1', 'RATTMMOTOR 2.2 kW kit + ATO or AT5-2200X VFD', A + 'B073TRP92V',
         '$251 + $178-346', 500.00, 'Only about 1.2-1.6 kW on a 120 V circuit; full 2.2 kW once you have 240 V (then use the kit\'s own VFD).', 'product page / snippets'),
        ('(choice) ER collets', 'ER11/ER16 or ER20 set to match', '1', 'Chiloskit ER20 13 pcs (or an ER11 set)', A + 'B08B1H4RSR',
         '$25.21', 25.21, 'Skip if the kit includes a set', 'search snippet'),
        ('(choice) Spindle pump relay', 'SSR, DC in, AC out', '1', 'SSR-25DA with heatsink (eBay)', 'https://www.ebay.com/itm/405564584590',
         '$17.44', 17.44, 'Runs the spindle water pump whenever the spindle runs. Fuse the branch.', 'search snippet'),
        ('(choice) Spindle coolant', 'Distilled water + 10-20 % RV antifreeze, bucket', '1', 'Local store', '',
         '~$10', 10.00, 'Water-cooled spindles only', 'estimate'),
    ]),
    ('Part 3 - Enclosure and flood coolant', [
        ('2020 extrusion', '4x766, 2x756, 4x684, 2x600, 3x560 mm', '2 (10x 1000 mm)', 'KathyLiely 2020 T-slot 1000 mm, 10 pcs', A + 'B0DQ7WTJHL',
         '$49.99', 99.98, 'One piece per stick; 5 sticks spare. Take the 2x 244 from your 400s.', 'product page'),
        ('ACM sheet', '3 mm, all four wall/roof panels', '1 (4x8 ft)', 'Sign supply / Piedmont Plastics (not Amazon)', 'https://piedmontplastics.com/p/acm-sheet-3mm-x-30-x-48-black',
         '?', None, 'The 726x684 sides don\'t fit any in-stock Amazon sheet. One 4x8 covers all four panels and the drip shield. Amazon 24x36 2-pack (B0F18ZQ7DJ, $65.99) covers back + roof only.', 'quote only'),
        ('Door', 'Clear polycarbonate 560x756', '1', 'SIBE polycarbonate 1/8 in, 24x36', A + 'B0772W49WL',
         '$24.63', 24.63, '', 'product page'),
        ('Corner brackets', '~30', '1', 'JCSPBYL 30 sets 2020 corner brackets', A + 'B0DQDT9K64',
         '$12.99', 12.99, '', 'product page'),
        ('T-nuts', 'M5 drop-in, 100', '1', 'POLISI3D 100 M5 drop-in T-nuts', A + 'B07TSM9XN7',
         '$7.65', 7.65, '', 'product page'),
        ('Button-head screws', 'M5 x 10, 100', '1', 'uxcell M5x10 button head, 100', A + 'B01AXUT6VA',
         '$13.99', 13.99, '', 'product page'),
        ('Hinges + handle', '2020, 6 mm slot', '1 kit', 'KOOTANS 2020 hinge and handle kit', A + 'B07NQ5WHW9',
         '$14.59', 14.59, 'M4 or M5 not stated', 'product page'),
        ('Gas struts', '2x ~50 N, 200 mm', '1 pair', 'SBOTTON 200 mm gas struts, 50 N', A + 'B0B2S4LNN2',
         '$38.76', 38.76, 'Check force against the door weight', 'product page'),
        ('Door catch', 'Magnetic', '1 (4-pack)', 'Onarway cabinet magnets', A + 'B07WQY14JR',
         '$13.99', 13.99, '', 'product page'),
        ('(opt) Door interlock', '2NC key switch', '1', 'CZ-93B safety switch', A + 'B0D8Y4WK66',
         '$22.13', 22.13, 'Wire into the E-stop or feed-hold loop', 'related-items list'),
        ('Panel trim', 'U-strip for 3 mm panels', '1', 'BLCCLOY 2020 panel U-strip, 25x 420 mm', A + 'B0FXWQ9941',
         '$17.99', 17.99, '10.5 m; just short of every edge', 'product page'),
        ('Brush seal', 'For 2x 72 mm motor cutouts', '1 m', 'SLZ dust-shoe brush strip 50 mm', A + 'B0GVHQQ699',
         '$20.00', 20.00, '', 'product page'),
        ('Bulkhead', '1/4 NPT, thin panel', '1 (2-pack)', 'FloFlex 1/4 in bulkhead, short', A + 'B0CSZ76G4K',
         '$9.99', 9.99, 'Measure the hole size first', 'product page'),
        ('Sump filter mesh', '100 um', '1', '100 micron filter sock (cut open)', A + 'B082S88S92',
         '$10.59', 10.59, 'Cut open and clamp in the printed filter frame', 'product page'),
        ('Magnet bar', '100 x 25 mm', '1', 'ULIBERMAGNET 12000 Gs filter rod 100x25', A + 'B0CWGNDRNL',
         '$29.99', 29.99, 'Lies on the sump floor and catches fine steel', 'product page'),
        ('Flood coolant pump', '24 V brushless submersible, ~800 L/h, 5 m head, <= 60 mm tall', '1', 'Search Amazon: "24V brushless submersible pump 800L/H 5M"', '',
         '?', None, 'Low enough for the 4 in sump and no mains voltage in the coolant. Runs from the 24 V supply via the controller\'s MOSFET output. Replaces the $113 120 V pump.', 'not found on Amazon'),
        ('Return tubing', '8 mm OD PU', '1 (5.5 m)', 'uxcell 8 mm PU tubing', A + 'B00WW704BY',
         '$10.19', 10.19, '+$1.21 shipping', 'product page'),
        ('Ball valve', '1/4 NPT', '1', 'Beduan brass mini ball valve', A + 'B07PMPXC5X',
         '$7.99', 7.99, '', 'product page'),
        ('Manifold', '1/4 NPT Y', '1', 'FASPARTS brass Y block', A + 'B01B5BY0BC',
         '$11.99', 11.99, 'One bullet says 1/2 in thread: check before ordering', 'product page'),
        ('Loc-Line nozzles', '1/4 in kit', '2', 'Loc-Line LP-40413 coolant hose kit', A + 'B002QG4F8Y',
         '$15.15', 30.30, '', 'product page'),
        ('Push-to-connect fittings', '8 mm x 1/4 NPT', '1 (10)', 'Qjaiune push fittings', A + 'B098QMJHWP',
         '$7.49', 7.49, 'One at the pump outlet, so the return line unplugs and the sump slides out', 'product page'),
        ('Coolant concentrate', 'Semi-synthetic, 1 gal', '1', 'Fusion Cool 2240', A + 'B09LSL9JS7',
         '$52.95', 52.95, 'Mix 5-10 %', 'product page'),
    ]),
]

OWNED = [
    'HGR15-400 rails x2 + 4 HGH15CA blocks (X)',
    'SFU1204-400 kit with BK10/BF10, DSG12H housing, coupler (X)',
    'NEMA 23 bracket for BK10 (X)',
    'Open-loop NEMA 23 (Z)',
    'Extrusion: 10x 2040 x 400, 4x 2020 x 400, 4x 2020 x 200',
    'Bambu A1 mini, taps, drill press',
]


def money(v):
    return f'${v:,.2f}'


def main():
    rows, md = [], []
    md += ['# Sourcing list', '',
           'Parts to buy for the machine in `model/DIYCNC.FCStd` / `docs/report.txt`, sourced on Amazon (US) where it',
           'makes sense. Prices and stock were checked on **2026-10-09/10**. "?" means the price was not visible',
           '(Amazon blocks automated page reads); check the live listing. Shipping and tax are not included.',
           'Off-Amazon picks are marked "not Amazon": they are there because Amazon doesn\'t carry the part or',
           'is much dearer. Rows marked (opt) or (choice) are left out of the totals.', '',
           'The same list is in `docs/sourcing.csv` for a spreadsheet.', '']
    summary = []
    for sec, items in SECTIONS:
        priced = sum(i[6] for i in items if i[6] is not None and not i[0].startswith('('))
        unpriced = [i[0] for i in items if i[6] is None and not i[0].startswith('(')]
        summary.append((sec, priced, unpriced))
        md += [f'## {sec}', '',
               '| Item | Spec | Qty | Listing | Price | Line | Notes |',
               '|---|---|---|---|---|---|---|']
        for item, spec, qty, listing, url, unit, line, notes, src in items:
            link = f'[{listing}]({url})' if url else listing
            md.append(f'| {item} | {spec} | {qty} | {link} | {unit} | {money(line) if line is not None else "?"} | {notes} |')
            rows.append([sec, item, spec, qty, listing, url, unit, '' if line is None else f'{line:.2f}', notes, src])
        md += ['', f'**Priced subtotal: {money(priced)}**' + (f' + {len(unpriced)} unpriced: {", ".join(unpriced)}' if unpriced else ''), '']

    part = lambda n: [x for x in summary if x[0].startswith(f'Part {n}')]
    p1 = sum(p for _, p, _ in part(1))
    p2 = sum(p for s_, p, _ in part(2) if 'spindle' not in s_)
    p3, u3 = sum(p for _, p, _ in part(3)), sum((u for *_, u in part(3)), [])
    total, n_unpriced = p1, 0
    head = ['## Totals', '',
            'The list is in three parts, so you can buy and build in that order: **Part 1** is the machine',
            'itself without the expensive equipment (castings, steel, rails, ballscrews, chip protection),',
            '**Part 2** is the motors, controller, wiring and spindle, and **Part 3** is the enclosure and',
            'flood coolant. The machine runs after Part 2 with brush-on cutting fluid; the castings already',
            'have the inserts, gutters, drain and sump space for Part 3.', '',
            '| Part | Section | Priced |', '|---|---|---|']
    for n in (1, 2, 3):
        head += [f'| {n} | {(s_.split(": ", 1)[-1] if ": " in s_ else s_.split(" - ", 1)[-1]).capitalize()} | {money(p)} |' for s_, p, _ in part(n)
                 if 'spindle' not in s_]
    head += ['', '| Part | About |', '|---|---|',
             f'| **1. Frame** | **{money(p1)}** |',
             f'| **2. Electronics + spindle** | **{money(p2)}** + spindle: $250-375 (1.5 kW 110 V kit) or $430-600 (2.2 kW + 120 V step-up VFD) |',
             f'| **3. Enclosure + flood coolant** | **{money(p3)}** + {len(u3)} unpriced ({", ".join(u3)}): about $650-700 |',
             f'| **Total** | **about ${(p1 + p2 + 250 + 650) / 1000:.2f}-{(p1 + p2 + 600 + 700) / 1000:.2f}k** |', '',
             'Shipping and tax are extra (Raka ships free over $100). The whiting and Bolt Depot ship heavy or separately;',
             'buying the whiting and the steel locally saves most of it. Steel-yard and remnant prices are',
             'estimates: call a yard with the cut list.', '',
             '**JLCMC and JLCCNC (checked 2026-10-10).** JLCMC list prices are about half of Amazon for',
             'rails and couplings (e.g. the Y rail pair $27.40), but US orders prepay a 55 % duty plus DHL',
             'shipping, so the whole motion order comes to about $250-300 against about $190 here. There is',
             'no ready-made SFU1204 (lead 4) kit, and the 1605 screw-end machining for BK12/BF12 is not',
             'confirmed. Worth adding the rails and couplers only to a JLC order you are placing anyway.',
             'JLCCNC machining of the three aluminium plates with all holes is estimated at $430-850',
             'delivered (90 % duty prepaid on machined aluminium): only worth it for the X carriage if you',
             'want its hole pattern exact. Retail cut-to-size shops (e.g. Metal Supermarkets, about $820 for',
             'the tube, risers and aluminium) also cost more than the sources here.', '']
    i = md.index('The same list is in `docs/sourcing.csv` for a spreadsheet.') + 2
    md[i:i] = head

    md += ['## Already owned', ''] + [f'- {o}' for o in OWNED] + ['',
           '## Not included', '',
           '- Cutting tools, a vise and clamps (workholding).',
           '- The water hoses that come with the spindle kit (check the barb size before buying more).',
           '- Wire, ferrules, fuses and breakers for the electrical box.', '',
           '## Check before ordering', '',
           '1. **Couplers.** Both ballscrew kits ship with 6.35 mm-bore couplers; your motors have 8 mm shafts.',
           '   Also check your owned open-loop motor\'s shaft and current.',
           '2. **VFD on 120 V.** No real 2.2 kW drive takes 120 V and outputs 220 V; the step-up drives stop',
           '   at 1.5 kW. The spindle runs at up to ~1.5 kW now and gets its full 2.2 kW when you switch to',
           '   the kit\'s 220 V VFD on 240 V. Use a dedicated 20 A circuit.',
           '3. **No cutting.** Rails, ballscrews and tube are used at the lengths they are sold in; the risers,',
           '   plates and top plates are ordered cut to size. Only the M12 threaded rod is cut (hacksaw).',
           '4. **Tubes and rebar.** Buy plain (black) steel, not galvanized: epoxy bonds poorly to zinc.',
           '   Wire-brush off rust and loose scale, degrease just before casting. Stock-length tube is',
           '   +/-1/8 in on length, with an internal weld seam: file the seam where the spigots and printed',
           '   sleeves go. 0.120 in wall (11 ga) works as well as 1/8 in.',
           '5. **Imperial sizes.** The plates and risers are already inch sizes in the model. The 3/8 in',
           '   top plates are 0.5 mm thinner than the modelled 10 mm, which doesn\'t matter.',
           '6. **Low stock.** Several picks showed "only N left", including the closed-loop kits.',
           '']
    with open(os.path.join(SRC, 'sourcing.md'), 'w') as fh:
        fh.write('\n'.join(md))
    with open(os.path.join(DOCS, 'sourcing.csv'), 'w', newline='') as fh:
        w = csv.writer(fh)
        w.writerow(['Section', 'Item', 'Spec', 'Qty', 'Listing', 'URL', 'Unit price', 'Line total (USD)', 'Notes', 'Price source (2026-10-09)'])
        w.writerows(rows)
        w.writerow([])
        for s, p, u in summary:
            w.writerow(['Subtotal', s, '', '', '', '', '', f'{p:.2f}', f'{len(u)} unpriced', ''])
        w.writerow(['Total', 'priced items', '', '', '', '', '', f'{total:.2f}', f'{n_unpriced} unpriced', ''])
    print(total, [(s, round(p, 2), len(u)) for s, p, u in summary])


main()
