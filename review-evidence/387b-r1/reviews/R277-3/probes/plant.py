#!/usr/bin/env python3
"""Plant one reviewer probe mutation into a disposable tree copy.
Usage: plant.py <tree> <probe-name>. Each anchor must occur exactly once."""
import sys
from pathlib import Path

DP = "hdl/milan/milan_datapath.sv"
MCR = "hdl/ieee1722/avtp/KL_media_clock_restart.sv"
PROBES = {
    # the step toggle gated by the CRF clock-source selection (pre-#387 shape)
    "step_gated_by_source": (DP,
        "                       | media_rebase_p_w;",
        "                       | (crf_clk_selected_r & media_rebase_p_w);"),
    # a software settime no longer restarts mr (adjtime still does)
    "settime_no_mr": (DP,
        "                       | media_rebase_p_w;",
        "                       | eff_ptp_adjust_w;"),
    # the plane-off CLKV adjtime no longer restarts mr (settime still does)
    "adjtime_no_mr": (DP,
        "                       | media_rebase_p_w;",
        "                       | cfg_ptp_cmd_load;"),
}
tree, name = Path(sys.argv[1]), sys.argv[2]
rel, anchor, repl = PROBES[name]
p = tree / rel
t = p.read_text()
n = t.count(anchor)
if n != 1:
    sys.exit(f"anchor count {n} != 1 for {name}")
p.write_text(t.replace(anchor, repl))
print(f"planted {name} in {rel}")
