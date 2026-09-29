#!/usr/bin/env python3
"""Reviewer probe mutants, applied to a SCRATCH tree only (exact-text replace, must hit once).

pm-flag-survives-reset : the published configuration-valid flop ignores rst_n
pm-scfg-no-range-check : SET_CONFIGURATION's range check becomes a NOP (a refused index is stored)
usage: probe_mutants.py <scratch tree root> <mutant>
"""
import sys
from pathlib import Path

MUTANTS = {
    "pm-flag-survives-reset": ("hdl/aecp/KL_aecp_engine.sv",
        "    if (!rst_n) begin\n      dyn_cfg_v_r <= 1'b0;\n    end else if",
        "    if (1'b0) begin\n      dyn_cfg_v_r <= 1'b0;\n    end else if"),
    "pm-scfg-no-range-check": ("hdl/aecp/ucode/gen_ucode.py",
        "    u('CHECK_ARG', ra=12, rb=9, fmt=FMT_W,\n      cnd=REL_LT, imm=E_SCFGBAD),\n",
        "    u('NOP'),\n"),
}

root, name = Path(sys.argv[1]), sys.argv[2]
rel, old, new = MUTANTS[name]
f = root / rel
t = f.read_text()
assert t.count(old) == 1, f"{name}: anchor count {t.count(old)}"
f.write_text(t.replace(old, new))
print(f"{name} planted in {rel}")
