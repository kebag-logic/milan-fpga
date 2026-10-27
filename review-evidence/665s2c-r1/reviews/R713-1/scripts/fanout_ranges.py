"""Fan-out ranges over every probe with a fanout record of more than one recipient, per arm group: per-recipient CPU cycles
and the probe's ms, with the misses. usage: fanout_ranges.py RUNS_DIR"""
import json
import sys
from pathlib import Path

def rows(arm):
    for p in arm.glob('*.json'):
        for r in json.loads(p.read_text()).get('probes', []):
            if r.get('status') == 'measured' and r.get('fanout'):
                yield r

sets = {'A1 cache': ['P1-64x1'], 'B1 cache': ['B1-64x1'], 'A8 cache': ['P8-64x1'], 'B8 cache': ['B8-64x1'],
        'A1 none': ['P1-none'], 'A8 none': ['P8-none']}
runs = Path(sys.argv[1])
for name, arms in sets.items():
    every = [r for a in arms for r in rows(runs / a)]
    print(f'{name}: every fan-out record, recipients {sorted({r["fanout"]["recipients"] for r in every})}, groups {sorted({r["probe"].split(".")[0] for r in every})}')
    rs = [r for r in every if r['fanout']['recipients'] > 1]
    per = [r['fanout']['per_recipient_cpu_cycles'] for r in rs]
    ms = [r['ms'] for r in rs]
    miss = [r for r in rs if not r['within_t_svc']]
    over = [r for r in rs if not r['within_ceiling']]
    rec = sorted({r['fanout']['recipients'] for r in rs})
    print(f'{name}: {len(rs)} fan-outs, recipients {rec}, per recipient {min(per):,} to {max(per):,}; '
          f'ms {min(ms):.2f} to {max(ms):.2f}; miss {len(miss)} '
          f'({min((r["ms"] for r in miss), default=0):.2f} to {max((r["ms"] for r in miss), default=0):.2f}); over ceiling {len(over)}')
