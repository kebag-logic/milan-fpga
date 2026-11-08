#!/usr/bin/env python3
"""List the firmware boundary gate's builders found by text that are programs, and how ctrl_configs classifies
each of the leg's (tb/verilator/milan_dp) programs.

usage: probe_classified.py CHECKOUT_ROOT
"""
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
import ctrl_configs as cc  # noqa: E402

known = {cc.rel(Path(b.path)) if hasattr(b, "path") else str(b) for b in cc.BUILDERS}
classes = {"PART_OF": getattr(cc, "PART_OF", {}), "OUTSIDE": cc.OUTSIDE, "SUITES": cc.SUITES}
for path, text in cc.checkout_builders():
    name = cc.rel(path)
    if not name.startswith("tb/verilator/milan_dp/"):
        continue
    where = [k for k, v in classes.items() if name in v]
    print(f"{name}: program={cc.program(path, text)} classified={where or 'BUILDERS?' if name in str(known) else where}")
