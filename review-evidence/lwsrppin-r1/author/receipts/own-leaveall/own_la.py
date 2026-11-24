#!/usr/bin/env python3
"""Run only srp_arms.own_leaveall_arms from a parent checkout. Usage: own_la.py <parent-root> <out-dir>"""
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
import ctrl_build  # noqa: E402,F401  (puts the harness on the path)
import fw_gtest  # noqa: E402
import srp_arms  # noqa: E402
from ctrl_build import CTRL, Tree  # noqa: E402
from ctrl_reuse import cut_reuse  # noqa: E402

out.mkdir(parents=True, exist_ok=True)
tree = Tree(CTRL, out / "checkout", out / "reuse", fw_gtest.Build(jobs=4))
cut_reuse(tree.reuse)
rc = 0
for o in srp_arms.own_leaveall_arms(tree, (root / "third_party/lwSRP").resolve()):
    print(f"=== ARM {o.arm} rc={o.rc}")
    print(o.log)
    rc |= 1 if o.rc else 0
print(f"own_la: rc={rc}")
sys.exit(rc)
