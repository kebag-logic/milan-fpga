#!/usr/bin/env python3
"""Reviewer reproduction of the slice rule (#894 ruling: the slice with the largest least
relative margin over the five rows at 1x1/1if), computed here from rows_tiers.rows() at every
slice on a 50 us grid, with the margin (bound - W) / bound taken by this script, not by
rows_tiers.least_margin. Also on a 10 us grid, to show the 50 us grid does not hide a better slice.

usage: slice_rule.py REPO_ROOT
"""
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "tb/verilator/ctrl_service_budget"))
import rows_tiers as rt  # noqa: E402

BOUNDS = {"R4": 20.0, "R5": 90.0, "R6": 90.0, "first": 20.0, "last": 125.0}
for point in ("1x1/1if", "8x8/2if"):
    i = rt.point_inputs(root, point)
    lo, hi = rt.smallest_slice(i), i.h["CTRL_LOOP_DRAIN_US"]
    print(f"== {point}: smallest slice the code could take {lo} us, CTRL_LOOP_DRAIN_US {hi} us, "
          f"tree slice {i.h.get('CTRL_LOOP_SLICE_US')}")
    for grid in (50, 10):
        best = None
        first = -(-lo // grid) * grid
        rows_out = []
        for us in range(first, hi + 1, grid):
            r = rt.rows(root, point, rt.BUILT._replace(slice_us=us), i)
            ws = {k: r[k][0] for k in BOUNDS}
            if any(w is None for w in ws.values()):
                m, bind = float("-inf"), "unsolved"
            else:
                rel = {k: (BOUNDS[k] - ws[k]) / BOUNDS[k] for k in BOUNDS}
                bind = min(rel, key=rel.get)
                m = rel[bind]
            rows_out.append((us, m, bind, ws))
            if best is None or m > best[1]:
                best = (us, m, bind)
        if grid == 50:
            for us, m, bind, ws in rows_out:
                print(f"  {us:5d} us  least {m:+.4f} ({bind})  " +
                      " ".join(f"{k}={'-' if w is None else f'{w:.2f}'}" for k, w in ws.items()))
        print(f"  grid {grid} us: best {best[0]} us, least relative margin {best[1]:+.4f}, binding {best[2]}")
    print(f"  rows_tiers.slice_choice: {rt.slice_choice(root, point)}")
