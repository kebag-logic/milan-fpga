#!/usr/bin/env python3
"""Run the firmware-unit service-bounds arm alone against a checkout.

Usage: run_service_bounds.py <checkout> <scratch-out>
"""
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(root / "sw/firmware/gtest"))
import ctrl_build  # noqa: E402
import ctrl_service_bounds  # noqa: E402

out.mkdir(parents=True, exist_ok=True)
tree = ctrl_build.Tree(src=root / "sw/firmware/ctrl", out=out, reuse=out / "reuse")
try:
    outcome = ctrl_service_bounds.arm_service_bounds(tree)
except ctrl_build.Refusal as exc:
    print("REFUSAL:", exc)
    sys.exit(2)
print(outcome.log)
sys.exit(outcome.rc)
