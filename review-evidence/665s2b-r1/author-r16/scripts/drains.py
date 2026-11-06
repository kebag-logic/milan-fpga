#!/usr/bin/env python3
"""Each save window's drain (#665): from its opening (MARK composed) to the end of the pass that released the last
of its records (the latest end_sys of its graded rows), per leg, and the longest over the windows opened from idle,
at the age limit and one short of it. A window opened with the step's age at zero takes an aged step only at its
third centisecond, at least two ticks (20 ms) after it opens, so 20 ms less the longest drain from idle is that
margin over the whole tick.

usage: drains.py BUILDS LEG ...
"""
import json
import re
import sys
from pathlib import Path

builds, legs = Path(sys.argv[1]), sys.argv[2:]
SYS_HZ = 100_000_000
for leg in legs:
    res = json.loads((builds / leg / 'results/results.json').read_text())
    sets: dict[str, list[tuple[float, str, str]]] = {'idle': [], 'aged2': [], 'aged1': []}
    for g in res['results']:
        name = g['group']
        if '@' not in name:
            continue
        log = (builds / leg / 'results' / f'{name}.log').read_text(errors='replace')
        start = int(re.search(r'^MARK (\d+) composed$', log, re.M).group(1))
        rows = [r for r in g['probes'] if r.get('status') == 'measured' and '.service.' in r['probe']]
        last = max(rows, key=lambda r: r['end_sys'])
        key = 'aged2' if '-aged2-' in name else 'aged1' if '-aged1-' in name else 'idle'
        sets[key].append(((last['end_sys'] - start) * 1000 / SYS_HZ, name, last['probe'].rpartition('.service.')[2]))
    for key, rows in sets.items():
        if not rows:
            continue
        top = max(rows)
        print(f'{leg} {key}: {len(rows)} windows, the longest drain {top[0]:.3f} ms ({top[1]}, {top[2]}); '
              f'20 ms less it: {20 - top[0]:.3f} ms')
