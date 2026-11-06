#!/usr/bin/env python3
"""Recompute the round 1 / round 2 path comparison from the published results.json files. Usage: compare_rounds.py <evidence-root>"""
import json, sys
from pathlib import Path
root = Path(sys.argv[1])
total = same = 0
for run in ('1x1-idle', '1x1-ans', '8x8-idle', '8x8-ans'):
    a = json.load(open(root / 'author/receipts/runs' / run / 'results.json'))
    b = json.load(open(root / 'author-r2/receipts/runs' / run / 'results.json'))
    key = lambda r: (r['hook'], r['group'], r['probe'], r['interface'])
    A = {key(r): r for r in a['rows']}; B = {key(r): r for r in b['rows']}
    assert len(A) == len(a['rows']) and len(B) == len(b['rows']), 'duplicate keys'
    gone = sorted(set(A) - set(B)); added = sorted(set(B) - set(A))
    fields = ('ms', 'cpu_cycles', 'wait_ms', 'bound_ms', 'within', 'unbounded', 'loaded', 'margin_ms', 'normative_ms', 'slack_cycles', 'family', 'path')
    diffs = [(k, f, A[k].get(f), B[k].get(f)) for k in A if k in B for f in fields if A[k].get(f) != B[k].get(f)]
    total += len(A); same += sum(1 for k in A if k in B and all(A[k].get(f) == B[k].get(f) for f in fields))
    fa, fb = set(a['findings']), set(b['findings'])
    print(f"{run}: then {len(A)} now {len(B)} gone {len(gone)} added {len(added)} field diffs {len(diffs)}; refusals {len(a['refusals'])}/{len(b['refusals'])}; "
          f"findings then {len(fa)} now {len(fb)}, lost {len(fa-fb)}, gained {len(fb-fa)}; exe same {a['build']==b['build']}")
    for x in sorted(fa - fb)[:5]: print('   LOST', x[:150])
    for x in sorted(fb - fa):
        if 'counters.all.t' not in x: print('   GAINED(non-descriptor)', x[:150])
    print('   added not per-descriptor:', [k for k in added if '.t' not in k[2]])
    for d in diffs[:8]: print('   DIFF', d)
print('paths identical in every field:', same, 'of', total)
