#!/usr/bin/env python3
"""Append a probe .cpp to a disposable copy of the checkout's test_aecp.cpp and run the
named tests through aecp_arms.core_arm at one and two interfaces.
Usage: run_cpp_probe.py CHECKOUT PROBE SCRATCH MODE FILTER"""
import shutil, sys
from pathlib import Path
checkout, probe, scratch = (Path(a).resolve() for a in sys.argv[1:4])
mode, selected = sys.argv[4], sys.argv[5]
tests = scratch / "test"
if tests.exists():
    raise SystemExit(f"{tests} exists")
shutil.copytree(checkout / "sw/firmware/ctrl/test", tests, ignore=shutil.ignore_patterns("__pycache__"))
with open(tests / "test_aecp.cpp", "a") as f:
    f.write(probe.read_text())
sys.path.insert(0, str(checkout / "sw/firmware/ctrl/test"))
import aecp_arms, ctrl_build, fw_gtest  # noqa: E402
aecp_arms.HERE = tests
worst = 0
for n in (1, 2):
    tree = ctrl_build.Tree(checkout / "sw/firmware/ctrl", scratch / f"build{n}", scratch / f"reuse{n}",
                           fw_gtest.Build(jobs=4), ctrl_build.STACK)
    r = aecp_arms.core_arm(tree, checkout / "configs/endstation_ax7101_1x1_tdm8.yaml", n, mode, selected)
    print(f"== mode {mode} interfaces {n}: rc {r.rc}\n{r.log}", flush=True)
    worst = max(worst, r.rc)
raise SystemExit(worst)
