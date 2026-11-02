#!/usr/bin/env python3
"""Run one owner control COUNT times from a tree and summarise status and time.

Usage: python3 -I repeat.py HEAD_SCRIPTS TREE CONTROL COUNT JOBS

Each run is the head's run_mutant (new session, file output, 150 s bound).
Prints every non-green run's last line and a summary: green/red/cut counts and
the median and largest wall time of the runs.
"""
import concurrent.futures
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(sys.argv[1]).resolve()))
from process_test_support import run_mutant  # noqa: E402

tree, control, count, jobs = Path(sys.argv[2]).resolve(), sys.argv[3], int(sys.argv[4]), int(sys.argv[5])
with concurrent.futures.ThreadPoolExecutor(jobs) as pool:
    results = list(pool.map(lambda _n: run_mutant(tree, control), range(count)))
counts = {"green": 0, "red": 0, "cut": 0}
for status, _seconds, output in results:
    verdict = "cut" if status is None else "red" if status else "green"
    counts[verdict] += 1
    if verdict != "green":
        lines = [line for line in output.splitlines() if line.strip()]
        print(f"{verdict}: {lines[-1][:300] if lines else ''}")
times = [seconds for _status, seconds, _output in results]
print(f"{tree.name} / {control}: {counts} median {statistics.median(times):.2f} s max {max(times):.2f} s")
sys.exit(0 if counts["green"] == count else 1)
