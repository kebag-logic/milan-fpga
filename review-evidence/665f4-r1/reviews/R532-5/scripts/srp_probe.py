#!/usr/bin/env python3
"""Reviewer probe: run one SRP GoogleTest selection from an exported tree.

usage: srp_probe.py ROOT LWSRP_CHECKOUT REV IFS FILTER OUTDIR [SUITE]
ROOT is an exported copy of the parent tree (its own scripts are imported);
REV overrides the pin guard so a disposable lwSRP commit (old pin or plant)
can be measured; the guard still requires that checkout to be clean at REV.
Prints the arm verdict and per-test FAIL lines; rc 0 pass, 1 test failure, 2 refusal.
"""
import sys
from pathlib import Path
root, lw, rev, ifs, flt, out = sys.argv[1:7]
suite = sys.argv[7] if len(sys.argv) > 7 else "srp_mbx.cpp"
sys.path[:0] = [f"{root}/sw/firmware/ctrl/test", f"{root}/sw/firmware/gtest"]
import ctrl_arms
ctrl_arms.LWSRP_REV = rev
from ctrl_build import CTRL, Tree, Refusal
import fw_gtest
from srp_arms import arm_srp
try:
    res = arm_srp(Tree(CTRL, Path(out), Path(out) / "reuse", fw_gtest.Build(jobs=4)),
                  Path(lw), int(ifs), test=(suite, flt))
except Refusal as e:
    print("REFUSED", e); sys.exit(2)
fails = [l for l in res.log.splitlines() if "[FAIL]" in l or "FAILED" in l]
summary = [l for l in res.log.splitlines() if l.startswith("==") or l.startswith("RESULT")]
print(f"rc={res.rc} ifs={ifs} rev={rev[:8]} filter={flt}")
print("\n".join(summary[-3:])); print("\n".join(fails[:40]))
Path(out, "probe.log").write_text(res.log)
sys.exit(res.rc)
