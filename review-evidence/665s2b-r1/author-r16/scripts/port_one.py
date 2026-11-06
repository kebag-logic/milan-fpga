#!/usr/bin/env python3
"""Build and run the firmware's port arm (test_port_loop.cpp, the loop's tests) of a checkout (#665), through the
gate's own arm_port, so the loop's tests can be iterated without the whole firmware gate.

usage: port_one.py CHECKOUT OUT
"""
import sys
from pathlib import Path

checkout, out = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(checkout / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(checkout / "sw/firmware/gtest"))
import fw_gtest  # noqa: E402
from ctrl_build import CTRL, Tree  # noqa: E402
from ctrl_arms import arm_port  # noqa: E402

(out / "build").mkdir(parents=True, exist_ok=True)
(out / "reuse").mkdir(parents=True, exist_ok=True)
result = arm_port(Tree(CTRL, out / "build", out / "reuse", fw_gtest.Build(jobs=4)))
print(result.log)
print(f"rc={result.rc}")
