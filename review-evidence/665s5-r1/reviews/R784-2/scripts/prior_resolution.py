#!/usr/bin/env python3
"""counters-late's catch rule on this review's own unplanted hooks-counters run, which is what a no-op plant yields."""
import json, sys
from pathlib import Path
S, root = Path(sys.argv[1]), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_hooks'))
import hooks_selftest as st, hooks, run
res = json.load(open(S / 'b1x1/results/results.json'))
late = [x for x in res['findings'] if x.startswith('LATE ')]
plant = hooks.plants()['counters-late'][1]
print(f'unplanted hooks-counters at 1x1: {len(late)} LATE findings; catch rule wants {run.plant_wanted(plant)!r}; matches {run.plant_findings(plant, res["findings"])}')
for b, p in (('b1x1', '1x1'), ('b8x8', '8x8')):
    g = json.load(open(S / b / 'results/hooks-counters.json'))
    worst = 0.0
    rows = [x for x in g['probes'] if x['probe'].startswith('counters.all.t')]
    for r in rows:
        first = (r['fanout']['first_sys'] - r['start_sys']) / 1e5
        fan = (r['fanout']['last_sys'] - r['fanout']['first_sys']) / 1e5
        worst = max(worst, abs(fan - round(fan, 2)))
    print(p, 'per-descriptor rows', len(rows), 'first notice range', round(min((x['fanout']['first_sys']-x['start_sys'])/1e5 for x in rows), 2), 'own fan-out range',
          round(min((x['fanout']['last_sys']-x['fanout']['first_sys'])/1e5 for x in rows), 2), round(max((x['fanout']['last_sys']-x['fanout']['first_sys'])/1e5 for x in rows), 2))
