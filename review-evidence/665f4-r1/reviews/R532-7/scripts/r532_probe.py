#!/usr/bin/env python3
"""Reviewer probe runner (R532-6): build one GoogleTest source against a tree's SRP arm.

usage: r532_probe.py ROOT LWSRP OUT IFS TESTFILE [FILTER]
ROOT    a parent tree (the review clone or a disposable planted export); its own
        harness scripts are imported, so CTRL resolves inside ROOT.
LWSRP   lwSRP checkout at the parent's recorded pin (the pin guard is enforced).
TESTFILE a probe .cpp; it is staged beside ROOT's own srp_fixture.hpp.
Prints a summary and FAIL lines; rc 0 pass, 1 test failure, 2 refusal/build error.
"""
import shutil
import sys
from pathlib import Path
root, lw, out, ifs, test = sys.argv[1:6]
flt = sys.argv[6] if len(sys.argv) > 6 else "*"
sys.path[:0] = [f"{root}/sw/firmware/ctrl/test", f"{root}/sw/firmware/gtest"]
import os
if os.environ.get("R532_LWSRP_REV"):
    # Deliberate dependency plant: the guard still requires a clean checkout at this revision.
    import ctrl_arms
    ctrl_arms.LWSRP_REV = os.environ["R532_LWSRP_REV"]
import srp_arms
from ctrl_build import CTRL, Tree, Refusal
import fw_gtest
stage = Path(out) / "stage"
stage.mkdir(parents=True, exist_ok=True)
shutil.copyfile(Path(root) / "sw/firmware/ctrl/test/srp_fixture.hpp", stage / "srp_fixture.hpp")
shutil.copyfile(test, stage / Path(test).name)
srp_arms.HERE = stage
try:
    res = srp_arms.arm_srp(Tree(CTRL, Path(out), Path(out) / "reuse", fw_gtest.Build(jobs=1)),
                           Path(lw), int(ifs), test=(Path(test).name, flt))
except Refusal as e:
    print("REFUSED", e)
    sys.exit(2)
Path(out, "probe.log").write_text(res.log)
lines = res.log.splitlines()
print(f"rc={res.rc} ifs={ifs} test={Path(test).name} filter={flt} root={root}")
print("\n".join(l for l in lines if l.startswith(("[  PASSED", "[  FAILED", "[       OK", "withdraw", "exhausted", "retry")) or "Failure" in l or "checks:" in l))
sys.exit(1 if res.rc else 0)
