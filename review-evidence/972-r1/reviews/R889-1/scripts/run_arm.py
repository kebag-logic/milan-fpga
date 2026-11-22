#!/usr/bin/env python3
"""run_arm.py ROOT OUT ARM - build and run one arm of the control firmware's host gate (platboot1 or adp) on the
repository copy at ROOT, its builds under OUT; print the arm's log and exit with its rc. A reviewer's focused
driver: it imports the tree's own ctrl_build/plat_arms, so what runs is the tree's own build and grade."""
import sys
from pathlib import Path

root, out, arm = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3]
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
import ctrl_build  # noqa: E402
import fw_gtest  # noqa: E402

tree = ctrl_build.Tree(ctrl_build.CTRL, out / "checkout", out / "reuse", fw_gtest.Build(jobs=4))
if arm == "platboot1":
    import plat_arms
    o = plat_arms.arm_platboot(tree, 1)
elif arm == "platboot2":
    import plat_arms
    o = plat_arms.arm_platboot(tree, 2)
else:
    import ctrl_arms
    o = getattr(ctrl_arms, "arm_" + arm)(tree)
print(o.log)
print(f"ARM {arm} rc={o.rc}")
sys.exit(o.rc)
