#!/usr/bin/env python3
"""run_acmp_arm.py TREE OUT [--arm acmp|acmpif2] - build and run one ACMP arm of a scratch copy's firmware.

TREE is a scratch copy of the reviewed head (never the reviewed clone); its own ctrl_build/ctrl_arms are
imported, so the arm builds TREE's sources and TREE's tests. Prints the arm's rc and its log.
"""
import argparse
import sys
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("tree", type=Path)
ap.add_argument("out", type=Path)
ap.add_argument("--arm", default="acmp")
a = ap.parse_args()
test_dir = a.tree / "sw/firmware/ctrl/test"
sys.path[:0] = [str(test_dir), str(a.tree / "sw/firmware/gtest")]
import ctrl_build  # noqa: E402
import ctrl_arms  # noqa: E402
import fw_gtest  # noqa: E402

assert Path(ctrl_build.CTRL).resolve().is_relative_to(a.tree.resolve()), ctrl_build.CTRL
a.out.mkdir(parents=True, exist_ok=True)
tree = ctrl_build.Tree(ctrl_build.CTRL, a.out / "build", a.out / "reuse", fw_gtest.Build(jobs=4))
fn = getattr(ctrl_arms, f"arm_{a.arm}")
try:
    o = fn(tree)
except ctrl_build.Refusal as exc:
    print(f"REFUSED: {exc}")
    sys.exit(2)
print(o.log)
print(f"arm {o.arm} rc {o.rc}")
sys.exit(o.rc)
