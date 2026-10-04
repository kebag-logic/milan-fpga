#!/usr/bin/env python3
"""Re-derive tb/srp_top/README.md's issue-#230 control table from campaign
receipts: for each row, the FAIL lines per shape ([sources/sinks] suffix), the
named failing checks (the tag after "FAIL:") and the shapes caught at.

Usage: verify_table.py <README.md> <campaign output dir>
Prints one line per row, MATCH or DIFF with both sides; exit 1 on any DIFF.
"""
import re
import sys
from pathlib import Path

readme, out = Path(sys.argv[1]), Path(sys.argv[2])
SHAPES = ["1/1", "2/2", "3/5", "9/9"]
rows = []
in_table = False
for line in readme.read_text().splitlines():
    if line.startswith("| Control | From | Edit | Named failing checks |"):
        in_table = True
        continue
    if in_table:
        if not line.startswith("|"):
            break
        if line.startswith("|---"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        rows.append(cells)

bad = 0
for c in rows:
    label = c[0].strip("`")
    want_tags = [t.strip() for t in c[3].split(",")]
    want = [int(re.match(r"\d+", x).group()) for x in c[4:8]]
    want_at = c[8]
    log = out / f"{label}.log"
    if not log.exists():
        print(f"{label}: NO-RECEIPT")
        bad += 1
        continue
    fails = [l for l in log.read_text().splitlines() if l.startswith("FAIL:")]
    got = [sum(1 for l in fails if l.endswith(f"[{s}]")) for s in SHAPES]
    tags = sorted({l.split(":", 2)[1].strip() for l in fails},
                  key=lambda t: (re.sub(r"\d+", "", t), int(re.sub(r"\D", "", t) or 0)))
    at = f"{sum(1 for g in got if g)} of 4"
    ok = got == want and tags == want_tags and at == want_at
    bad += not ok
    print(f"{label}: {'MATCH' if ok else 'DIFF'} readme={want} {want_tags} {want_at} "
          f"receipt={got} {tags} {at}")
print(f"{len(rows)} rows, {bad} not matching")
sys.exit(1 if bad else 0)
