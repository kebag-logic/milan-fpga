#!/usr/bin/env python3
"""Render receipts/gates/summary.tsv as the handoff's gate table; exit 1 if any step is not rc 0."""
import sys
from pathlib import Path

rows = [ln.split("\t") for ln in Path(sys.argv[1]).read_text().splitlines() if ln.strip()]
rows.sort(key=lambda r: int(r[0]))
out = ["| Step | Job | Name | Result | Time | Receipt |", "|---|---|---|---|---|---|"]
bad = 0
for idx, job, name, result, secs in rows:
    receipt = next((p.name for p in Path(sys.argv[1]).parent.glob(f"{int(idx):02d}-*.txt")), "-")
    out.append(f"| {idx} | {job} | {name} | {result} | {secs} | `gates/{receipt}` |" if receipt != "-" else
               f"| {idx} | {job} | {name} | {result} | {secs} | - |")
    bad += result.startswith("rc=") and result != "rc=0"
print("\n".join(out))
print(f"\n{sum(r[3] == 'rc=0' for r in rows)} steps rc 0, {bad} not rc 0, "
      f"{sum(r[3].startswith('not rerun') for r in rows)} setup steps not rerun.")
sys.exit(1 if bad else 0)
