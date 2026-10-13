"""Writes docs/src/sourcing.md and docs/1-sourcing/sourcing.csv from the sourcing results (checked 2026-10-09).

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
        ('Epoxy', '~10.3 kg low-viscosity laminating epoxy (8.5 % mix), plus ~10 % waste', '1 (3 gal)', 'Raka Standard 2:1 Epoxy Laminating Kit: 127 Thin resin + 606 Slow hardener, 3 gal (not Amazon)', 'https://www.raka.com/collections/epoxy-kits/products/standard-epoxy-kits-1',
         '$172.99', 172.99, 'About 12.5 kg, $13.8/kg; free shipping (Raka: orders over $100). Cast the test bars first; if the mix needs more than 8.5 %, add the 1.5 qt kit ($32.99). Alt: US Composites 635, 4 gal $245. Avoid deep-pour casting resins and 1:1 tabletop epoxies.', 'vendor page'),
        ('Fines', 'Whiting (calcium carbonate) 325 mesh, ~11 kg', '1 (50 lb)', 'Clay-King calcium carbonate whiting, 50 lb (not Amazon)', 'https://www.clay-king.com/product/calcium-carbonate-whiting/',
         '$0.84/lb', 42.00, 'No crystalline silica (check the SDS), so a basic N95 is enough. A local pottery supplier saves the heavy shipping. Avoid garden lime and talc.', 'vendor page'),
        ('Aggregate', '~86 kg: fine sand 16, coarse sand 19, pea gravel 23, 3/8 in gravel 23 kg, plus test bars', '~6 bags', 'Pool filter sand + Quikrete all-purpose sand + Vigoro pea gravel + 3/8 in stone (Home Depot)', 'https://www.homedepot.com/p/Vigoro-0-5-cu-ft-Bagged-Pea-Gravel-Pebble-Landscape-Rock-54255/202523000',
         '~$9/bag', 55.00, 'Buy locally. Wash and dry fully. The fine sand includes the beam and uprights\' (the alumina replaces only their coarse sand).', 'search snippets (est.)'),
        ('Alumina grit, coarse', 'Brown fused aluminum oxide #16 (12-20 is fine), ~19 kg (17.3 net): the coarse sand in the beam and uprights', '1 (50 lb)', 'IMS Blasting brown aluminum oxide, 50 lb (pick 16 grit)', 'https://www.imsblasting.com/product-page/aluminum-oxide-50-lbs',
         '$109.99', 109.99, 'Free shipping. About +5 % frame stiffness (96.5 / 150 / 129 N/um against 89 / 138 / 117 with sand; analysis/alumina.py). It is cast in: decide before the pour. Alt: Kleen Blast AO5016 $90 + shipping (blast media is excluded from its free shipping).', 'vendor page'),
        ('(opt) Alumina grit, fine', 'Black aluminum oxide 70 grit, ~10 kg (8.9 net): the fine sand in the beam and uprights', '1 (25 lb)', 'Central Pneumatic black aluminum oxide 70 grit, 25 lb (Harbor Freight, item 56704)', 'https://www.harborfreight.com/search?q=aluminum%20oxide%20blast%20media',
         '$39.99', 39.99, 'Upgrade, decided before the pour: with the #16, the frame comes to 101 / 158 / 136 N/um (about +5 % more). Without it, the fine sand stays sand (in the aggregate row).', 'vendor page'),
        ('Mold board', '3/4 in white melamine (a true 0.750 in), about 2.2 m2 of boards: cut list and layout in the mold guide', '1 (4 x 8 ft)', 'Veranda melamine white particleboard panel, 3/4 in x 4 ft x 8 ft (Home Depot, model 461877)', 'https://www.homedepot.com/p/Veranda-3-4-in-x-4-ft-x-8-ft-Melamine-White-Particleboard-Panel-461877/100070209',
         '$43.98', 43.98, 'One sheet: one upright mold casts both uprights, and the bridges and struts come out of the offcuts (three-stage cut in the mold guide). Have the store rip the long strips. Measure the thickness: the printed saddles and brackets are drawn for 19.05 mm (mold_board in the model).', 'category listing (check in store)'),
        ('Mold cleats', '1x2 lumber, 5.0 m: the strips along the walls\' feet', '3 (8 ft)', '1x2 furring strip (Home Depot / Lowe\'s)', '',
         '~$2.50', 7.50, 'They lie on the floor outside the walls and never touch the mix.', 'estimate'),
        ('Mold hardware', 'M4 x 30 (87), M4 x 35 (30), M4 x 45 (33), M4 x 20 (4, leg pinch screws), M4 nuts (154) and washers (150); M3 x 25 with nuts and washers (20)', 'packs of 100 / 50', 'Zinc-plated metric (Zoro, Bolt Depot or a hardware store; Zoro M4 x 30 is $9.89 per 100)', 'https://www.zoro.com/i/G0869522/',
         '~$40', 40.00, 'Exact counts in the mold guide; add about 10 % spare. Reused for every casting.', 'estimate (Zoro listings)'),
        ('Mold rods and bolts', 'Plain steel rod: 1/2 in 2x 3 ft; 1/2-13 x 1-1/2 in bolts (2), 3/8-16 x 3 in (2); M5 x 20 (17, insert screws), M5 x 30 (12), M5 x 40 (8), M6 x 30 (6), M6 x 40 (6)', '1 set', 'Everbilt plain steel rod and hex bolts (Home Depot); the metric screws in packs online', '',
         '~$40', 40.00, 'Greased, they form the beam\'s stud holes and the dowel holes and hold the steel and the inserts to the mold boards. Reused.', 'estimate'),
        ('Mold release wax', 'Partall Paste #2', '1', 'Partall Paste #2, 12 oz (Fiberglass Supply)', 'https://www.fiberglasssupply.com/partall/',
         '$20.96', 20.96, '3-5 coats, then the PVA.', 'vendor page'),
        ('Mold release film', 'PVA, over the wax', '1 (pint)', 'Partall #10 PVA film (Fiberglass Supply)', 'https://www.fiberglasssupply.com/partall/',
         '$8.36', 8.36, '', 'vendor page'),
        ('Edge rounds and fillets', '3/8 in PVC quarter-round, about 6 m; a tube of silicone', '1 set', 'PVC quarter-round molding + clear silicone (hardware store)', '',
         '~$20', 20.00, 'Quarter-round in the corners that make outside edges; silicone fillets elsewhere (the mold guide).', 'estimate'),
        ('Steel, stock flat bar and tube', 'Flat bar 3/8 in x 1-1/2 (4.2 ft), x 2 (3.1 ft), x 2-1/2 (8.4 ft), x 5 (3.3 ft); 1/2 x 2-1/2 in (2.6 ft). Tube 1/8 wall: 2x3 (4.0 ft), 2x2 (1.8 ft + 4x 8-1/8 in), 1-1/2x1-1/2 (3.4 ft + 4x 6 in)', '~110 lb', 'A local steel yard or Metal Supermarkets, cut to the list in docs/1-sourcing/steel/ (Online Metals, Speedy Metals and Zoro sell the same sizes by the piece)', '',
         '~$300', 300.00, 'About $1.50-3/lb at a yard or service center with cutting: get a quote with the cut list (Baltimore: Alro Metals Outlet, Essex; Metal Supermarkets, Golden Ring Rd). At about $2/lb it is near $220. Speedy Metals stock pieces are about $258 + $100-150 shipping, and you cut them. Retail cut pieces cost far more (Zoro: about $27/ft for 3/8 x 2-1/2 in bar). Drill and tap from docs/1-sourcing/steel/steel-templates.pdf.', 'estimate (Speedy Metals and Zoro listings)'),
        ('Rail risers', 'Cold-rolled 1018 x 1-1/4 in: 3/4 thick 2x 600 mm; 5/8 thick 2x 400 + 2x 300 mm', '~4 + 5 ft', 'Steel yard (local)', '',
         '~$40', 40.00, 'About 26 lb at $1-2/lb. Online: Speedy Metals $60 + shipping. Pieced bars are fine (two rail screws per piece).', 'estimate'),
        ('Aluminum plates', '6061 drops: table 3/4 x 10.5 x 13 in, X 5/8 x 7 x 16.5, Z 5/8 x 6.25 x 12.25', '~22 lb', 'eBay "6061 aluminum plate remnant" / local drops', '',
         '~$85', 85.00, 'About $2.3-4.5/lb delivered if you find drops; budget up to $120-190 if not (Speedy Metals 6061 cut to size is about $194 + shipping, Midwest MIC-6 $242). Ask the steel yard for drops. Check flatness; face the table on the machine.', 'estimate (eBay and Speedy Metals listings)'),
        ('Threaded rod', '1/2-13, cut to 4x 363, 2x 153, 2x 687, 4x 270, 6x 225 mm', '4x 6 ft', 'Everbilt 1/2-13 zinc threaded rod (Home Depot)', 'https://www.homedepot.com/p/332733421',
         '$14.93', 59.72, '6 ft: 687, 687, 363; 6 ft: 363, 363, 363, 270, 153; 6 ft: 270, 270, 270, 225, 225, 225; 6 ft: 225, 225, 225, 153 (hacksaw).', 'search snippet'),
        ('Beam studs', '3/8-16 grade B7 threaded rod: 8x 190 mm studs, 3x 107 mm ties; 3/8-16 nuts and washers (11)', '3x 3 ft', 'Redboar grade B7 threaded rod, 36 in, 5-pack (or Zoro, $16.25 each)', 'https://redboarchain.com/collections/threaded-fasteners/Threaded-Rod',
         '$49.10', 49.10, 'Grade B7 is about as strong as a grade 8 bolt; plain zinc rod is not. 36 in: 190, 190, 190, 190; 190, 190, 190, 190; 107, 107, 107 (with saw kerfs, two rods are not enough).', 'search snippet'),
        ('Pipe nipples', '1/2 in x 3 in black steel pipe nipple (beam spacers)', '3', 'Everbilt black pipe nipple (Home Depot)', '',
         '~$3', 9.00, '', 'estimate'),
        ('Bolts for the base grid', '1/4-20 hex bolts with nuts and washers: 24x 4 in (rail bars onto the girders), 4x 2-1/4 in (pads)', '1 set', 'Hardware store', '',
         '~$15', 15.00, '', 'estimate'),
        ('Nuts and washers', '1/2-13 nuts x32, 1/2 in SAE washers x32, 3/8 grade 8 washers x8', '5 packs', 'Everbilt packs (Home Depot)', 'https://www.homedepot.com/p/204284519',
         '~$28', 28.00, 'Nuts 15-pack $4.89; 1/2 washers 25-pack $9.75; 3/8 washers 25-pack $3.84', 'search snippets'),
        ('Dowel pins', '3/8 x 1-1/4 in (6) and 3/8 x 1 in (4, base split)', '2 (10-packs)', 'Steel dowel pins (Zoro)', 'https://www.zoro.com/i/G410073219/',
         '~$12', 11.58, 'They only locate the castings', 'search snippet (1-1/4 in pack $5.79)'),
        ('Feet', '1/2-13 x 2 in hex bolt + jam nut + rubber pad, per leg', '4', 'Hardware store bolts + rubber anti-vibration pads', '',
         '~$12', 12.00, 'The bolt screws into the nut in each leg end; turn it to level, lock with the jam nut. Leveling mounts (S&W NYL B24, $9.49 each) if you prefer.', 'estimate'),
        ('O-ring cord', 'NBR 3 mm, 2.5 m', '1 (3 m)', 'uxcell nitrile round strip 3 mm x 3 m', A + 'B0CNKM7L8B',
         '$6.56', 6.56, '', 'product page'),
        ('Cord splice glue', 'Cyanoacrylate', '1', 'Loctite 406, 20 g', A + 'B07H2YGBTJ',
         '$9.86', 9.86, '', 'product page'),
        ('M5 cast-in inserts', '17: the enclosure (11), the way-cover rollers (4) and the cable-chain mount (2). Nothing structural threads into the epoxy granite', '1 (30)', 'uxcell knurled brass M5 x 16 mm', A + 'B07R7LL1SG',
         '$11.08', 11.08, 'Screw each to the mold floor (wall) with a greased screw so it ends up flush. Cast them in even if the covers come later.', 'product page'),
        ('Low-head screws', 'DIN 7984 M5 x 20 (8, X risers) and M5 x 25 (10, Y risers)', '18', 'DIN 7984 low-head, class 8.8, by the piece (Olander, Bolt Depot or McMaster-Carr)', 'https://www.olander.com/items/.5C20LHCW',
         '~$15', 15.00, 'Head 3.5 mm tall, sits below the rail in the 4.5 mm counterbore. Zoro sells them only in 100-packs ($9.99 + $14.29).', 'search snippet (about $0.47 each + shipping)'),
        ('Support screws', 'M6 x 40 (12: the Y and X BK/BF into their tapped steel)', '1 (100)', 'Zoro M6x40 100-pack', 'https://www.zoro.com/i/G2650606/',
         '$10.15', 10.15, 'The casting is relieved behind each tapped hole, so they never bottom', 'search snippet'),
        ('Rail screws', 'M4 x 16', '1 (100)', 'iexcell M4x16 12.9', A + 'B08B1T9VM3',
         '$8.26', 8.26, '', 'product page'),
        ('Block screws', 'M4 x 20', '1 (50)', 'iexcell M4x20 12.9', A + 'B08B1T7K14',
         '$7.86', 7.86, 'Check length against the plate thickness', 'product page'),
        ('PETG filament', '1.1 kg (sliced): mold kit, core posts, formers and fillers, cast-in parts and machine parts', '2 (1 kg)', 'SUNLU PETG 1 kg', A + 'B0FS1FJLCW',
         '$15.99', 31.98, 'The pocket cores are foam (next row). Printing them instead (foam=False in the model) needs about 1.4 kg more.', 'product page'),
        ('XPS foam board', '2 in x 2 ft x 8 ft: the base pocket cores', '1', 'Owens Corning FOAMULAR 250, 2 in x 2 ft x 8 ft (Home Depot, model 24DD)', 'https://www.homedepot.com/p/Owens-Corning-FOAMULAR-250-2-in-x-2-ft-x-8-ft-R-10-Tongue-and-Groove-Rigid-Foam-Board-Insulation-Sheathing-24DD/100320335',
         '~$25', 25.00, 'Plus packing tape and double-sided carpet tape (~$10). Sizes in the mold guide.', 'estimate (price not shown)'),
        ('Foam tape', 'Double-sided carpet tape + packing tape', '1 each', 'Hardware store', '',
         '~$10', 10.00, '', 'estimate'),
        ('Drain nipple', '1/2 NPT brass', '1 (2-pack)', 'Legines brass barb 1/2 NPT x 5/8', A + 'B077DMKGLB',
         '$10.99', 10.99, 'Cast into the base, pointing down into the sump. +$7.59 shipping; a hardware-store 1/2 NPT brass nipple works too.', 'product page'),
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
         '$31.36', 31.36, 'Alt: CNCMANS HM12-57 B09QS2S3BT $28.98. AliExpress HM10-57 / HM12-57 brackets are about $10-15 each (2-4 weeks): about $35 less for the pair.', 'product page'),
        ('Couplers, Y', '8x10 mm, D25 L30', '1 (3-pack)', 'CNCTOPBAOS 8x10 plum coupling, 3 pcs', A + 'B082TT7B84',
         '$13.99', 13.99, 'Spares; check that D25 fits inside the bracket', 'product page'),
        ('Couplers, Z', '8x8 mm, D25 L30', '1 (2-pack)', 'Yeebyee 8x8 plum coupling, 2 pcs', A + 'B0GTV7VMZB',
         '$12.89', 12.89, 'The spare covers X if your kit came with 6.35x8. Alt (both rows): AliExpress plum couplers, about $3-5 each, 2-4 weeks.', 'product page'),
        ('Grease and syringe', 'Lithium NLGI 2 + a grease syringe with a needle tip, for the blocks\' M4 nipples', '1 each', 'Lithium grease tube + needle-tip grease syringe (hardware store or Amazon)', '',
         '~$12', 12.00, 'Enough for the blocks until the grease gun (add later).', 'estimate'),
        ('(opt) M4 grease nipples', 'M4x0.7 straight', '1 pack', 'HARFINGTON 15 pcs M4x0.7', A + 'B0CLP8NGRJ',
         '$13.94', 13.94, 'Only if the block nipples are missing or the coupler won\'t seat', 'product page'),
    ]),
    ('Part 1 - Frame: first chips', [
        ('Cutting fluid', 'Brush-on / drip, until flood coolant (part 3)', '1', 'Tap Magic or similar cutting fluid', '',
         '~$12', 12.00, 'Brush or drip it on; the base gutters and drain carry it down.', 'estimate'),
        ('Drain bin', 'Any plastic bin or tub that fits under the drain, between the legs', '1', 'Hardware store', '',
         '~$8', 8.00, 'Until the stainless sump (add later) or the flood coolant (part 3).', 'estimate'),
    ]),
    ('Part 1 - Frame: add later (niceties)', [
        ('Way cover strip', '0.1 mm 301 stainless', '1', 'SPCCGG 301 strip 0.1 x 300 x 1000 mm', A + 'B0DNQVM7RB',
         '$54.10', 54.10, 'Gives all three strips. If it turns out soft, use 304 full-hard B09ZQQJ34Z for the 85 mm strips. Fit the covers before steady steel work: chips wear the Y screw and rails.', 'product page'),
        ('Way cover springs', 'Constant force, about 0.5 x 30 in, 2.6 lb, for the printed rollers', '4', 'AndyMark am-4666 constant-force spring', 'https://andymark.com/products/0-5-in-wide-30-in-long-constant-force-spring',
         '$6.50', 26.00, 'One per narrow strip, two for the wide one; plus shipping. Alt: SUS301 5-pack (Amazon B0DMM8YSMM) $35.99, or tape-measure springs.', 'vendor page'),
        ('Spiral screw cover', '20 mm ID, size 20-250-40-28', '1', 'Spiral steel bellows cover (eBay, US seller)', 'https://www.ebay.com/itm/388297460024',
         '$21.85 + $4.99', 26.84, 'Clamps between the nut housing and the BK12: no fixing in the casting. Amazon: MISONONEIK B0GTDV8DZN about $47.', 'search snippet'),
        ('Roller screws', 'M5 x 12 button head (6): the roller feet into the cast-in inserts and the tapped BK pad', '6', 'Hardware store', '',
         '~$3', 3.00, 'The fixings are already in the base.', 'estimate'),
        ('Drip shield', '518 x 79 mm, 3 mm ACM', '0', 'Cut from the ACM sheet offcut (part 3)', '',
         '$0', 0.00, 'Clamped under the front beam stud nuts: no other fixing.', 'design change'),
        ('Sump', 'Full-size steam-table pan, 4 in deep (~13 L)', '1', 'Winco SPJH-104, 22 ga stainless (not Amazon)', 'https://www.katom.com/080-SPJH104.html',
         '$22.16-26.81', 26.81, 'Not found on Amazon; restaurant-supply stores (KaTom, GoFoodservice $23.63) or a local one. Slides in under the base, between the legs.', 'search result'),
        ('Chip basket', '1/3-size pan, 2-1/2 in deep', '1', 'CAC STPT-S25-2 1/3 pan (not Amazon)', 'https://www.gofoodservice.com/p/cac-stpt-s25-2',
         '$9.98', 9.98, 'Solid pan: drill 6 mm holes in the floor (or buy a perforated 1/3 x 2-1/2 in pan). Sits at the front, under the drain.', 'search result'),
        ('Grease gun', 'Mini, 3 oz cartridges', '1', 'Performance Tool W54205 mini grease gun kit', A + 'B002V0AIWW',
         '$17.59', 17.59, '', 'product page'),
        ('Needle tip', 'For the blocks\' M4 nipples', '1', 'LubriMatic 05-037 needle', A + 'B000FMO6XU',
         '$6.98', 6.98, '', 'product page'),
        ('Grease cartridges', 'Lithium NLGI 2', '1 (3x3 oz)', 'LubriMatic 11312, 3x 3 oz', A + 'B01JM4PCVG',
         '$11.79', 11.79, '', 'product page'),
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
         '$25.99', 25.99, 'Holds the controller, three drivers and both supplies on a plywood or aluminum backplate; the VFD mounts outside. Steel alt: VEVOR 12x10x6 $48.90.', 'reseller snapshot (LeMotech is sold on Amazon)'),
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
           'Parts to buy for the machine in `model/DIYCNC.FCStd` / `docs/5-design/report.txt`, sourced on Amazon (US) where it',
           'makes sense. Prices and stock were checked on **2026-10-09/10**. "?" means the price was not visible',
           '(Amazon blocks automated page reads); check the live listing. Shipping and tax are not included.',
           'Off-Amazon picks are marked "not Amazon": they are there because Amazon doesn\'t carry the part or',
           'is much dearer. Rows marked (opt) or (choice) are left out of the totals, and so is the "add later"',
           'section of Part 1.', '',
           'The same list is in `docs/1-sourcing/sourcing.csv` for a spreadsheet.', '']
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

    later = lambda s_: 'add later' in s_
    part = lambda n: [x for x in summary if x[0].startswith(f'Part {n}') and not later(x[0])]
    p1 = sum(p for _, p, _ in part(1))
    p1n = sum(p for s_, p, _ in summary if later(s_))
    p2 = sum(p for s_, p, _ in part(2) if 'spindle' not in s_)
    p3, u3 = sum(p for _, p, _ in part(3)), sum((u for *_, u in part(3)), [])
    total, n_unpriced = p1, 0
    head = ['## Totals', '',
            'The list is in three parts, so you can buy and build in that order: **Part 1** is the machine',
            'itself without the expensive equipment (castings, steel, rails, ballscrews), **Part 2** is the',
            'motors, controller, wiring and spindle, and **Part 3** is the enclosure and flood coolant. The',
            'machine runs after Part 2 with brush-on cutting fluid.', '',
            '**Add later (niceties).** The way covers, the screw cover, the drip shield, the stainless sump',
            'and the grease gun bolt on whenever you buy them: everything they fix to is already cast in (inserts',
            'and a tapped pad for the roller feet, inserts for the cable-chain mount, the beam studs for the drip',
            'shield) or needs no fixing, and so are the inserts, gutters, drain and sump space for Part 3. Fit the',
            'way covers before steady steel work. Anything cast in (the alumina grit, the inserts, the drain) has',
            'to be decided before the pour.', '',
            '| Part | Section | Priced |', '|---|---|---|']
    for n in (1, 2, 3):
        head += [f'| {n} | {(s_.split(": ", 1)[-1] if ": " in s_ else s_.split(" - ", 1)[-1]).capitalize()} | {money(p)} |' for s_, p, _ in part(n)
                 if 'spindle' not in s_]
        if n == 1:
            head += [f'| 1 | Add later (niceties), not in the frame total | {money(p1n)} |']
    head += ['', '| Part | About |', '|---|---|',
             f'| **1. Frame** | **{money(p1)}** + {money(p1n)} of niceties, added later |',
             f'| **2. Electronics + spindle** | **{money(p2)}** + spindle: $250-375 (1.5 kW 110 V kit) or $430-600 (2.2 kW + 120 V step-up VFD) |',
             f'| **3. Enclosure + flood coolant** | **{money(p3)}** + {len(u3)} unpriced ({", ".join(u3)}): about $650-700 |',
             f'| **Total** | **about ${(p1 + p2 + 250 + 650) / 1000:.2f}-{(p1 + p2 + 600 + 700) / 1000:.2f}k**, plus the niceties |', '',
             'Shipping and tax are extra (Raka ships free over $100). The whiting and Bolt Depot ship heavy or separately;',
             'buying the whiting and the steel locally saves most of it. Steel-yard and remnant prices are',
             'estimates: call a yard with the cut list.', '',
             '**JLCMC and JLCCNC (checked 2026-10-10).** JLCMC list prices are about half of Amazon for',
             'rails and couplings (e.g. the Y rail pair $27.40), but US orders prepay a 55 % duty plus DHL',
             'shipping, so the whole motion order comes to about $250-300 against about $190 here. There is',
             'no ready-made SFU1204 (lead 4) kit, and the 1605 screw-end machining for BK12/BF12 is not',
             'confirmed. Worth adding the rails and couplers only to a JLC order you are placing anyway.',
             'JLCCNC machining of the three aluminum plates with all holes is estimated at $430-850',
             'delivered (90 % duty prepaid on machined aluminum): only worth it for the X carriage if you',
             'want its hole pattern exact. Retail cut-to-size shops (e.g. Metal Supermarkets, about $820 for',
             'the tube, risers and aluminum) also cost more than the sources here.', '']
    i = md.index('The same list is in `docs/1-sourcing/sourcing.csv` for a spreadsheet.') + 2
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
           '   top plates are 0.5 mm thinner than the modeled 10 mm, which doesn\'t matter.',
           '6. **Low stock.** Several picks showed "only N left", including the closed-loop kits.',
           '']
    with open(os.path.join(SRC, 'sourcing.md'), 'w') as fh:
        fh.write('\n'.join(md))
    with open(os.path.join(DOCS, '1-sourcing', 'sourcing.csv'), 'w', newline='') as fh:
        w = csv.writer(fh)
        w.writerow(['Section', 'Item', 'Spec', 'Qty', 'Listing', 'URL', 'Unit price', 'Line total (USD)', 'Notes', 'Price source (2026-10-09)'])
        w.writerows(rows)
        w.writerow([])
        for s, p, u in summary:
            w.writerow(['Subtotal', s, '', '', '', '', '', f'{p:.2f}', f'{len(u)} unpriced', ''])
        w.writerow(['Total', 'Part 1, frame (without the add-later niceties)', '', '', '', '', '', f'{total:.2f}',
                    f'{n_unpriced} unpriced', ''])
    print(total, [(s, round(p, 2), len(u)) for s, p, u in summary])


main()
