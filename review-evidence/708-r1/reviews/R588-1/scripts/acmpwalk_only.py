#!/usr/bin/env python3
"""Run only the acmpwalk arm of a checkout's test_ctrl_firmware.py.

Usage: python3 -I acmpwalk_only.py <repo checkout> <out dir>
The checkout's own ctrl_build / ctrl_reuse / ctrl_arms are imported, so the
reuse cut proves that checkout's processor gitlink and blobs as the gate does.
Exit 0 when the arm passed, 1 on a finding, 2 on a refusal.
"""
import sys
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(repo / "sw/firmware/ctrl/test"))

import ctrl_arms  # noqa: E402
import fw_gtest  # noqa: E402
from ctrl_build import CTRL, Refusal, Tree, stack_pin  # noqa: E402
from ctrl_reuse import cut_reuse  # noqa: E402

assert CTRL.resolve().is_relative_to(repo), CTRL
fw_gtest.EXECUTION.run = True
print(f"toolchain: {fw_gtest.toolchain()}")
try:
    tree = Tree(CTRL, out / "checkout", out / "reuse", fw_gtest.Build(jobs=4))
    print(f"tsn-c-stack at {stack_pin()}")
    cut_reuse(tree.reuse)
    for inc in sorted((out / "reuse").glob("*.inc")):
        print("reuse:", inc.name, inc.read_text().splitlines()[1])
    failed = ctrl_arms.report([ctrl_arms.arm_acmpwalk(tree)])
except Refusal as exc:
    print(f"REFUSED: {exc}")
    sys.exit(2)
print("acmpwalk_only:", "FAIL" if failed else "PASS")
sys.exit(1 if failed else 0)
