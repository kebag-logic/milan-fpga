#!/usr/bin/env python3
"""Reviewer spot-check of named engine mutation controls.

Usage:
  spot_mutants.py <tree> <work> build
  spot_mutants.py <tree> <work> clean
  spot_mutants.py <tree> <work> mutant "<control name>"

<tree> is a disposable extraction of the repository at the reviewed head;
<work> is a scratch directory. The verilator on PATH must be the pinned one.
"build" stages and builds the unmutated harness once into <work>; "clean"
runs the unmutated shipping and priority1 255 passes; "mutant" plants one
control from the arm's own table and grades it with the arm's own
run_mutant (every named check must fail). The driver's code is used as
published; only the selection differs.
"""
import sys
from pathlib import Path

tree, work, mode = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3]
sys.path.insert(0, str(tree / "tb/verilator/engine"))
import mutants  # noqa: E402

work.mkdir(parents=True, exist_ok=True)
exe = work / "obj_clean" / "Vengine_clean"
if mode == "build":
    src = mutants.stage(work, "clean")
    ok = mutants.build(src, work, "clean") is not None
    print("build", "ok" if ok else "FAILED")
    sys.exit(0 if ok else 1)
if mode == "clean":
    rundir = work / "run_clean"
    assert mutants.generate_image(work / "src_clean", rundir)
    rc, out = mutants.run_harness(exe, rundir)
    print(out[-400:])
    print("verdict", mutants.verdict(rc, out))
    sys.exit(rc)
name = sys.argv[4]
sel = [m for m in mutants.MUTATIONS if m[0] == name]
assert len(sel) == 1, name
sub = work / ("m_" + "".join(c if c.isalnum() else "_" for c in name))
sub.mkdir(exist_ok=True)
ok = mutants.run_mutant(sub, exe, sel[0])
sys.exit(0 if ok else 1)
