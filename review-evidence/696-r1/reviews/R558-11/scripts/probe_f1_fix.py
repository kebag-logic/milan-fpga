#!/usr/bin/env python3
"""Apply R558-11-F1's and R558-11-R1's example wording to a scratch checkout.

Usage: python3 -I probe_f1_fix.py <scratch checkout>
Each replaced sentence must occur exactly once; the probe refuses otherwise.
Restore afterwards with: git -C <scratch checkout> checkout -- docs/design/MARK_II_AREA_PLAN.md
"""
import sys
from pathlib import Path

path = Path(sys.argv[1]) / "docs/design/MARK_II_AREA_PLAN.md"
text = path.read_text()
edits = [
    ("The base route equals the `route-1x1` record in every gated figure.\n"
     "Against that record, the M5 route passes with no failing endpoint.\n",
     "The base route equals #645/#647's `route-1x1` record, the gate record at dev `e8454e27`, "
     "in every gated figure; [#696](https://github.com/kebag-logic/milan-fpga/issues/696)'s "
     "50,013-LUT re-record has since replaced it.\n"
     "Against that record, the M5 route passes with no failing endpoint; it also passes against #696's record.\n"),
    ("pending the week-4 re-measure (D8).\nThe gate record stays unchanged under D7.\n",
     "pending the week-4 re-measure (D8).\nM5 does not re-record the gate under D7.\n"),
]
for old, new in edits:
    if text.count(old) != 1:
        sys.exit(f"anchor count {text.count(old)} != 1: {old[:60]!r}")
    text = text.replace(old, new)
path.write_text(text)
print("applied", len(edits), "edits")
