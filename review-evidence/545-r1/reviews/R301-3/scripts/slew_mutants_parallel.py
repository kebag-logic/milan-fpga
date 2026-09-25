#!/usr/bin/env python3
"""Parallel driver for tb/verilator/mmcm_servo/slew_mutants.py.

Imports the campaign's own MUTANTS/STREAK_MUTANTS tables and run_case()
verdict function unchanged; only the scheduling differs (clean controls first,
then every defect concurrently, at most 8 jobs). Usage: <repo-root>
"""
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "tb/verilator/mmcm_servo"))
import slew_mutants as sm  # noqa: E402

source = sm.RTL.read_text()
with tempfile.TemporaryDirectory(prefix="servo-slew-mutants-par-",
                                 dir=sys.argv[2] if len(sys.argv) > 2 else None) as d:
    work = Path(d)
    with ThreadPoolExecutor(max_workers=2) as ex:
        clean = [ex.submit(sm.run_case, work, "clean", source, None),
                 ex.submit(sm.run_case, work, "clean_unit", source, None, True)]
        results = [f.result() for f in clean]
    if not all(results):
        print("== clean control failed ==")
        sys.exit(1)
    arms = []
    for name, anchor, repl, failure in (*sm.MUTANTS, *sm.STREAK_MUTANTS):
        if source.count(anchor) != 1:
            print(f"FAIL {name}: expected exactly one mutation anchor")
            results.append(False)
            continue
        unit = any(name == item[0] for item in sm.STREAK_MUTANTS)
        arms.append((name, source.replace(anchor, repl), failure, unit))
    with ThreadPoolExecutor(max_workers=8) as ex:
        futs = [ex.submit(sm.run_case, work, n, s, f, u) for n, s, f, u in arms]
        results += [f.result() for f in futs]
failures = sum(not p for p in results)
print(f"== mmcm_servo slew mutants (parallel driver): checks: {len(results)}   failures: {failures} ==")
sys.exit(1 if failures else 0)
