#!/usr/bin/env python3
"""talker_arms.py TREE OUT: run TREE's SRP Talker arms (srp_arms.talker_arms: srp_talker.cpp at 1x1/1if and 8x8/2if,
SrpGate at 8x8/2if) and SRP+ACMP at two interfaces, building under OUT; exit 1 when any arm failed."""
import sys
from pathlib import Path

tree_root, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(tree_root / 'sw/firmware/ctrl/test'))
sys.path.insert(0, str(tree_root / 'sw/firmware/gtest'))
import ctrl_arms  # noqa: E402
import srp_arms  # noqa: E402
import fw_gtest  # noqa: E402
from ctrl_build import CTRL, Tree  # noqa: E402
from ctrl_reuse import cut_reuse  # noqa: E402

lwsrp = (tree_root / 'third_party/lwSRP').resolve()
out.mkdir(parents=True, exist_ok=True)
tree = Tree(CTRL, out / 'build', out / 'reuse', fw_gtest.Build(jobs=8))
cut_reuse(tree.reuse)
outcomes = list(srp_arms.talker_arms(tree, lwsrp))
if len(sys.argv) < 4 or sys.argv[3] != 'talker-only':
    outcomes.append(srp_arms.arm_srp(tree, lwsrp, 2, test='test_acmp_mbx.cpp'))
failed = ctrl_arms.report(outcomes)
print(f"talker arms: {'FAIL' if failed else 'PASS'}")
sys.exit(1 if failed else 0)
