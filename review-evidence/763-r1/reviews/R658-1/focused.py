#!/usr/bin/env python3
"""Reproduce focused checks using an exact checkout and disposable output."""
import argparse
import json
import os
from pathlib import Path
import shutil
import sys

p = argparse.ArgumentParser()
p.add_argument("repo", type=Path)
p.add_argument("packet", type=Path)
p.add_argument("mode", choices=("clean", "owner", "store", "shapes"))
a = p.parse_args()
repo, packet = a.repo.resolve(), a.packet.resolve()
sys.path.insert(0, str(repo / "sw/firmware/ctrl/test"))
import aecp_arms
import aecp_mutants
from ctrl_build import CTRL, STACK, Tree, stack_pin
import fw_gtest

work = packet / "scratch" / a.mode
work.mkdir(parents=True, exist_ok=True)
os.environ["TMPDIR"] = str(packet / "scratch")
print("stack pin", stack_pin(STACK), flush=True)
aecp_mutants.controls()
src = CTRL
d = None
if a.mode in ("owner", "store"):
    src = work / "ctrl"
    for name in ("ctrl", "ctrl_nvm"):
        shutil.copytree(CTRL.parent / name, work / name, dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    name = "nvm-empty-map-keeps-defaults" if a.mode == "owner" else "nvm-unused-payload-reads-erased"
    d = next(d for d in aecp_mutants.DEFECTS if d.name == name)
    target = src / d.path
    original = target.read_text()
    assert original.count(d.old) == 1
    target.write_text(original.replace(d.old, d.new))
tree = Tree(src, work / "build", work / "reuse", fw_gtest.Build(jobs=4), STACK)
shipping = repo / "configs/endstation_ax7101_1x1_tdm8.yaml"
new = "Nvm.EmptyAndNonDefaultMapsSurviveTheRealStorePowerCycle"
results = []
try:
    if a.mode == "shapes":
        tree = Tree(src, work / "build", work / "reuse",
                    fw_gtest.Build(jobs=4, address_sanitizer=True), STACK)
        cases = [(f.stem, f, 1, "nvm", "Nvm.*", False)
                 for f in sorted((repo / "configs").glob("endstation_*.yaml"))]
    elif d:
        cases = [("named", shipping, 2, "app", ":".join(t for t, _ in d.checks), True),
                 ("without-new", shipping, 2, "app", "*-" + new, a.mode == "owner")]
    else:
        cases = [(f"app-if{i}", shipping, i, "app", "*", False) for i in (1, 2)]
    for label, config, interfaces, mode, selected, expect_fail in cases:
        result = aecp_arms.core_arm(tree, config, interfaces, mode, selected)
        name = f"{a.mode}-{label}"
        (packet / (name + ".log")).write_text(result.log)
        (packet / (name + ".rc")).write_text(str(result.rc) + "\n")
        caught = {t: aecp_mutants.caught(t, words, result) for t, words in d.checks} if d and label == "named" else {}
        ok = result.rc == (1 if expect_fail else 0) and all(caught.values())
        print(name, "rc", result.rc, "expected", int(expect_fail), "caught", caught, "OK", ok, flush=True)
        results.append({"name": name, "rc": result.rc, "expected_failure": expect_fail,
                        "named_checks": caught, "ok": ok})
finally:
    if d:
        target.write_text(original)
(packet / (a.mode + "-results.json")).write_text(json.dumps(results, indent=2) + "\n")
raise SystemExit(int(any(not r["ok"] for r in results)))
