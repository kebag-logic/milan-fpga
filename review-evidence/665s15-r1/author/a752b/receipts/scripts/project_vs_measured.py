#!/usr/bin/env python3
"""The 32x32/2if costs measured by round 21's parts.py on this lane's instrumented leg, beside two projections of
them, and the error of each (projected less measured):

  - S2b round 22's (arrivals2.py's project(): the line through 1x1/1if's and 8x8/2if's stated costs, in streams 2
    and 16, at 64), from S2b's own head's costs (COSTS-FINAL.json);
  - the same line through this base's own 1x1/1if and 8x8/2if stated costs, measured by parts.py on this lane's
    instrumented legs of the same firmware (PARTS-1x1.json, PARTS-8x8.json).

usage: python3 -I project_vs_measured.py PARTS-32x32.json COSTS-FINAL.json PARTS-1x1.json PARTS-8x8.json OUT.md

Every column is a stated cost in S2b's unit: the most measured plus 5 %, rounded up to 5 us at 100 CPU cycles a
microsecond (parts.py's stated()). A cost S2b states that this base cannot measure the same way is listed with the
reason, and no error.
"""
import json
import sys
from pathlib import Path

parts, costs, p1, p8 = (json.loads(Path(a).read_text()) for a in sys.argv[1:5])
out = Path(sys.argv[5])


def project(c1: float, c8: float, n: int = 64) -> float:
    """arrivals2.py's project(), restated: the line through (2, c1) and (16, c8), at n streams."""
    return c8 + (n - 16) * (c8 - c1) / (16 - 2)


#: Each S2b cost key, and the parts.py figure that is the same measurement at this base, or why there is none.
SAME = {
    'record.srp': 'record.srp', 'record.aecp': 'record.aecp', 'record.acmp': 'record.acmp',
    'record.adp': 'record.adp', 'record.maap': 'record.maap', 'rebuild': 'rebuild',
    'centisecond': 'centisecond_consumers',
}
WHY = {
    'events': "parts.py cuts a pass's events at ctrl_loop's service_rx, which this base's image inlines",
    'events_none': "as events",
    'polls_least': "as events: parts.py records the least polls of a pass that took a record, read at service_rx",
    'event.ADP': "S2b's eventcost.py figure, from its own head's event records; not run here",
    'event.ACMP': "as event.ADP", 'event.MAAP': "as event.ADP", 'event.AECP': "as event.ADP",
    'event.TICK': "as event.ADP", 'event.GM': "as event.ADP", 'event.LINK': "as event.ADP",
    'base': "graded by S2b round 22's poll_grade.py on its own head's loop, which this base does not carry",
}
for k in ('item.withdraw', 'item.rebuild', 'item.walk', 'item.reclaim', 'item.retained', 'item.mrpdu',
          'item.acmp', 'item.aecp'):
    WHY[k] = "as base"
m32, m1, m8 = parts['parts'], p1['parts'], p8['parts']
rows = ['| Cost | S2b 1x1/1if, us | S2b 8x8/2if, us | S2b projected 32x32/2if, us | this base 1x1/1if, us '
        '| this base 8x8/2if, us | projected from this base, us | measured 32x32/2if, us (most cycles, instances) '
        '| error of S2b\'s, us | error of this base\'s, us |',
        '|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
for key in costs['8x8/2if']:
    c1, c8 = costs['1x1/1if'][key], costs['8x8/2if'][key]
    proj = project(c1, c8)
    name = SAME.get(key)
    if name and name in m32 and name in m1 and name in m8:
        meas, b1, b8 = m32[name], m1[name]['stated_us'], m8[name]['stated_us']
        own = project(b1, b8)
        rows.append(f'| `{key}` | {c1} | {c8} | {proj:.1f} | {b1} | {b8} | {own:.1f} | {meas["stated_us"]} '
                    f'({meas["most_cycles"]:,}, {meas["instances"]:,}) | {proj - meas["stated_us"]:+.1f} '
                    f'| {own - meas["stated_us"]:+.1f} |')
    else:
        rows.append(f'| `{key}` | {c1} | {c8} | {proj:.1f} | | | | not measured: '
                    f'{WHY.get(key, "no same figure at this base")} | | |')
out.write_text('\n'.join(rows) + '\n')
print('\n'.join(rows))
