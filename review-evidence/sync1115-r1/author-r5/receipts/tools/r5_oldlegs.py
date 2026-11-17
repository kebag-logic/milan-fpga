#!/usr/bin/env python3
"""r5_oldlegs.py HARNESS OUT.json: round 2's thirteen harness legs (budget2/, 10b2fe21's testbench, no owner record),
each group log read by HARNESS's grader: every MRP timer run-out whose first build sends nothing, where the round-5
anchor (mrpdu_grade.anchor; with no owner recorded, the latest of the log's participants' transmit opportunities) puts
its lateness against where round 4's rule put it (the last join callback between), and whether its outcome moves. An
analysis of the logs, not a regrade: these builds predate round 4's testbench and the head refuses to reuse them."""
import importlib.util
import json
import sys
from pathlib import Path

spec = importlib.util.spec_from_file_location('r5_compare', Path(__file__).with_name('r5_compare.py'))
sys.argv = [sys.argv[0], sys.argv[1], '/dev/null', '/dev/null', *sys.argv[2:]]
compare = importlib.util.module_from_spec(spec)
spec.loader.exec_module(compare)
S = Path('<scratch>')
out = {}
for log_path in sorted((S / 'budget2').glob('b*/results*/*.log')):
    e = compare.empties(log_path)
    key = str(log_path.relative_to(S / 'budget2'))
    out[key] = dict({k: v for k, v in e.items() if k != 'every'}, every_moved=[x for x in e['every'] if x['anchor_moved']])
    print(key, e['count'], e['moved'], len(e['outcome_changed']), e['worst_after_anchor_ms'], flush=True)
total = dict(logs=len(out), builds=sum(v['count'] for v in out.values()), moved=sum(v['moved'] for v in out.values()),
             outcome_changed=sum(len(v['outcome_changed']) for v in out.values()),
             worst_after_anchor_ms=max([v['worst_after_anchor_ms'] for v in out.values()
                                        if v['worst_after_anchor_ms'] is not None], default=None))
print('TOTAL', json.dumps(total))
Path(sys.argv[4]).write_text(json.dumps(dict(total=total, logs=out), indent=1) + '\n')
