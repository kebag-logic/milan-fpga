#!/usr/bin/env python3
"""Unit probes of mutants.py's in_list_order, default_jobs and --jobs parse.

usage: probe_scheduler.py <tree>
Imports the tree's tb/verilator/engine/mutants.py (no build, no harness).
"""
import os
import random
import subprocess
import sys
import threading
import time
from pathlib import Path

tree = Path(sys.argv[1])
eng = tree / "tb/verilator/engine"
sys.path.insert(0, str(eng))
sys.dont_write_bytecode = True
import mutants as m  # noqa: E402

results = []


def check(ok, what):
    results.append(ok)
    print(f"{'PASS' if ok else 'FAIL'} {what}")


class Tracker:
    def __init__(self):
        self.lock = threading.Lock()
        self.now = self.peak = 0
        self.started = []

    def task(self, i, delay, boom=False):
        def run():
            with self.lock:
                self.now += 1
                self.peak = max(self.peak, self.now)
                self.started.append(i)
            time.sleep(delay)
            with self.lock:
                self.now -= 1
            if boom:
                raise RuntimeError(f"task {i}")
            return i
        return run


random.seed(102)
for jobs in (1, 2, 4, 8, 32):
    t = Tracker()
    delays = [random.uniform(0.0, 0.05) for _ in range(20)]
    tasks = [t.task(i, d) for i, d in enumerate(delays)]
    got = list(m.in_list_order(jobs, tasks))
    check(got == list(range(20)), f"jobs {jobs}: results in list order")
    if jobs <= 8:   # fewer workers than tasks: the FIFO queue is observable
        check(t.peak == jobs, f"jobs {jobs}: peak concurrency {t.peak} == {jobs}")
        check(t.started == list(range(20)), f"jobs {jobs}: tasks start in list order")
    else:           # more workers than tasks: threads start lazily and race
        check(t.peak <= jobs, f"jobs {jobs}: peak concurrency {t.peak} <= {jobs}")

# completion order differs from list order: first task slowest
t = Tracker()
tasks = [t.task(0, 0.3)] + [t.task(i, 0.0) for i in range(1, 6)]
got = list(m.in_list_order(4, tasks))
check(got == list(range(6)), "slow first task still yields first")

# an exception: earlier results come out, then it propagates, nothing runs on
for jobs in (1, 4):
    t = Tracker()
    tasks = [t.task(i, 0.02, boom=(i == 3)) for i in range(10)]
    seen = []
    try:
        for r in m.in_list_order(jobs, tasks):
            seen.append(r)
        raised = False
    except RuntimeError:
        raised = True
    check(raised and seen == [0, 1, 2], f"jobs {jobs}: exception after results 0..2 ({seen})")
    check(t.now == 0, f"jobs {jobs}: no task still running after the exception")

# closing early waits for running tasks (the arm then removes its directory)
t = Tracker()
gen = m.in_list_order(4, [t.task(i, 0.2) for i in range(10)])
next(gen)
gen.close()
check(t.now == 0, "close() leaves no task running")
check(len(t.started) < 10, f"close() cancels tasks not yet started ({len(t.started)} started)")

# default_jobs from the affinity mask, capped at JOBS_CAP
for cpus, want in (("96", 1), ("96-98", 3), ("96-111", 8)):
    r = subprocess.run(["taskset", "-c", cpus, sys.executable, "-B", "-c",
                        f"import sys; sys.path.insert(0, {str(eng)!r}); "
                        "import mutants; print(mutants.default_jobs())"],
                       capture_output=True, text=True)
    check(r.stdout.strip() == str(want), f"default_jobs under CPUs {cpus} = {r.stdout.strip()} (want {want})")

# --jobs parsing rejects before any build
for bad in ("0", "-1", "abc", "1.5"):
    start = time.monotonic()
    r = subprocess.run([sys.executable, "-B", "mutants.py", "--jobs", bad],
                       cwd=str(eng), capture_output=True, text=True,
                       env={**os.environ, "PATH": "/nonexistent"})
    took = time.monotonic() - start
    check(r.returncode == 2 and "--jobs" in r.stderr and took < 10,
          f"--jobs {bad}: rc {r.returncode}, {took:.1f} s, {r.stderr.strip().splitlines()[-1]!r}")
r = subprocess.run([sys.executable, "-B", "mutants.py", "--help"],
                   cwd=str(eng), capture_output=True, text=True)
check(r.returncode == 0 and "--jobs" in r.stdout, "--help names --jobs")
print(r.stdout)

failed = results.count(False)
print(f"{len(results)} checks: {len(results) - failed} PASS, {failed} FAIL")
sys.exit(1 if failed else 0)
