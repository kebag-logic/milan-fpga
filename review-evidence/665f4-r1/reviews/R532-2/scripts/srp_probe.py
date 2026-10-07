#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer probe driver: build and run one SRP GoogleTest file with the
repository's own arm (srp_arms.arm_srp), against an optional copied/mutated
firmware source tree. Never edits the checkout.

usage: srp_probe.py --repo R --test T.cpp [--src CTRL_COPY] [--lwsrp L]
                    [--interfaces N] [--filter GLOB] --out DIR
"""
import argparse, shutil, sys
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--repo", type=Path, required=True)
ap.add_argument("--test", type=Path, required=True)
ap.add_argument("--src", type=Path)
ap.add_argument("--lwsrp", type=Path)
ap.add_argument("--interfaces", type=int, default=1)
ap.add_argument("--filter", default="*")
ap.add_argument("--debug", action="store_true")
ap.add_argument("--no-pin", action="store_true", help="planted-defect lwSRP copy: skip the pin check")
ap.add_argument("--out", type=Path, required=True)
a = ap.parse_args()
repo = a.repo.resolve()
sys.path.insert(0, str(repo / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(repo / "sw/firmware/gtest"))
import ctrl_build, fw_gtest, srp_arms
out = a.out.resolve(); out.mkdir(parents=True, exist_ok=True)
tests = out / "tests_src"; tests.mkdir(exist_ok=True)
for f in (repo / "sw/firmware/ctrl/test").glob("*.hpp"):
    shutil.copy(f, tests / f.name)
shutil.copy(a.test, tests / a.test.name)
srp_arms.HERE = tests
if a.no_pin:
    srp_arms.lwsrp_pin = lambda path: "planted-copy"
src = (a.src or repo / "sw/firmware/ctrl").resolve()
tree = ctrl_build.Tree(src, out / "build", out / "reuse", fw_gtest.Build(jobs=4))
o = srp_arms.arm_srp(tree, (a.lwsrp or repo / "third_party/lwSRP").resolve(), a.interfaces,
                     debug=a.debug, test=(a.test.name, a.filter))
print(o.log[-6000:])
print(f"PROBE rc={o.rc}")
sys.exit(o.rc)
