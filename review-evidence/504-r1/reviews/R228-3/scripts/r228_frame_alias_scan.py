# SPDX-License-Identifier: MIT
"""R228-3: exec'd inside gate 1b (see r228_gate_run.py, R228_PROBE_FILE).

Compiles the PRISTINE firmware with the gate's own census_take() and, per
function, compares every sp-relative store with the s0-relative slots the
same function models (s0 = sp + frame size set by the prologue). Reports
any sp-keyed store whose footprint overlaps an s0-keyed slot, i.e. the
aliasing the frame model does not invalidate across frame registers.
"""
import json
import os
import re
from pathlib import Path

taken = census_take(firmware_source, "pristine alias scan")          # noqa: F821
functions = rv32_functions(taken["text"])                              # noqa: F821
report = {"arch": taken["arch"], "functions": 0, "overlaps": [], "sp_stores": 0}
mem = re.compile(r"^(-?\d+)\((sp|s0)\)$")
for name, body in functions.items():
    frame, s0_slots, sp_stores = None, set(), []
    for _label, mnem, ops in body:
        if mnem is None:
            continue
        args = [a.strip() for a in ops.split(",")]
        if mnem == "addi" and args[:2] == ["sp", "sp"] and frame is None:
            frame = -int(args[2])
        if mnem == "addi" and args[:2] == ["s0", "sp"]:
            frame = int(args[2])
        width = rv32_store_bytes(mnem)                                 # noqa: F821
        if args and mem.match(args[-1]):
            off, reg = int(mem.match(args[-1]).group(1)), mem.match(args[-1]).group(2)
            size = width or 4
            if reg == "s0":
                s0_slots.add((off, size))
            elif width is not None:
                sp_stores.append((off, size, f"{mnem} {ops}"))
    report["functions"] += 1
    report["sp_stores"] += len(sp_stores)
    if frame is None:
        continue
    for off, size, text in sp_stores:
        lo = off - frame
        for s_off, s_size in s0_slots:
            if lo <= s_off + s_size - 1 and s_off <= lo + size - 1:
                report["overlaps"].append({"function": name, "sp_store": text,
                                           "as_s0": lo, "s0_slot": s_off})
Path(os.environ["R228_PROBE_OUT"]).write_text(json.dumps(report, indent=1) + "\n")
print(f"R228 PROBE alias scan: {report['functions']} functions, "
      f"{report['sp_stores']} sp-relative stores, {len(report['overlaps'])} overlap an s0 slot")
