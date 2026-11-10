#!/usr/bin/env python3
"""Each event an instrumented budget-harness log's loop took, by type, and the CPU cycles its sinks spent on it (#665,
round 20 item 4).

usage: python3 -I eventcost.py RESULTS_DIR...

The fabric writes an event as four ring words (EVW lines); the first carries its type in its low half-word and its
timer slot, for a TIMER, in bits 16 to 23 of the second (mbx_contract.h, MBX_EV_TIMER_W1_SLOT_LSB). The loop takes events in ring order (mbx_event_take, a CALL
line). An event's cost is from the take that returned it to the next take, or, for a pass's last, to its first
service_rx. A take that found the ring empty returns nothing: in a pass that took fewer than
CTRL_LOOP_EVENTS_PER_PASS events the last take is that one.
"""
import bisect
import collections
import json
import sys
from pathlib import Path

TYPES = {1: 'TIMER', 2: 'LINK', 3: 'GM', 4: 'TICK', 5: 'COUNTERS_CHANGED', 6: 'AVB_INFO_CHANGED', 7: 'AS_PATH_CHANGED',
         8: 'AMAP_LIVE_WRITE'}


def events_of(path):
    """(the ring's events in write order as (type, slot)), (passes), (take cpu), (service_rx cpu), (tick spans)."""
    written, passes, takes, rx, ticks = [], [], [], [], []
    words = []
    for line in open(path, errors='replace'):
        f = line.split()
        if not f:
            continue
        if f[0] == 'EVW':
            words.append(int(f[3], 16))
            if len(words) == 4:
                written.append((words[0] & 0xffff, (words[1] >> 16) & 0xff))
                words = []
        elif f[0] == 'PASS':
            passes.append((int(f[3]), int(f[4])))
        elif f[0] == 'CALL' and f[3] == 'mbx_event_take':
            takes.append(int(f[2]))
        elif f[0] == 'CALL' and f[3] == 'ctrl_loop:service_rx':
            rx.append(int(f[2]))
        elif f[0] == 'SPAN' and f[5] == 'ctrl_loop:dispatch_ticks':
            ticks.append((int(f[2]), int(f[3])))
    return written, passes, sorted(takes), sorted(rx), sorted(ticks)


def costs(path):
    written, passes, takes, rx, ticks = events_of(path)
    tick_at = [s for s, _ in ticks]
    out, taken = [], 0
    for start, cycles in passes:
        end = start + cycles
        first_rx = rx[bisect.bisect_left(rx, start):bisect.bisect_left(rx, end)]
        if not first_rx:
            continue
        stop = first_rx[0]
        mine = takes[bisect.bisect_left(takes, start):bisect.bisect_left(takes, stop)]
        got = len(mine) if len(mine) == 8 else len(mine) - 1
        for k in range(max(got, 0)):
            a, b = mine[k], (mine[k + 1] if k + 1 < len(mine) else stop)
            lo, hi = bisect.bisect_left(tick_at, a), bisect.bisect_left(tick_at, b)
            spent = b - a - sum(d for _, d in ticks[lo:hi])
            if taken < len(written):
                kind, slot = written[taken]
                out.append((TYPES.get(kind, str(kind)) + (f'#{slot}' if kind == 1 else ''), spent))
            taken += 1
    return out


def main():
    worst, count = collections.defaultdict(int), collections.Counter()
    for d in sys.argv[1:]:
        for path in sorted(Path(d).glob('*.log')):
            if 'RESULT' not in path.read_text(errors='replace')[-4000:]:
                continue
            for kind, spent in costs(path):
                worst[kind] = max(worst[kind], spent)
                count[kind] += 1
    print(json.dumps({k: {'most_cycles': worst[k], 'taken': count[k]} for k in sorted(worst)}, indent=1))


if __name__ == '__main__':
    main()
