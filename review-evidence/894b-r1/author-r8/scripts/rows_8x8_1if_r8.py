"""8x8/1if's rows by every source and its long-window load, DERIVED, not measured: reported, owed to #872 (#894's
shape ruling, item (b); FR_NFR 3.4.1). Round 3's rows_8x8_1if_r3.py on the tree that merges #902's 234bc149 (round 5):
- the constants are the tree's at 8x8/1if's shape (shape_costs.of_point): its slice and builds, its SRP drain limit,
  THE RETRY's costs, every other constant one interface's (16 owed-notice slots, AECP_QUEUED_MS 130, the pace);
- the counts are load_grade.POINTS['8x8/1if']'s, and the notices a reset leaves 40 (shape_costs.notices_most);
- the polls are the shape's own (poll_grade.STATED_US at (1, 9, 9));
- the records' and events' costs are 8x8/2if's stated ones (load_grade's NEAREST, rows_grade's LINK), set here in
  memory, since rows_grade names no 8x8/1if point;
- the largest legal command's record is the tree's at 8x8/1if (rows_tiers.LONG_RECORD_US) and its notice the shape's
  aecp_long (poll_grade); the paced class the tree's at 8x8/1if (edit_rows.EDIT_RECORD_US, keyed on the shape).
usage: python3 -I rows_8x8_1if_r5.py ROOT"""
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_budget'))
import load_grade, poll_grade, rows_grade, rows_tiers as rt, shape_costs  # noqa: E402,E401

P, TWO = '8x8/1if', '8x8/2if'
rows_grade.ROW_COSTS[P] = dict(rows_grade.ROW_COSTS[TWO])
rt.DATAPATH_US[P] = dict(rt.DATAPATH_US[TWO])
polls = poll_grade.stated_us(shape_costs.of_point(P, root))
rt.LONG_NOTICE_US[P] = polls[poll_grade.LONG]
i = rt.point_inputs(root, P)
notices = shape_costs.notices_most(root / 'configs' / 'endstation_ax7101_8x8.yaml', 1, root)
i = i._replace(c={**i.c, **{f'item.{k}': polls[k] for k in ('withdraw', 'rebuild', 'aecp')}},
               s={**i.s, 'notices': notices}, h={**i.h, 'AECP_NOTICES_MOST': notices})
bounds = rt.bounds_at(i)
s = shape_costs.of_point(P, root)
import edit_rows  # noqa: E402
print(f'# {P}, derived, paced class {edit_rows.EDIT_RECORD_US[edit_rows.point_of(i)]} us ({edit_rows.point_of(i)}), at {shape_costs.at(s, root)} (shape {tuple(s)}): slice {i.slice_us} us, pace {i.pace_ms} ms, '
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
long = {**load_grade.STATED_US, TWO: {**load_grade.STATED_US[TWO], 'record.aecp': rt.LONG_RECORD_US[P],
                                                   'item.aecp.notice': rt.LONG_NOTICE_US[P]}}
print(f'With every AECP command the largest legal one: {sum(load_grade.load(root, P, long).values()):.3f}')
