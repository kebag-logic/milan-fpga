#!/usr/bin/env python3
"""Recompute every run's rows and pass share from the published raw results.json files.

usage: recompute_rows.py <author-r12-results/receipts/measure>
Reads only JSON. For each run prints clock, refusals, the worst instance of each path against
min(T_svc, ceiling), and work passes re-derived from each group's own over_passes/passes/worst."""
import json, sys, pathlib
root = pathlib.Path(sys.argv[1])
SHARE = 200000
for d in sorted(root.iterdir()):
    r = json.loads((d / 'results.json').read_text())
    print(f"== {d.name} point={r['point']} clock={r.get('clock',{}).get('label')} groups={len(r['results'])} refusals={len(r['refusals'])} misses={len(r['misses'])} share_misses={len(r['share_misses'])}")
    tot = over = 0; longest = 0; lg = None
    for g in r['results']:
        s = g['passes'].get('share'); w = g['passes'].get('worst')
        tot += s['passes']; over += s['over']
        if w and w['cycles'] > longest: longest, lg = w['cycles'], g['group']
    print(f"  work passes {tot}, over {over}, longest {longest} cycles = {longest/1e5:.3f} ms in {lg}; share cycles {r['results'][0]['passes']['share']['cycles']}")
    for p in r['paths']:
        print('  ', {k: p.get(k) for k in ('path','interface','worst','ms','bound_ms','budget_ms','ceiling_ms','verdict','within') if k in p})
    print('  windows', [(w['group'], w.get('events_held'), w['window_ms'], w['cycles'], w['ms'], w['serviced'], w['unreleased']) for w in r['windows']])
    print('  maximum', r['composed_maximum'] if not isinstance(r['composed_maximum'], dict) else {k: v for k, v in r['composed_maximum'].items() if k not in ('windows',)})
