#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Reviewer probe: build and run only the parent's ADP and walk arms (sw/firmware/ctrl/test ctrl_arms.arm_adp,
arm_walk) on one stack variant. Usage: parent_adp_probe.py PARENT_ROOT VARIANT_NAME STACK_DIR OUT_DIR ARMS
STACK_DIR holds the variant's src/, include/ and tests/ (the stack's tests are taken from it too)."""
import sys, json
from pathlib import Path
root, name, stack, out, arms = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3]), Path(sys.argv[4]), sys.argv[5].split(",")
sys.path.insert(0, str(root / "sw/firmware/ctrl/test")); sys.path.insert(0, str(root / "sw/firmware/gtest"))
import ctrl_build, ctrl_arms, fw_gtest
ctrl_build.STACK = stack; ctrl_build.STACK_TESTS = stack / "tests"
from ctrl_reuse import cut_reuse
out.mkdir(parents=True, exist_ok=True)
tree = ctrl_build.Tree(ctrl_build.CTRL, out / "checkout", out / "reuse", fw_gtest.Build(jobs=4), stack)
cut_reuse(tree.reuse)
res = {"variant": name}
for arm in arms:
    try:
        o = {"adp": ctrl_arms.arm_adp, "walk": ctrl_arms.arm_walk}[arm](tree)
        (out / f"{arm}.log").write_text(o.log)
        lines = o.log.splitlines()
        res[arm] = {"rc": o.rc, "g_lines": [l.strip() for l in lines if l.strip().startswith(("G1", "G2", "G3", "G4", "G5"))],
                    "fail_lines": [l.strip()[:220] for l in lines if "[FAIL" in l or "FAILED" in l][:40]}
    except ctrl_build.Refusal as exc:
        res[arm] = {"refused": str(exc)[:2000]}
print(json.dumps(res, indent=1))
