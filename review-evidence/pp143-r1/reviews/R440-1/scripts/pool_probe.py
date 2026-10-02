#!/usr/bin/env python3
"""Probe tb/common/mutant_pool.in_order: declared order under shuffled finish times, an
exception raised at its unit's turn, cancellation of unstarted units on early exit, and jobs<=0."""
import random
import sys
import threading
import time
sys.path.insert(0, sys.argv[1] + "/tb/common")
from mutant_pool import DEFAULT_JOBS, add_jobs_argument, in_order  # noqa: E402
import argparse

started: list[int] = []
lock = threading.Lock()


def work(unit):
    with lock:
        started.append(unit)
    time.sleep(random.uniform(0, 0.05))
    if unit == "boom":
        raise RuntimeError("boom")
    return unit * 10


random.seed(1)
units = list(range(40))
for jobs in (1, 3, 8, 64, 0, -2):
    with in_order(work, units, jobs) as results:
        out = list(results)
    assert out == [u * 10 for u in units], (jobs, out)
print("order: declared order at jobs 1, 3, 8, 64, 0, -2: OK")

started.clear()
units = [1, 2, "boom", 4, 5, 6, 7, 8, 9, 10, 11, 12]
seen = []
try:
    with in_order(work, units, 2) as results:
        for r in results:
            seen.append(r)
except RuntimeError as e:
    print(f"exception at its turn: results before it {seen}, raised {e!r}; "
          f"units started {len(started)} of {len(units)}")
assert seen == [10, 20]

started.clear()
units = list(range(1, 30))
with in_order(work, units, 2) as results:
    first = next(results)
print(f"early exit after the first result: units started {len(started)} of {len(units)}; "
      f"live worker threads after the block {threading.active_count() - 1}")
assert len(started) < len(units)

p = argparse.ArgumentParser()
add_jobs_argument(p)
print("default --jobs", p.parse_args([]).jobs, "DEFAULT_JOBS", DEFAULT_JOBS,
      "| --jobs 8 ->", p.parse_args(["--jobs", "8"]).jobs)
