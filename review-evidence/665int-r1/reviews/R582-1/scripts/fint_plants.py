#!/usr/bin/env python3
"""Run only the lane F-INT publication plants of the firmware campaigns (PR #704).

Usage: fint_plants.py <source-tree> <lwsrp-checkout> <work-dir> {ctrl|srp}

ctrl: every ctrl_mutants.MUTANTS entry whose name starts with "pub-" or
"model-pub-", through ctrl_mutants.campaign (the gate's own driver).
srp: every srp_mutants.DEFECTS entry whose name starts with "pub-" or
"cancelled-link", through srp_mutants.campaign at two interfaces.
Each line the drivers print names the plant and its verdict.
"""
import sys
from pathlib import Path

TREE, LWSRP, WORK = (Path(a).resolve() for a in sys.argv[1:4])
WHICH = sys.argv[4]
sys.path[:0] = [str(TREE / "sw/firmware/ctrl/test"), str(TREE / "sw/firmware/gtest")]
import ctrl_mutants  # noqa: E402
import srp_mutants  # noqa: E402
import test_ctrl_firmware  # noqa: E402
from ctrl_build import CTRL, Tree  # noqa: E402
import fw_gtest  # noqa: E402

if WHICH == "ctrl":
    chosen = tuple(m for m in ctrl_mutants.MUTANTS if m.name.startswith(("pub-", "model-pub-")))
    print(f"F-INT ctrl plants: {len(chosen)} of {len(ctrl_mutants.MUTANTS)}", flush=True)
    tree = Tree(CTRL, WORK / "checkout", WORK / "reuse", fw_gtest.Build(jobs=4))
    test_ctrl_firmware.cut_reuse(tree.reuse)
    ctrl_mutants.MUTANTS = chosen
    ctrl_mutants.unnamed_tests = lambda: []   # the subset cannot name every test; the full gate checks that
    failed = ctrl_mutants.campaign(WORK / "mutants", tree.reuse, 4)
else:
    chosen = tuple(d for d in srp_mutants.DEFECTS if d.name.startswith(("pub-", "cancelled-link")))
    print(f"F-INT srp plants: {len(chosen)} of {len(srp_mutants.DEFECTS)}", flush=True)
    srp_mutants.DEFECTS = chosen
    failed = srp_mutants.campaign(WORK / "srp-mutants", LWSRP, 4)
print(f"fint_plants {WHICH}: {'FAIL' if failed else 'PASS'}", flush=True)
sys.exit(1 if failed else 0)
