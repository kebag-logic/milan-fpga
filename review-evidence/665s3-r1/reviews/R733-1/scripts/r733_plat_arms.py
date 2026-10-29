#!/usr/bin/env python3
"""Reviewer run: the split platform's five arms (plat, platboot at one and two interfaces, platrv32, plattrace)
as test_ctrl_firmware.py's suites run them, without the other suites.

usage: r733_plat_arms.py CHECKOUT WORKDIR
"""
import sys
from pathlib import Path

checkout = Path(sys.argv[1]).resolve()
work = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(checkout / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(checkout / "sw/firmware/gtest"))

import ctrl_arms  # noqa: E402
import fw_gtest  # noqa: E402
import plat_arms  # noqa: E402
from ctrl_build import CTRL, Refusal, Tree, stack_pin  # noqa: E402
from ctrl_reuse import cut_reuse  # noqa: E402

print(f"toolchain: {fw_gtest.toolchain()}")
tree = Tree(CTRL, work / "checkout", work / "reuse", fw_gtest.Build(jobs=4))
print(f"tsn-c-stack at {stack_pin()}")
cut_reuse(tree.reuse)
try:
    outcomes = plat_arms.all_arms(tree, True)
except Refusal as exc:
    print(f"REFUSED: {exc}")
    raise SystemExit(2)
failed = ctrl_arms.report(outcomes)
print(f"r733 platform arms: {'FAIL' if failed else 'PASS'}")
raise SystemExit(1 if failed else 0)
