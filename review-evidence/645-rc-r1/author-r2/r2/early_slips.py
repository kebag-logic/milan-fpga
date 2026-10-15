#!/usr/bin/env python3
"""Slips before B17's first burst, per bind, in two sweeps of the same grid.

usage: early_slips.py <head sweep dir> <base sweep dir>
A slip before the first burst falls in the arming window on the head (the ring acts
42.7 ms after the first PDU, long before any first burst here). Lists every bind with
one, on either side, with its kind, its time from the burst and the head's window class.
"""
import re
import sys
from pathlib import Path

res = re.compile(r"RESULT-645-BIND: B17 cycle (\d+) phase ([0-9.]+) .*?\((inside|OUTSIDE) B17's window\)")
sl = re.compile(r"info: B17 cycle (\d+): slip \((dup|skip)\) ([-+0-9.]+) s after the bind, ([-+0-9.]+) s from")


def early(d):
    out, cls = {}, {}
    for log in Path(d).glob("bind_*.log"):
        cur = None
        for line in log.read_text().splitlines():
            m = res.search(line)
            if m:
                cur = (log.stem, int(m.group(1)))
                cls[cur] = (float(m.group(2)), m.group(3))
                continue
            m = sl.search(line)
            if m and cur and int(m.group(1)) == cur[1] and float(m.group(4)) < 0.0:
                out.setdefault(cur, []).append((m.group(2), round(float(m.group(4)), 6)))
    return out, cls


(h, hc), (b, _) = early(sys.argv[1]), early(sys.argv[2])
keys = sorted(set(h) | set(b))
same = sum(h.get(k) == b.get(k) for k in keys)
print(f"binds with a slip before the first burst: head {len(h)}, dev's datapath {len(b)}, identical on both {same}")
for k in keys:
    print(f"  {k[0]} cycle {k[1]} phase {hc[k][0]:.5f} ({hc[k][1]} on the head): head {h.get(k)} dev {b.get(k)}")
