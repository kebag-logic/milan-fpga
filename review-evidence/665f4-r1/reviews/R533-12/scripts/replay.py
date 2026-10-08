#!/usr/bin/env python3
"""Run original public temporal-feedback acceptance probes."""
import argparse
from pathlib import Path
import shutil
import sys

p = argparse.ArgumentParser()
p.add_argument("--repo", type=Path, required=True)
p.add_argument("--packet", type=Path, required=True)
p.add_argument("--interfaces", type=int, choices=(1, 2), required=True)
p.add_argument("--jobs", type=int, default=3)
a = p.parse_args()
repo, packet = a.repo.resolve(), a.packet.resolve()
sys.dont_write_bytecode = True
sys.path.insert(0, str(repo / "sw/firmware/ctrl/test"))
from ctrl_build import CTRL, Tree
import fw_gtest
import srp_arms

work = packet / "scratch" / f"replay-if{a.interfaces}"
src = work / "ctrl"
shutil.copytree(CTRL, src, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
suite = src / "test/test_acmp_mbx.cpp"
with suite.open("a") as out:
    for probe in sorted((packet / "scripts/prior-probes").glob("*.hpp")):
        shutil.copyfile(probe, src / "test" / probe.name)
        out.write(f'\n#include "{probe.name}"\n')
srp_arms.HERE = src / "test"
tree = Tree(src, work / "build", work / "reuse", fw_gtest.Build(jobs=a.jobs))
result = srp_arms.arm_srp(tree, repo / "third_party/lwSRP", a.interfaces,
                        test=("test_acmp_mbx.cpp", "R533Feedback.*:R11Feedback.*"))
print(result.log)
raise SystemExit(result.rc)
