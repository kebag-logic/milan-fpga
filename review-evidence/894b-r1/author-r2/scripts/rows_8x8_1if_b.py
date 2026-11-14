"""8x8/1if's rows by every source and its long-window load, DERIVED, not measured: reported, the gap owed to #872 (#894's
ruling issuecomment-6867393730, item (b)). Round 1's rows_8x8_1if.py, at phase B's inputs (#894's round 2 ruling
issuecomment-6871343905):
- the constants are the tree's at 8x8/1if's shape (shape_costs.of_point): the 1,475 us slice and its builds, every other
  constant one interface's (the headers at MBX_N_IF 1: 16 owed-notice slots, AECP_QUEUED_MS 130);
- the counts are load_grade.POINTS['8x8/1if']'s (8 sinks, 16 registrations, 20 descriptors with counters), and the
  notices a reset leaves 40, AECP_NOTICES_MOST at the shape (shape_costs.notices_most), where rows_grade reads 12;
- the polls are the shape's own (poll_grade.STATED_US at (1, 9, 9), phase B's measurement plus 5 %);
- the records' and events' costs are 8x8/2if's stated ones (load_grade's NEAREST, rows_grade's LINK), the nearest
  measured shape; rows_grade.py names no 8x8/1if point and is not this lane's to change, so they are set here, in memory;
- the largest legal command's record and notice are phase B's 8x8/1if measurement (aecp-largest-notice, the
  answering-ports arm): 154,850 and 30,097 CPU cycles, 1,630 and 320 us.
usage: python3 -I rows_8x8_1if.py ROOT"""
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_budget'))
import load_grade, poll_grade, rows_grade, rows_tiers as rt, shape_costs  # noqa: E402,E401

P, TWO = '8x8/1if', '8x8/2if'
rows_grade.ROW_COSTS[P] = dict(rows_grade.ROW_COSTS[TWO])
rt.DATAPATH_US[P] = dict(rt.DATAPATH_US[TWO])
rt.LONG_NOTICE_US[P], rt.LONG_RECORD_US[P] = 320, 1630
polls = poll_grade.stated_us(shape_costs.of_point(P, root))
i = rt.point_inputs(root, P)
notices = shape_costs.notices_most(root / 'configs' / 'endstation_ax7101_8x8.yaml', 1, root)
i = i._replace(c={**i.c, **{f'item.{k}': polls[k] for k in ('withdraw', 'rebuild', 'aecp')}},
               s={**i.s, 'notices': notices}, h={**i.h, 'AECP_NOTICES_MOST': notices})
bounds = rt.bounds_at(i)
s = shape_costs.of_point(P, root)
print(f'# {P}, derived, at {shape_costs.at(s, root)} (shape {tuple(s)}): slice {i.slice_us} us, pace {i.pace_ms} ms, '
      f'owed slots {i.owed}, build {i.c["build"]} us, build_one {i.c["build_one"]} us, item.mrpdu {i.c["item.mrpdu"]} us, '
      f'record.aecp {i.c["record.aecp"]} us, record.aecp.long {i.c["record.aecp.long"]} us, item.aecp.long '
      f'{i.c["item.aecp.long"]} us, notices {i.s["notices"]}')
print('| Row | W, ms | Bound, ms | Over by, ms | Largest terms, ms |')
print('|---|---:|---:|---:|---|')
for row, (w, terms) in rt.rows(root, P, rt.BUILT, i).items():
    top = ', '.join(f'{k} {v:.2f}' for k, v in sorted(terms.items(), key=lambda t: -t[1])[:3])
    shown = 'none under 2,000' if w is None else f'{w:.2f}'
    over = '' if w is None else f'{w - bounds[row]:+.2f}'
    print(f'| {row} | {shown} | {bounds[row]} | {over} | {top} |')
for name, column in (('at the pin', load_grade.STATED_US), ('with tsn-c-stack#32', load_grade.STATED_US_DONOR)):
    terms = load_grade.load(root, P, column)
    print(f'\nLong-window load {name}: {sum(terms.values()):.3f} (the ruling holds 0.75); largest terms ' +
          ', '.join(f'{k} {v:.3f}' for k, v in sorted(terms.items(), key=lambda t: -t[1])[:5]))
long = {**load_grade.STATED_US, TWO: {**load_grade.STATED_US[TWO], 'record.aecp': 1630, 'item.aecp.notice': 320}}
print(f'With every AECP command the largest legal one: {sum(load_grade.load(root, P, long).values()):.3f}')
