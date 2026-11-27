#!/usr/bin/env python3
"""Reviewer probe driver: build and run srp_mbx.cpp (with an appended probe test) in a disposable tree copy.

usage: run_probe.py <probe-tree> <pinned lwSRP checkout> <out dir> <config yaml relative to the tree> <gtest filter>
"""
import sys
from pathlib import Path

tree_root, lwsrp, out, config, selected = (Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]),
                                           sys.argv[4], sys.argv[5])
sys.path.insert(0, str(tree_root / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(tree_root / "sw/firmware/gtest"))
import fw_gtest  # noqa: E402
from ctrl_build import Tree  # noqa: E402
import srp_arms  # noqa: E402

out.mkdir(parents=True, exist_ok=True)
tree = Tree(src=tree_root / "sw/firmware/ctrl", out=out, reuse=out / "reuse", build=fw_gtest.Build(jobs=4))
result = srp_arms.arm_srp(tree, lwsrp, 1, test=("srp_mbx.cpp", selected), config=tree_root / config)
print(result.log)
print(f"ARM {result.arm} rc={result.rc}")
sys.exit(result.rc)
