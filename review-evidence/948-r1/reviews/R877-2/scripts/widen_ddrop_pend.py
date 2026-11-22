#!/usr/bin/env python3
"""Probe (reviewer, disposable): widen the monitor's per-input DEPKT drop
accumulator ddrop_pend_r from 3 to 6 bits, to test whether [FO10]'s lost drop
increments under tap bubbles are its saturation at 7.
Usage: widen_ddrop_pend.py <tree>"""
import sys
from pathlib import Path
p = Path(sys.argv[1]) / "hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv"
s = p.read_text()
edits = [
    ("  logic [2:0] ddrop_pend_r  [N_LISTENERS_P];", "  logic [5:0] ddrop_pend_r  [N_LISTENERS_P];"),
    ("          ddrop_pend_r[s] <= ddrop_pend_r[s] + 3'd1;", "          ddrop_pend_r[s] <= ddrop_pend_r[s] + 6'd1;"),
    ("                                      - 3'(ddrop_add_r)\n                                      + ((depkt_drop_p_i &&\n                                          depkt_drop_mask_i[ev_s_r])\n                                         ? 3'd1 : 3'd0);",
     "                                      - 6'(ddrop_add_r)\n                                      + ((depkt_drop_p_i &&\n                                          depkt_drop_mask_i[ev_s_r])\n                                         ? 6'd1 : 6'd0);"),
]
for a, b in edits:
    if s.count(a) != 1:
        print("anchor not unique:", a[:50]); sys.exit(1)
    s = s.replace(a, b)
p.write_text(s)
print("widened ddrop_pend_r in", p)
