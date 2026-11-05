#!/usr/bin/env python3
"""Run the engine mutation arm's own control and mutants in parallel workers.

usage: arm_jobs.py <engine dir> <out dir> [--jobs N] [--budget-s S] [--names a|b]

Each job is the arm's own code: the control repeats mutants.main()'s
unmutated run (stage, build, image, harness, verdict) and every mutant is
mutants.run_mutant() on one MUTATIONS entry. A job's verdict and every line
it printed go to <out>/<NNN>.json; a finished job is skipped on a rerun, so
the arm completes over several foreground invocations, each under budget.
"""
import argparse
import concurrent.futures as cf
import contextlib
import importlib.util
import io
import json
import os
import sys
import tempfile
import time
from pathlib import Path

_MOD = {}


def arm(engine: Path):
    """The engine dir's mutants module, loaded once per worker process."""
    if "m" not in _MOD:
        sys.path.insert(0, str(engine))
        sys.path.insert(0, str(engine.parent.parent))
        spec = importlib.util.spec_from_file_location("mutants", engine / "mutants.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _MOD["m"] = mod
        _MOD["work"] = Path(tempfile.mkdtemp(prefix="engine-arm-"))
    return _MOD["m"], _MOD["work"]


def clean_exe(m, work: Path):
    """The unmutated build this worker shares between generator mutants."""
    if "clean" not in _MOD:
        src = m.stage(work, "clean")
        _MOD["clean"] = m.build(src, work, "clean")
    return _MOD["clean"]


def job(engine: str, index: int) -> dict:
    """Run job `index`: -1 is the control, else MUTATIONS[index]."""
    m, work = arm(Path(engine))
    t0 = time.monotonic()
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        if index < 0:
            src = m.stage(work, "control")
            exe = m.build(src, work, "control")
            run = work / "run_control"
            if exe is None or not m.generate_image(src, run):
                ok, verdict = False, "did not build"
            else:
                verdict = m.verdict(*m.run_harness(exe, run))
                ok = verdict == "pass"
            print(f"[{'PASS' if ok else 'FAIL'}] the unmutated engine: {verdict}")
            name = "control"
        else:
            mutation = m.MUTATIONS[index]
            name = mutation[0]
            exe = clean_exe(m, work) if mutation[1] == m.GENERATOR else None
            ok = m.run_mutant(work, exe, mutation)
    return dict(index=index, name=name, ok=ok, seconds=round(time.monotonic() - t0, 1),
                lines=out.getvalue().splitlines())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("engine")
    ap.add_argument("out")
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--budget-s", type=float, default=560.0)
    ap.add_argument("--longest-s", type=float, default=240.0)
    ap.add_argument("--names", default="")
    a = ap.parse_args()
    engine = str(Path(a.engine).resolve())
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    m, _ = arm(Path(engine))
    want = [n for n in a.names.split("|") if n]
    todo = [-1] + list(range(len(m.MUTATIONS)))
    if want:
        todo = [i for i in todo if (i < 0 and "control" in want)
                or (i >= 0 and m.MUTATIONS[i][0] in want)]
    todo = [i for i in todo if not (out / f"{i + 1:03d}.json").exists()]
    t0 = time.monotonic()
    done = 0
    with cf.ProcessPoolExecutor(max_workers=a.jobs) as pool:
        running = {}
        while todo or running:
            while todo and len(running) < a.jobs and \
                    time.monotonic() - t0 < a.budget_s - a.longest_s:
                i = todo.pop(0)
                running[pool.submit(job, engine, i)] = i
            if not running:
                break
            finished, _ = cf.wait(running, return_when=cf.FIRST_COMPLETED)
            for f in finished:
                i = running.pop(f)
                r = f.result()
                (out / f"{i + 1:03d}.json").write_text(json.dumps(r, indent=1) + "\n")
                done += 1
                print(f"{'ok ' if r['ok'] else 'BAD'} {i + 1:03d} {r['seconds']:7.1f}s {r['name']}",
                      flush=True)
    left = len([i for i in [-1] + list(range(len(m.MUTATIONS)))
                if not (out / f"{i + 1:03d}.json").exists()])
    print(f"this call: {done} jobs, {time.monotonic() - t0:.0f} s; {left} left of {len(m.MUTATIONS) + 1}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
