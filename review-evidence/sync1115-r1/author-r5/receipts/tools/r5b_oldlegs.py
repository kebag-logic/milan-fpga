#!/usr/bin/env python3
"""r5b_oldlegs.py HARNESS OUT.json: round 2's thirteen harness legs (budget2/, 10b2fe21's testbench, which records no
owner), each group log read by HARNESS's grader: its MRP timer run-outs by outcome (mrpdu_grade.outcomes) and the
unowned ones a run names (join_grade.held, run.stated_misses), so whether the log now fails on them alone. An analysis
of the logs, not a regrade: these builds predate round 4's testbench and the head refuses to reuse them."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(sys.argv[1]) / 'tb/verilator/ctrl_service_budget'))
import grade  # noqa: E402
import join_grade  # noqa: E402
import mrpdu_grade  # noqa: E402
import run  # noqa: E402

S = Path('<scratch>')
out = {}
for log_path in sorted((S / 'budget2').glob('b*/results*/*.log')):
    text = log_path.read_text(errors='replace')
    log = grade.parse(text[:text.rfind('\n') + 1], 100_000_000, 100_000_000)
    runs: dict[str, int] = {}
    for _, _, outcome in mrpdu_grade.outcomes(log):
        runs[outcome] = runs.get(outcome, 0) + 1
    named = [m for m in run.stated_misses([dict(group='g', passes=dict(joins=join_grade.held(log)))])
             if m.endswith('(owner unresolved)')]
    key = str(log_path.relative_to(S / 'budget2'))
    out[key] = dict(run_outs=sum(runs.values()), runs=runs, named_unowned=len(named),
                    owned_entries=len(log.owners), fails_on_unowned=bool(named))
    print(key, out[key], flush=True)
total = dict(logs=len(out), with_run_outs=sum(1 for v in out.values() if v['run_outs']),
             failing_on_unowned=sum(1 for v in out.values() if v['fails_on_unowned']),
             run_outs=sum(v['run_outs'] for v in out.values()),
             unowned=sum(v['runs'].get('unowned', 0) for v in out.values()),
             named_unowned=sum(v['named_unowned'] for v in out.values()),
             owned_entries=sum(v['owned_entries'] for v in out.values()))
print('TOTAL', json.dumps(total))
Path(sys.argv[2]).write_text(json.dumps(dict(total=total, logs=out), indent=1) + '\n')
