#!/usr/bin/env python3
"""Summarise the #726 fixture's per-descriptor window CSV from a run.log.

Usage: windows.py <run.log> [<run.log> ...]
Prints, per log: graded (windows 2..4) row-window counts by notification
count and descriptor type, minimum/maximum gaps, and the SERVICE maxima.
"""
import sys
from collections import Counter

for path in sys.argv[1:]:
    rows, service = [], {}
    for line in open(path, encoding="utf-8", errors="replace"):
        f = line.strip().split(",")
        if len(f) == 8 and f[0].isdigit() and f[1] in ("5", "6"):
            rows.append(f)
        elif f[0] == "SERVICE" and len(f) == 3:
            service[int(f[1])] = int(f[2])
    graded = [r for r in rows if int(r[4]) >= 2]
    by = Counter((("IN" if r[1] == "5" else "OUT"), int(r[5])) for r in graded)
    allw = Counter((("IN" if r[1] == "5" else "OUT"), int(r[4]), int(r[5])) for r in rows)
    gaps = [(float(r[6]), float(r[7])) for r in rows if int(r[4]) == 0]
    real = [g for g in gaps if g[1] > 0]
    print(f"== {path}")
    print(f"  row-windows total={len(rows)} graded={len(graded)}")
    print(f"  graded by (type, notifications): {dict(sorted(by.items()))}")
    print(f"  startup windows 0/1 by (type, window, n): "
          f"{dict(sorted((k, v) for k, v in allw.items() if k[1] < 2))}")
    if real:
        print(f"  min gap ms={min(g[0] for g in real):.3f} "
              f"max gap ms={max(g[1] for g in real):.3f} over {len(real)} rows with >=2 notifications")
    print(f"  rows with <2 notifications (gap undefined): {len(gaps) - len(real)}")
    if service:
        print(f"  max service cycles={max(service.values())} (ms={max(service.values())/1000:.3f})")
