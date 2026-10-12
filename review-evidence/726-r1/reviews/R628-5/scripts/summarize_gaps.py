#!/usr/bin/env python3
"""Summarize the #726 fixture's GAPS/SERVICE/TX_COUNT/check lines from a run.log.

Usage: summarize_gaps.py <run.log> [...]
GAPS columns: shape,type,index,recipient,start,count,min_ms,max_ms,tail_ms,service_ms
"""
import sys

for path in sys.argv[1:]:
    rows, ok, fail, tx = [], 0, 0, []
    for line in open(path, errors="replace"):
        if line.startswith("GAPS,"):
            f = line.strip().split(",")
            rows.append((int(f[2]), int(f[3]), int(f[4]), int(f[6]), float(f[7]),
                         float(f[8]), float(f[9]), float(f[10])))
        elif line.startswith("TX_COUNT,"):
            tx.append(line.strip())
        elif "[ok]" in line or "[ ok ]" in line:
            ok += 1
        elif "[FAIL]" in line:
            fail += 1
    gaps = sum(max(r[3] - 1, 0) for r in rows)
    print(f"{path}: rows={len(rows)} graded_gaps={gaps} checks_ok={ok} fail={fail}")
    if rows:
        print(f"  min_gap_ms={min(r[4] for r in rows):.3f} max_gap_ms={max(r[5] for r in rows):.3f}"
              f" max_tail_ms={max(r[6] for r in rows):.3f} max_service_ms={max(r[7] for r in rows):.3f}")
        for ty in (5, 6):
            counts = sorted({r[3] for r in rows if r[0] == ty})
            print(f"  type {ty}: notifications per row {counts}")
        worst = [r for r in rows if r[5] > 1000 + r[7]]
        print(f"  rows with max_gap > 1000 + service: {len(worst)}")
    for t in tx:
        print("  " + t)
