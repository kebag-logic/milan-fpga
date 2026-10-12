#!/usr/bin/env python3
"""Run only the pub-acmp-* plants of a tree's ctrl_mutants table, plus no-op controls.

usage: pub_acmp_plants.py <tree root> <work dir> [--controls]
Imports the tree's own sw/firmware/ctrl/test modules (reviewed source, not modified),
narrows ctrl_mutants.MUTANTS to the names starting 'pub-acmp-', prints each plant's
path and the fixture's occurrence count in the file the campaign plants, then runs the
tree's own campaign() over exactly those. With --controls it adds, for each plant, a
no-op twin (new == old) that must ESCAPE, so a catch cannot come from the harness alone.
"""
import dataclasses
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
work = Path(sys.argv[2]).resolve()
controls = "--controls" in sys.argv
sys.path[:0] = [str(root / "sw/firmware/ctrl/test"), str(root / "sw/firmware/gtest")]
import ctrl_mutants  # noqa: E402
import ctrl_build  # noqa: E402

pub = tuple(m for m in ctrl_mutants.MUTANTS if m.name.startswith("pub-acmp-"))
print(f"tree {root}: {len(pub)} pub-acmp plants")
for m in pub:
    stack = getattr(ctrl_build, "STACK_PREFIX", None)
    if stack and m.path.startswith(stack):
        target = ctrl_build.STACK / m.path.removeprefix(stack)
    else:
        target = ctrl_build.CTRL / m.path
    print(f"  {m.name}: {m.path} -> {target.relative_to(root)} fixture x{target.read_text().count(m.old)}")
table = pub
if controls:
    table = tuple(x for m in pub for x in (m, dataclasses.replace(m, name="CONTROL-noop-" + m.name, new=m.old)))
ctrl_mutants.MUTANTS = table
work.mkdir(parents=True, exist_ok=True)
escaped = ctrl_mutants.campaign(work, work / "reuse", 4)
print(f"campaign returned escaped={escaped}")
