#!/usr/bin/env python3
"""Each cost round 4's tools measured (costs24.py's costs.json, aecp_kinds.py's aecp.json, the datapath eventcost.py's
JSON) against every statement the tree under test makes of it at a point (1x1/1if by default):
  load_grade.GRADED (STATED_US_DONOR, the graded column) and load_grade.STATED_US (the pin column);
  rows_grade.ROW_COSTS (event.LINK);
  poll_grade.STATED_US[1] (the polls' base and items the harness holds every pass to; an SRP record's own apply to the
  retained item's, a kept ACMP command's accepted offer to the pin column's record.acmp);
  whole_grade.stated_us(1) (ctrl_loop.h: a build's, a build of one's and an aged step's pass);
  rows_tiers.DATAPATH_US, LONG_NOTICE_US, LONG_RECORD_US.
A measurement exceeds a statement when its rule figure (cycles / 100 x 1.05, rounded up to 5 us; the rule every table
states from) is above it; 'raw' also when cycles / 100 alone is.

usage: python3 -I compare_point.py TREE COSTS.json AECP.json DATAPATH.json RECORDS.json [POINT]  (#894 round 11: any point,
its interface count's poll_grade and whole_grade tables)
"""
import json
import math
import sys
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tree / 'tb/verilator/ctrl_service_budget'))
import load_grade  # noqa: E402
import poll_grade  # noqa: E402
import rows_grade  # noqa: E402
import rows_tiers  # noqa: E402
import whole_grade  # noqa: E402

P = sys.argv[6] if len(sys.argv) > 6 else '1x1/1if'
N_IF = load_grade.POINTS[P]['n_if']
rule = lambda c: int(math.ceil(c * 1.05 / 100 / 5 - 1e-9) * 5)
costs = json.loads(Path(sys.argv[2]).read_text())
most, where = costs['_most_cycles'], costs['_where']
kinds = json.loads(Path(sys.argv[3]).read_text())
datapath = json.loads(Path(sys.argv[4]).read_text())
records = json.loads(Path(sys.argv[5]).read_text())
G, S = load_grade.GRADED[P], load_grade.STATED_US[P]
POLL, WHOLE = poll_grade.stated_us(N_IF), whole_grade.stated_us(N_IF)
POLL_KEY = {'base': 'base', **{f'item.{k}': k for k in POLL}, 'item.record': 'retained'}
rows = []


def add(name, cycles, at, statements):
    for src, us in statements:
        if us is None:
            continue
        rows.append((name, cycles, at, src, us))


for k in sorted(most):
    c, at = most[k], where[k]
    st = [(f'load_grade.GRADED {k}', G.get(k)), (f'load_grade.STATED_US {k}', S.get(k)),
          (f'rows_grade.ROW_COSTS {k}', rows_grade.ROW_COSTS[P].get(k))]
    if k in POLL_KEY:
        st.append((f'poll_grade.STATED_US[{N_IF}] {POLL_KEY[k]}', POLL[POLL_KEY[k]]))
    if k == 'item.acmp_kept':
        st.append(('poll_grade.record_us (load_grade.STATED_US record.acmp)', poll_grade.record_us(N_IF)))
    if k == 'item.aecp_long':
        st.append(('rows_tiers.LONG_NOTICE_US', rows_tiers.LONG_NOTICE_US[P]))
    wk = {'build': 'build', 'build_one': 'build-one', 'step': 'step'}.get(k)
    if wk:
        st.append((f'whole_grade.stated_us({N_IF}) {wk} (ctrl_loop.h)', WHOLE[wk]))
    if k == 'record.aecp':
        continue                                                # per group below, by its group's statement
    if not any(us is not None for _, us in st):
        rows.append((k, c, at, 'no statement found', None))
    add(k, c, at, st)
for kind, v in kinds.items():
    key = f'item.aecp.{kind}'
    add(key, v['most_cycles'], v['where'], [(f'load_grade.GRADED {key}', G.get(key)),
                                             (f'load_grade.STATED_US {key}', S.get(key))])
for ev, v in datapath.items():
    if ev in rows_tiers.DATAPATH_US[P]:
        add(f'event.{ev}', v['max_cycles'], v['at'],
            [(f'rows_tiers.DATAPATH_US {ev}', rows_tiers.DATAPATH_US[P][ev])])
for k, v in records.items():
    if v['most']:
        add(f"record.aecp [{v['group']}]", v['most']['cycles'], f"{k}: {v['most']['command']}",
            [(v['stated_name'], v['stated_us'])] + ([('load_grade.STATED_US record.aecp', S['record.aecp'])]
                                                    if v['group'] != 'aecp-largest-notice' else []))
print(f'{"cost":40} {"most cycles":>11} {"us":>8} {"rule":>5} {"stated":>6} verdict  statement; where')
over = []
for name, c, at, src, us in rows:
    if us is None:
        print(f'{name:40} {c:>11,} {c / 100:>8.2f} {rule(c):>5} {"-":>6} -        {src}; {at}')
        continue
    v = 'OVER-raw' if c / 100 > us else ('OVER' if rule(c) > us else 'within')
    line = f'{name:40} {c:>11,} {c / 100:>8.2f} {rule(c):>5} {us:>6} {v:8} {src}; {at}'
    print(line)
    if v != 'within':
        over.append(line)
print(f'\n# {len(over)} statement(s) exceeded (OVER: by the rule; OVER-raw: cycles / 100 alone exceeds it)')
for line in over:
    print(line)
