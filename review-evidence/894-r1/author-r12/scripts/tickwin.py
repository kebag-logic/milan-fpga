"""What the passes after one step's command cost, in one harness log: each event the loop took in the window, by type,
its CPU cycles measured as round 20's eventcost.py measures event.TICK (from the take that returned it to the next
take, or for a pass's last to its first service_rx, less its dispatch_ticks spans), and the AECP poll's and the AECP
bridge's delivery spans (aecp_mbx:poll, ctrl_app_aecp:deliver) and the record (aecp_mbx:frame), each beside the
stated cost the rule gives it (the cycles at 100 MHz plus 5 %, rounded up to 5 us).

The window runs from the MARK naming the step to the next MARK (the scenario's next step).

usage: python3 -I tickwin.py LOG STEP_MARK"""
import bisect
import collections
import math
import sys

TYPES = {1: 'TIMER', 2: 'LINK', 3: 'GM', 4: 'TICK', 5: 'COUNTERS_CHANGED', 6: 'AVB_INFO_CHANGED', 7: 'AS_PATH_CHANGED',
         8: 'AMAP_LIVE_WRITE'}
rule = lambda c: int(math.ceil(c * 1.05 / 100 / 5 - 1e-9) * 5)  # noqa: E731

path, step = sys.argv[1], sys.argv[2]
written, passes, takes, rx, ticks, spans, marks = [], [], [], [], [], [], []
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
    elif f[0] == 'SPAN' and len(f) > 5:
        if f[5] == 'ctrl_loop:dispatch_ticks':
            ticks.append((int(f[2]), int(f[3])))
        if f[5] in ('aecp_mbx:poll', 'ctrl_app_aecp:deliver', 'aecp_mbx:frame'):
            spans.append((int(f[2]), int(f[3]), f[5]))
    elif f[0] == 'MARK':
        marks.append((int(f[1]), f[2]))
takes.sort(); rx.sort(); ticks.sort()
k = next(n for n, (_, m) in enumerate(marks) if m == step)
lo_bus, hi_bus = marks[k][0], (marks[k + 1][0] if k + 1 < len(marks) else 1 << 62)
lo, hi = lo_bus - 64, hi_bus - 64  # CPU cycles trail the bus by the reset offset (SPAN lines carry both)
tick_at = [s for s, _ in ticks]
events, taken = [], 0
for start, cycles in passes:
    end = start + cycles
    first_rx = rx[bisect.bisect_left(rx, start):bisect.bisect_left(rx, end)]
    if not first_rx:
        continue
    stop = first_rx[0]
    mine = takes[bisect.bisect_left(takes, start):bisect.bisect_left(takes, stop)]
    got = len(mine) if len(mine) == 8 else len(mine) - 1
    for n in range(max(got, 0)):
        a, b = mine[n], (mine[n + 1] if n + 1 < len(mine) else stop)
        t0, t1 = bisect.bisect_left(tick_at, a), bisect.bisect_left(tick_at, b)
        spent = b - a - sum(d for _, d in ticks[t0:t1])
        if taken < len(written):
            kind, slot = written[taken]
            if lo <= a < hi:
                events.append((a, TYPES.get(kind, str(kind)) + (f'#{slot}' if kind == 1 else ''), spent))
        taken += 1
print(f'# {path.rsplit("/", 1)[-1]}: step {step}, bus cycles {lo_bus} to {hi_bus}')
most = collections.defaultdict(lambda: (0, 0))
for a, kind, spent in events:
    if spent > most[kind][0]:
        most[kind] = (spent, a)
for kind, (spent, a) in sorted(most.items()):
    n = sum(1 for _, k2, _ in events if k2 == kind)
    print(f'event {kind:16s} {n:4d} taken, most {spent:6,} CPU cycles at {a}, {rule(spent)} us by the rule')
for start, cycles, name in sorted(spans):
    if lo <= start < hi and (name == 'aecp_mbx:frame' or cycles > 3000):
        print(f'span  {name:22s} at {start}: {cycles:6,} CPU cycles, {rule(cycles)} us by the rule')
