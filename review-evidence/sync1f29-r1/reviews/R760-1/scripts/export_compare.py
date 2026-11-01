#!/usr/bin/env python3
"""Compare two export trees file by file after removing timestamps, output paths and the comment-only hierarchy tree."""
import re, sys, hashlib
from pathlib import Path
a, b = Path(sys.argv[1]), Path(sys.argv[2])
def norm(p, root):
    t = p.read_bytes().decode('utf-8', 'replace')
    t = t.replace(str(root), '<OUT>')
    t = re.sub(r'\S*/scratch/tree(-dev|-exp)?', '<TREE>', t)
    t = re.sub(r'(?m)^(.*(Generated|built|Auto-generated).*)\b\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}.*$', '<STAMP>', t)
    t = re.sub(r'\b\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\b', '<STAMP>', t)
    t = re.sub(r'(?ms)^// -{5,}\n// Module hierarchy.*?^// -{5,}\n', '', t)
    t = re.sub(r'(?m)^[ /*]*[└├│].*\n', '', t)
    return t
bad = tot = 0
for cfg in sorted(d.name for d in a.iterdir() if d.is_dir()):
    fa = {p.relative_to(a / cfg) for p in (a / cfg).rglob('*') if p.is_file() and p.name != 'litex.log'}
    fb = {p.relative_to(b / cfg) for p in (b / cfg).rglob('*') if p.is_file() and p.name != 'litex.log'}
    diff = sorted(str(f) for f in fa ^ fb)
    same = 0
    for f in sorted(fa & fb):
        tot += 1
        if norm(a / cfg / f, a / cfg) == norm(b / cfg / f, b / cfg):
            same += 1
        else:
            bad += 1; diff.append('DIFFERS ' + str(f))
    print(f'{cfg}: {same} of {len(fa | fb)} generated files equal; differences: {diff}')
print(f'total files {tot}, differing {bad}')
sys.exit(bool(bad))
