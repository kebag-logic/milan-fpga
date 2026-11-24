#!/usr/bin/env python3
"""Run only the two SRP arm families the merge joined (own-LeaveAll from one side, loop-pass link from the other)
from a milan-fpga checkout, into a scratch output directory, with the gate's own Tree and lwSRP pin check.

Usage: python3 -B run_merged_srp_arms.py <checkout> <out-dir> [jobs]
Exit 0 when all four arms pass.
"""
import sys
from pathlib import Path
co, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
jobs = int(sys.argv[3]) if len(sys.argv) > 3 else 4
sys.path.insert(0, str(co / "sw/firmware/ctrl/test"))
import test_ctrl_firmware  # noqa: F401  (sets the gate's import paths)
import fw_gtest, srp_arms, ctrl_arms
from ctrl_build import CTRL, Tree, stack_pin
lw = co / "third_party/lwSRP"
print("tsn-c-stack at", stack_pin())
print("lwSRP pin check:", ctrl_arms.lwsrp_pin(lw), "==", ctrl_arms.LWSRP_REV)
tree = Tree(CTRL, out / "checkout", out / "reuse", fw_gtest.Build(jobs=jobs))
outs = srp_arms.own_leaveall_arms(tree, lw) + srp_arms.link_pass_arms(tree, lw)
bad = 0
for o in outs:
    tail = [l for l in o.log.splitlines() if "PASSED" in l or "FAILED" in l][-2:] if hasattr(o, "log") else []
    print(("[ok] " if o.rc == 0 else "[FAIL] ") + o.arm, "|", " ; ".join(tail))
    bad += o.rc != 0
print("merged-srp-arms:", "PASS" if not bad else f"FAIL ({bad})", f"{len(outs)} arms")
sys.exit(1 if bad else 0)
