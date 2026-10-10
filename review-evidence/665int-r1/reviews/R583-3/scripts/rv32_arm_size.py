#!/usr/bin/env python3
"""rv32_arm_size.py - run the firmware gate's own rv32 arm (the portable
control set plus the MMIO platform, freestanding RV32I with the pinned SDK)
over a ctrl source tree and print its size line.
Usage: MILAN_RV32_CC=<sdk gcc> python3 -B rv32_arm_size.py <gate-tree> <ctrl-dir> <out-dir>
<gate-tree> supplies the gate's scripts; <ctrl-dir> is the ctrl source measured."""
import sys
from pathlib import Path
gate, ctrl, out = (Path(a).resolve() for a in sys.argv[1:4])
sys.path.insert(0, str(gate / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(gate / "sw/firmware/gtest"))
import ctrl_arms, fw_gtest  # noqa: E402
from ctrl_build import Tree  # noqa: E402
tree = Tree(ctrl, out / "checkout", out / "reuse", fw_gtest.Build(jobs=4))
o = ctrl_arms.arm_rv32(tree, True)
print(f"{ctrl}: rc {o.rc}\n{o.log}")
