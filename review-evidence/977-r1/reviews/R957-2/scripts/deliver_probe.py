#!/usr/bin/env python3
"""Disposable mutation probe of ctrl_app_srp.c deliver(): build test_acmp_mbx.cpp's SrpBinding suite on a copy of
sw/firmware/ctrl with one textual mutation and report the gtest verdict.
Usage: deliver_probe.py <repo> <workdir> <name> <shape 1x1|8x8> [<old> <new>]   (no old/new: the unmutated control)"""
import shutil, sys
from pathlib import Path
repo, work, name, shape = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], sys.argv[4]
sys.path.insert(0, str(repo / "sw/firmware/ctrl/test")); sys.path.insert(0, str(repo / "sw/firmware/gtest"))
import ctrl_build, fw_gtest, srp_arms
src = work / name / "ctrl"
if src.exists():
    shutil.rmtree(src)
shutil.copytree(repo / "sw/firmware/ctrl", src, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
if len(sys.argv) > 6:
    old, new = sys.argv[5].encode().decode("unicode_escape"), sys.argv[6].encode().decode("unicode_escape")
    f = src / "app/ctrl_app_srp.c"
    text = f.read_text()
    assert text.count(old) == 1, f"mutation anchor found {text.count(old)} times"
    f.write_text(text.replace(old, new))
tree = ctrl_build.Tree(src, work / name / "out", work / name / "reuse", fw_gtest.Build(jobs=4))
config = srp_arms.ENTITY_8X8 if shape == "8x8" else srp_arms.DEFAULT_ENTITY
o = srp_arms.arm_srp(tree, repo / "third_party/lwSRP", 1, test=("test_acmp_mbx.cpp", "SrpBinding.*"), config=config)
fails = [l for l in o.log.splitlines() if l.startswith("[  FAILED  ]") or "Failure" in l]
passed = [l for l in o.log.splitlines() if l.startswith("[  PASSED  ]")]
print(f"probe={name} shape={shape} rc={o.rc} passed={passed[-1] if passed else '-'}")
for l in fails[:12]:
    print("  ", l)
(work / name / f"{shape}.log").write_text(o.log)
sys.exit(0)
