#!/usr/bin/env python3
"""Reviewer probe (R496-3): two AXI4-Lite defects that CROSS write data or
address with a neighbour's without losing a beat (the B count stays right),
each built into a copy of the head and run through `make run-axil`. Only a
read-back of each write's own register can catch them (A7).

usage: axil_pairing_mutants.py <exported head tree> <scratch dir> [verilator]
"""
import pathlib
import shutil
import subprocess
import sys

TREE = pathlib.Path(sys.argv[1]).resolve()
OUT = pathlib.Path(sys.argv[2]).resolve()
VERILATOR = sys.argv[3] if len(sys.argv) > 3 else "verilator"
RTL = "hdl/milan/mailbox/KL_mbx_axil.sv"

ARMS = {
    "wdata-overwritten-while-held": (
        "      if (s_wvalid_i && !w_full_r) begin\n        w_full_r <= 1'b1;\n"
        "        w_data_r <= s_wdata_i;\n        w_strb_r <= s_wstrb_i;\n"
        "      end else if (go_wr_w) begin\n        w_full_r <= 1'b0;\n      end",
        "      if (s_wvalid_i) begin\n        w_data_r <= s_wdata_i;\n        w_strb_r <= s_wstrb_i;\n"
        "      end\n      if (s_wvalid_i && !w_full_r) begin\n        w_full_r <= 1'b1;\n"
        "      end else if (go_wr_w) begin\n        w_full_r <= 1'b0;\n      end"),
    "awaddr-overwritten-while-held": (
        "      if (s_awvalid_i && !aw_full_r) begin\n        aw_full_r <= 1'b1;\n"
        "        aw_addr_r <= s_awaddr_i[MBX_ADDR_W_C+1:2];\n      end else if (go_wr_w) begin",
        "      if (s_awvalid_i) aw_addr_r <= s_awaddr_i[MBX_ADDR_W_C+1:2];\n"
        "      if (s_awvalid_i && !aw_full_r) begin\n        aw_full_r <= 1'b1;\n"
        "      end else if (go_wr_w) begin"),
}


def main() -> int:
    for name, (old, new) in ARMS.items():
        root = OUT / f"m_{name}"
        if root.exists():
            shutil.rmtree(root)
        for sub in ("hdl/milan/mailbox", "tb/verilator/mbx", "tb/common", "sw/firmware/ctrl", "sw/mailbox"):
            shutil.copytree(TREE / sub, root / sub)
        p = root / RTL
        s = p.read_text()
        assert s.count(old) == 1, name
        p.write_text(s.replace(old, new))
        r = subprocess.run(["make", "run-axil", f"VERILATOR={VERILATOR}"], cwd=root / "tb/verilator/mbx",
                           capture_output=True, text=True, check=False)
        lines = [ln for ln in (r.stdout + r.stderr).splitlines() if "[FAIL]" in ln or "checks:" in ln]
        print(f"== {name} rc={r.returncode}")
        for ln in lines:
            print(f"   {ln.strip()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
