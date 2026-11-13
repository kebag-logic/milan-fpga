#!/usr/bin/env python3
"""Reviewer probe runner: one SRP gtest arm of a disposable tree copy, at 1 and 2 interfaces.

usage: run_srp_probe.py PROBE_TREE ORIGINAL_CLONE OUT_DIR FILTER
The probe tree's firmware is built; the original clone supplies the pinned lwSRP and
tsn-c-stack checkouts, read only.
"""
import sys
from pathlib import Path

probe, orig, out, flt = (Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(),
                         Path(sys.argv[3]).resolve(), sys.argv[4])
sys.path.insert(0, str(probe / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(probe / "sw/firmware/gtest"))
import fw_gtest  # noqa: E402
import srp_arms  # noqa: E402
from ctrl_build import Tree, CTRL  # noqa: E402

rc = 0
for n_if in (1, 2):
    tree = Tree(CTRL, out / f"if{n_if}", out / f"reuse{n_if}", fw_gtest.Build(jobs=4),
                stack=orig / "third_party/tsn-c-stack")
    o = srp_arms.arm_srp(tree, orig / "third_party/lwSRP", n_if, test=("srp_mbx.cpp", flt))
    print(f"== arm {o.arm} rc={o.rc}")
    print("\n".join(line for line in o.log.splitlines()
                    if "PROBE" in line or "FAILED" in line or "Failure" in line or "PASSED" in line
                    or "Expected" in line or "Which is" in line or "revokes" in line or "boundary" in line
                    or "Value of" in line or "Actual" in line))
    rc |= o.rc
sys.exit(rc)
