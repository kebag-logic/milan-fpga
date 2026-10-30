#!/usr/bin/env python3
"""Elaborate the 1x1 shipping shape with --no-media-clock-servo and report the servo hook lines.

Usage: pruned_probe.py <clone> <output-dir>
Reuses the shipping elaboration of sw/builder/test_shipping_clock_constraints.py with one
added flag; its exactly-one-hook assertion is expected to fail on a pruned build at head.
"""
import json, sys, types
from pathlib import Path
clone, out = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(clone / "sw/builder"))
import test_shipping_clock_constraints as t
shim = types.SimpleNamespace(loads=lambda s: (lambda d: (d["argv"].append("--no-media-clock-servo"), d)[1])(json.loads(s)),
                             dumps=json.dumps)
t.json = shim
try:
    t.elaborate_shipping("ax7101_1x1_tdm8", "e1", out)
    print("PRUNED-PROBE: shipping assertions passed (servo hook emitted)")
except AssertionError as exc:
    print(f"PRUNED-PROBE: assertion {exc}")
tcl = (out / "gateware" / "alinx_ax7101.tcl")
tcl = tcl if tcl.exists() else next(out.rglob("alinx_ax7101.tcl"))
lines = [l for l in tcl.read_text().splitlines() if "kl_servo_reset_sync_constraints" in l]
print("PRUNED-PROBE servo hook lines:", lines)
v = next(out.rglob("alinx_ax7101.v")).read_text()
print("PRUNED-PROBE MCSERVO_P in top:", [l.strip() for l in v.splitlines() if "MCSERVO_P" in l][:3])
