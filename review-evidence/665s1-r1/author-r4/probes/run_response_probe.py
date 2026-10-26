#!/usr/bin/env python3
"""Run R701-3's response_probe.py, unmodified, on a disposable copy of the
firmware's test directory, then the test it edits at one and two interfaces.

Usage: run_response_probe.py CHECKOUT PROBE SCRATCH
The probe edits SCRATCH/sw/firmware/ctrl/test/test_aecp.cpp only; the build
reads the checkout's firmware and writes under SCRATCH (as probe_ack.py does).
"""
import shutil
import subprocess
import sys
from pathlib import Path

checkout, probe, scratch = (Path(a).resolve() for a in sys.argv[1:4])
tests = scratch / "sw/firmware/ctrl/test"
if tests.exists():
    shutil.rmtree(tests)
shutil.copytree(checkout / "sw/firmware/ctrl/test", tests, ignore=shutil.ignore_patterns("__pycache__"))
applied = subprocess.run([sys.executable, "-I", str(probe), str(scratch)], check=False)
print("probe applied, rc", applied.returncode, flush=True)
if applied.returncode:
    raise SystemExit(applied.returncode)
sys.path.insert(0, str(checkout / "sw/firmware/ctrl/test"))
import aecp_arms  # noqa: E402
import ctrl_build  # noqa: E402
import fw_gtest  # noqa: E402
aecp_arms.HERE = tests
worst = 0
for interfaces in (1, 2):
    tree = ctrl_build.Tree(checkout / "sw/firmware/ctrl", scratch / f"build{interfaces}", scratch / f"reuse{interfaces}",
                           fw_gtest.Build(jobs=8))
    result = aecp_arms.core_arm(tree, checkout / "configs/endstation_ax7101_1x1_tdm8.yaml", interfaces, "mailbox",
                                "Face.ALateCommitIsOwedAndPublishedAgainWhole")
    print(f"== interfaces {interfaces}: rc {result.rc}")
    print(result.log)
    worst = max(worst, result.rc)
raise SystemExit(worst)
