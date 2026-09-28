#!/usr/bin/env python3
"""R380-4: exposure of the pinned processor tree to separators the sweep does
not claim. Run from the parent root with protocol-processor at its pin.
A. Counts lines in docs/hdl/tb whose first non-blank token is '--', ';', '>',
   '%%', and lines containing '<br/>' or SVG <text>/<tspan> elements.
B. Builds a wider variant of the named sweep whose joints also cross '-', ';',
   '>', '%', '<br/>'-style tags and any XML tag run, and reports matched lines
   it adds over the sweep as written (candidate statements the sweep misses).
C. For SVG files, strips tags (joining text runs with spaces) and runs the
   multi-word alternatives on the flattened text.
Measurement only; exit 0.
"""
import re, subprocess, glob, html
D3 = 'docs/design/SAVED_STATE_MATERIALIZATION.md'
PP = 'protocol-processor'
sec = open(D3, encoding='utf-8').read().split('### 15.2', 1)[1].split('\n## 16.', 1)[0]
PAT = re.match(r"^rg -n -U -i -C 2 '(.*)' docs hdl tb$", [l for l in sec.splitlines() if l.startswith('rg ')][0]).group(1)
def rg(args):
    return subprocess.run(['rg'] + args, cwd=PP, capture_output=True, text=True).stdout
print('## A. unclaimed prefix usage (matching lines in docs hdl tb)')
for label, p in [('--', r'^\s*-- '), (';', r'^\s*; '), ('>', r'^\s*> '), ('%%', r'^\s*%%'), ('<br/>', r'<br\s*/?>'), ('svg <text>/<tspan>', r'<(text|tspan)\b')]:
    out = rg(['-c', p, 'docs', 'hdl', 'tb'])
    n = sum(int(l.rsplit(':', 1)[1]) for l in out.splitlines() if l)
    print(f'   {label:20} {n} lines in {len(out.splitlines())} files')
J = r'(?:[[:space:]/!#*;>%-]|<[^>\n]*>)+'
W = PAT.replace('[[:space:]/!#*]+', J)
def lines(p):
    out = rg(['-n', '-U', '-i', p, 'docs', 'hdl', 'tb'])
    return {(m.group(1), int(m.group(2))) for m in (re.match(r'^(.+?):(\d+):', l) for l in out.splitlines()) if m}
s, w = lines(PAT), lines(W)
print(f'## B. sweep matched lines {len(s)}; wider variant {len(w)}; added {len(w - s)}')
for f, n in sorted(w - s):
    src = open(f'{PP}/{f}', encoding='utf-8', errors='replace').read().splitlines()[n - 1].strip()[:140]
    print(f'   ADDED {f}:{n}  {src}')
multi = [a for a in PAT.split('|') if '[[:space:]' in a]
print('## C. flattened SVG text, multi-word alternatives:', len(multi))
hits = 0
for f in sorted(glob.glob(f'{PP}/docs/**/*.svg', recursive=True)):
    t = html.unescape(re.sub(r'<[^>]*>', ' ', open(f, encoding='utf-8', errors='replace').read()))
    t = re.sub(r'\s+', ' ', t)
    for a in multi:
        py = a.replace('[[:space:]/!#*]+', r'[\s/!#*]+')
        for m in re.finditer(py, t, re.I):
            hits += 1
            print(f'   SVG {f[len(PP)+1:]}: ...{t[max(0,m.start()-60):m.end()+60]}...')
print(f'   svg files {len(glob.glob(f"{PP}/docs/**/*.svg", recursive=True))}, flattened multi-word hits {hits}')
