#!/usr/bin/env python3
"""Probe (R506-1): an uncovered arc that moves inside an excluded function.
The planted source of fw_coverage_selftest.py: g's `if (a == 7)` is excluded
("1 arc, 1 line"). Here that branch is now taken (its arc and its line run),
and a different arc and a different line of g are left uncovered instead.
The README says a row "stops matching (its branch became reachable, or
something else in the function went uncovered)" and fails the gate.
Usage: exclusion_swap_probe.py <repo checkout>"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(sys.argv[1]) / "sw/firmware/gtest"))
import fw_coverage as cov
import fw_coverage_selftest as st

p = st.Planted()
try:
    def ln(n, count, arcs=()):
        return {"line_number": n, "count": count,
                "branches": [{"count": a, "throw": False} for a in arcs]}
    base = st.doc(str(p.root / st.FILE))
    print("control (the selftest's clean measurement):", p.verdict([base], [st.row()], st.FULL) or "no finding")
    swapped = {"files": [{"file": str(p.root / st.FILE),
                          "functions": base["files"][0]["functions"],
                          "lines": [ln(1, 2), ln(3, 2, (2, 1, 1, 1)), ln(4, 1), ln(5, 1), ln(7, 3),
                                    ln(9, 3, (1, 2)),       # the excluded `a == 7` branch: now taken
                                    ln(10, 1),              # and its line runs
                                    ln(11, 3, (0, 3)),      # another arc of g, never taken
                                    ln(12, 0)]}]}           # another line of g, never run
    found = p.verdict([swapped], [st.row()], st.FULL)
    print("swapped (named branch covered, another arc and line of g uncovered):", found or "no finding")
finally:
    p.close()
