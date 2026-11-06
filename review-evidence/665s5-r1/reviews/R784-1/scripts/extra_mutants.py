"""Extra grader mutants against the hook harness's own self-test (run in-process, nothing written to the checkout).
Usage: python3 -I -B extra_mutants.py <checkout> <receipts/runs dir>"""
import json, sys
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch
root, runs = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_hooks'))
import hooks_build, hooks  # noqa: E402,F401  imported first, as run.py imports them
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_hooks'))  # as hooks_selftest does after them
import hooks_selftest  # noqa: E402
hooks, run = hooks_selftest.hooks, hooks_selftest.run
HELD = run.held_row
def relaxed_held(held, spec):            # held push graded with its W added to the bound
    r = HELD(held, spec)
    if not r.get('missing'):
        r['bound_ms'] += r['wait_ms']; r['within'] = r['ms'] <= r['bound_ms']
    return r
def missing_fits(held, spec):            # a held push never sent is neither missing nor over: no finding
    r = HELD(held, spec); r.pop('missing', None); r['within'] = True; r['unbounded'] = False; return r
SUMMARY = run.summary
def best_not_worst(graded):              # the table's 'worst' cell picks the fastest path
    out = SUMMARY(graded)
    for name, s in out.items():
        for k in ('alone', 'loaded'):
            part = [r for r in graded['rows'] if r['hook'] == name and r['loaded'] == (k == 'loaded')]
            if part: s['worst'][k] = min(part, key=lambda r: r['ms'])
    return out
MUT = [('held push graded with W added to its bound', patch.object(run, 'held_row', relaxed_held)),
       ('a held push never sent is no finding', patch.object(run, 'held_row', missing_fits)),
       ('summary reports the best path as the worst', patch.object(run, 'summary', best_not_worst))]
for name, p in MUT:
    with p:
        buf = StringIO()
        with redirect_stdout(buf):
            got = hooks_selftest.run_checks()
    failed = [k for k, v in got.items() if v]
    print(f'EXTRA MUTANT {name}: {"caught by " + ", ".join(failed) if failed else "ESCAPED (no self-test check fails)"}')
# Independent recomputation of each hook's worst path from the published rows (not from the published summary).
for d in ('1x1-idle', '1x1-ans', '8x8-idle', '8x8-ans'):
    r = json.load(open(runs / d / 'results.json'))
    bad = []
    for h, s in r['summary'].items():
        for k in ('alone', 'loaded'):
            part = [x for x in r['rows'] if x['hook'] == h and x['loaded'] == (k == 'loaded')]
            if not part: continue
            top = max(part, key=lambda x: (x['unbounded'], x['ms'] - x['wait_ms']))
            if top['probe'] != s['worst'][k]['probe']: bad.append((h, k, top['probe'], s['worst'][k]['probe']))
            lat = sorted({f.split(':')[1].strip() for f in r['findings'] if f.startswith(f'LATE {h}:')})
            miss = sorted({x['probe'] for x in r['rows'] if x['hook'] == h and not x['within']})
            if lat != miss: bad.append((h, 'LATE findings != rows over bound', lat, miss))
    print(f'{d}: worst-path recomputation and LATE-vs-rows consistency: {"OK" if not bad else bad}')
