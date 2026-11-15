#!/usr/bin/env python3
"""tx_probe.py <repo>: the built design's tx row and stated CTRL_LOOP_TX_MS
at each point, by the tree's own tier model (read-only)."""
import sys, pathlib
root = pathlib.Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "tb/verilator/ctrl_service_budget"))
import rows_tiers as rt
for p in ("1x1/1if", "8x8/2if"):
    i = rt.point_inputs(root, p)
    print(p, "tx", rt.solve("tx", i, rt.BUILT)[0], "txL", rt.solve("txL", i, rt.BUILT)[0], "stated", i.tx_stated)
