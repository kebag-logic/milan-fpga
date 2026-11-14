#!/usr/bin/env python3
"""event_spans.py KIND LOG: the dearest event of KIND in LOG, by eventcost.py's cost (its window less its ticks), and the SPAN and CALL
lines inside its window, each name with its count and total cycles (SPAN durations; CALL counted)."""
import bisect, collections, sys
sys.path.insert(0, '$MANAGEMENT/2026-09-23/895-a775/scripts/costs')
import eventcost  # noqa: E402
kind, path = sys.argv[1], sys.argv[2]
written, passes, takes, rx, ticks = eventcost.events_of(path)
best, taken = None, 0
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
        if taken < len(written):
            t, slot = written[taken]
            name = eventcost.TYPES.get(t, str(t)) + (f'#{slot}' if t == 1 else '')
            tick_at = [x for x, _ in ticks]
            lo, hi = bisect.bisect_left(tick_at, a), bisect.bisect_left(tick_at, b)
            spent = b - a - sum(d for _, d in ticks[lo:hi])
            if name == kind and (best is None or spent > best[2]):
                best = (a, b, spent)
        taken += 1
a, b, spent = best
spans, calls = collections.defaultdict(lambda: [0, 0]), collections.Counter()
for line in open(path, errors='replace'):
    f = line.split()
    if len(f) > 3 and f[0] in ('SPAN', 'CALL'):
        at = int(f[2])
        if a <= at < b:
            if f[0] == 'SPAN':
                spans[f[5]][0] += 1; spans[f[5]][1] += int(f[3])
            else:
                calls[f[3]] += 1
print(f'{kind} dearest event {a}..{b}: {spent} cycles past its ticks ({b - a} with them)')
for n, (c, d) in sorted(spans.items(), key=lambda x: -x[1][1]):
    print(f'  SPAN {n:40} x{c:4} {d:8}')
for n, c in calls.most_common():
    print(f'  CALL {n:40} x{c:4}')
