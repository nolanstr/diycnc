"""Slice every STL in print/ with Bambu Studio's command line (A1 mini, 0.4 mm nozzle, 0.2 mm layers,
Bambu PETG Basic) at the settings the print guide gives for each kind of part, and write the
filament each one really takes to print/sliced.csv.

    python3 model/slice_prints.py

build_cnc.py reads print/sliced.csv (if its files match the current STLs) for the print guide.
"""

import csv
import json
import math
import os
import re
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRINT = os.path.join(ROOT, 'print')
APP = '/Applications/BambuStudio.app/Contents'
BBL = APP + '/Resources/profiles/BBL'
MACHINE = BBL + '/machine/Bambu Lab A1 mini 0.4 nozzle.json'
PROCESS = BBL + '/process/0.20mm Standard @BBL A1M.json'
FILAMENT = BBL + '/filament/Bambu PETG Basic @BBL A1M 0.4 nozzle.json'
DIAMETER, DENSITY = 1.75, 1.27          # mm, g/cm^3

# walls, sparse infill: the same as the print guide
SETTINGS = {'core': (2, 10), 'former': (2, 10), 'filler': (2, 10), 'plug': (2, 10),
            'kit': (3, 15), 'part': (3, 15), 'liner': (3, 40), 'cast-in': (3, 40)}


def process_file(tmp, kind):
    walls, infill = SETTINGS[kind]
    cfg = json.load(open(PROCESS))
    cfg.update({'name': f'diycnc {kind}', 'wall_loops': str(walls), 'sparse_infill_density': f'{infill}%'})
    path = os.path.join(tmp, f'{kind}.json')
    json.dump(cfg, open(path, 'w'))
    return path


def slice_one(stl, proc, tmp):
    out = tempfile.mkdtemp(dir=tmp)
    subprocess.run([APP + '/MacOS/BambuStudio', '--slice', '0', '--arrange', '1',
                    '--load-settings', f'{MACHINE};{proc}', '--load-filaments', FILAMENT,
                    '--outputdir', out, stl], capture_output=True, timeout=900)
    gcode = os.path.join(out, 'plate_1.gcode')
    if not os.path.exists(gcode):
        return None, None
    text = open(gcode).read(200000)
    length = float(re.search(r'total filament length \[mm\] : ([\d.]+)', text).group(1))
    t = re.search(r'model printing time: ([^;]+);', text).group(1).strip()
    return length * math.pi * (DIAMETER / 2) ** 2 / 1000 * DENSITY, t


def minutes(t):
    m = re.findall(r'(\d+)([dhms])', t)
    return sum(int(v) * {'d': 1440, 'h': 60, 'm': 1, 's': 1 / 60}[u] for v, u in m)


def main():
    if not os.path.exists(APP):
        sys.exit('Bambu Studio not found')
    rows = list(csv.DictReader(open(os.path.join(PRINT, 'manifest.csv'))))
    tmp = tempfile.mkdtemp()
    procs = {k: process_file(tmp, k) for k in SETTINGS}
    jobs = [(r, os.path.join(PRINT, r['folder'], r['file'])) for r in rows]
    with ThreadPoolExecutor(4) as ex:
        res = list(ex.map(lambda j: slice_one(j[1], procs[j[0]['kind']], tmp), jobs))
    out, total, mins = [], 0.0, 0.0
    for (r, _), (g, t) in zip(jobs, res):
        qty = int(r['qty'])
        each = round(g, 1) if g is not None else ''
        out.append(dict(folder=r['folder'], file=r['file'], kind=r['kind'], qty=qty, grams_each=each,
                        grams=round(g * qty, 1) if g is not None else '', time_each=t or 'FAILED',
                        estimate=r['grams']))
        if g is not None:
            total += g * qty
            mins += minutes(t) * qty
        else:
            print('failed:', r['file'])
    with open(os.path.join(PRINT, 'sliced.csv'), 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)
    est = sum(float(r['grams']) for r in rows)
    print(f'sliced {len(out)} files: {total:.0f} g PETG (estimate was {est:.0f} g), about {mins / 60:.0f} h of printing')


if __name__ == '__main__':
    main()
