#!/usr/bin/env python3
"""Each event's cost by type from budget-harness logs: from the CALL of mbx_event_take that took its record to the
next cut (the next mbx_event_take or the pass's first ctrl_loop:service_rx), in CPU cycles: its take and every sink's
work, as the load gate's event.* costs are cut (poll_items.PART_CALLS). Records are matched to takes in ring order:
a take takes the oldest record posted (its last EVW word) before it, or none.
usage: eventcost.py TREE LOG... -> JSON per type: count, max cycles, max us, stated us (max x 1.05, up to 5 us)."""
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tree / 'tb/verilator/ctrl_service_budget'))
import grade  # noqa: E402

TAKE, RX = 'mbx_event_take', 'ctrl_loop:service_rx'
NAMES = {1: 'TIMER', 2: 'LINK', 3: 'GM', 4: 'TICK', 5: 'FACE', 6: 'AVB_INFO_CHANGED', 7: 'AS_PATH_CHANGED',
         8: 'AMAP_LIVE_WRITE'}
cost = defaultdict(list)
for path in sys.argv[2:]:
    text = Path(path).read_text(errors='replace')
    text = text[:text.rfind('\n') + 1]
    log = grade.parse(text, 100_000_000, 100_000_000)
    calls = sorted((int(r[1]), int(r[0]), r[2]) for kind, *r in log.traced if kind == 'CALL' and r[2] in (TAKE, RX))
    records = sorted((cycle, words[0] & 0xff) for cycle, words in log.records)
    pending, k = [], 0
    for i, (cpu, sys_, name) in enumerate(calls):
        if name != TAKE:
            continue
        while k < len(records) and records[k][0] < sys_:
            pending.append(records[k][1])
            k += 1
        if not pending or i + 1 == len(calls):
            continue
        kind = pending.pop(0)
        cost[NAMES.get(kind, str(kind))].append((calls[i + 1][0] - cpu, Path(path).name, sys_))
out = {}
for kind, rows in sorted(cost.items()):
    top = max(rows)
    us = top[0] / 100
    out[kind] = dict(count=len(rows), max_cycles=top[0], max_us=round(us, 2), at=f'{top[1]}@{top[2]}',
                     stated_us=5 * math.ceil(us * 1.05 / 5))
print(json.dumps(out, indent=1))
