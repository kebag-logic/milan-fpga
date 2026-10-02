#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Run tb/verilator/aaf_clock_meter/mutants.py's own MUTANTS list, unchanged,
with at most N parallel workers (each build single-threaded).

Usage: run_meter_mutants_parallel.py <tree> [workers] [name ...]
<tree> is an exported copy of the head under review. The verdict rule is the
suite's own (mutants.run_case): a mutant counts only if its build succeeds,
the harness exits 1 and the named check is among its [FAIL] lines.
"""
import concurrent.futures as cf
import importlib.util
import os
import sys
import tempfile
from pathlib import Path


def main() -> int:
    tree = Path(sys.argv[1]).resolve()
    workers = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    only = set(sys.argv[3:])
    os.environ.setdefault("VERILATOR_JOBS", "1")
    spec = importlib.util.spec_from_file_location(
        "mutants", tree / "tb/verilator/aaf_clock_meter/mutants.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    sources = {k: p.read_text() for k, p in mod.RTL.items()}
    todo = [m for m in mod.MUTANTS if not only or m[0] in only]
    with tempfile.TemporaryDirectory(prefix="r433-meter-mut-", dir=str(tree.parent)) as d:
        work = Path(d)

        def one(m):
            name, rtl, edits, target, failure = m
            mutated = mod.mutate(sources[rtl], edits)
            if mutated is None:
                return name, False, "anchor not unique"
            exe = mod.build(work, name, rtl, mutated, target)
            if exe is None:
                return name, False, "build failed"
            return name, mod.run_case(exe, name, target, failure), failure

        with cf.ThreadPoolExecutor(max_workers=workers) as ex:
            results = list(ex.map(one, todo))
    bad = [r for r in results if not r[1]]
    for name, ok, why in results:
        print(f"SUMMARY {'KILLED' if ok else 'ESCAPED/ERROR'} {name}: {why}")
    print(f"meter mutants: {len(results) - len(bad)}/{len(results)} killed by their named check")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
