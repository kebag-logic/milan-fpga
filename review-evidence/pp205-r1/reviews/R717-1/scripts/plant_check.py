#!/usr/bin/env python3
"""Static check: every ACMP mutant arm of the reviewed head still plants (each old text
occurs exactly once) in a copy of that head. No build, no run.

Usage: python3 plant_check.py TREE
"""
import sys
import tempfile
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tree / "tb/pp_top"))
import acmp_mutants as am  # noqa: E402

refused = []
with tempfile.TemporaryDirectory(prefix="r717-plant-") as t:
    for i, m in enumerate(am.MUTANTS):
        work = Path(t) / f"{i:03d}-{m.name}"
        am.copy_tree(tree, work, m.suite)
        reason = am.plant(work, m.edits)
        if reason:
            refused.append((m.name, reason))
print(f"{len(am.MUTANTS)} arms, {len(refused)} refused")
for name, reason in refused:
    print("REFUSED", name, reason)
sys.exit(1 if refused else 0)
