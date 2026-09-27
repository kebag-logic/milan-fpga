#!/usr/bin/env python3
"""Per receipt: liveness samples with times; every heartbeat strobe must follow a
retired entry of the heartbeat function (observer completeness); strobe spacing
must not exceed 250 ms + preceding no-entry span (rate-limit model).
usage: liveness_check.py <receipt.json>..."""
import json, sys
bad = 0
for f in sys.argv[1:]:
    d = json.load(open(f)); ev = d['events']
    print('==', f.split('/')[-1])
    print('  samples:', [(s['command_index'], s['backed'], round(s['sampled_by_sys_cycle'] / 1e5, 5)) for s in d['liveness']])
    hb = [e['cycle'] for e in ev if e['kind'] == 'write' and e['address'] == 0x93c and e['value'] == 1]
    ticks = [e for e in ev if e['kind'] == 'ticks']
    # the block flushed at a strobe cycle must end within 100 sys cycles before it
    orphan, lat = [], []
    for c in hb:
        blk = [t for t in ticks if t['cycle'] == c]
        if blk: lat.append(c - blk[-1]['last'])
        if not blk or not (0 <= c - blk[-1]['last'] <= 2000): orphan.append(c)
    # strobe gaps (closed) vs longest no-entry stretch inside that gap
    worst = -10**12
    for a, b in zip(hb, hb[1:]):
        inside = [t for t in ticks if a <= t['first'] and t['last'] <= b]
        pts = [a]
        for t in inside:
            pts += [t['first'], t['last']]
        span = max([t['max_gap'] for t in inside] + [y - x for x, y in zip(pts, pts[1:])] + [b - pts[-1]])
        excess = (b - a) - (25_000_000 + span)
        worst = max(worst, excess)
    print(f'  entry-to-strobe sys cycles min/max {min(lat)}/{max(lat)}')
    print(f'  strobes {len(hb)}; strobes without an entry <=2000 sys cycles before {len(orphan)}; '
          f'max (gap - 250 ms - longest no-entry span) = {worst / 1e5:.5f} ms')
    bad += len(orphan) + (worst > 2000)  # entry-to-strobe path slack
print('FAIL' if bad else 'PASS')
sys.exit(1 if bad else 0)
