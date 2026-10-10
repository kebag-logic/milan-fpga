#!/usr/bin/env python3
"""census_extra_forms.py - R582-3: further population-level forms planted into copies of the head's datapath.

Usage: census_extra_forms.py <tree>. Each must be refused (any finding); prints REFUSED or ACCEPTED.
"""
import sys
from dataclasses import replace
from pathlib import Path
tree = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tree / "sw/mailbox"))
import publication_census as pc  # noqa: E402
src = pc.load(tree / "hdl/milan/milan_datapath.sv", tree / "hdl/milan/KL_pp_shadow.sv")
known = pc.fields(pc.mailbox_model.load())
W = "pp_cd_srp_over_limit_w"
C = "  wire crft_class_a_w = (ACMP_SRC_C > N_STREAMS) &"
V = "    .vlan_en_i  (crft_class_a_w),"
def routed(decl):
    return src.datapath.replace(C, decl + C, 1).replace(V, "    .vlan_en_i  (crft_class_a_w & ~probe_w),", 1)
FORMS = [
    ("generate-if condition", f"  wire probe_w;\n  if (1) begin : g_probe\n    assign probe_w = 1'b0;\n  end\n  if ({W}) begin : g_p2 end\n"),
    ("let construct", f"  let probe_l = {W};\n  wire probe_w;\n  assign probe_w = probe_l;\n"),
    ("sensitivity list", f"  logic probe_w;\n  always @({W}) probe_w = 1'b1;\n"),
    ("macro body", f"  `define PROBE_M {W}\n  wire probe_w;\n  assign probe_w = `PROBE_M;\n"),
    ("ternary select", f"  wire probe_w = {W} ? 1'b1 : 1'b0;\n"),
    ("concatenation lvalue", f"  wire probe_w, probe_x;\n  assign {{probe_w, probe_x}} = {{{W}, 1'b0}};\n"),
]
bad = 0
clean, _ = pc.findings(src, pc.CENSUS, known)
print(f"control: {len(clean)} finding(s)")
for what, decl in FORMS:
    try:
        got, _ = pc.findings(replace(src, datapath=routed(decl)), pc.CENSUS, known)
    except pc.CensusError as exc:
        got = [f"CensusError: {exc}"]
    bad += not got
    print(f"[{'REFUSED' if got else 'ACCEPTED'}] {what}: {got[0][:170] if got else 'PASS'}")
print(f"extra forms: {len(FORMS) - bad} of {len(FORMS)} refused")
