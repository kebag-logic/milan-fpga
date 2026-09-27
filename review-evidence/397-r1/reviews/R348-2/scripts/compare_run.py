#!/usr/bin/env python3
"""Compare a reviewer run receipt with the published receipt of the same plan.
usage: compare_run.py <reviewer.json> <published.json>"""
import json, sys
a, b = (json.load(open(p)) for p in sys.argv[1:3])
print('reviewer log sha256 ', a['log_sha256']); print('published log sha256', b['log_sha256'])
same = {k: a[k] == b[k] for k in ('raw_log', 'rows', 'budget_findings', 'heartbeat', 'liveness', 'input_hashes')}
print(same)
ma = dict(a['media']); mb = dict(b['media'])
print('media equal ignoring shape key:', {k: v for k, v in ma.items() if k != 'shape'} == {k: v for k, v in mb.items() if k != 'shape'},
      '| shape key reviewer/published:', ma.get('shape'), mb.get('shape'))
print('findings:', a['budget_findings'])
sys.exit(0 if all(same.values()) else 1)
