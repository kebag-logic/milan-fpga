#!/usr/bin/env python3
"""Scratch (never committed): compare R447's partition_check.py output with the round-2 prose.

Usage: partition_vs_prose.py <partition_check log> <checkout>
Reads the published script's own lines for the complete own-logic partition and the processor
top's own logic, and requires both pages to state those figures. Prints one line per figure and
a mismatch tally; exit 1 on any mismatch.
"""
from pathlib import Path
import re
import sys

log, repo = Path(sys.argv[1]).read_text(), Path(sys.argv[2])
pages = {"findings": (repo / "docs/findings/234_PP_SHADOW_AREA_BASELINE.md").read_text(),
         "AREA_BUDGET": (repo / "docs/design/AREA_BUDGET.md").read_text()}
part = re.search(r"every scope's own logic \(complete partition of the wrapper\): net LUT ([+-]\d+), "
                 r"abs LUT (\d+), net FF ([+-]\d+)", log)
top = re.search(r"u_pp own logic: LUT ([+-]\d+), FF ([+-]\d+)", log)
wants = [f"a net {part[1]} LUTs and {part[3]} FFs", f"sum to {part[2]} LUTs", f"{top[1]} LUTs and {top[2]} FFs"]
bad = 0
for page, text in pages.items():
    for want in wants:
        ok = want in text
        bad += 0 if ok else 1
        print(f"{'OK ' if ok else 'BAD'} {page}: {want!r}")
print(f"partition_check lines against the prose: {bad} mismatches")
sys.exit(1 if bad else 0)
