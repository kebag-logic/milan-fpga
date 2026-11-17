"""8x8/1if's stated-table survey by the rule: each cost the measurement's tools found (costs24.py's costs.json,
aecp_kinds.py's aecp.json, the datapath eventcost.py's JSON; #665 round 28's and #902's tools, read only), against
every statement the tree under test makes of it at 8x8/1if, read at the point's shape (THE SHAPES), never at another
point's by its interface count:
  load_grade.stated(8x8/1if) in both columns (GRADED and STATED_US): the records' and events' costs its NEAREST
    point's, 8x8/2if's, and the polls, THE TRANSMIT's builds and an owed MRPDU its own shape's;
  poll_grade.stated_us at its shape (EIGHT_ONE: the polls' base and items the harness holds every pass to; an SRP
    record's own apply to the retained item's);
  whole_grade.stated_us at its shape (ctrl_loop.h's THE SHAPES: a build's, a build of one's; THE STEP's pass);
  rows_grade.ROW_COSTS and rows_tiers.DATAPATH_US at its NEAREST point (event.LINK and the datapath events);
  rows_tiers.LONG_RECORD_US and the largest legal notice (poll_grade aecp_long) at 8x8/1if; edit_rows.EDIT_RECORD_US.
A measurement exceeds a statement when its rule figure (cycles / 100 x 1.05, rounded up to 5 us) is above it; 'raw'
also when cycles / 100 alone is. The AECP records by class are record_classes.py's (in the tree). Prints every line,
then each statement exceeded; exit 1 when any is.
usage: python3 -I compare_8x8_1if.py TREE COSTS.json AECP.json DATAPATH.json"""
import json
import math
import sys
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tree / 'tb/verilator/ctrl_service_budget'))
import edit_rows  # noqa: E402
import load_grade  # noqa: E402
import poll_grade  # noqa: E402
import rows_grade  # noqa: E402
import rows_tiers  # noqa: E402
import shape_costs  # noqa: E402
import whole_grade  # noqa: E402

P = '8x8/1if'
NEAR = load_grade.NEAREST[P]
SHAPE = shape_costs.of_point(P, tree)
rule = lambda c: int(math.ceil(c * 1.05 / 100 / 5 - 1e-9) * 5)  # noqa: E731
costs = json.loads(Path(sys.argv[2]).read_text())
most, where = costs['_most_cycles'], costs['_where']
kinds = json.loads(Path(sys.argv[3]).read_text())
datapath = json.loads(Path(sys.argv[4]).read_text())
G, S = load_grade.stated(tree, P, load_grade.GRADED), load_grade.stated(tree, P, load_grade.STATED_US)
POLL, WHOLE = poll_grade.stated_us(SHAPE), whole_grade.stated_us(SHAPE)
POLL_KEY = {'base': 'base', **{f'item.{k}': k for k in POLL}, 'item.record': 'retained'}
rows = []


def add(name: str, cycles: int, at: str, statements: list) -> None:
    for src, us in statements:
        if us is not None:
            rows.append((name, cycles, at, src, us))


for k in sorted(most):
    c, at = most[k], where[k]
    st = [(f'load_grade.stated(8x8/1if) GRADED {k}', G.get(k)), (f'load_grade.stated(8x8/1if) STATED_US {k}', S.get(k)),
          (f'rows_grade.ROW_COSTS[{NEAR}] {k}', rows_grade.ROW_COSTS[NEAR].get(k))]
    if k in POLL_KEY:
        st.append((f'poll_grade.STATED_US[{tuple(SHAPE)}] {POLL_KEY[k]}', POLL[POLL_KEY[k]]))
    if k == 'item.acmp_kept':
        st.append(('load_grade.stated(8x8/1if) STATED_US record.acmp', S.get('record.acmp')))
    if k == 'item.aecp_long':
        st.append((f'poll_grade.STATED_US[{tuple(SHAPE)}] aecp_long', POLL['aecp_long']))
    wk = {'build': 'build', 'build_one': 'build-one', 'step': 'step'}.get(k)
    if wk:
        st.append((f'whole_grade.stated_us({tuple(SHAPE)}) {wk} (ctrl_loop.h)', WHOLE[wk]))
    if k == 'record.aecp':
        continue  # by class: record_classes.py
    if not any(us is not None for _, us in st):
        rows.append((k, c, at, 'no statement found', None))
    add(k, c, at, st)
for kind, v in kinds.items():
    key = f'item.aecp.{kind}'
    add(key, v['most_cycles'], v['where'], [(f'load_grade.stated(8x8/1if) GRADED {key}', G.get(key)),
                                             (f'load_grade.stated(8x8/1if) STATED_US {key}', S.get(key))])
for ev, v in datapath.items():
    if ev in rows_tiers.DATAPATH_US[NEAR]:
        add(f'event.{ev}', v['max_cycles'], v['at'], [(f'rows_tiers.DATAPATH_US[{NEAR}] {ev}',
                                                       rows_tiers.DATAPATH_US[NEAR][ev])])
print(f'# 8x8/1if at shape {tuple(SHAPE)}; its records and events NEAREST {NEAR}\'s; record.aecp by class in '
      f'record_classes.py (long {rows_tiers.LONG_RECORD_US[P]}, paced {edit_rows.EDIT_RECORD_US[P]}, other '
      f'{G["record.aecp"]} us)')
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
sys.exit(1 if over else 0)
