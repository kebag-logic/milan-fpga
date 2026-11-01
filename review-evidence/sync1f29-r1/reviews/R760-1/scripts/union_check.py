#!/usr/bin/env python3
"""For each file both lines touched: lines either side added since the merge base that are absent at the head."""
import subprocess, sys
from collections import Counter
BASE, OURS, DEV, HEAD = '97aab1d0', '5b5f4336', '1f29f189', '9f81df0054'
def show(rev, path):
    r = subprocess.run(['git', 'show', f'{rev}:{path}'], capture_output=True, text=True, errors='replace')
    return Counter(r.stdout.splitlines()) if r.returncode == 0 else Counter()
def names(a, b):
    return set(subprocess.run(['git', 'diff', '--name-only', a, b], capture_output=True, text=True).stdout.split())
both = sorted(names(BASE, OURS) & names(BASE, DEV))
total = 0
for f in both:
    b, o, d, h = (show(r, f) for r in (BASE, OURS, DEV, HEAD))
    for side, s in (('split', o), ('dev', d)):
        lost = [l for l in (s - b) if l not in h and l.strip()]
        total += len(lost)
        print(f'{f}\t{side}\tadded-lines-absent-at-head={len(lost)}')
        for l in lost:
            print('    ' + l[:300])
print('files', len(both), 'lost lines', total)
