#!/usr/bin/env python3
"""Per bind: the in-window binds' slips (count and time from the first burst). usage: inside_check.py <sweep_dir>"""
import re
import sys
from pathlib import Path
res = re.compile(r"RESULT-645-BIND: B17 cycle (\d+) phase .*?\((inside|OUTSIDE) B17's window\).*?SLIP_LB \+(\d+) dups \+(\d+) skips")
sl = re.compile(r"info: B17 cycle (\d+): slip \((dup|skip)\) ([-+0-9.]+) s after the bind, ([-+0-9.]+) s from the first burst")
stats = {"inside": 0, "inside_one_frame_at_burst": 0, "inside_other": [], "outside": 0, "outside_frames": {}}
for log in sorted(Path(sys.argv[1]).glob("bind_*.log")):
    cur = None
    for line in log.read_text().splitlines():
        m = res.search(line)
        if m:
            if cur: stats_tail = None
            cur = {"run": log.stem, "c": int(m.group(1)), "inside": m.group(2) == "inside",
                   "dups": int(m.group(3)), "skips": int(m.group(4)), "slips": []}
            if cur["inside"]:
                stats["inside"] += 1
            else:
                stats["outside"] += 1
            # slips for this bind follow the RESULT line
            continue
        m = sl.search(line)
        if m and cur:
            cur["slips"].append(float(m.group(4)))
            continue
        if cur and (line.startswith("  [") or line.startswith("RESULT-") or line.startswith("==")):
            pass
    # second pass with explicit grouping
for log in sorted(Path(sys.argv[1]).glob("bind_*.log")):
    lines = log.read_text().splitlines()
    for i, line in enumerate(lines):
        m = res.search(line)
        if not m:
            continue
        slips = []
        for nxt in lines[i + 1:]:
            if res.search(nxt):
                break
            s = sl.search(nxt)
            if s:
                slips.append(float(s.group(4)))
        if m.group(2) == "inside":
            ok = int(m.group(3)) == 2 and int(m.group(4)) == 0 and len(slips) == 1 and 0.0 <= slips[0] < 0.01
            stats["inside_one_frame_at_burst"] += ok
            if not ok:
                stats["inside_other"].append((log.stem, m.group(1), m.group(3), slips))
        else:
            k = len(slips)
            stats["outside_frames"][k] = stats["outside_frames"].get(k, 0) + 1
print(stats)
