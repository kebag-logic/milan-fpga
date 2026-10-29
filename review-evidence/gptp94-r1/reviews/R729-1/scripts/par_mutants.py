#!/usr/bin/env python3
"""Run the engine mutation arm of one FPGA-gPTP clone in parallel.

Same verdict logic as tb/verilator/engine/mutants.py (it is imported and its
own run_mutant() is called per mutant); only the scheduling differs: a pool
of worker processes, each Verilator build at -j 2.

usage: par_mutants.py <clone> <jobs> [--extra <module.py>] [--only <substr>]
  --extra: a python file defining EXTRA_MUTATIONS (same tuple format); when
           given, only those mutants run (reviewer probes).
"""
import argparse
import contextlib
import importlib.util
import io
import multiprocessing
import sys
import tempfile
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("clone")
ap.add_argument("jobs", type=int)
ap.add_argument("--extra")
ap.add_argument("--only")
args = ap.parse_args()

eng = Path(args.clone).resolve() / "tb/verilator/engine"
sys.path.insert(0, str(eng))
sys.path.insert(0, str(eng.parent.parent))
spec = importlib.util.spec_from_file_location("mutants", eng / "mutants.py")
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)
i = M.VFLAGS.index("-j")
M.VFLAGS[i + 1] = "2"

muts = list(M.MUTATIONS)
if args.extra:
    xs = importlib.util.spec_from_file_location("extra", args.extra)
    X = importlib.util.module_from_spec(xs)
    xs.loader.exec_module(X)
    muts = list(X.EXTRA_MUTATIONS)
if args.only:
    muts = [m for m in muts if args.only in m[0]]

WORK = None
CLEAN = None


def one(idx):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        ok = M.run_mutant(WORK, CLEAN, muts[idx])
    return idx, ok, buf.getvalue()


with tempfile.TemporaryDirectory(prefix="r729-mut-",
                                 dir=str(Path(__file__).resolve().parent.parent
                                         / "scratch")) as td:
    WORK = Path(td)
    src = M.stage(WORK, "clean")
    run = WORK / "run_clean"
    CLEAN = M.build(src, WORK, "clean")
    if CLEAN is None or not M.generate_image(src, run):
        print("[FAIL] unmutated sources did not build")
        sys.exit(1)
    ans = M.verdict(*M.run_harness(CLEAN, run))
    passes = fails = 0
    if ans == "pass":
        passes += 1
        print("[PASS] the unmutated engine still passes the harness")
    else:
        fails += 1
        print(f"[FAIL] the unmutated engine does NOT pass ({ans})")
    sys.stdout.flush()
    res = {}
    with ProcessPoolExecutor(max_workers=args.jobs,
                             mp_context=multiprocessing.get_context("fork")) as ex:
        for idx, ok, text in ex.map(one, range(len(muts))):
            res[idx] = (ok, text)
    for idx in range(len(muts)):
        ok, text = res[idx]
        sys.stdout.write(text)
        passes += ok
        fails += (not ok)
    total = passes + fails
    print(f"\n{total} checks: {passes} PASS, {fails} FAIL")
    sys.exit(1 if fails else 0)
