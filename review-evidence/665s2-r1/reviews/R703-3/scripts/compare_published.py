#!/usr/bin/env python3
"""Compare the reviewer's graded groups with the author's published per-group results.
Usage: compare_published.py MY_RESULTS_DIR PUBLISHED_DIR"""
import json
import sys
from pathlib import Path
mine, theirs = Path(sys.argv[1]), Path(sys.argv[2])
same = diff = 0
for p in sorted(theirs.glob('*.json')):
    if p.name == 'results.json' or not (mine / p.name).exists():
        continue
    a, b = json.loads((mine / p.name).read_text()), json.loads(p.read_text())
    ra = {r['probe']: r for r in a['probes']}
    for r in b['probes']:
        x = ra.get(r['probe'])
        keys = ('status', 'ms', 'bound_ms', 'ahead', 'starved', 'unanswered', 'owed_ahead', 'fanout')
        if x is None or any(x.get(k) != r.get(k) for k in keys):
            diff += 1
            print('DIFF', p.stem, r['probe'], {k: (x or {}).get(k) for k in keys}, {k: r.get(k) for k in keys})
        else:
            same += 1
    for k in ('worst', 'composed'):
        if a['passes'][k] != b['passes'][k]:
            diff += 1
            print('DIFF', p.stem, k)
print(f'{same} probe rows identical, {diff} differences')
