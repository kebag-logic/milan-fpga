#!/usr/bin/env python3
"""The 32x32/2if costs measured by S2b round 21's parts.py on this lane's instrumented leg of the round 4 image, beside
S2b round 22's projection of them (arrivals2.py's project(): the line through its 1x1/1if and 8x8/2if stated costs, in
streams 2 and 16, at 64; from its own head's costs, COSTS-FINAL.json), and the error (projected less measured). Round 2's
measured figure, on round 2's image, is shown beside it.

usage: python3 -I project_vs_measured_r4.py PARTS-32x32.json COSTS-FINAL.json ROUND2-PARTS-32x32.json IMAGE_SHA256 OUT.md

Every figure is a stated cost in S2b's unit: the most measured plus 5 %, rounded up to 5 us at 100 CPU cycles a
microsecond (parts.py's stated()). A cost S2b states that this base cannot measure the same way is listed with the
reason, and no error.
"""
import json
import sys
from pathlib import Path

parts, costs, r2 = (json.loads(Path(a).read_text()) for a in sys.argv[1:4])
image, out = sys.argv[4], Path(sys.argv[5])


def project(c1: float, c8: float, n: int = 64) -> float:
    """arrivals2.py's project(), restated: the line through (2, c1) and (16, c8), at n streams."""
    return c8 + (n - 16) * (c8 - c1) / (16 - 2)


SAME = {'record.srp': 'record.srp', 'record.aecp': 'record.aecp', 'record.acmp': 'record.acmp',
        'record.adp': 'record.adp', 'record.maap': 'record.maap', 'rebuild': 'rebuild',
        'centisecond': 'centisecond_consumers'}
WHY = {'events': "parts.py cuts a pass's events at ctrl_loop's service_rx, which this base's image inlines",
       'events_none': "as events",
       'polls_least': "as events: parts.py records the least polls of a pass that took a record, read at service_rx",
       'base': "graded by S2b round 22's poll_grade.py on its own head's loop, which this base does not carry"}
for k in ('event.ADP', 'event.ACMP', 'event.MAAP', 'event.AECP', 'event.TICK', 'event.GM', 'event.LINK'):
    WHY[k] = "S2b's eventcost.py figure, from its own head's event records; not run here"
for k in ('item.withdraw', 'item.rebuild', 'item.walk', 'item.reclaim', 'item.retained', 'item.mrpdu',
          'item.acmp', 'item.aecp'):
    WHY[k] = "as base"
m32, old = parts['parts'], r2['parts']
rows = [f'The 32x32/2if image: `ctrl_app.elf` SHA-256 `{image}`.', '',
        '| Cost | S2b 1x1/1if, us | S2b 8x8/2if, us | S2b projected 32x32/2if, us | measured 32x32/2if, us '
        '(most cycles, instances) | error of S2b\'s, us | round 2 measured, us |',
        '|---|---:|---:|---:|---:|---:|---:|']
for key in costs['8x8/2if']:
    c1, c8 = costs['1x1/1if'][key], costs['8x8/2if'][key]
    proj = project(c1, c8)
    name = SAME.get(key)
    if name and name in m32:
        meas = m32[name]
        was = old.get(name, {}).get('stated_us', '')
        rows.append(f'| `{key}` | {c1} | {c8} | {proj:.1f} | {meas["stated_us"]} ({meas["most_cycles"]:,}, '
                    f'{meas["instances"]:,}) | {proj - meas["stated_us"]:+.1f} | {was} |')
    else:
        rows.append(f'| `{key}` | {c1} | {c8} | {proj:.1f} | not measured: {WHY.get(key, "no same figure at this base")} | | |')
out.write_text('\n'.join(rows) + '\n')
print('\n'.join(rows))
