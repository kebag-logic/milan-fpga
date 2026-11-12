#!/usr/bin/env python3
"""Run chosen SRP / platform firmware arms of a checkout (lane 895 helper).

usage: run_arms.py CHECKOUT OUT SPEC...
  SPEC = srp:<suite>:<if>[:<config stem>] | srpdebug:<if> | platboot:<if> | plat | aecp | shapes
"""
import sys
from pathlib import Path
checkout = Path(sys.argv[1]).resolve(); out = Path(sys.argv[2]).resolve()
test = checkout / "sw/firmware/ctrl/test"
sys.path.insert(0, str(test)); sys.path.insert(0, str(checkout / "sw/firmware/gtest"))
import fw_gtest, srp_arms, ctrl_arms, plat_arms
from ctrl_build import CTRL, Tree, stack_pin
from ctrl_reuse import cut_reuse
tree = Tree(CTRL, out / "checkout", out / "reuse", fw_gtest.Build(jobs=16))
print("tsn-c-stack at", stack_pin()); cut_reuse(tree.reuse)
lwsrp = (checkout / "third_party/lwSRP").resolve()
outcomes = []
for spec in sys.argv[3:]:
    kind, *rest = spec.split(":")
    if kind == "srp":
        suite, n_if, *cfg = rest
        kw = {"test": suite}
        if cfg:
            kw["config"] = checkout / "configs" / f"{cfg[0]}.yaml"
        outcomes.append(srp_arms.arm_srp(tree, lwsrp, int(n_if), **kw))
    elif kind == "srpdebug":
        outcomes.append(srp_arms.arm_srp(tree, lwsrp, int(rest[0]), debug=True))
    elif kind == "platboot":
        outcomes.append(plat_arms.arm_platboot(tree, int(rest[0])))
    elif kind == "plat":
        outcomes.extend(plat_arms.all_arms(tree, True))
    elif kind == "aecp":
        import aecp_arms
        outcomes.extend(aecp_arms.all_arms(tree))
    elif kind == "shapes":
        outcomes.extend(srp_arms.all_shapes(tree, lwsrp, True))
failed = ctrl_arms.report(outcomes)
print("RESULT", "FAIL" if failed else "PASS")
sys.exit(1 if failed else 0)
