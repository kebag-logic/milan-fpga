#!/usr/bin/env python3
"""The event ring at a leg's composed mark: every event record posted from 40 ms before the mark to 10 ms after it
(its slot and type, off the EVW lines), the GM pad changes, and each pass that spans the mark.

usage: python3 -I ring_at_mark.py LOG [MARK]   (MARK defaults to composed)
"""
import sys

log, want = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else 'composed')
TYPES = {3: 'GM', 4: 'TICK'}
evt, recs, gms, passes, mark = {}, [], [], [], None
with open(log) as f:
    for line in f:
        p = line.split()
        if not p:
            continue
        if p[0] == 'MARK' and p[2] == want:
            mark = int(p[1])
        elif p[0] == 'EVW':
            c, a, d = int(p[1]), int(p[2]), int(p[3], 16)
            evt[a] = (c, d)
            if a % 4 == 3 and all(x in evt for x in range(a - 3, a + 1)):
                w = [evt.pop(x)[1] for x in range(a - 3, a + 1)]
                recs.append((c, a // 4 % 16, w[0] & 0xFF))
        elif p[0] == 'GM':
            gms.append((int(p[1]), int(p[2])))
        elif p[0] == 'PASS':
            idx, start, _, cyc = (int(v) for v in p[1:5])
            passes.append((idx, start, cyc))
print(f'mark {want} at system cycle {mark}; offsets below are system cycles from it (100 per microsecond)')
for c, slot, kind in recs:
    if mark - 4_000_000 <= c <= mark + 1_000_000:
        print(f'record {c - mark:+11d} slot {slot:2d} {TYPES.get(kind, hex(kind))}')
inside = [c for c, *_ in recs if mark <= c <= mark + 1_000_000 and _[1] == 3]
print(f'GM pad changes: {len(gms)}, from {gms[0][0] - mark:+d} to {gms[-1][0] - mark:+d}; GM records posted within '
      f'10 ms of the mark: {sum(1 for c, s, k in recs if k == 3 and mark <= c <= mark + 1_000_000)}')
for idx, start, cyc in passes:
    end = start + 2 * cyc            # the CPU runs at half the system clock
    if start <= mark <= end:
        print(f'pass {idx} spans the mark: starts {start - mark:+d}, {cyc:,} CPU cycles ({cyc / 50_000:.1f} ms), '
              f'ends {end - mark:+d}')
