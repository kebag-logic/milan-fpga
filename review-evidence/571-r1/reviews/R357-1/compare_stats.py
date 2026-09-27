#!/usr/bin/env python3
"""R357-1: compare two Verilator --stats reports, ignoring the argv line,
absolute scratch paths and time/memory measurements.
Usage: compare_stats.py <base_stats.txt> <head_stats.txt>"""
import re, sys
def norm(p):
    out = []
    for line in open(p):
        if line.strip().startswith("Arguments:"):
            continue
        if re.search(r"(?i)time|memory|walltime|cpu|allocated|jobs", line):
            continue
        out.append(re.sub(r"$REVIEWS/571-r357-1-packet/scratch/(base|head)", "<tree>", line.rstrip()))
    return out
a, b = norm(sys.argv[1]), norm(sys.argv[2])
import difflib
d = [l for l in difflib.unified_diff(a, b, "base", "head", n=0, lineterm="")]
stat_rows = sum(1 for l in a if re.search(r"\s\d+(\.\d+)?$", l))
print(f"compared {len(a)} normalized lines ({stat_rows} numeric rows); diff lines: {len(d)}")
print("\n".join(d[:60]))
sys.exit(1 if d else 0)
