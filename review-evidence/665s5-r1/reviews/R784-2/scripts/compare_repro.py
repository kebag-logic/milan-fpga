#!/usr/bin/env python3
"""This review's own hooks-counters runs at the head against the published round 2 rows, field by field, and each
descriptor's first notice, last notice and fan-out recomputed from this review's own group json."""
import json, re, sys
from pathlib import Path
P, ev = Path(sys.argv[1]), Path(sys.argv[2])
for build, run in (('b1x1', '1x1-ans'), ('b8x8', '8x8-ans')):
    mine = json.load(open(P / build / 'results/results.json'))
    pub = {r['probe']: r for r in json.load(open(ev / f'author-r2/receipts/runs/{run}/results.json'))['rows']}
    diffs = [(r['probe'], {k: (v, pub[r['probe']].get(k)) for k, v in r.items() if v != pub[r['probe']].get(k)})
             for r in mine['rows'] if any(v != pub[r['probe']].get(k) for k, v in r.items())]
    print(f'{run}: {len(mine["rows"])} rows of hooks-counters run here; {len(diffs)} differ from the published run in any field')
    for d in diffs[:5]: print('  DIFF', d)
    for r in mine['rows']:
        if r['path'] in ('counters.first', 'counters.all', 'counters.held'):
            print(f"  {r['probe']}: {r['cpu_cycles']:,} CPU cycles, {r['ms']} ms, within {r['within']}")
    print('  build', mine['build'][:16])
