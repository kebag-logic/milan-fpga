#!/usr/bin/env python3
"""Plant this round's four new verdict-pin controls into the ROUND-1 gate.

usage: old_gate_controls.py <tree> <new test_builder.py>

<tree>/sw/builder/test_builder.py must be the round-1 builder (597dba85).
The new controls and their helper are copied byte for byte from <new
test_builder.py>, inserted at the same place, and the loop is made to REPORT
an acceptance instead of raising, then to return after the controls. Run with
run_gate1b.py; each control prints ACCEPTED (the round-1 pins kept the slot
and the resolver passed it) or REFUSED with its reason.
"""
import sys
from pathlib import Path

old_path = Path(sys.argv[1]) / "sw/builder/test_builder.py"
old, new = old_path.read_text(), Path(sys.argv[2]).read_text()

helper_start = new.index("    def in_nvm_boot(macro: str, statement: str, what: str) -> str:\n")
helper_end = new.index("    verdict_pin_breaks = (\n")
helper = new[helper_start:helper_end]
controls_start = new.index('        ("a phase-2 line-splice write inside nvm_boot()"')
controls_end = new.index("    )\n    verdict_pin_refused = []\n")
controls = new[controls_start:controls_end]

anchor = "    verdict_pin_breaks = (\n"
assert old.count(anchor) == 1
old = old.replace(anchor, helper + anchor, 1)
close = "    )\n    verdict_pin_refused = []\n"
assert old.count(close) == 1
old = old.replace(close, controls + close, 1)

# Only this round's four controls are measured here.
loop = "        for what, pin, planted, units in verdict_pin_breaks:\n"
assert old.count(loop) == 1
old = old.replace(loop, "        for what, pin, planted, units in verdict_pin_breaks[5:]:\n", 1)
refused = "                verdict_pin_refused.append(what)\n"
assert old.count(refused) == 1
old = old.replace(refused, (
    "                print('ROUND-1 GATE REFUSED', repr(what), '::',\n"
    "                      str(exc)[:600], flush=True)\n") + refused, 1)
accepted = ("                raise AssertionError(\n"
            "                    f\"the resolver accepted {what}: aem_loaded's slot \"\n")
assert old.count(accepted) == 1
old = old.replace(accepted, (
    "                print('ROUND-1 GATE ACCEPTED', repr(what), flush=True)\n"
    "                continue\n") + accepted, 1)
stop = "    #: ... and the store-class mutants measured on the resolver ALONE, so\n"
assert old.count(stop) == 1
old = old.replace(stop, "    return\n" + stop, 1)
old_path.write_text(old)
print("planted the four controls into the round-1 gate at", old_path)
