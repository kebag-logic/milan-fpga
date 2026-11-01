#!/usr/bin/env python3
"""Reviewer-planted cuts of the datapath's shape wiring, graded by gate 1h's own reader.

usage: plant_gate1h.py <tree>; loads <tree>/sw/builder/test_builder.py and reads its datapath.
"""
import importlib.util, re, sys
from pathlib import Path
tree = Path(sys.argv[1])
sys.path.insert(0, str(tree / "sw/builder"))
spec = importlib.util.spec_from_file_location("tb", tree / "sw/builder/test_builder.py")
tb = importlib.util.module_from_spec(spec); sys.modules["tb"] = tb; spec.loader.exec_module(tb)
rtl = (tree / "hdl/milan/milan_datapath.sv").read_text()
T = "        .ETH_TICK_NS_P (GPTP_ETH_TICK_NS_P),\n"
C = "        .ETH_CYC_PER_OCTET_P(GPTP_ETH_CYC_PER_OCTET_P),\n"
assert rtl.count(T) == 1 and rtl.count(C) == 1
plants = [
 ("tick binding deleted", rtl.replace(T, "")),
 ("octet binding deleted", rtl.replace(C, "")),
 ("tick tied to 8", rtl.replace(T, "        .ETH_TICK_NS_P (8),\n")),
 ("octet tied to 1", rtl.replace(C, "        .ETH_CYC_PER_OCTET_P(1),\n")),
 ("bindings crossed", rtl.replace(T, "        .ETH_TICK_NS_P (GPTP_ETH_CYC_PER_OCTET_P),\n").replace(C, "        .ETH_CYC_PER_OCTET_P(GPTP_ETH_TICK_NS_P),\n")),
 ("tick scaled", rtl.replace(T, "        .ETH_TICK_NS_P (GPTP_ETH_TICK_NS_P * 2),\n")),
 ("octet to another parameter", rtl.replace(C, "        .ETH_CYC_PER_OCTET_P(GPTP_PHC_TICK_NS_P),\n")),
 ("tick default 40", rtl.replace("parameter int unsigned GPTP_ETH_TICK_NS_P = 8,", "parameter int unsigned GPTP_ETH_TICK_NS_P = 40,")),
 ("octet default 2", rtl.replace("parameter int unsigned GPTP_ETH_CYC_PER_OCTET_P = 1,", "parameter int unsigned GPTP_ETH_CYC_PER_OCTET_P = 2,")),
 ("tick made a localparam", rtl.replace("parameter int unsigned GPTP_ETH_TICK_NS_P = 8,", "localparam int unsigned GPTP_ETH_TICK_NS_P = 8,")),
 ("second plane", rtl.replace("    KL_gptp_shadow #(\n", "    KL_gptp_shadow #(.TDATA_WIDTH_P(8)) u_gptp_shadow (.clk_i(axis_clk));\n    KL_gptp_shadow #(\n", 1)),
 ("instance renamed", rtl.replace(") u_gptp_shadow (", ") u_plane (")),
 ("tick binding commented out", rtl.replace(T, "        // .ETH_TICK_NS_P (GPTP_ETH_TICK_NS_P),\n")),
 ("octet binding commented out", rtl.replace(C, "        // .ETH_CYC_PER_OCTET_P(GPTP_ETH_CYC_PER_OCTET_P),\n")),
 ("tick binding in a block comment", rtl.replace(T, "        /* .ETH_TICK_NS_P (GPTP_ETH_TICK_NS_P), */\n")),
 ("tick binding in a dead ifdef", rtl.replace(T, "`ifdef NEVER_DEFINED\n" + T + "`endif\n")),
 ("real default commented, moved to 40", rtl.replace("  parameter int unsigned GPTP_ETH_TICK_NS_P = 8,", "  // parameter int unsigned GPTP_ETH_TICK_NS_P = 8,\n  parameter int unsigned GPTP_ETH_TICK_NS_P = 40,")),
]
assert not tb._datapath_shape_findings(rtl), "the head itself must pass"
print("head: gate 1h reader returns no finding")
missed = 0
for name, text in plants:
    assert text != rtl, name
    bad = tb._datapath_shape_findings(text)
    print(f"{'REFUSED ' if bad else 'ACCEPTED'} {name}: {bad}")
    missed += not bad
print(f"plants {len(plants)} accepted {missed}")
