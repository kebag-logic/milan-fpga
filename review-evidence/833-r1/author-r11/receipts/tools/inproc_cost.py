#!/usr/bin/env python3
"""owner_stated_seconds in one process, timed by perf_counter: REPS runs from each tree, interleaved.

usage: python3 -I -B inproc_cost.py <old tree> <new tree> <reps>
Each tree's control runs in its own fresh interpreter, which imports it once and times REPS calls.
"""
import subprocess
import sys

CODE = '''
import io, contextlib, sys, time
sys.path.insert(0, sys.argv[1] + "/scripts")
import test_suite_cancellation as t
from owned_process import OwnedProcesses
times = []
with OwnedProcesses():
    for _ in range(int(sys.argv[2])):
        began = time.perf_counter()
        with contextlib.redirect_stdout(io.StringIO()):
            t.owner_stated_seconds()
        times.append(time.perf_counter() - began)
times.sort()
print(f"median {times[len(times) // 2] * 1000:.1f} ms min {times[0] * 1000:.1f} ms max {times[-1] * 1000:.1f} ms")
'''
old, new, reps = sys.argv[1], sys.argv[2], sys.argv[3]
for round_ in range(3):
    for label, tree in (("round 10", old), ("head", new)):
        out = subprocess.run([sys.executable, "-I", "-B", "-c", CODE, tree, reps], capture_output=True, text=True,
                             timeout=600)
        print(f"{label} {round_ + 1}: {out.stdout.strip() or out.stderr.strip()[-300:]}", flush=True)
