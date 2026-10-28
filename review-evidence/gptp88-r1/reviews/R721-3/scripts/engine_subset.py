#!/usr/bin/env python3
"""Run a named subset of the engine mutation arm, in parallel.

Usage: engine_subset.py TREE JOBS REGEX [OUTDIR]

TREE is an extracted copy of the reviewed head (git archive). Every entry of
TREE/tb/verilator/engine/mutants.py MUTATIONS whose name or named checks match
REGEX is planted and graded by the arm's own run_mutant() (same staging, same
named-check rule), after the arm's own unmutated control. With OUTDIR, the full
harness output of every run is kept there, one file per mutant, so the FAIL
lines each mutant printed can be audited.
"""
import concurrent.futures as cf
import contextlib
import importlib.util
import io
import re
import sys
import tempfile
from pathlib import Path

tree, jobs, rx = Path(sys.argv[1]).resolve(), int(sys.argv[2]), re.compile(sys.argv[3])
outdir = Path(sys.argv[4]).resolve() if len(sys.argv) > 4 else None
eng = tree / "tb/verilator/engine"
sys.path.insert(0, str(eng))
spec = importlib.util.spec_from_file_location("engine_mutants", eng / "mutants.py")
arm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(arm)

if outdir:
    outdir.mkdir(parents=True, exist_ok=True)
    real_run = arm.run_harness

    def keep(exe, rundir):
        rc, out = real_run(exe, rundir)
        (outdir / f"{Path(rundir).name}.log").write_text(f"rc {rc}\n{out}")
        return rc, out
    arm.run_harness = keep

chosen = [m for m in arm.MUTATIONS if rx.search(m[0]) or rx.search(m[4])]
sys.stdout.reconfigure(line_buffering=True)
print(f"subset: {len(chosen)} of {len(arm.MUTATIONS)} mutants match {rx.pattern!r}")
with tempfile.TemporaryDirectory(prefix="eng-subset-", dir=str(tree)) as td:
    work = Path(td)
    src = arm.stage(work, "clean")
    run = work / "run_clean"
    exe = arm.build(src, work, "clean")
    assert exe is not None and arm.generate_image(src, run), "control build"
    ctl = arm.verdict(*arm.run_harness(exe, run))
    print(f"control: {ctl}")

    def one(m):
        return m[0], arm.run_mutant(work, exe, m)

    passed = 0
    with cf.ThreadPoolExecutor(max_workers=jobs) as pool:
        for name, ok in pool.map(one, chosen):
            passed += ok
print(f"\nsubset verdict: control {ctl}; {passed}/{len(chosen)} mutants caught")
sys.exit(0 if ctl == "pass" and passed == len(chosen) else 1)
