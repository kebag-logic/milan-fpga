#!/usr/bin/env python3
"""Reviewer probe driver: run one SRP suite file from a probe copy at N interfaces."""
import sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
suite, filt, ifs, out = sys.argv[2], sys.argv[3], int(sys.argv[4]), Path(sys.argv[5]).resolve()
sys.path[:0] = [str(root/"sw/firmware/ctrl/test"), str(root/"sw/firmware/gtest")]
import srp_arms, fw_gtest
from ctrl_build import Tree, CTRL
srp_arms.lwsrp_pin = lambda p: "probe"
tree = Tree(CTRL, out/"build", out/"reuse", fw_gtest.Build(jobs=4))
r = srp_arms.arm_srp(tree, root/"third_party/lwSRP", ifs, test=(suite, filt))
print(r.log); print("PROBE_RC", r.rc); sys.exit(0 if r.rc == 0 else 1)
