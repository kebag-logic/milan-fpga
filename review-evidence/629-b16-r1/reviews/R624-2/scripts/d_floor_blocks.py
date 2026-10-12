#!/usr/bin/env python3
"""Classify every one-second block of a loop-control grade (per_block lists)
as silent (no signal), off the loop's floor (> median + 3 dB) or at the floor.
usage: d_floor_blocks.py <grade.json>..."""
import json, sys
def walk(x, path=''):
    if isinstance(x, dict):
        if 'per_block' in x and 'median' in x:
            yield path, x
        for k, v in x.items():
            yield from walk(v, f'{path}/{k}')
    elif isinstance(x, list):
        for i, v in enumerate(x):
            yield from walk(v, f'{path}[{i}]')
for f in sys.argv[1:]:
    for p, t in walk(json.load(open(f))):
        med = t['median']['thdn_db']; pb = t['per_block']
        silent = [i for i, b in enumerate(pb) if b['level_dbfs'] < -200]
        off = [i for i, b in enumerate(pb) if i not in silent and b['thdn_db'] > med + 3]
        at = len(pb) - len(silent) - len(off)
        print(f'{f} {p}: blocks {len(pb)}, silent {silent}, off-floor {off}, at the floor {at}, rule-count {len(pb) - len(off)}')
