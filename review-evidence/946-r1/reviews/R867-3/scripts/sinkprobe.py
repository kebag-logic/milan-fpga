#!/usr/bin/env python3
"""Reviewer probe for #946 round 3: run the sink suite (test_plat_sinks.cpp) at both shapes on a firmware tree,
optionally with ctrl_plat.c (or any firmware file) replaced, or with text substitutions planted.

usage: sinkprobe.py REPO OUT [--file REL=SRC]... [--sub REL::OLD::NEW]... [--shapes 8|all]
REPO is a checkout at the head under review; nothing in it is modified (a copy of sw/firmware/ctrl is planted)."""
import argparse, shutil, sys
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("repo", type=Path)
ap.add_argument("out", type=Path)
ap.add_argument("--file", action="append", default=[])
ap.add_argument("--sub", action="append", default=[])
ap.add_argument("--shapes", default="all")
ap.add_argument("--jobs", type=int, default=4)
a = ap.parse_args()
test = a.repo / "sw/firmware/ctrl/test"
sys.path.insert(0, str(test))
sys.path.insert(0, str(a.repo / "sw/firmware/gtest"))
import fw_gtest, plat_arms, ctrl_arms  # noqa: E402
import os
if os.environ.get("SINKPROBE_NO_PIN"):
    ctrl_arms.lwsrp_pin = lambda path: None  # a copied tree carries no submodule metadata
from ctrl_build import CTRL, STACK, Tree, Refusal, Outcome  # noqa: E402

src = CTRL
if a.file or a.sub:
    work = a.out / "work"
    if work.exists():
        shutil.rmtree(work)
    shutil.copytree(CTRL, work / "ctrl", ignore=shutil.ignore_patterns("__pycache__"))
    src = work / "ctrl"
    for f in a.file:
        rel, s = f.split("=", 1)
        shutil.copyfile(s, src / rel)
    for s in a.sub:
        rel, old, new = s.split("::", 2)
        old = old.encode().decode("unicode_escape"); new = new.encode().decode("unicode_escape")
        t = (src / rel).read_text()
        if t.count(old) != 1:
            sys.exit(f"substitution fixture occurs {t.count(old)} times in {rel}")
        (src / rel).write_text(t.replace(old, new))
tree = Tree(src, a.out / "build", a.out / "reuse", fw_gtest.Build(jobs=a.jobs), STACK)
shapes = plat_arms.SINK_SHAPES if a.shapes == "all" else plat_arms.SINK_SHAPES[:1]
rc = 0
for cfg, n in shapes:
    try:
        o = plat_arms.arm_platsinks(tree, cfg, n)
    except Refusal as exc:
        o = Outcome("platsinks", 2, f"refused: {exc}")
    print(f"=== {cfg.stem}: rc={o.rc}")
    print(o.log)
    rc = max(rc, o.rc)
sys.exit(rc)
