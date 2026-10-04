#!/usr/bin/env python3
"""Reviewer probe P1: in a DISPOSABLE tree copy, remove the AAF bind-fall unlock
(task #32) from KL_avtp_rx_monitor_ctx so an AAF unbind is counted only by the
100 ms silence walk. The [UNB] AAF U3 checks must then fail.

Usage: plant_aaf_probe.py <tree>
"""
import sys
from pathlib import Path

p = Path(sys.argv[1]) / "hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv"
old = "        if (bind_fall_i[s] && locked_sh_r[s]) sil_pend_r[s] <= 1'b1;\n"
new = "        if (1'b0 && bind_fall_i[s] && locked_sh_r[s]) sil_pend_r[s] <= 1'b1;\n"
text = p.read_text()
if text.count(old) != 1:
    sys.exit(f"REFUSED: pattern occurs {text.count(old)} times")
p.write_text(text.replace(old, new))
print(f"planted P1 in {p}")
