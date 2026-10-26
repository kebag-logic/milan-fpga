#!/usr/bin/env python3
"""Run a reviewer's test-editing probe, unmodified, on a disposable copy of the
firmware's test directory, then the tests it names at one and two interfaces.

Usage: run_probe.py CHECKOUT PROBE SCRATCH MODE FILTER
The probe takes SCRATCH as its tree and edits SCRATCH/sw/firmware/ctrl/test/test_aecp.cpp
only; the build reads the checkout's firmware and writes under SCRATCH. MODE is aecp_arms'
"mailbox" or "app" arm. Round 4's run_response_probe.py with the arm and filter as arguments.
"""
import shutil
import subprocess
import sys
from pathlib import Path

checkout, probe, scratch = (Path(a).resolve() for a in sys.argv[1:4])
mode, selected = sys.argv[4], sys.argv[5]
tests = scratch / "sw/firmware/ctrl/test"
if tests.exists():
    raise SystemExit(f"{tests} exists: use a fresh scratch directory")
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
    result = aecp_arms.core_arm(tree, checkout / "configs/endstation_ax7101_1x1_tdm8.yaml", interfaces, mode, selected)
    print(f"== interfaces {interfaces}: rc {result.rc}")
    print(result.log)
    worst = max(worst, result.rc)
raise SystemExit(worst)
