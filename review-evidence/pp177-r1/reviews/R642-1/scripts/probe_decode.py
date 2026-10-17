#!/usr/bin/env python3
"""Reviewer probe edits on the exact-head tb/aecp_cmds decode controls.

usage: probe_decode.py <clone> <output> <verilator>
Runs check_variant from the clone's tb/aecp_cmds/mutants.py for each probe
edit; a probe is detected when the recorded-sweep gate fails with a FAIL line
naming GET_AVB_INFO. Results are recorded, never raised.
"""
import importlib.util
import json
import sys
from pathlib import Path

clone, output, verilator = sys.argv[1:4]
spec = importlib.util.spec_from_file_location("ctl", Path(clone) / "tb/aecp_cmds/mutants.py")
ctl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ctl)
ENGINE = "hdl/aecp/KL_aecp_engine.sv"
GATE = "else if (cfg_ix_r != DT_AVB_INTERFACE_C) begin\n                upc_r  <= UPC_NOTIMPL_C;"
FLOOR = "if (cmd_r.cdl < 11'd16)                 upc_r <= UPC_BADARG_C;\n" \
        "              else if (cfg_ix_r != DT_AVB_INTERFACE_C) begin"
PROBES = [
    ("p-floor-15", FLOOR, FLOOR.replace("11'd16", "11'd15")),
    ("p-gate-ignores-bit12", GATE,
     GATE.replace("(cfg_ix_r != ", "((cfg_ix_r & 16'hEFFF) != ")),
    ("p-gate-on-desc-ty", GATE, GATE.replace("(cfg_ix_r != ", "(desc_ty_r != ")),
]
out = Path(output).resolve()
out.mkdir(parents=True, exist_ok=True)
records = []
for name, old, new in [("golden", None, None)] + PROBES:
    edit = None if old is None else (ENGINE, old, new, 1)
    expected = "" if old is None else "GET_AVB_INFO"
    result = ctl.check_variant((name, edit, expected, out, verilator))
    result["verdict"] = ("PASS" if result["passed"] else "FAIL") if old is None else \
        ("DETECTED" if result["passed"] else "SURVIVED")
    print(json.dumps(result), flush=True)
    records.append(result)
(out / "results.json").write_text(json.dumps(records, indent=2) + "\n")
