#!/usr/bin/env python3
"""txstmt_probe.py <repo>: rows_tiers.tx_statements at the tree (read-only)."""
import sys, pathlib
root = pathlib.Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "tb/verilator/ctrl_service_budget"))
import rows_tiers as rt
print("POINTS", rt.POINTS)
print("tx_statements", rt.tx_statements(root))
