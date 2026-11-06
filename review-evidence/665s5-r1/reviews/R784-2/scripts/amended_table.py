#!/usr/bin/env python3
"""Read each published table.md: which path rows have an amended bound unlike the bound, and what that changes."""
import json, re, sys
from pathlib import Path
ev = Path(sys.argv[1])
for run, n_if in (('1x1-idle', 1), ('1x1-ans', 1), ('8x8-idle', 2), ('8x8-ans', 2)):
    text = (ev / f'author-r2/receipts/runs/{run}/table.md').read_text()
    res = json.load(open(ev / f'author-r2/receipts/runs/{run}/results.json'))
    by = {r['probe']: r for r in res['rows']}
    rows = []
    for line in text.splitlines():
        c = [x.strip() for x in line.split('|')[1:-1]]
        if len(c) == 13 and c[1].startswith('`'):
            rows.append(c)
    print(f'== {run}: {len(rows)} path rows in table, {len(res["rows"])} in results')
    kinds, flips = {}, []
    for c in rows:
        hook, probe, ms, bound, am, within = c[0], c[1].strip('`'), c[4], float(c[7]), float(c[8]), c[9]
        r = by[probe]
        assert bound == round(r['bound_ms'], 6) or f'{r["bound_ms"]:g}' == c[7], (probe, bound, r['bound_ms'])
        assert (within == 'yes') == r['within'], probe
        delta = am - bound
        key = (hook, 'counters.all*' if r['path'].startswith('counters.all') else 'other', delta)
        kinds[key] = kinds.get(key, 0) + 1
        if not r['unbounded'] and (r['ms'] <= bound) != (r['ms'] <= am):
            flips.append((probe, r['ms'], bound, am, r['group']))
    for k, v in sorted(kinds.items(), key=str):
        if k[2] != 0: print('  differs', k, v)
    print('  rows with the same bound:', sum(v for k, v in kinds.items() if k[2] == 0))
    print(f'  a verdict the amended bound would change: {len(flips)}')
    for f in flips: print('    ', f)
    srp = [r for r in res['rows'] if r['hook'] == 'H-SRP' and not r['unbounded'] and r['bound_ms'] < r['ms'] <= r['bound_ms'] + 2]
    print('  H-SRP within 2 ms over bound:', [(r['probe'], r['ms'], r['bound_ms']) for r in srp])
    c = sorted([(r['ms'], r['probe'], r['within']) for r in res['rows'] if r['path'].startswith('counters.all')])
    if c: print('  ALL rows', len(c), 'ms:', [x[0] for x in c])
