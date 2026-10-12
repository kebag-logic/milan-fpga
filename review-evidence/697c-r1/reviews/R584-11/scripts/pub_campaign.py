#!/usr/bin/env python3
"""Plant only the pub-acmp-* defects of the control campaign, through the campaign's own plant() and caught().

usage: pub_campaign.py <tree> <work directory> [--old-path]
  The ACMP core arm runs first on the unplanted tree and must pass (so a later [FAIL] is the plant's).
  --old-path re-points the eleven core plants at dev's "acmp/acmp.c" (a control: plant() must refuse each).
Exit 0 iff every plant is caught by its named killer on its words (or, with --old-path, every plant refuses).
"""
import dataclasses
import sys
from pathlib import Path

tree_root = Path(sys.argv[1]).resolve()
work = Path(sys.argv[2]).resolve()
old_path = "--old-path" in sys.argv
test_dir = tree_root / "sw/firmware/ctrl/test"
sys.path[:0] = [str(test_dir), str(tree_root / "sw/firmware/gtest")]

import ctrl_arms  # noqa: E402
import ctrl_mutants  # noqa: E402
import fw_gtest  # noqa: E402
from ctrl_build import CTRL, Refusal, Tree, stack_pin  # noqa: E402
from ctrl_reuse import cut_reuse  # noqa: E402

print(f"tree {tree_root}")
print(f"tsn-c-stack at {stack_pin()}")
table = [m for m in ctrl_mutants.MUTANTS if m.name.startswith("pub-acmp-")]
core = [m for m in table if m.path.endswith("acmp.c") and "acmp_mbx" not in m.path]
print(f"pub-acmp plants: {len(table)} ({len(core)} in the ACMP core, paths {sorted({m.path for m in core})})")
if old_path:
    table = [dataclasses.replace(m, path="acmp/acmp.c") for m in core]
    refused = 0
    for m in table:
        try:
            ctrl_mutants.plant(m, work)
            print(f"[APPLIED] {m.name} at acmp/acmp.c")
        except (Refusal, FileNotFoundError) as exc:
            refused += 1
            print(f"[refused] {m.name}: {type(exc).__name__}")
    print(f"old path: {refused} of {len(table)} refused")
    sys.exit(0 if refused == len(table) else 1)

build = fw_gtest.Build(jobs=4)
tree = Tree(CTRL, work / "checkout", work / "reuse", build)
cut_reuse(tree.reuse)
base = ctrl_arms.arm_acmp(tree)
print(f"baseline acmp arm rc={base.rc} fails={sum('[FAIL]' in ln for ln in base.log.splitlines())}")
if base.rc != 0:
    print(base.log[-3000:])
    sys.exit(2)
ctrl_mutants.MUTANTS = tuple(table)
escaped = ctrl_mutants.campaign(work / "mutants", tree.reuse, 4)
sys.exit(1 if escaped else 0)
