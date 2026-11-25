#!/usr/bin/env python3
"""Work passes over THE SHARE in a harness results directory: share_census.py RESULTS_DIR.

Reads every group log's `PASS <n> <start> <..> <cycles>` lines (the same lines round 1's harness_grade.py reads) and
prints, per group, its pass count, its longest pass and the passes over THE SHARE (200,000 CPU cycles, share.py's
2 ms at 100 MHz), then the totals. A pass over THE SHARE is listed with its group, so a reader can see whether it is
one kept_grade owes to #977 (srp-bound) or a failure.
"""
import re
import sys
from pathlib import Path

SHARE = 200_000
results = Path(sys.argv[1])
total = over = 0
longest = (0, "")
rows = []
for f in sorted(results.glob("*.log")):
    cyc = [int(m[1]) for m in re.finditer(r"^PASS \d+ \d+ \d+ (\d+)", f.read_text(errors="replace"), re.M)]
    if not cyc:
        continue
    o = [c for c in cyc if c > SHARE]
    total += len(cyc); over += len(o)
    if max(cyc) > longest[0]:
        longest = (max(cyc), f.stem)
    if o:
        rows.append(f"  OVER {f.stem}: {len(o)} pass(es) over THE SHARE, longest {max(o):,}")
print(f"{results}: {total} work passes in {len(list(results.glob('*.log')))} logs; {over} over THE SHARE {SHARE:,}; "
      f"longest {longest[0]:,} ({longest[1]})")
print("\n".join(rows) if rows else "  no group has a pass over THE SHARE")
