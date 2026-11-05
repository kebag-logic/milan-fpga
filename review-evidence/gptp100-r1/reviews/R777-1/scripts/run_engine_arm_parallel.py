#!/usr/bin/env python3
"""Reviewer driver: run the engine mutation arm (tb/verilator/engine/mutants.py)
with N mutants in parallel, reusing the arm's own staging, build, harness run,
verdict and named-check logic (run_mutant / named_verdict) unchanged.

Only two things differ from `python3 mutants.py`:
  * the work directory is a fixed path (so it can be inspected), and each
    mutant's staged tree, build and run directory are removed after its
    verdict is recorded, to bound disk use;
  * Verilator's own build parallelism (-j in VFLAGS) is set by --build-j.

Usage: run_engine_arm_parallel.py ENGINE_DIR WORK_DIR [--jobs N] [--build-j M]
       [--only SUBSTR ...]
Exit 0 only when the unmutated control passes and every mutant is caught.
"""
from __future__ import annotations

import argparse
import contextlib
import io
import multiprocessing as mp
import shutil
import sys
import time
from pathlib import Path

ARM = None
WORK = None
CLEAN_EXE = None


def _init(engine_dir: str, work: str, clean_exe: str, build_j: str) -> None:
    global ARM, WORK, CLEAN_EXE
    sys.path.insert(0, engine_dir)
    import mutants as arm  # the arm under review, imported from its own dir
    _set_build_j(arm, build_j)
    ARM, WORK, CLEAN_EXE = arm, Path(work), Path(clean_exe)


def _set_build_j(arm, build_j: str) -> None:
    v = arm.VFLAGS
    i = v.index("-j")
    v[i + 1] = build_j


def _one(idx: int):
    mutation = ARM.MUTATIONS[idx]
    name = mutation[0]
    tag = "".join(c if c.isalnum() else "_" for c in name)
    buf = io.StringIO()
    t0 = time.time()
    with contextlib.redirect_stdout(buf):
        ok = ARM.run_mutant(WORK, CLEAN_EXE, mutation)
    dt = time.time() - t0
    for p in (WORK / tag, WORK / f"run_{tag}", WORK / f"obj_{tag}"):
        shutil.rmtree(p, ignore_errors=True)
    return idx, name, ok, buf.getvalue(), dt


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("engine_dir")
    ap.add_argument("work_dir")
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--build-j", default="1")
    ap.add_argument("--only", nargs="*", default=None)
    a = ap.parse_args()
    engine_dir = str(Path(a.engine_dir).resolve())
    work = Path(a.work_dir).resolve()
    work.mkdir(parents=True, exist_ok=True)
    sys.path.insert(0, engine_dir)
    import mutants as arm
    _set_build_j(arm, a.build_j)

    clean_src = arm.stage(work, "clean")
    clean_run = work / "run_clean"
    clean_exe = arm.build(clean_src, work, "clean")
    if clean_exe is None or not arm.generate_image(clean_src, clean_run):
        print("[FAIL] the unmutated sources did not build")
        return 1
    answer = arm.verdict(*arm.run_harness(clean_exe, clean_run))
    passes = fails = 0
    if answer == "pass":
        passes += 1
        print("[PASS] the unmutated engine still passes the harness", flush=True)
    else:
        fails += 1
        print(f"[FAIL] the unmutated engine does NOT pass ({answer})", flush=True)

    idxs = [i for i, m in enumerate(arm.MUTATIONS)
            if a.only is None or any(s in m[0] for s in a.only)]
    print(f"INFO {len(idxs)} mutants, {a.jobs} at a time, build -j {a.build_j}",
          flush=True)
    ctx = mp.get_context("fork")
    results = {}
    with ctx.Pool(a.jobs, initializer=_init,
                  initargs=(engine_dir, str(work), str(clean_exe),
                            a.build_j)) as pool:
        for idx, name, ok, text, dt in pool.imap_unordered(_one, idxs):
            results[idx] = (name, ok, text, dt)
            print(f"INFO done {len(results)}/{len(idxs)} "
                  f"{'caught' if ok else 'NOT CAUGHT'} {name} ({dt:.0f}s)",
                  flush=True)
    print("\n==== verdicts in arm order ====")
    for idx in idxs:
        name, ok, text, dt = results[idx]
        sys.stdout.write(text)
        if ok:
            passes += 1
        else:
            fails += 1
    total = passes + fails
    print(f"\n{total} checks: {passes} PASS, {fails} FAIL")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
