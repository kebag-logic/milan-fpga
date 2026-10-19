#!/usr/bin/env python3
"""Run the engine suite's own mutation arm (tb/verilator/engine/mutants.py of
the tree under test) in parallel slices, without changing it.

Each slice is a separate process: it imports that mutants.py, builds and runs
its own unmutated control, then calls the module's own run_mutant() for every
MUTATIONS index i with i % N == k. Verdicts are the module's own. One log per
slice; the parent prints the union tally.

Usage: mutslices.py ENGINE_DIR OUT_DIR --jobs N
"""
import argparse, contextlib, io, re, subprocess, sys, tempfile
from pathlib import Path


def slice_main(engine_dir: str, k: int, n: int) -> int:
    sys.path.insert(0, engine_dir)
    import mutants as m
    with tempfile.TemporaryDirectory(prefix=f"engine-mutslice{k}-") as td:
        work = Path(td)
        src = m.stage(work, "clean")
        run = work / "run_clean"
        exe = m.build(src, work, "clean")
        if exe is None or not m.generate_image(src, run):
            print("[FAIL] the unmutated sources did not build")
            return 1
        ans = m.verdict(*m.run_harness(exe, run))
        print(f"[{'PASS' if ans == 'pass' else 'FAIL'}] slice {k} control: {ans}",
              flush=True)
        bad = 0 if ans == "pass" else 1
        for i, mut in enumerate(m.MUTATIONS):
            if i % n != k:
                continue
            print(f"-- arm {i}: {mut[0]}", flush=True)
            if not m.run_mutant(work, exe, mut):
                bad += 1
            sys.stdout.flush()
    return 1 if bad else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("engine_dir"); ap.add_argument("out")
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--slice", type=int, default=-1)
    a = ap.parse_args()
    if a.slice >= 0:
        return slice_main(a.engine_dir, a.slice, a.jobs)
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    procs = []
    for k in range(a.jobs):
        log = (out / f"slice-{k}.log").open("w")
        procs.append((k, log, subprocess.Popen(
            [sys.executable, __file__, a.engine_dir, a.out,
             "--jobs", str(a.jobs), "--slice", str(k)],
            cwd=a.engine_dir, stdout=log, stderr=subprocess.STDOUT)))
    rcs = {k: p.wait() for k, _, p in procs}
    text = "".join((out / f"slice-{k}.log").read_text() for k in range(a.jobs))
    arms = len(re.findall(r"^-- arm \d+:", text, re.M))
    caught = len(re.findall(r"^\[PASS\] mutant caught:", text, re.M))
    controls = len(re.findall(r"^\[PASS\] slice \d+ control: pass", text, re.M))
    summary = (f"arms {arms}, caught {caught}, controls passing {controls}/{a.jobs}, "
               f"slice rcs {rcs}\n")
    (out / "summary.txt").write_text(summary)
    print(summary, end="")
    return 0 if all(rc == 0 for rc in rcs.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
