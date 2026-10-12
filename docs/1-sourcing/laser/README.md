# Laser-cut steel

The steel skeletons: plates that slot together. Send these to a laser-cutting service (JLCCNC, SendCutSend, OSH Cut), Metal Supermarkets, or anyone with a CNC plasma or router table. Mild steel (A36 or 1018), units mm. Each part is in three formats, same name: `dxf/` (the flat outline), `step/` and `stl/` (the plate lying flat at its thickness). The name starts with the thickness and how many to cut. Holes to be tapped are drawn at the tap drill size; tap them before assembly. Keep slots and tabs clean of dross: they should slide together by hand. Slots are 0.25 mm a side over the tabs (laser); for plasma set CLR in model/skeleton.py to about 0.5 and re-run.

32 different parts, 64 plates in all, about 48 kg.

| Part | Plate | Qty | Size (mm) | kg (all) | Notes |
|---|---|---|---|---|---|
| `1-2in_2x_top-plate-lower` | 1/2 in | 2 | 68.0 x 198.0 | 2.5 | tap 4 x 3/8-16 |
| `1-2in_2x_top-plate-upper` | 1/2 in | 2 | 68.0 x 198.0 | 2.5 |  |
| `3-8in_1x_base-cross-nose` | 3/8 in | 1 | 524.0 x 55.5 | 2.1 |  |
| `3-8in_2x_base-girder-bar-front` | 3/8 in | 2 | 38.1 x 272.6 | 1.5 |  |
| `3-8in_2x_base-girder-bar-rear` | 3/8 in | 2 | 38.1 x 343.6 | 1.9 |  |
| `3-8in_2x_base-girder-end-back-rear` | 3/8 in | 2 | 90.0 x 85.0 | 1.1 |  |
| `3-8in_1x_base-pad-bf` | 3/8 in | 1 | 80.0 x 43.2 | 0.2 | tap 2 x M6 |
| `3-8in_1x_base-pad-bk` | 3/8 in | 1 | 80.0 x 40.7 | 0.2 | tap 4 x M6 |
| `3-8in_2x_base-pedestal-bar-front` | 3/8 in | 2 | 62.0 x 66.0 | 0.5 |  |
| `3-8in_2x_base-pedestal-bar-rear` | 3/8 in | 2 | 62.0 x 293.0 | 2.5 |  |
| `3-8in_2x_base-rail-bar-front` | 3/8 in | 2 | 38.1 x 288.0 | 1.5 | tap 2 x M5 |
| `3-8in_2x_base-rail-bar-rear` | 3/8 in | 2 | 38.1 x 359.0 | 1.9 | tap 3 x M5 |
| `3-8in_2x_base-seat-front` | 3/8 in | 2 | 60.0 x 66.0 | 0.5 |  |
| `3-8in_2x_base-seat-rear` | 3/8 in | 2 | 60.0 x 285.0 | 2.3 |  |
| `3-8in_2x_beam-cap` | 3/8 in | 2 | 68.0 x 134.0 | 1.1 |  |
| `3-8in_1x_beam-face-plate` | 3/8 in | 1 | 510.0 x 140.0 | 3.6 | tap 8 x M5, 6 x M6 |
| `3-8in_2x_beam-seat` | 3/8 in | 2 | 68.0 x 134.0 | 1.1 |  |
| `3-8in_2x_upright-foot` | 3/8 in | 2 | 56.0 x 375.0 | 3.0 |  |
| `1-4in_1x_base-cross-bf-front` | 1/4 in | 1 | 234.0 x 100.5 | 0.6 |  |
| `1-4in_1x_base-cross-bk-rear` | 1/4 in | 1 | 524.0 x 100.5 | 1.3 |  |
| `1-4in_2x_base-cross-split-front` | 1/4 in | 2 | 510.0 x 90.9 | 2.5 |  |
| `1-4in_4x_base-girder-end-split-front` | 1/4 in | 4 | 90.0 x 85.0 | 1.4 |  |
| `1-4in_2x_base-girder-web-front` | 1/4 in | 2 | 288.5 x 110.0 | 1.4 |  |
| `1-4in_2x_base-girder-web-rear` | 1/4 in | 2 | 359.5 x 110.0 | 1.7 |  |
| `1-4in_2x_base-leg-plate-front` | 1/4 in | 2 | 46.0 x 55.0 | 0.2 |  |
| `1-4in_2x_base-leg-plate-rear` | 1/4 in | 2 | 73.2 x 55.0 | 0.4 |  |
| `1-4in_4x_base-pedestal-web-front` | 1/4 in | 4 | 66.0 x 110.0 | 0.7 |  |
| `1-4in_4x_base-pedestal-web-rear` | 1/4 in | 4 | 293.0 x 110.0 | 2.9 |  |
| `1-4in_1x_beam-back-plate` | 1/4 in | 1 | 510.0 x 140.0 | 1.8 |  |
| `1-4in_2x_beam-diaphragm-end` | 1/4 in | 2 | 104.6 x 140.0 | 1.3 |  |
| `1-4in_3x_beam-diaphragm-mid` | 1/4 in | 3 | 104.6 x 100.0 | 0.9 |  |
| `1-4in_2x_upright-brace` | 1/4 in | 2 | 171.1 x 233.4 | 0.6 |  |
