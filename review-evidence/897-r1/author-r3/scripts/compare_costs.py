#!/usr/bin/env python3
"""The CPU budget harness at the head against the base, per arm and point: each path's worst instance (CPU cycles and
ms against its bound), each group's worst work pass, the counts of refusals and misses, read from the two runs'
results.json (run.py's own record, read-only). usage: compare_costs.py HEAD_BUILD BASE_BUILD LABEL"""
import json, sys
from pathlib import Path
h, b, label = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
H = json.loads((h / 'results/results.json').read_text()); B = json.loads((b / 'results/results.json').read_text())
key = lambda p: (p['path'], p['interface'])
hp = {key(p): p for p in H['paths']}; bp = {key(p): p for p in B['paths']}
print(f"## {label}: head build {H['build'][:12]}, base build {B['build'][:12]}, point {H['point']}")
print(f"counts head {H['counts']} base {B['counts']}")
for k in ('refusals', 'misses', 'share_misses', 'notice_misses'):
    print(f"{k}: head {len(H.get(k) or [])} base {len(B.get(k) or [])}")
print("| path | if | head cycles | base cycles | delta | head ms (bound) | within bound |")
print("|---|---:|---:|---:|---:|---|---|")
worst_delta = (0, None)
for k in sorted(set(hp) | set(bp)):
    a = hp.get(k, {}).get('worst') or {}; c = bp.get(k, {}).get('worst') or {}
    ha, ba = a.get('cpu_cycles'), c.get('cpu_cycles')
    d = (ha - ba) if ha is not None and ba is not None else None
    if d is not None and abs(d) > abs(worst_delta[0]): worst_delta = (d, k)
    print(f"| {k[0]} | {k[1]} | {ha} | {ba} | {d if d is not None else 'n/a'} | {a.get('ms')} ({a.get('bound_ms')}) | {a.get('within_ceiling') and a.get('bound_within_budget')} |")
for r, s in zip(H['results'], B['results']):
    hw, bw = r['passes']['worst'] or {}, s['passes']['worst'] or {}
    print(f"group {r['group']}: worst work pass head {hw.get('cycles')} base {bw.get('cycles')} cycles; work passes head {r['passes']['work']} base {s['passes']['work']}")
print(f"largest path delta: {worst_delta[0]} cycles at {worst_delta[1]}")
