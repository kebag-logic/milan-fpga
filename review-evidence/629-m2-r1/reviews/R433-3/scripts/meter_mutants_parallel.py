#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Run tb/verilator/aaf_clock_meter/mutants.py's campaign in parallel.

Imports the suite's own MUTANTS, mutate(), build() and run_case() unchanged
from a disposable copy of the head, so every verdict is the campaign's own
(clean control must pass; each mutant must fail by its named check), only
scheduled across worker threads instead of serially.
Usage: meter_mutants_parallel.py <copy of the head> <workdir> [jobs]
"""
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

repo, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
jobs = int(sys.argv[3]) if len(sys.argv) > 3 else 8
sys.path.insert(0, str(repo / "tb/verilator/aaf_clock_meter"))
import mutants as m  # noqa: E402

work.mkdir(parents=True, exist_ok=True)
sources = {key: path.read_text() for key, path in m.RTL.items()}
plan = [("clean", "meter", (), "cases:selection", None), *m.MUTANTS]


def one(entry):
    name, rtl, edits, target, failure = entry
    mutated = m.mutate(sources[rtl], edits) if edits else sources[rtl]
    if mutated is None:
        return name, False
    exe = m.build(work, name, rtl, mutated, target)
    return name, exe is not None and m.run_case(exe, name, target, failure)


with ThreadPoolExecutor(max_workers=jobs) as pool:
    results = list(pool.map(one, plan))
bad = [n for n, ok in results if not ok]
print(f"aaf_clock_meter mutants (parallel replay): {len(results) - len(bad)}/{len(results)} as required")
for n in bad:
    print(f"NOT AS REQUIRED: {n}")
sys.exit(1 if bad else 0)
