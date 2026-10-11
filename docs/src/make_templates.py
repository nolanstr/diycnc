"""Printable 1:1 drilling templates for the mold boards: one PDF per mold in docs/3-molds/templates/.

    python3 docs/src/make_templates.py      (make_pdfs.py runs it too)

Each board is tiled onto US Letter pages at full size. Only pages with holes on them are printed; every
page carries a grid labeled in the board's own coordinates, so a page can be placed on its own, and the
board's edges where the page reaches them. Reads docs/src/boards/boards.json, written by
model/build_cnc.py.
"""

import json
import math
import os
import subprocess
import tempfile
from datetime import date

SRC = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.dirname(SRC)
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
PAGE = (215.9, 279.4)                  # Letter, mm
MARGIN = 7.5                           # most printers print to within 6.35 mm (1/4 in) of the edge
HEAD = 17.0                            # header band at the top of each page
OVERLAP = 12.0
MOLDS = [('base', 'Base mold'), ('upright', 'Upright molds'), ('beam', 'Beam mold')]
COLORS = {3.2: '#7a4fb5', 3.4: '#7a4fb5', 4.5: '#c0561a', 5.5: '#1f7a4d', 6.5: '#1f7a4d', 9.6: '#9a2b2b',
          10.0: '#9a2b2b', 13.1: '#1d5fa8', 13.5: '#1d5fa8', 16.3: '#1d5fa8', 63.5: '#444'}


def tiles(w, h):
    """Page windows (x0, y0) in board mm, origin bottom-left, covering the board with OVERLAP, the board
    centred in them. Each also has its own area (no overlap) that holes are counted in."""
    cw, ch = PAGE[0] - 2 * MARGIN, PAGE[1] - 2 * MARGIN - HEAD
    nx = max(1, math.ceil((w + 1 - OVERLAP) / (cw - OVERLAP)))
    ny = max(1, math.ceil((h + 1 - OVERLAP) / (ch - OVERLAP)))
    sx = -(nx * (cw - OVERLAP) + OVERLAP - w) / 2
    sy = -(ny * (ch - OVERLAP) + OVERLAP - h) / 2
    return [(sx + i * (cw - OVERLAP), sy + j * (ch - OVERLAP), i, j, nx, ny) for j in range(ny) for i in range(nx)], cw, ch


def page_svg(b, x0, y0, cw, ch, label, fb):
    """One page: the board drawn at 1:1 through a cw x ch window whose bottom-left is (x0, y0)."""
    W, H = PAGE
    ox, oy = MARGIN, MARGIN + HEAD                    # window's top-left on the page
    X = lambda x: ox + (x - x0)
    Y = lambda y: oy + (y0 + ch - y)
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}" '
         f'font-family="Helvetica, Arial, sans-serif">',
         f'<defs><clipPath id="c"><rect x="{ox}" y="{oy}" width="{cw}" height="{ch}"/></clipPath></defs>',
         f'<text x="{MARGIN}" y="{MARGIN + 4.5}" font-size="4.6" font-weight="bold" fill="#1d2422">{b["name"]}'
         f'{" (x" + str(b["qty"]) + ": mark each)" if b["qty"] > 1 else ""}</text>',
         f'<text x="{MARGIN}" y="{MARGIN + 9.5}" font-size="3.2" fill="#5b6662">page {label} · full size · '
         f'lay it on the {"top (outside) face" if b["view"] == "outside" else "cast face (the side the mix touches)"}'
         f' · board {b["size"][0]:.0f} x {b["size"][1]:.0f} mm</text>']
    # 50 mm scale bar, top right
    sx = W - MARGIN - 52
    o += [f'<rect x="{sx}" y="{MARGIN + 2}" width="50" height="3" fill="none" stroke="#222" stroke-width="0.3"/>',
          f'<rect x="{sx}" y="{MARGIN + 2}" width="25" height="3" fill="#222"/>',
          f'<text x="{sx + 25}" y="{MARGIN + 9.5}" font-size="2.8" text-anchor="middle" fill="#222">'
          f'50 mm: measure it</text>']
    o.append(f'<g clip-path="url(#c)">')
    # grid every 50 mm, labeled in board coordinates
    for gx in range(int(math.floor(x0 / 50)) * 50, int(x0 + cw) + 51, 50):
        o.append(f'<line x1="{X(gx):.2f}" y1="{oy}" x2="{X(gx):.2f}" y2="{oy + ch}" stroke="#c9d0cc" stroke-width="0.2"/>')
        o.append(f'<text x="{X(gx) + 0.8:.2f}" y="{oy + ch - 1.2:.2f}" font-size="2.4" fill="#8a948f">x {gx}</text>')
    for gy in range(int(math.floor(y0 / 50)) * 50, int(y0 + ch) + 51, 50):
        o.append(f'<line x1="{ox}" y1="{Y(gy):.2f}" x2="{ox + cw}" y2="{Y(gy):.2f}" stroke="#c9d0cc" stroke-width="0.2"/>')
        o.append(f'<text x="{ox + 0.8}" y="{Y(gy) - 0.8:.2f}" font-size="2.4" fill="#8a948f">y {gy}</text>')
    pts = ' '.join(f'{X(x):.2f},{Y(y):.2f}' for x, y in b['outline'])
    o.append(f'<polygon points="{pts}" fill="none" stroke="#111" stroke-width="0.6"/>')
    if b['pour']:
        py, pa, pb = b['pour']
        o.append(f'<line x1="{X(pa):.2f}" y1="{Y(py):.2f}" x2="{X(pb):.2f}" y2="{Y(py):.2f}" stroke="#2b72c9" '
                 f'stroke-width="0.5" stroke-dasharray="4,2"/>')
        for lx in range(int(pa) + 15, int(pb) - 40, 120):
            o.append(f'<text x="{X(lx):.2f}" y="{Y(py) + 4:.2f}" font-size="3" fill="#2b72c9">POUR LINE: fill to here '
                     f'({fb:.0f} mm below the top edge)</text>')
    for k, (x, y, d, what, drill) in enumerate(b['holes'], 1):
        c = COLORS.get(round(d, 1), '#c0561a')
        r = d / 2
        o += [f'<circle cx="{X(x):.2f}" cy="{Y(y):.2f}" r="{r:.2f}" fill="none" stroke="{c}" stroke-width="0.35"/>',
              f'<line x1="{X(x) - max(r, 3) - 3:.2f}" y1="{Y(y):.2f}" x2="{X(x) + max(r, 3) + 3:.2f}" y2="{Y(y):.2f}" '
              f'stroke="{c}" stroke-width="0.2"/>',
              f'<line x1="{X(x):.2f}" y1="{Y(y) - max(r, 3) - 3:.2f}" x2="{X(x):.2f}" y2="{Y(y) + max(r, 3) + 3:.2f}" '
              f'stroke="{c}" stroke-width="0.2"/>',
              f'<text x="{X(x) + max(r, 2) + 0.8:.2f}" y="{Y(y) - max(r, 2) - 0.6:.2f}" font-size="3.4" font-weight="bold" '
              f'fill="{c}">{k}</text>']
    o.append('</g>')
    # legend: the hole sizes on this page
    sizes = sorted({(d, drill) for x, y, d, what, drill in b['holes'] if x0 <= x <= x0 + cw and y0 <= y <= y0 + ch})
    lx = MARGIN
    for d, drill in sizes:
        c = COLORS.get(round(d, 1), '#c0561a')
        txt = f'{d:g} mm' + (f' ({drill})' if drill else '')
        o += [f'<circle cx="{lx + 1.6:.2f}" cy="{MARGIN + HEAD - 2.6:.2f}" r="1.4" fill="{c}"/>',
              f'<text x="{lx + 4:.2f}" y="{MARGIN + HEAD - 1.6:.2f}" font-size="2.9" fill="{c}">{txt}</text>']
        lx += 6 + len(txt) * 1.55
    o.append(f'<rect x="{ox}" y="{oy}" width="{cw}" height="{ch}" fill="none" stroke="#999" stroke-width="0.25" '
             f'stroke-dasharray="1.5,1.5"/>')
    o.append('</svg>')
    return '\n'.join(o)


def cover(title, index, fb):
    W, H = PAGE
    return f'''<div class="page cover">
<h1>{title}: drilling templates</h1>
<p class="sub">DIY CNC epoxy-granite mill · {date.today():%B %Y} · full size, US Letter</p>
<h2>Printing</h2>
<ol>
<li>Print at <b>Actual size / 100 %</b>. Turn off "Fit to page" and "Scale to fit". Letter paper, portrait.</li>
<li>Measure the square below: it must be 100 mm (and the bar on every page 50 mm). If it is off by more than
1 mm, fix the scaling and print again.</li>
<li>Only pages with holes are printed. Every page has a grid labeled in the board's own millimeters, from the
bottom-left corner as you look at the marked face, so you can place any page on its own.</li>
</ol>
<h2>Marking a board</h2>
<ol>
<li>Lay the board on the bench with the face named at the top of its pages up (the cast face, or the top face for
bridges and cleats).</li>
<li>Start with the page that has the board's corner on it: line its printed edges up with the board's edges and tape it
down. Add the next pages overlapping by about 12 mm, with the grid lines on top of each other; trim one edge if
it helps. Where a page shows no board edge, measure to a labeled grid line with a square instead.</li>
<li>Push an awl or a center punch through every crosshair. The circle is the finished hole size, the number is the
hole's number in the guide's table, and the color is its size: the legend at the top of each page gives the drill.</li>
<li>Pull the paper off, and drill from the marked face (clamp a scrap underneath). Drill a 1/8 in pilot first for
anything 13 mm or bigger; the 63.5 mm holes are a 2-1/2 in hole saw.</li>
<li>Walls: pencil the dashed <b style="color:#2b72c9">pour line</b> ({fb:.0f} mm below the top edge) on the cast face, or
mark it later with the printed pour-line gauge. The casting is filled to this line.</li>
<li>Boards marked "x2" are the same board twice: mark both from one print.</li>
</ol>
<div class="square"><div>100 mm</div></div>
<h2>Pages</h2>
<table><tr><th>Board</th><th>Qty</th><th>Pages</th><th>Holes</th></tr>{index}</table>
</div>'''


CSS = '''@page { size: Letter portrait; margin: 0; }
html, body { margin: 0; padding: 0; font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; color: #1d2422; }
.page { width: 215.9mm; height: 279.4mm; page-break-after: always; overflow: hidden; position: relative; }
.page svg { display: block; }
.cover { box-sizing: border-box; padding: 14mm 15mm; font-size: 9.5pt; line-height: 1.4; }
.cover h1 { font-size: 19pt; margin: 0 0 2pt; } .cover .sub { color: #5b6662; margin: 0 0 8pt; font-size: 9pt; }
.cover h2 { font-size: 11.5pt; margin: 10pt 0 3pt; border-bottom: 1px solid #c9d0cc; }
.cover ol { margin: 0; padding-left: 16pt; } .cover li { margin: 2pt 0; }
.square { width: 100mm; height: 100mm; border: 0.4mm solid #111; margin: 8pt 0; position: relative; }
.square div { position: absolute; top: 45%; width: 100%; text-align: center; font-size: 11pt; }
table { border-collapse: collapse; font-size: 8.5pt; width: 100%; }
th, td { border: 1px solid #c9d0cc; padding: 2pt 5pt; text-align: left; } th { background: #eef1ef; }'''


def main():
    data = json.load(open(os.path.join(SRC, 'boards', 'boards.json')))
    fb = data['freeboard']
    out_dir = os.path.join(DOCS, '3-molds', 'templates')
    os.makedirs(out_dir, exist_ok=True)
    for mold, title in MOLDS:
        pages, index = [], []
        for b in data['boards']:
            if b['mold'] != mold or not b['holes']:
                continue
            w, h = b['size']
            ts, cw, ch = tiles(w, h)
            kept = []
            for x0, y0, i, j, nx, ny in ts:
                own = lambda x, y: (x0 + (OVERLAP / 2 if i else -1e3) <= x < x0 + cw - (OVERLAP / 2 if i < nx - 1 else -1e3)
                                    and y0 + (OVERLAP / 2 if j else -1e3) <= y < y0 + ch - (OVERLAP / 2 if j < ny - 1 else -1e3))
                if any(own(x, y) for x, y, *_ in b['holes']):
                    kept.append((x0, y0, f'{chr(65 + (ny - 1 - j))}{i + 1}'))
            first = len(pages) + 2
            for x0, y0, lab in kept:
                pages.append(f'<div class="page">{page_svg(b, x0, y0, cw, ch, lab, fb)}</div>')
            index.append(f'<tr><td>{b["name"]}</td><td>{b["qty"]}</td><td>{first}-{first + len(kept) - 1} '
                         f'({len(kept)})</td><td>{len(b["holes"])}</td></tr>')
        html = (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>'
                + cover(title, ''.join(index), fb) + ''.join(pages) + '</body></html>')
        with tempfile.NamedTemporaryFile('w', suffix='.html', delete=False) as fh:
            fh.write(html)
            tmp = fh.name
        pdf = os.path.join(out_dir, f'{mold}-templates.pdf')
        subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--no-pdf-header-footer', f'--print-to-pdf={pdf}',
                        f'file://{tmp}'], check=True, capture_output=True)
        os.remove(tmp)
        print(f'3-molds/templates/{mold}-templates.pdf: {len(pages) + 1} pages')


if __name__ == '__main__':
    main()
