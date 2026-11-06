#!/usr/bin/env python3
"""Replay the amended column over the published rows with the head's rule, without importing the harness. Usage: amended_audit.py <evidence-root>"""
import json, sys
from pathlib import Path
root = Path(sys.argv[1]) / 'author-r2/receipts/runs'
CEIL = {'adp': 200.0, 'disc': 20.0, 'acmp': 20.0, 'aecp': 24.0, 'notify': 24.0, 'maap': 50.0, 'srp': 18.0}
base = lambda fam: min(20.0, CEIL[fam])
Q = {1: 20.0, 2: 60.0}
for run in ('1x1-idle', '1x1-ans', '8x8-idle', '8x8-ans'):
    b = json.load(open(root / run / 'results.json'))
    n = 2 if run.startswith('8') else 1
    changed, flips, srpband = [], [], []
    for r in b['rows']:
        svc = 20.0 if r['hook'] == 'H-SRP' else Q[n] if r['path'].startswith('counters.all') else base(r['family'])
        am = r['bound_ms'] - base(r['family']) + svc
        if am != r['bound_ms']:
            changed.append((r['hook'], r['path']))
        now = (not r['unbounded']) and r['ms'] <= am
        if now != r['within']:
            flips.append((r['probe'], round(r['ms'], 3), r['bound_ms'], am, r['within'], now))
    hooks_changed = sorted({h for h, _ in changed})
    print(f"{run}: rows {len(b['rows'])}, amended differs on {len(changed)} rows, hooks {hooks_changed}, "
          f"non-SRP changed {sorted({p for h, p in changed if h != 'H-SRP'})[:30]}")
    print(f"   verdict would flip on {len(flips)} rows")
    for f_ in flips: print('    FLIP', f_)
    rows = [r for r in b['rows'] if r['path'].startswith('counters.')]
    rows.sort(key=lambda r: r['ms'])
    if rows:
        over = [r for r in rows if r['path'].startswith('counters.all.') and not r['within']]
        desc = [r for r in rows if r['path'].startswith('counters.all.')]
        print(f"   per-descriptor {len(desc)}, over bound {len(over)}")
        prev = 0
        for r in rows:
            print(f"    {r['probe']:30s} grp {r['group']:20s} ms {r['ms']:9.3f} d {r['ms']-prev:7.3f} cyc {r['cpu_cycles']:>10} bound {r['bound_ms']:g} within {r['within']} wait {r['wait_ms']}")
            prev = r['ms']
    w = b['summary']['H-COUNTERS']['worst']
    print('   summary worst', {k: (v['probe'], v['ms']) for k, v in w.items()})
    print('   H-SRP rows in (18,20]:', [(r['probe'], r['ms'] - r['wait_ms']) for r in b['rows'] if r['hook'] == 'H-SRP' and 18.0 < r['ms'] - r['wait_ms'] <= 20.0 and not r['unbounded']])
