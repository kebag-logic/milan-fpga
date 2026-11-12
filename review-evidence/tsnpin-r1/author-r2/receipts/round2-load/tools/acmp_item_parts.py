#!/usr/bin/env python3
"""acmp_item_parts.py LOG: each ACMP poll span (acmp_mbx:on_poll) cut into the core's poll (acmp_poll, the owed frame
it sends) and the commands handled inside it (acmp_rx, the kept record's re-offer and each redelivered record's), from
the budget harness's SPAN lines of a build that traces both. Prints the heaviest poll whole and its parts, and the
heaviest poll less the command handling nested in it."""
import sys
from bisect import bisect_left
polls, inner = [], {'acmp_poll': [], 'acmp_rx': [], 'acmp_mbx:on_frame': []}
for line in open(sys.argv[1], errors='replace'):
    if line.startswith('SPAN '):
        f = line.split()
        if len(f) >= 6:
            start, cycles, label = int(f[2]), int(f[3]), f[5]
            if label == 'acmp_mbx:on_poll':
                polls.append((start, cycles))
            elif label in inner:
                inner[label].append((start, cycles))
for v in inner.values():
    v.sort()
def nested(label, s, c):
    rows = inner[label]; i = bisect_left(rows, (s, -1)); out = []
    while i < len(rows) and rows[i][0] < s + c:
        out.append(rows[i][1]); i += 1
    return out
heavy = max(polls, key=lambda p: p[1])
parts = {k: nested(k, *heavy) for k in inner}
print(f'{sys.argv[1]}: {len(polls)} polls; heaviest {heavy[1]:,} CPU cycles: acmp_poll {sum(parts["acmp_poll"]):,}, '
      f'acmp_rx {len(parts["acmp_rx"])} call(s) {sum(parts["acmp_rx"]):,} (on_frame {len(parts["acmp_mbx:on_frame"])}), '
      f'the rest {heavy[1] - sum(parts["acmp_poll"]) - sum(parts["acmp_rx"]):,}')
net = max(c - sum(nested('acmp_rx', s, c)) for s, c in polls)
own = max((sum(nested('acmp_poll', s, c)) for s, c in polls), default=0)
print(f'heaviest poll less the commands it handled: {net:,} CPU cycles; heaviest core poll inside one: {own:,}')
