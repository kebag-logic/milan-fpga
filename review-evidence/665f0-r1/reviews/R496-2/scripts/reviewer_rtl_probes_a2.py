#!/usr/bin/env python3
"""Reviewer probes (R496-2) for the A2 group (W before AW), which has no planted
arm of its own. Usage: reviewer_rtl_probes_a2.py TREE SCRATCH"""
import sys
from pathlib import Path
tree, root = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(tree / "tb/verilator/mbx"))
import mutants as mx  # noqa: E402
A = mx.Arm
PROBES = (
    A("p-axil-write-without-aw", "KL_mbx_axil.sv", "assign wr_ok_w = aw_full_r && w_full_r && !bvalid_r && !busy_r;",
      "assign wr_ok_w = w_full_r && !bvalid_r && !busy_r;", 1, "A2"),
    A("p-axil-held-w-overwritten", "KL_mbx_axil.sv", "if (s_wvalid_i && !w_full_r) begin\n        w_full_r <= 1'b1;\n        w_data_r <= s_wdata_i;",
      "if (s_wvalid_i) begin\n        w_full_r <= 1'b1;\n        w_data_r <= s_wdata_i;", 1, "A2"),
)
root.mkdir(parents=True, exist_ok=True)
for p in PROBES:
    rc, log = mx.build_and_run(mx.plant(p, root), root / p.name, p.host)
    fails = [ln.strip() for ln in log.splitlines() if "[FAIL]" in ln]
    a2 = [f for f in fails if "A2" in f]
    print(f"[{'caught' if rc == 1 and fails else 'ESCAPED'}] {p.name}: {len(fails)} [FAIL], {len(a2)} in A2; first: {fails[0] if fails else 'none'}")
