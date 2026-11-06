#!/usr/bin/env python3
"""Build one SRP suite of a checkout's firmware tree and run its selected tests (#665), through the campaign's own
arm_srp, so a test can be iterated without the whole firmware gate.

usage: srp_one.py CHECKOUT OUT SUITE.cpp FILTER INTERFACES [debug]
"""
import sys
from pathlib import Path

checkout, out, suite, selected, interfaces = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], sys.argv[4], \
    int(sys.argv[5])
debug = len(sys.argv) > 6 and sys.argv[6] == "debug"
sys.path.insert(0, str(checkout / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(checkout / "sw/firmware/gtest"))
import fw_gtest  # noqa: E402
from ctrl_build import CTRL, Tree  # noqa: E402
from srp_arms import arm_srp  # noqa: E402

tree = Tree(CTRL, out / "build", out / "reuse", fw_gtest.Build(jobs=4))
(out / "build").mkdir(parents=True, exist_ok=True)
(out / "reuse").mkdir(parents=True, exist_ok=True)
result = arm_srp(tree, checkout / "third_party/lwSRP", interfaces, debug=debug, test=(suite, selected))
print(result.log)
print(f"rc={result.rc}")
