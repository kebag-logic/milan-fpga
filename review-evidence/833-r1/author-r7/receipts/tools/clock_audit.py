#!/usr/bin/env python3
"""Audit the starved clock of owner_stated_seconds: each run's pass clocks, steps, and the tick before each stated time.

usage: python3 -I -B clock_audit.py <tree>
"""
import sys
import types
from pathlib import Path

tree = Path(sys.argv[1])
sys.path.insert(0, str(tree / "scripts"))
import test_suite_cancellation as tsc  # noqa: E402

runs = []
real_ns = tsc.SimpleNamespace
real_cleanup = tsc.starved_cleanup


def ns(**kw):
    if "sleep" in kw:
        mono, sleep = kw["monotonic"], kw["sleep"]
        run = runs[-1]

        def sleeping(seconds):
            before = mono()
            sleep(seconds)
            run["steps"].append(mono() - before)
        kw["sleep"] = sleeping
    return real_ns(**kw)


def cleanup(owner, listing, names, stated, reaped=lambda _c: set()):
    runs.append({"stated": stated, "steps": []})
    events = real_cleanup(owner, listing, names, stated, reaped)
    runs[-1]["events"] = events
    return events


tsc.SimpleNamespace, tsc.starved_cleanup = ns, cleanup
tsc.owner_stated_seconds()
bad = 0
for n, run in enumerate(runs, 1):
    clocks, c = [0.0], 0.0
    for step in run["steps"]:
        c += min(step, 0.5)
        clocks.append(c)
    times = sorted({e[0] for e in run["stated"]})
    missing = [t for t in times if t > 0 and not (t in clocks and t - tsc.TICK in clocks)]
    short = [s for s in run["steps"] if s < 0.5]
    print(f"run {n}: {len(clocks)} passes, stated {[round(t, 7) for t in times]}, slow steps "
          f"{sorted({round(s, 7) for s in run['steps'] if s > 0.5})}, short steps {len(short)} "
          f"(min {min(short):.3g} s), max clock {clocks[-1]:.7f}, missing tick-before/at: {missing}")
    bad += bool(missing)
print("clock audit:", "FAIL" if bad else "PASS")
sys.exit(1 if bad else 0)
