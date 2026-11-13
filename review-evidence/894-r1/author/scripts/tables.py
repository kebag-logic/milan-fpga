#!/usr/bin/env python3
"""The measured tables of a point from its legs' regraded results.json: each tier's longest row against decision D's
bound (tier 1: AECP, ACMP, ADP, MAAP, 20 ms; SRP 90 ms), the queued notices (the first of each queue, every one), the
MRPDU rows, the three egress-held paths of tsn-c-stack #26 apart, the heaviest pass and the slices.
usage: tables.py POINT RESULTS.json... -> markdown"""
import json
import sys

EGRESS = ('backlog.owed_behind', 'backlog-owed.service.aecp.last', 'backlog.owed')   # longest first
TIER1 = {'aecp', 'acmp', 'adp', 'maap'}
point, paths = sys.argv[1], sys.argv[2:]
rows, notices, egress, passes, slices = {}, [], {}, [], {}
for path in paths:
    r = json.load(open(path))
    for g in r['results']:
        w = g['passes']['worst']
        if w:
            passes.append((w['cycles'], g['group']))
        s = g['passes'].get('slices') or {}
        for k, v in (s.get('longest') or {}).items():
            slices[k] = max(slices.get(k, (0, ''))[0], v), g['group'] if v >= slices.get(k, (0, ''))[0] else slices[k][1]
        for p in g['probes']:
            if p.get('status') not in ('measured', 'never answered') and 'ms' not in p:
                continue
            name = p['probe']
            if any(name.startswith(e) or p.get('path', [''])[0].startswith(e) for e in EGRESS):
                key = next(e for e in EGRESS if name.startswith(e) or p.get('path', [''])[0].startswith(e))
                egress[key] = max(egress.get(key, (0, '')), (p.get('ms', 0), g['group']))
                continue
            if p.get('status') != 'measured':
                continue
            ring, fam = p.get('ring'), p.get('family')
            tier = 'mrpdu' if p.get('path', [''])[0] == 'mrpdu' else 'tier 1' if ring in TIER1 else \
                'SRP' if ring == 'srp' else None
            if tier is None:
                continue
            k = (tier, ring)
            if k not in rows or p['ms'] > rows[k][0]:
                rows[k] = (p['ms'], g['group'], name)
    for n in r.get('notices', []):
        notices.append(n)
bound = {'tier 1': 20.0, 'SRP': 90.0, 'mrpdu': 20.0}
print(f'**{point}, by measurement** ({len(paths)} legs)\n')
print('| Tier | Row | Longest, ms | Bound, ms | Margin | Group |')
print('|---|---|---:|---:|---:|---|')
for (tier, ring), (ms, group, name) in sorted(rows.items()):
    b = bound[tier]
    print(f'| {tier} | {ring} | {ms:.3f} | {b:g} | {(b - ms) / b:.3f} | {group} |')
if notices:
    first = {}
    for n in notices:
        first[n['group']] = min(first.get(n['group'], 1e9), n['ms'])
    worst_first = max(first.values())
    last = max(n['ms'] for n in notices)
    print(f"| queued notices | the first of a queue, the latest | {worst_first:.3f} | {'20' if point.startswith('1x1') else '22'} |"
          f" | {len(first)} queues |")
    print(f"| queued notices | every one, the latest of {len(notices)} | {last:.3f} | {notices[0]['budget_ms']:g} | "
          f"{(notices[0]['budget_ms'] - last) / notices[0]['budget_ms']:.3f} | |")
for key, (ms, group) in sorted(egress.items()):
    print(f'| egress held (tsn-c-stack #26) | {key} | {ms:.3f} | 20 | | {group} |')
if passes:
    c, g = max(passes)
    print(f'\nHeaviest work pass {c:,} CPU cycles ({c / 100_000:.3f} ms, THE SHARE 2.000 ms), {g}.')
print('Longest tier-2 slices: ' + ', '.join(f'{k} {v:,} cycles ({g})' for k, (v, g) in sorted(slices.items())) + '.')
