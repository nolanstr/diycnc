"""Builds the PDFs in docs/ from the Markdown in docs/src/ (Markdown -> HTML -> headless Chrome).

    python3 docs/src/make_pdfs.py

Needs the Python `markdown` package and Google Chrome.
"""

import os
import re
import subprocess
import sys
import tempfile
from datetime import date

import markdown

SRC = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.dirname(SRC)
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
LIST = re.compile(r'^(- |\d+\. )')

# source, output, page orientation
DOCUMENTS = [
    ('build-guide.md', 'build-guide.pdf', 'portrait'),
    ('print-guide.md', 'print-guide.pdf', 'portrait'),
    ('sourcing.md', 'sourcing.pdf', 'landscape'),
    ('design-notes.md', 'design-notes.pdf', 'portrait'),
]

CSS = """
@page { size: Letter %(orient)s; margin: 16mm 15mm 16mm 15mm; }
:root { --ink: #1d2422; --muted: #5b6662; --rule: #c9d0cc; --head: #2c3a35; --fill: #eef1ef; --accent: #a8641a; }
html { font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; font-size: 10pt; color: var(--ink); }
body { margin: 0; line-height: 1.45; }
h1 { font-size: 22pt; margin: 0 0 4pt; color: var(--head); letter-spacing: -0.01em; }
.sub { color: var(--muted); font-size: 9pt; margin-bottom: 14pt; border-bottom: 2px solid var(--accent); padding-bottom: 6pt; }
h2 { font-size: 14pt; color: var(--head); margin: 18pt 0 6pt; padding-bottom: 2pt; border-bottom: 1px solid var(--rule);
     break-after: avoid; }
h3 { font-size: 11pt; color: var(--head); margin: 12pt 0 4pt; break-after: avoid; }
p, li { orphans: 3; widows: 3; }
ul, ol { padding-left: 16pt; }
li { margin: 2pt 0; }
code { font-family: Menlo, Consolas, monospace; font-size: 8.5pt; background: var(--fill); padding: 0 2pt; border-radius: 2pt; }
pre { background: var(--fill); padding: 6pt 8pt; border-radius: 3pt; overflow-wrap: anywhere; white-space: pre-wrap; }
pre code { background: none; padding: 0; }
table { border-collapse: collapse; width: 100%%; margin: 6pt 0 10pt; font-size: %(table_pt)spt; }
th, td { border: 1px solid var(--rule); padding: 3pt 5pt; text-align: left; vertical-align: top; }
th { background: var(--fill); color: var(--head); }
tr { break-inside: avoid; }
td code { white-space: nowrap; }
img { display: block; max-width: 100%%; max-height: 105mm; margin: 6pt auto 10pt; break-inside: avoid; }
a { color: var(--accent); text-decoration: none; }
strong { color: var(--head); }
"""


def build(src, out, orient):
    with open(os.path.join(SRC, src)) as fh:
        text = fh.read()
    title = text.splitlines()[0].lstrip('# ').strip()
    # Python-Markdown nests lists only at 4-space indents, and needs a blank line before a list
    lines, prev = [], ''
    for ln in text.splitlines()[1:]:
        ln = re.sub(r'^ {2,3}(?=\S)', '    ', ln)
        if LIST.match(ln) and prev.strip() and not LIST.match(prev) and not prev.startswith(' '):
            lines.append('')
        lines.append(ln)
        prev = ln
    body_md = '\n'.join(lines)
    body = markdown.markdown(body_md, extensions=['tables', 'fenced_code', 'sane_lists'])
    css = CSS % dict(orient=orient, table_pt='8' if orient == 'landscape' else '8.5')
    html = (f'<!doctype html><html><head><meta charset="utf-8"><title>{title}</title>'
            f'<base href="file://{SRC}/"><style>{css}</style></head><body>'
            f'<h1>{title}</h1><div class="sub">DIY CNC epoxy-granite mill · {date.today():%B %Y}</div>'
            f'{body}</body></html>')
    with tempfile.NamedTemporaryFile('w', suffix='.html', delete=False) as fh:
        fh.write(html)
        tmp = fh.name
    pdf = os.path.join(DOCS, out)
    subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--no-pdf-header-footer',
                    '--allow-file-access-from-files', f'--print-to-pdf={pdf}', f'file://{tmp}'],
                   check=True, capture_output=True)
    os.remove(tmp)
    print(f'{out}: {os.path.getsize(pdf) / 1e6:.1f} MB')


def main():
    if not os.path.exists(CHROME):
        sys.exit('Google Chrome not found at ' + CHROME)
    for src, out, orient in DOCUMENTS:
        build(src, out, orient)


if __name__ == '__main__':
    main()
