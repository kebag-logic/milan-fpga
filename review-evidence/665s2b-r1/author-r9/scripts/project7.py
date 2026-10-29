#!/usr/bin/env python3
"""Scratch: per composed row (last ACMP, AECP and SRP records), arm A, the worst instance over the backlog groups,
and what each fetch geometry would make of it by round 6's fetch L1 model: the window less its measured refill wait
times the fraction of refills the model removes at that geometry (icache_geometry.py on the window's trace).
usage: project7.py LEG ..."""
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import prof  # noqa: E402
import icache_geometry as ig  # noqa: E402
T = Path('$VALIDATION_STORAGE/665s2b-a683k')
GEO = ((64, 1), (32, 2), (16, 4), (128, 1), (64, 2), (256, 1), (128, 2), (64, 4))
print('| Run | Row | Group | Window, ms | Refills (wait, ms) | ' +
      ' | '.join(f'{s * w * 64 // 1024} KiB {w}-way' for s, w in GEO[1:]) + ' |')
print('|---|---|---|---:|---:|' + '---:|' * (len(GEO) - 1))
for leg in sys.argv[1:]:
    rows = {}
    for g in prof.GROUPS:
        results = T / 'builds' / leg / 'results'
        res = json.loads((results / f'{g}.json').read_text())
        log = T / 'traces' / f'{leg}-{g}' / f'{g}.log'
        start = min(prof.window(res, r)[0] for r, _ in prof.ROWS if prof.window(res, r))
        c0 = next(int(l.split()[1]) for l in open(log) if l.startswith('PC '))
        off = c0 - (start - 300000)
        for row in ('acmp', 'aecp', 'srp'):
            w = prof.window(res, row)
            if w is None or (g == 'backlog-owed' and row == 'aecp'):
                continue
            a = prof.analyse(results, g, row, 1)
            warm, inside, fetches = ig.load(str(log), w[0] + off, w[1] + off)
            base = ig.refills(warm, inside, 64, 1)
            proj = [a['window_ms'] - a['irefill_ms'] * (1 - ig.refills(warm, inside, s, k) / base) for s, k in GEO[1:]]
            cand = (a['window_ms'], g, a['irefills'], a['irefill_ms'], proj)
            if row not in rows or cand[0] > rows[row][0]:
                rows[row] = cand
    for row in ('acmp', 'aecp', 'srp'):
        ms, g, n, wait, proj = rows[row]
        print(f'| {leg} | {row.upper()} record, last | `{g}` | {ms:.2f} | {n:,} ({wait:.2f}) | '
              + ' | '.join(('**%.2f**' if p > 10 else '%.2f') % p for p in proj) + ' |', flush=True)
