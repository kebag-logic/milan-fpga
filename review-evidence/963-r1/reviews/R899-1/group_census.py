#!/usr/bin/env python3
"""Compare live group identities with the published 481-pair differential."""
import json
import sys
from pathlib import Path
root,packet=(Path(v).resolve() for v in sys.argv[1:])
sys.path.insert(0,str(root/'tb/verilator/ctrl_service_budget'))
import run
import scenario
rows=json.loads((packet/'scratch/review-evidence/963-r1/author/receipts/harness-final/strict-rows.json').read_text())
count=0
for point,name in [('1x1','native-head-1x1'),('8x8-1if','native-head-ap')]:
    spec=json.loads((packet/'scratch'/name/'build.json').read_text())
    pt=scenario.point(point,spec)
    for arm in sorted({x['arm'] for x in rows if x['point']==point}):
        spec['variant']=arm
        expected={g.name for g in run.all_groups(pt,spec)}
        got={x['group'] for x in rows if x['point']==point and x['arm']==arm}
        assert expected==got,(point,arm,expected-got,got-expected)
        count+=len(expected)
assert count==481
print('PASS: all 481 live group names equal the published strict pairs across both points and eight arms.')
