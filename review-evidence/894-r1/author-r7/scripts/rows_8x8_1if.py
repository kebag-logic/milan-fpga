"""(round 7: ACMP's declined offers, #908, at 8x8/2if's stated cost like the rest.)
8x8/1if's rows by every source and its long-window load, DERIVED, not measured (#894's slice ruling of 2026-11-13,
item 2: modelled and reported, the gap owed to #872). The tier model holds no 8x8/1if point and rows_grade.py is not
this lane's to change, so the point is added in memory only:
- the constants are one interface's (the headers at MBX_N_IF 1: the 900 us slice, 16 owed-notice slots);
- the counts are 8x8's at one interface (8 sinks, 16 registrations, 18 descriptors with counters: 16 streams, the
  interface and its clock domain);
- every cost is 8x8/2if's stated one (load_grade.STATED_US, poll_grade's two-interface items, ctrl_loop.h's two-interface
  builds and step, rows_grade's LINK), the nearest measured shape;
- but the largest legal command's record and notice are round 6's 8x8/1if measurement (the aecp-largest-notice group
  on the harness's 8x8-1if point at the merge of #810's 084cf7a8, measured_inputs.py): 151,246 and 29,860 CPU
  cycles, so 1,590 and 315 us (175,914 and 29,984 before the merge); THE PACE is the tree's, AECP_PACE_MS 6 ms, R4L's bound 240 ms under it; the MRPDU bound is the tree's, 240 ms less CTRL_LOOP_JOIN_CS (19 cs), 50 ms.
usage: python3 -I rows_8x8_1if.py ROOT"""
import sys
from pathlib import Path

root = Path(sys.argv[1])
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_budget'))
import load_grade, poll_grade, rows_grade, rows_tiers as rt  # noqa: E402,E401

P, TWO = '8x8/1if', '8x8/2if'
load_grade.POINTS[P] = dict(n_if=1, sinks_per_if=8, registrations=16, counter_descriptors=18)
polls = poll_grade.stated_us(2)
table = dict(load_grade.STATED_US[TWO])
table.update({'base': polls['base'], **{f'item.{k}': polls[k] for k in ('reclaim', 'retained', 'mrpdu', 'acmp', 'walk', 'acmp_declined')},
              'build': 1995, 'build_one': 1215, 'step': 1030})
load_grade.STATED_US[P] = table
rows_grade.ROW_COSTS[P] = dict(rows_grade.ROW_COSTS[TWO])
rt.DATAPATH_US[P] = dict(rt.DATAPATH_US[TWO])
rt.LONG_NOTICE_US[P], rt.LONG_RECORD_US[P] = 315, 1590
i = rt.point_inputs(root, P)
i = i._replace(c={**i.c, **{f'item.{k}': polls[k] for k in ('withdraw', 'rebuild', 'aecp')}})
bounds = rt.bounds_at(i)
print(f'# {P}, derived: slice {i.slice_us} us, pace {i.pace_ms} ms, owed slots {i.owed}, record.aecp {i.c["record.aecp"]} us, '
      f'record.aecp.long {i.c["record.aecp.long"]} us, item.aecp.long {i.c["item.aecp.long"]} us')
print('| Row | W, ms | Bound, ms | Over by, ms | Largest terms, ms |')
print('|---|---:|---:|---:|---|')
for row, (w, terms) in rt.rows(root, P, rt.BUILT, i).items():
    top = ', '.join(f'{k} {v:.2f}' for k, v in sorted(terms.items(), key=lambda t: -t[1])[:3])
    shown = 'none under 2,000' if w is None else f'{w:.2f}'
    over = '' if w is None else f'{w - bounds[row]:+.2f}'
    print(f'| {row} | {shown} | {bounds[row]} | {over} | {top} |')
plain = i._replace(c={**i.c, 'record.aecp.long': i.c['record.aecp']})
print('\nWith the largest legal command charged as an ordinary record (what its notice alone gives):')
print(', '.join(f'{row} {"none" if w is None else f"{w:.2f}"}' for row, (w, _) in
                rt.rows(root, P, rt.BUILT, plain).items() if row in rt.LONG_ROWS))
terms = load_grade.load(root, P, load_grade.STATED_US)
print(f'\nLong-window load at the stated costs: {sum(terms.values()):.3f} (the ruling holds 0.75); largest terms ' +
      ', '.join(f'{k} {v:.3f}' for k, v in sorted(terms.items(), key=lambda t: -t[1])[:5]))
long = dict(table, **{'record.aecp': 1590, 'item.aecp.notice': 315})
lt = load_grade.load(root, P, {**load_grade.STATED_US, P: long})
print(f'With every AECP command the largest legal one: {sum(lt.values()):.3f}')
