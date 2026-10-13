#!/usr/bin/env python3
"""Run only the firmware gate's service-bounds arm (reviewer probe).

Usage: python3 run_service_bounds_arm.py <repo> <work-dir>
Prints the arm's verdict and log; exit status is the arm's rc.
"""
import sys
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
work = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(repo / "sw/firmware/gtest"))
sys.path.insert(0, str(repo / "sw/firmware/ctrl/test"))
import fw_gtest  # noqa: E402
from ctrl_build import Tree  # noqa: E402
from ctrl_service_bounds import arm_service_bounds  # noqa: E402

work.mkdir(parents=True, exist_ok=True)
tree = Tree(repo / "sw/firmware/ctrl", work / "build", work / "reuse", fw_gtest.Build(jobs=4))
outcome = arm_service_bounds(tree)
print(outcome.log)
print(f"arm={outcome.arm} rc={outcome.rc}")
sys.exit(outcome.rc)
