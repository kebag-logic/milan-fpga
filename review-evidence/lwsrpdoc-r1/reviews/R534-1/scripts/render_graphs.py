#!/usr/bin/env python3
"""Reviewer-owned Mermaid extraction and render (independent of doc/tools).
Usage: render_graphs.py <clone> <outdir>. Writes <page>-<line>.mmd/.svg/.png and a TSV summary
with node/edge counts and longest label so readability can be judged, not just parse success."""
import re, subprocess, sys
from pathlib import Path
clone, out = Path(sys.argv[1]), Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
rows = []
for md in sorted(list(clone.glob('*.md')) + list((clone / 'doc').rglob('*.md'))):
    lines = md.read_text().splitlines(); i = 0
    while i < len(lines):
        m = re.match(r'^\s*(~~~|```)mermaid\s*$', lines[i])
        if not m: i += 1; continue
        start = i + 1; j = i + 1
        while not re.match(r'^\s*' + re.escape(m[1]) + r'\s*$', lines[j]): j += 1
        src = '\n'.join(lines[i + 1:j]); i = j + 1
        rel = md.relative_to(clone).as_posix(); stem = f"{rel.replace('/', '-')}-{start}"
        (out / f'{stem}.mmd').write_text(src + '\n')
        kind = src.split()[0]
        if kind == 'sequenceDiagram':
            nodes = set(re.findall(r'participant\s+(\w+)', src)); edges = len(re.findall(r'-+>>', src))
            labels = re.findall(r'(?:->>|-->>|Note over [^:]+):\s*(.+)', src)
        elif kind.startswith('stateDiagram'):
            pairs = re.findall(r'^\s*(\S+)\s*-->\s*(\S+?)(?::|\s*$)', src, re.M)
            nodes = {x for p in pairs for x in p if x != '[*]'}; edges = len(pairs)
            labels = re.findall(r'-->\s*\S+\s*:\s*(.+)', src)
        else:
            nodes = set(re.findall(r'(\w+)\[', src)); edges = len(re.findall(r'-\.?->', src))
            labels = re.findall(r'\[([^\]]+)\]', src)
        direction = (re.search(r'^(?:flowchart|graph)\s+(\w+)', src) or re.search(r'direction\s+(\w+)', src))
        longest = max((len(l) for l in labels), default=0)
        rcs = []
        for ext in ('svg', 'png'):
            cmd = ['mmdc', '-i', str(out / f'{stem}.mmd'), '-o', str(out / f'{stem}.{ext}'), '-b', 'white']
            if ext == 'png': cmd += ['-s', '2']
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=120); rcs.append(r.returncode)
        rows.append((rel, start, kind, len(nodes), edges, direction[1] if direction else 'default', longest, rcs[0], rcs[1]))
print('page\tline\ttype\tnodes\tedges\tdirection\tlongest_label_chars\tsvg_rc\tpng_rc')
for r in rows: print('\t'.join(map(str, r)))
print(f'# graphs={len(rows)} failures={sum(1 for r in rows if r[7] or r[8])}')
