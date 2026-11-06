#!/usr/bin/env python3
"""Run a named subset of the engine mutation arm in parallel workers.

usage: engine_arm_subset.py <clone>/tb/verilator/engine <out.jsonl> [--jobs N]

Runs the arm's own unmutated control (the same steps as mutants.main():
stage, build, image, harness, verdict) and every #100 control
(p100_mutants.P100_MUTATIONS) through mutants.run_mutant(), which demands
that each mutant fail every check it names. One JSON line per job.
Exit 0 only when the control passes and every selected mutant is caught.
"""
import argparse
import concurrent.futures as cf
import contextlib
import importlib.util
import io
import json
import sys
import tempfile
import time
from pathlib import Path

_M = {}


def arm(engine: Path):
    if "m" not in _M:
        sys.path.insert(0, str(engine))
        sys.path.insert(0, str(engine.parent.parent))
        spec = importlib.util.spec_from_file_location("mutants", engine / "mutants.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _M["m"] = mod
        _M["work"] = Path(tempfile.mkdtemp(prefix="r778-arm-"))  # under $TMPDIR
    return _M["m"], _M["work"]


def job(engine: str, index: int) -> dict:
    m, work = arm(Path(engine))
    t0 = time.monotonic()
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        if index < 0:
            src = m.stage(work, "control")
            exe = m.build(src, work, "control")
            run = work / "run_control"
            if exe is None or not m.generate_image(src, run):
                ok, why = False, "did not build"
            else:
                why = m.verdict(*m.run_harness(exe, run))
                ok = why == "pass"
            print(f"[{'PASS' if ok else 'FAIL'}] control: {why}")
            name = "control"
        else:
            mu = m.MUTATIONS[index]
            name = mu[0]
            clean = None
            if mu[1] == m.GENERATOR:
                if "clean" not in _M:
                    _M["clean"] = m.build(m.stage(work, "clean"), work, "clean")
                clean = _M["clean"]
            ok = m.run_mutant(work, clean, mu)
    return dict(index=index, name=name, ok=ok, seconds=round(time.monotonic() - t0, 1),
                lines=out.getvalue().splitlines())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("engine")
    ap.add_argument("out")
    ap.add_argument("--jobs", type=int, default=8)
    a = ap.parse_args()
    engine = str(Path(a.engine).resolve())
    m, _ = arm(Path(engine))
    sys.path.insert(0, engine)
    import p100_mutants  # noqa: E402
    want = {mu[0] for mu in p100_mutants.P100_MUTATIONS}
    todo = [-1] + [i for i, mu in enumerate(m.MUTATIONS) if mu[0] in want]
    print(f"selected: control + {len(todo) - 1} of {len(m.MUTATIONS)} mutants "
          f"({len(want)} #100 controls)", flush=True)
    bad = 0
    with open(a.out, "w") as fo, cf.ProcessPoolExecutor(max_workers=a.jobs) as pool:
        futs = {pool.submit(job, engine, i): i for i in todo}
        for f in cf.as_completed(futs):
            r = f.result()
            fo.write(json.dumps(r) + "\n")
            fo.flush()
            bad += not r["ok"]
            print(f"{'ok ' if r['ok'] else 'BAD'} {r['index'] + 1:03d} {r['seconds']:7.1f}s {r['name']}", flush=True)
    print(f"{len(todo)} checks: {len(todo) - bad} PASS, {bad} FAIL")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
