#!/usr/bin/env python3
"""acmp_item_split.py LOG...: each ACMP poll span (acmp_mbx:on_poll) less the record handlers nested in it
(acmp_mbx:on_frame, the redelivered records), from the budget harness's SPAN lines. Prints the heaviest poll whole,
the heaviest poll less its nested handlers, and the count of polls that redelivered a record."""
import sys
from bisect import bisect_left
for path in sys.argv[1:]:
    polls, frames = [], []
    for line in open(path, errors='replace'):
        if not line.startswith('SPAN '):
            continue
        f = line.split()
        if len(f) < 6:
            continue
        start, cycles, label = int(f[2]), int(f[3]), f[5]
        if label == 'acmp_mbx:on_poll':
            polls.append((start, cycles))
        elif label == 'acmp_mbx:on_frame':
            frames.append((start, cycles))
    frames.sort()
    starts = [s for s, _ in frames]
    whole = net = 0
    nested_polls = 0
    for s, c in polls:
        i = bisect_left(starts, s)
        inner = 0
        while i < len(frames) and frames[i][0] < s + c:
            inner += frames[i][1]
            i += 1
        nested_polls += inner > 0
        whole = max(whole, c)
        net = max(net, c - inner)
    print(f'{path}: {len(polls)} polls, {nested_polls} with nested record handlers; heaviest {whole:,} CPU cycles, '
          f'heaviest less its nested handlers {net:,}')
