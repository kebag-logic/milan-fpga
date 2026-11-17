#!/usr/bin/env python3
"""Run, in one tree copy, the platboot arms (1 and 2 interfaces) and optionally the control campaign
restricted to mutants whose name starts with one of the given prefixes.
usage: run_phy.py <tree> <out-dir> [--campaign PREFIX ...] [--jobs N]"""
import argparse, sys, tempfile
from pathlib import Path
ap = argparse.ArgumentParser()
ap.add_argument("tree"); ap.add_argument("out")
ap.add_argument("--campaign", nargs="*"); ap.add_argument("--jobs", type=int, default=4)
ap.add_argument("--no-arms", action="store_true")
a = ap.parse_args()
sys.path.insert(0, str(Path(a.tree) / "sw/firmware/ctrl/test"))
import test_ctrl_firmware as T, ctrl_mutants, plat_arms, ctrl_arms, fw_gtest
out = Path(a.out).resolve(); out.mkdir(parents=True, exist_ok=True)
print("toolchain:", fw_gtest.toolchain())
tree = T.Tree(T.CTRL, out / "checkout", out / "reuse", fw_gtest.Build(jobs=a.jobs))
T.cut_reuse(tree.reuse)
failed = False
if not a.no_arms:
    outs = [plat_arms.arm_platboot(tree, 1), plat_arms.arm_platboot(tree, 2)]
    for o in outs:
        print(f"=== arm {o.arm if hasattr(o,'arm') else ''} rc", getattr(o, "rc", "?"))
        print(o.log)
    failed = ctrl_arms.report(outs)
    print("arms:", "FAIL" if failed else "PASS")
if a.campaign:
    sel = tuple(m for m in ctrl_mutants.MUTANTS if m.name.startswith(tuple(a.campaign)))
    print(f"campaign over {len(sel)} mutants: {[m.name for m in sel]}")
    ctrl_mutants.MUTANTS = sel
    ctrl_mutants.unnamed_tests = lambda: []
    failed = ctrl_mutants.campaign(out / "mutants", tree.reuse, a.jobs) or failed
sys.exit(1 if failed else 0)
