#!/usr/bin/env python3
"""Apply one named mutation to a copied tree's KL_pp_nvm_port.sv for the
elab_bounds.sh mutant campaign. Every replacement must match exactly once.

usage: nvm_mutants.py <tree> <mutant>
"""
import sys
from pathlib import Path

tree, name = Path(sys.argv[1]), sys.argv[2]
f = tree / "hdl" / "packet_engine" / "KL_pp_nvm_port.sv"
s = f.read_text()
COND = "if (MAX_PAYLOAD_P > MAXP_BOUND_C) begin : g_maxp_check"
FAT = '$fatal(1, "KL_pp_nvm_port: MAX_PAYLOAD_P'
ARGS = "MAX_PAYLOAD_P, MAXP_BOUND_C, HDR_LEN_C);"
GUARD = (COND + "\n    " + FAT + '=%0d is above %0d: %0d + it overflows dev_len_o",\n'
         "           " + ARGS + "\n  end")
M = {
    "pristine": [],
    "guard-deleted": [(COND, "if (1'b0) begin : g_maxp_check")],
    "bound-plus-1": [(COND, "if (MAX_PAYLOAD_P > MAXP_BOUND_C + 1) begin : g_maxp_check")],
    "ge": [(COND, "if (MAX_PAYLOAD_P >= MAXP_BOUND_C) begin : g_maxp_check")],
    "msg-no-bound": [('=%0d is above %0d: %0d + it overflows dev_len_o",\n           ' + ARGS,
                      '=%0d overflows dev_len_o",\n           MAX_PAYLOAD_P);')],
    "initial": [(GUARD, "initial if (MAX_PAYLOAD_P > MAXP_BOUND_C) begin\n    " + FAT
                 + '=%0d is above %0d: %0d + it overflows dev_len_o",\n           ' + ARGS + "\n  end")],
    "error": [(FAT, '$error("KL_pp_nvm_port: MAX_PAYLOAD_P')],
    "error-nopath": [(FAT, '$error("KL_pp_nvm_port: MAX_PAYLOAD_P')],
    "warning": [(FAT, '$warning("KL_pp_nvm_port: MAX_PAYLOAD_P')],
    "info": [(FAT, '$info("KL_pp_nvm_port: MAX_PAYLOAD_P')],
    "hdr10": [("HDR_LEN_C  = 16'd8;", "HDR_LEN_C  = 16'd10;")],
    "len17": [("output logic [15:0] dev_len_o,", "output logic [16:0] dev_len_o,")],
    # expected equivalent at the shipped values: the bench pins the spec value
    "eq-literal-cond": [(COND, "if (MAX_PAYLOAD_P > 65527) begin : g_maxp_check")],
    "eq-literal-msg": [(ARGS, "MAX_PAYLOAD_P, 65527, 8);")],
    "eq-fatal0": [(FAT, '$fatal(0, "KL_pp_nvm_port: MAX_PAYLOAD_P')],
}[name]
for old, new in M:
    assert s.count(old) == 1, (name, old)
    s = s.replace(old, new)
f.write_text(s)
print(f"mutant {name}: {len(M)} replacement(s)")
