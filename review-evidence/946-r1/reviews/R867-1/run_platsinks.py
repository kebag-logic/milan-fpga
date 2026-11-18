#!/usr/bin/env python3
"""Run the #946 sink suite (plat_arms.arm_platsinks) at both of its shapes, and the
`plat` arm, against the checkout given, and print each arm's full log.

Usage: python3 run_platsinks.py <repo checkout> <output dir> [jobs]
Exit 0 when every arm passed.
"""
import sys
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2]).resolve()
jobs = int(sys.argv[3]) if len(sys.argv) > 3 else 4
sys.path.insert(0, str(repo / "sw/firmware/gtest"))
sys.path.insert(0, str(repo / "sw/firmware/ctrl/test"))

import fw_gtest  # noqa: E402
import plat_arms  # noqa: E402
import test_ctrl_firmware as gate  # noqa: E402
from ctrl_build import CTRL, Tree  # noqa: E402

print(f"checkout: {repo}")
print(f"toolchain: {fw_gtest.toolchain()}")
tree = Tree(CTRL, out / "checkout", out / "reuse", fw_gtest.Build(jobs=jobs))
gate.cut_reuse(tree.reuse)
outcomes = [plat_arms.arm_plat(tree)] + plat_arms.sink_arms(tree)
bad = 0
for o in outcomes:
    print(f"===== arm {o.arm} rc={o.rc}")
    print(o.log)
    bad += 0 if o.rc == 0 else 1
print(f"run_platsinks: {len(outcomes) - bad} of {len(outcomes)} arms passed")
sys.exit(1 if bad else 0)
