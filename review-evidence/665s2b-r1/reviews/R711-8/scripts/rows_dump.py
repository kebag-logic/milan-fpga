"""Reviewer check (R711-8): the head's rows by every source with every input and term, the rule checks, and the
sensitivity variants (retry in every row, one retry fewer, SRP's arrivals over the whole W). Run from the reviewed
clone's tb/verilator/ctrl_service_budget: python3 -B <this> dump|variants."""
import math, sys
from pathlib import Path
sys.path.insert(0, '.')
import rows_grade as r
root = Path('../../..').resolve()
if sys.argv[1] == 'dump':
    for pt in r.POINTS:
        i = r.point_inputs(root, pt)
        print(pt, 'h', {k: i.h[k] for k in ('CTRL_LOOP_DRAIN_US', 'CTRL_LOOP_RX_PER_PASS', 'CTRL_LOOP_TICK_US',
                                            'CTRL_LOOP_STEP_AGE', 'CTRL_LOOP_STEP_PASS_US')})
        print(' rate', i.rate, 'tick', i.tick_ms); print(' s', i.s)
        print(' c', {k: v for k, v in sorted(i.c.items())})
        for row, (w, d) in r.rows(root, pt).items():
            print(' ', row, w, {k: round(v, 3) for k, v in d.items()})
    print(r.rule_findings(root)); print(r.unsourced(root))
else:
    r.RETAINED_ROWS = ('R4', 'R5', 'R6')
    for pt in r.POINTS:
        for row, (w, d) in r.rows(root, pt).items():
            if row in r.SOLVED:
                print('retry-in-all', pt, row, w, round(d.get('item.retained', 0), 3))
    r.RETAINED_ROWS = ('R4',)
    orig = r.retained_retries
    r.retained_retries = lambda w, p, t: min(p, math.floor(w / t) + 1)
    for pt in r.POINTS:
        print('plus1-rule', pt, 'R4', r.rows(root, pt)['R4'][0])
    r.retained_retries = orig
    r.srp_window = lambda w, i: w
    for pt in r.POINTS:
        print('srp-whole-W', pt, 'R4', r.rows(root, pt)['R4'][0])
