#!/usr/bin/env python3
"""Dev's datapath on the binds the head harness classes inside B17's window.

usage: base_on_head_window.py <head sweep dir> <base sweep dir>
For every bind the head run classes inside B17's window, the same run and cycle on
dev's datapath: does it slip the ring exactly one frame (+2 dups, one slip event),
at its first burst (0 to 10 ms after it), and nothing else?
"""
import re
import sys
from pathlib import Path

res = re.compile(r"RESULT-645-BIND: B17 cycle (\d+) phase .*?\((inside|OUTSIDE) B17's window\).*?SLIP_LB "
                 r"\+(\d+) dups \+(\d+) skips")
sl = re.compile(r"info: B17 cycle (\d+): slip \((dup|skip)\) [-+0-9.]+ s after the bind, ([-+0-9.]+) s from")


def read(d):
    out = {}
    for log in Path(d).glob("bind_*.log"):
        cur = None
        for line in log.read_text().splitlines():
            m = res.search(line)
            if m:
                cur = (log.stem, int(m.group(1)))
                out[cur] = dict(win=m.group(2), dups=int(m.group(3)), skips=int(m.group(4)), slips=[])
                continue
            m = sl.search(line)
            if m and cur and int(m.group(1)) == cur[1]:
                out[cur]["slips"].append((m.group(2), float(m.group(3))))
    return out


head, base = read(sys.argv[1]), read(sys.argv[2])
inside = sorted(k for k, v in head.items() if v["win"] == "inside")
sig = [k for k in inside if base[k]["dups"] == 2 and base[k]["skips"] == 0 and len(base[k]["slips"]) == 1
       and 0.0 <= base[k]["slips"][0][1] < 0.01]
print(f"head-inside binds {len(inside)}; on dev's datapath exactly one frame at the first burst and nothing else: "
      f"{len(sig)}; base classes inside {sum(base[k]['win'] == 'inside' for k in inside)} of them")
for k in inside:
    if k not in sig:
        print("  other:", k, base[k])
