#!/usr/bin/env python3
"""pace_probe.py <repo>: txL and R4L at 1x1/1if under the built design at
every pace 1..13 ms, by the tree's own tier model (read-only)."""
import sys, pathlib
root = pathlib.Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "tb/verilator/ctrl_service_budget"))
import rows_tiers as rt, paced_rows as pr
i = rt.point_inputs(root, "1x1/1if")
print("tx_bound", i.tx_bound, "R4L bound", pr.PACED_BOUNDS["R4L"], "choice", pr.choice(root))
for p in range(1, pr.PACE_MOST_MS + 1):
    at = i._replace(pace_ms=p)
    print(p, "txL", rt.solve("txL", at, rt.BUILT)[0], "R4L", rt.solve("R4L", at, rt.BUILT)[0])
