#!/usr/bin/env python3
"""The notice groups' rows (#665, notice_window.py): over the eight groups of each leg, the retried notice from its
port's answer and each channel's longest held record, the least to the most, ms, bold over the bound.

usage: notice_table.py BUILDS "LABEL=LEG" ...   (each LEG is BUILDS/LEG/results/notice-retried-*.json)
"""
import json
import sys
from pathlib import Path

ROWS = (('stream_info', "a retried notice, from its port's answer to its last recipient's commit", 20.0),
        ('held.acmp', 'ACMP record, the longest held', 20.0), ('held.adp', 'ADP record, the longest held', 20.0),
        ('held.maap', 'MAAP record, the longest held', 20.0), ('held.aecp', 'AECP record, the longest held', 20.0),
        ('held.srp', 'SRP record, the longest held', 18.0))
builds, cols = Path(sys.argv[1]), sys.argv[2:]
data = {}
for col in cols:
    label, leg = col.split('=', 1)
    files = sorted((builds / leg / 'results').glob('notice-retried-*.json'))
    if len(files) != 8:
        sys.exit(f'{leg}: {len(files)} notice groups, not 8')
    seen: dict[str, list[float]] = {}
    for f in files:
        for p in json.loads(f.read_text())['probes']:
            key = p['probe'].split('.', 1)[1].rsplit('.', 1)[0]
            if p.get('ms') is not None:
                seen.setdefault(key, []).append(p['ms'])
    data[label] = seen
print('| Row | Bound, ms | ' + ' | '.join(data) + ' |')
print('|---|---:|' + '---:|' * len(data))
for key, name, bound in ROWS:
    cells = []
    for seen in data.values():
        v = seen.get(key)
        if not v:
            cells.append('-')
            continue
        lo, hi = min(v), max(v)
        cell = f'{lo:.2f} to {hi:.2f}'
        cells.append(f'**{cell}**' if hi > bound else cell)
    print(f'| {name} | {bound:g} | ' + ' | '.join(cells) + ' |')
