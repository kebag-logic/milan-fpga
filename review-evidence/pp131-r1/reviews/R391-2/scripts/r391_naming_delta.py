#!/usr/bin/env python3
"""Run the parent's naming scanner (scripts/measure_naming.py scan_text) over
the processor hdl/ of two or more trees and print the unit-naming candidates
each tree adds over the first.
Usage: r391_naming_delta.py <dir containing measure_naming.py> <tree_a> <tree_b> [...]"""
import sys, pathlib
sys.path.insert(0, sys.argv[1])
import measure_naming as mn

def cands(tree):
    out = {}
    for p in sorted(pathlib.Path(tree, "hdl").rglob("*.sv")):
        c, _e, _st = mn.scan_text(p.read_text(errors="replace"))
        for module, name, unit, doc, reason in c:
            out[f"{p.relative_to(tree)}:{module}:{name}"] = (unit, reason, doc)
    return out

base = cands(sys.argv[2])
print(f"{sys.argv[2]}: {len(base)} candidate(s)")
for t in sys.argv[3:]:
    c = cands(t)
    print(f"{t}: {len(c)} candidate(s); new over the first: {len(set(c) - set(base))}; "
          f"gone: {len(set(base) - set(c))}")
    for k in sorted(set(c) - set(base)):
        print("  NEW", k, c[k][:2])
    for k in sorted(set(base) - set(c)):
        print("  GONE", k)
