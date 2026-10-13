#!/usr/bin/env python3
"""Summarize a stream_counters run.log: checks, gap rows, TX/RX totals.

Usage: summarize_counters.py RUN_LOG [RUN_LOG...]
GAPS row layout (stream_counters.hpp): GAPS,shape,type,index,recipient,start,
count,min_ms,max_ms,tail_ms,service_ms.
"""
import re
import sys


def summarize(path: str) -> None:
    text = open(path, encoding="utf-8", errors="replace").read()
    lines = text.splitlines()
    passes = sum(1 for l in lines if "[PASS]" in l or l.lstrip().startswith("PASS"))
    fails = [l for l in lines if "[FAIL]" in l]
    result = [l for l in lines if "RESULT:" in l]
    gaps = [l.split(",") for l in lines if l.startswith("GAPS,")]
    rows = []
    for g in gaps:
        shape, ty, ix, r, start, cnt = (int(x) for x in g[1:7])
        mn, mx, tail, svc = (float(x) for x in g[7:11])
        rows.append((shape, ty, ix, r, start, cnt, mn, mx, tail, svc))
    print(f"== {path}")
    print(f"  result: {result[-1] if result else 'NONE'}; FAIL lines: {len(fails)}")
    for f in fails[:12]:
        print("   ", f.strip()[:160])
    if rows:
        ngaps = sum(max(r[5] - 1, 0) for r in rows)
        print(f"  gap rows: {len(rows)} (descriptor x recipient); consecutive gaps: {ngaps}")
        print(f"  notifications per row: {sorted(set(r[5] for r in rows))}")
        valid = [r for r in rows if r[5] >= 2]
        if valid:
            print(f"  min gap {min(r[6] for r in valid):.3f} ms; max gap {max(r[7] for r in valid):.3f} ms; "
                  f"max tail {max(r[8] for r in rows):.3f} ms; max service {max(r[9] for r in rows):.3f} ms")
        for ty in (5, 6):
            sub = [r for r in rows if r[1] == ty]
            if sub:
                print(f"  type {ty}: rows {len(sub)}, counts {sorted(set(r[5] for r in sub))}, "
                      f"max gap {max(r[7] for r in sub):.3f}")
    tx = [l for l in lines if l.startswith(("TX_COUNT,", "TX_RUN,"))]
    for l in tx:
        print("  ", l)
    oc = [l for l in lines if l.startswith("OUTPUT_CONDITION,")]
    for l in oc:
        print("  ", l)


for p in sys.argv[1:]:
    summarize(p)
