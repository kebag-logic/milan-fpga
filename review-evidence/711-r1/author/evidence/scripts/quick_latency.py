"""Run only the srp_latency arm at one and two interfaces from a checkout (scratch driver)."""
import sys
from pathlib import Path
checkout = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2]).resolve()
lwsrp = Path(sys.argv[3]).resolve()
sys.path.insert(0, str(checkout / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(checkout / "sw/firmware/gtest"))
import ctrl_arms, srp_arms, fw_gtest
from ctrl_build import CTRL, Tree
tree = Tree(CTRL, out / "checkout", out / "reuse", fw_gtest.Build(jobs=2))
outcomes = [srp_arms.arm_srp(tree, lwsrp, i, test="srp_latency.cpp") for i in (1, 2)]
failed = ctrl_arms.report(outcomes)
print("quick srp_latency:", "FAIL" if failed else "PASS")
sys.exit(1 if failed else 0)
