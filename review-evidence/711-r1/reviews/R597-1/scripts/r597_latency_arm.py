#!/usr/bin/env python3
"""Run only the srp_latency arm at one and two interfaces from a given checkout.

Usage: python3 -B r597_latency_arm.py <checkout> <build dir> <lwSRP checkout>
Exit 0 when both interface counts pass, 1 otherwise, 2 on refusal.
"""
import sys
from pathlib import Path
checkout, out, lwsrp = (Path(a).resolve() for a in sys.argv[1:4])
sys.path[:0] = [str(checkout / "sw/firmware/ctrl/test"), str(checkout / "sw/firmware/gtest")]
import ctrl_arms, srp_arms, fw_gtest
from ctrl_build import CTRL, Refusal, Tree
assert str(CTRL).startswith(str(checkout)), CTRL
tree = Tree(CTRL, out / "checkout", out / "reuse", fw_gtest.Build(jobs=2))
try:
    outcomes = [srp_arms.arm_srp(tree, lwsrp, i, test="srp_latency.cpp") for i in (1, 2)]
except Refusal as exc:
    print("REFUSED:", exc); sys.exit(2)
failed = ctrl_arms.report(outcomes)
for o in outcomes:
    print(f"ARM {o.arm} rc={o.rc}")
print("r597 srp_latency:", "FAIL" if failed else "PASS")
sys.exit(1 if failed else 0)
