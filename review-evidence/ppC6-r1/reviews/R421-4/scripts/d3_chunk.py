#!/usr/bin/env python3
"""Run tb/pp_top/d3_mutants.py's own judge() over a slice of its MUTANTS.

The stock driver re-runs every golden before each invocation; a foreground
call is capped at ten minutes, so this wrapper runs the goldens once
(`--goldens`) and the arms in slices (`--slice K/N`), with the driver's
unmodified plant/build/run/grade logic. Results append to <output>/<tag>.json.

usage: d3_chunk.py <repo> <output> (--goldens | --slice K/N) [--jobs J]
"""
import argparse
import concurrent.futures
import importlib.util
import json
import sys
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("repo", type=Path)
    ap.add_argument("output", type=Path)
    ap.add_argument("--goldens", action="store_true")
    ap.add_argument("--slice", default="")
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--verilator", default="verilator")
    a = ap.parse_args()
    sys.argv = ["d3_mutants.py"]
    spec = importlib.util.spec_from_file_location("d3m", a.repo / "tb/pp_top/d3_mutants.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    out = a.output.resolve()
    out.mkdir(parents=True, exist_ok=True)
    work = (a.repo.resolve(), out, a.verilator)
    if a.goldens:
        suites = sorted({x.suite for x in m.MUTANTS}, key=lambda s: (s.directory, s.run))
        jobs = [("golden-" + Path(s.directory).name, s, (), ()) for s in suites]
        tag = "goldens"
    else:
        k, n = (int(v) for v in a.slice.split("/"))
        chosen = list(m.MUTANTS)[k::n]
        jobs = [(x.name, x.suite, x.edits, x.checks) for x in chosen]
        tag = f"slice_{k}_of_{n}"
    with concurrent.futures.ThreadPoolExecutor(max(1, a.jobs)) as pool:
        records = list(pool.map(lambda j: m.judge(*j, work), jobs))
    for r in records:
        print(json.dumps({k: r.get(k) for k in ("mutant", "verdict", "missing")}), flush=True)
    (out / f"{tag}.json").write_text(json.dumps(records, indent=1) + "\n")
    good = ("PASS",) if a.goldens else ("KILLED",)
    bad = [r["mutant"] for r in records if r["verdict"] not in good]
    print(f"{tag}: {len(records) - len(bad)} of {len(records)} {'/'.join(good)}; not: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
