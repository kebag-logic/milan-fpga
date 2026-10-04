#!/usr/bin/env python3
"""Rebuild the lockstep reference RTL (ref/) from the base processor's hdl/srp.

The reference model is base c4cb84ff's eight SRP modules with every module
name renamed `<name>_ref` wherever it appears (declarations, instances,
comments), so both models elaborate in one Verilator build.
usage: make_ref.py <base hdl/srp> <out dir>   (base = `git archive c4cb84ff`)
"""
import re
import sys
from pathlib import Path

MODULES = ("admission", "decoder", "domain", "encoder", "listener_fsm", "talker_fsm", "top", "vlan")
NAME = re.compile(r"\b(KL_srp_(?:" + "|".join(MODULES) + r"))\b")

src, out = Path(sys.argv[1]), Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
for m in MODULES:
    text = (src / f"KL_srp_{m}.sv").read_text()
    (out / f"KL_srp_{m}_ref.sv").write_text(NAME.sub(r"\1_ref", text))
    print(f"KL_srp_{m}_ref.sv")
