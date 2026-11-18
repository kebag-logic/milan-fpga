#!/usr/bin/env python3
"""unitwin.py SLICE_US UNIT_US NEW_UNIT_US LOG...: whether a measured run would take the same SRP records with THE
DRAIN's unit at NEW_UNIT_US (ctrl_loop.c: tier 2 starts an SRP record only while the clock is before the pass's start
plus CTRL_LOOP_SLICE_US less CTRL_LOOP_SRP_UNIT_US). The pass's start is its clock read as ctrl_loop_service begins,
after the previous pass's polls ended, so each record's start less that end bounds what of the slice it started at.
A raised unit changes a decision only for a record started past SLICE - NEW_UNIT into the slice; a record deferred at
the old unit is deferred at the new. Prints, per log, the records, the latest start into the slice (bound) and any past
the new threshold (with a 2 us margin for the clock's microsecond). Scratch only; bus cycles at 100 MHz."""
import sys
from bisect import bisect_right

slice_us, unit, new = (int(a) for a in sys.argv[1:4])
limit = (slice_us - new - 2) * 100
for path in sys.argv[4:]:
    poll_ends, recs, takes = [], [], []
    with open(path, errors='replace') as f:
        for line in f:
            if line.startswith('CALL ') and line.rstrip().endswith(' mbx_event_take'):
                takes.append(int(line.split()[1]))
                continue
            if not line.startswith('SPAN '):
                continue
            p = line.split()
            if len(p) < 6:
                continue
            start, cycles, name = int(p[1]), int(p[3]), p[-1]
            if name == 'srp_mbx:receive':
                recs.append(start)
            elif name.endswith(':on_poll') or name.endswith(':poll') or name.endswith(':deliver'):
                poll_ends.append(start + cycles)
    poll_ends.sort()
    # a pass's start: its first event take after the previous pass's polls (service_events, just after its clock read)
    starts, j = [], 0
    for e in sorted(takes):
        k = bisect_right(poll_ends, e)
        if k != j or not starts:
            starts.append(e)
            j = k
    worst, past = 0, []
    for t in recs:
        k = bisect_right(starts, t) - 1
        if k < 0:
            continue
        into = t - starts[k] + 500  # 5 us for the clock read before the take

        worst = max(worst, into)
        if into > limit:
            past.append((t, into))
    print(f'{path}: {len(recs)} SRP records; the latest at most {worst / 100:.1f} us into its slice; '
          f'{len(past)} past {slice_us - new - 2} us (unit {unit} -> {new})' + (f': {past[:5]}' if past else ''))
