#!/usr/bin/env python3
"""Disposable reviewer arm: a settled sink's registrar takes LINK_DOWN (Flush!) but not
LINK_UP (Begin!). usage: plant_settled_begin_dropped.py <tree>"""
import sys
f = sys.argv[1] + "/hdl/srp/KL_srp_listener_fsm.sv"
s = open(f).read()
a = "                    || (link_ev_w && (reg_r[s] != R_MT_C));"
b = "                    || (link_ev_w && (!link_up_i || !armed_r[s]) && (reg_r[s] != R_MT_C));"
c = "        if (link_ev_w) begin\n          // issue #212: LINK_DOWN"
d = "        if (link_ev_w && (!link_up_i || !armed_r[s])) begin\n          // issue #212: LINK_DOWN"
assert s.count(a) == 1 and s.count(c) == 1, "anchor"
open(f, "w").write(s.replace(a, b).replace(c, d))
