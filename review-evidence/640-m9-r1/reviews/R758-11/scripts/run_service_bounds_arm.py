#!/usr/bin/env python3
"""Run the mailbox page's service-bounds arm directly, against a named clone and tsn-c-stack checkout.

Usage: run_service_bounds_arm.py <clone> <stack-checkout> <out-dir>
The script file itself has no entry point; this calls arm_service_bounds as test_ctrl_firmware.py does.
"""
import sys
from pathlib import Path
clone, stack, out = map(Path, sys.argv[1:4])
sys.dont_write_bytecode = True
sys.path[:0] = [str(clone / "sw/firmware/ctrl/test"), str(clone / "sw/firmware/gtest")]
import ctrl_build, ctrl_service_bounds, fw_gtest
tree = ctrl_build.Tree(ctrl_build.CTRL, out / "build", out / "reuse", fw_gtest.Build(jobs=4), stack)
result = ctrl_service_bounds.arm_service_bounds(tree)
print(result.log)
print("arm rc", result.rc)
sys.exit(result.rc)
