#!/usr/bin/env python3
"""Enumerate every per-page difference between two tracked_pages.py outputs
over the same page bytes. Usage: compare_tracked.py <a.json> <b.json> <root>

Prints, per field, the pages that differ; for blocks and line_kinds the
differing line numbers with both labels and the line text; for headings
the added and removed headings.
"""
import json
import sys
from pathlib import Path

a, b = json.load(open(sys.argv[1])), json.load(open(sys.argv[2]))
root = Path(sys.argv[3])
fields = ("refusals", "blocks", "line_kinds", "headings", "plan", "existing",
          "generated_block", "owns", "apply_changes")
summary = {f: [] for f in fields}
for page in sorted(a):
    for f in fields:
        if f == "line_kinds" and (a[page][f] is None or b[page][f] is None):
            continue
        if a[page][f] != b[page][f]:
            summary[f].append(page)
for f in fields:
    print(f"{f}: {len(summary[f])} page(s) differ")
for page in summary["headings"]:
    ah = [tuple(h) for h in a[page]["headings"]]
    bh = [tuple(h) for h in b[page]["headings"]]
    print(f"\nHEADINGS {page}: plan_same={a[page]['plan'] == b[page]['plan']}"
          f" existing_same={a[page]['existing'] == b[page]['existing']}"
          f" owns={b[page]['owns']}")
    print(f"   only in first : {[h for h in ah if h not in bh]}")
    print(f"   only in second: {[h for h in bh if h not in ah]}")
for f in ("blocks", "line_kinds"):
    for page in summary[f]:
        lines = (root / page).read_text().split("\n")
        rows = [(i, x, y) for i, (x, y) in enumerate(zip(a[page][f], b[page][f]))
                if x != y]
        nonblank = [r for r in rows if lines[r[0]].strip(" \t")]
        print(f"\n{f.upper()} {page}: {len(rows)} line(s) differ, "
              f"{len(nonblank)} non-blank")
        for i, x, y in nonblank[:12]:
            print(f"   {page}:{i + 1}: {x!r} -> {y!r} | {lines[i][:90]!r}")
        if len(nonblank) > 12:
            print(f"   ... {len(nonblank) - 12} more")
