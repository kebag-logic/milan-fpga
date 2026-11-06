#!/usr/bin/env python3
"""Recompute the README's History tables (50 MHz) from the published history results.json receipts.
Usage: python3 -I check_history.py <receipts dir> <README.md>"""
import json, sys
from pathlib import Path
rec, readme = Path(sys.argv[1]), Path(sys.argv[2]).read_text()
RUNS = {('1x1', 'idle'): '1x1-idle-50', ('1x1', 'answering'): '1x1-ans-50',
        ('8x8', 'idle'): '8x8-idle-50', ('8x8', 'answering'): '8x8-ans-50'}
data = {k: json.loads((rec / 'history' / v / 'results.json').read_text()) for k, v in RUNS.items()}
bad = 0
for k, d in data.items():
    print('info', k, d['clock'], d['cpu_hz'], 'refusals', len(d['refusals']), 'order',
          sum(x.startswith('ORDER') for x in d['findings']), 'superseded', len(d['superseded']))
    bad += d['cpu_hz'] != 50_000_000
for point in ('1x1', '8x8'):
    sec = readme.split(f'{point}, CPU 50 MHz on the Milan clock, ms; bold is over its bound:')[1].split('\n\n')[1]
    for line in sec.splitlines()[2:]:
        c = [x.strip() for x in line.strip('|').split('|')]
        got = []
        for loaded in (False, True):
            for arm in ('idle', 'answering'):
                part = [r for r in data[(point, arm)]['rows'] if r['hook'] == c[0] and r['loaded'] == loaded]
                if not part:
                    got.append('-'); continue
                top = max(part, key=lambda r: (r['unbounded'], r['ms'] - r['wait_ms']))
                v = 'never served' if top['unbounded'] else f"{top['ms']:.2f}"
                got.append(v if top['within'] else f'**{v}**')
        ok = got == c[2:6]
        bad += not ok
        print(('ok       ' if ok else 'MISMATCH '), point, c[0], 'readme', c[2:6], 'receipts', got)
print('mismatches:', bad)
sys.exit(1 if bad else 0)
