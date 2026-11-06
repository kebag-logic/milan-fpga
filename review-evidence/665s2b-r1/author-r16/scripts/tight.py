#!/usr/bin/env python3
"""The tightest rows of a graded results.json: each row's margin to its bound, least first. usage: tight.py RESULTS [N]"""
import json, sys
sys.path.insert(0, '$VALIDATION_STORAGE/665s2b-a683u/C/tb/verilator/ctrl_service_budget')
import scenario  # noqa: E402
d = json.load(open(sys.argv[1]))
n = int(sys.argv[2]) if len(sys.argv) > 2 else 10
rows = []
for g in d['results']:
    for r in g['probes']:
        if r.get('status') != 'measured' or r.get('unanswered') or r.get('starved'):
            continue
        b = min(scenario.T_SVC_MS, scenario.CEILING_MS[r['family']]) + r.get('wait_ms', 0.0)
        rows.append((b - r['ms'], r['ms'], b, r['probe']))
rows.sort()
for m, ms, b, p in rows[:n]:
    print(f'{m:+.3f} {ms:.3f}/{b:g} {p}')
print('share over:', sum(g['passes']['share']['over'] for g in d['results']), 'longest:',
      max(g['passes']['worst']['ms'] for g in d['results'] if g['passes']['worst']))
