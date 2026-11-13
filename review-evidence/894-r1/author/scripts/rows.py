#!/usr/bin/env python3
"""The measured rows of budget-harness results by tier: each ring's (and family's) longest row per group and over
every group, against decision D's tier bounds (tier 1: AECP, ACMP, ADP and MAAP rows and the first queued notice,
20 ms; SRP's rows 90 ms; the last queued notice 125 ms at 1x1/1if; MRPDU rows reported against the 20 ms the loop held
them to before the tiers), and the harness's own budget. usage: rows.py RESULTS.json... -> markdown on stdout."""
import json
import sys
from collections import defaultdict

TIER1 = {'aecp', 'acmp', 'adp', 'maap'}


def bound(ring, family):
    if family == 'mrpdu':
        return 'mrpdu', 20.0
    if ring == 'srp':
        return 'srp', 90.0
    if ring in TIER1:
        return 'tier1', 20.0
    return f'other:{ring}/{family}', None


worst = {}
per_group = defaultdict(dict)
points = set()
for path in sys.argv[1:]:
    r = json.load(open(path))
    points.add(r['point'])
    for g in r['results']:
        for p in g['probes']:
            if p.get('status') != 'measured' or 'ms' not in p:
                continue
            tier, b = bound(p.get('ring'), p.get('family'))
            key = (r['point'], tier, p.get('ring'), p.get('family'))
            row = dict(group=g['group'], probe=p['probe'], ms=p['ms'], budget=p.get('budget_ms'), bound=b)
            if key not in worst or p['ms'] > worst[key]['ms']:
                worst[key] = row
            k2 = (tier, p.get('ring'))
            if k2 not in per_group[g['group']] or p['ms'] > per_group[g['group']][k2]['ms']:
                per_group[g['group']][k2] = row
    for n in r.get('notices', []):
        key = (r['point'], 'notice', n.get('group', '')[:12], 'notice')
        row = dict(group=n['group'], probe='notice', ms=n['ms'], budget=n.get('budget_ms'), bound=n.get('budget_ms'))
        if key not in worst or n['ms'] > worst[key]['ms']:
            worst[key] = row
print('| Point | Tier | Ring/family | Longest (ms) | Bound (ms) | Margin (ms) | Relative | Harness budget | Group, probe |')
print('|---|---|---|---:|---:|---:|---:|---:|---|')
for (point, tier, ring, family), row in sorted(worst.items()):
    b = row['bound']
    margin = f"{b - row['ms']:.2f}" if b else ''
    rel = f"{(b - row['ms']) / b:.3f}" if b else ''
    print(f"| {point} | {tier} | {ring}/{family} | {row['ms']:.3f} | {b or ''} | {margin} | {rel} | "
          f"{row['budget']} | {row['group']}, {row['probe']} |")
least = defaultdict(lambda: None)
for (point, tier, _, _), row in worst.items():
    if row['bound']:
        m = (row['bound'] - row['ms']) / row['bound']
        if least[(point, tier)] is None or m < least[(point, tier)][0]:
            least[(point, tier)] = (m, row)
print()
print('| Point | Tier | Least relative margin | ms | bound | group, probe |')
print('|---|---|---:|---:|---:|---|')
for (point, tier), (m, row) in sorted(least.items()):
    print(f"| {point} | {tier} | {m:.3f} | {row['ms']:.3f} | {row['bound']} | {row['group']}, {row['probe']} |")
