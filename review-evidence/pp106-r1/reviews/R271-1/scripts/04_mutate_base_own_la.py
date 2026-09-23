#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Base-tree analogues of probes R10/R11: drop the own-LeaveAll term from the
talker (B10) and listener (B11) registrar aging at fbc1f715, to tell a gap
this PR introduced from one it inherited. Reuses 03_mutate.py's runner.
Usage: 04_mutate_base_own_la.py <base-tree> <scratch> <verilator> <out.txt>"""
import importlib.util
import pathlib
import sys

here = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("m", here / "03_mutate.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
m.MUTANTS = {
    "B10": ("hdl/srp/KL_srp_talker_fsm.sv",
            "  assign leaveall_any_w = leaveall_rx_i || leaveall_own_i;",
            "  assign leaveall_any_w = leaveall_rx_i;"),
    "B11": ("hdl/srp/KL_srp_listener_fsm.sv",
            "  assign leaveall_any_w = leaveall_rx_i || leaveall_own_i;",
            "  assign leaveall_any_w = leaveall_rx_i;"),
}
sys.argv = [sys.argv[0]] + sys.argv[1:]
m.main()
