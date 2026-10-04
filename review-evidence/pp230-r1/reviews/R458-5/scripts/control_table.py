#!/usr/bin/env python3
"""Recount the #230 storage control table from the srp_top campaign receipts.

usage: control_table.py <campaign-receipt-dir> <README.md>
Counts FAIL lines per shape tag [m/n] in each walk/FIFO control's receipt and
compares them with the README row (1/1, 2/2, 3/5, 9/9 columns).
"""
import re
import sys
from pathlib import Path

rd, readme = Path(sys.argv[1]), Path(sys.argv[2]).read_text()
shapes = ["1/1", "2/2", "3/5", "9/9"]
bad = 0
rows = 0
for line in readme.splitlines():
    m = re.match(r"\| `([a-z0-9-]+)` \|[^|]*\|[^|]*\|[^|]*\|" + r"\s*([^|]+)\|" * 4, line)
    if not m or not (rd / f"{m.group(1)}.log").exists() or not line.rstrip().endswith("of 4 |"):
        continue
    name = m.group(1)
    want = [int(re.match(r"\s*(\d+)", m.group(2 + i)).group(1)) for i in range(4)]
    text = (rd / f"{name}.log").read_text()
    got = [sum(1 for l in text.splitlines() if l.startswith("FAIL:") and l.rstrip().endswith(f"[{s}]"))
           for s in shapes]
    rows += 1
    ok = got == want
    bad += not ok
    print(f"{'OK ' if ok else 'BAD'} {name}: README {want} receipt {got}")
print(f"{rows} rows, {bad} mismatches")
sys.exit(1 if bad or rows == 0 else 0)
