#!/usr/bin/env python3
"""Run the clone's stream_counters.py driver against an instrumented copy of
sim_nxn.cpp/stream_counters.hpp (event-time prints only; RTL untouched apart
from the driver's own named variant). Usage:
trace_counters.py <clone> <instrumented-dir> <work> <driver args...>"""
import importlib.util, subprocess, sys
from pathlib import Path
clone, inst, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), Path(sys.argv[3]).resolve()
drv = clone / "tb/verilator/milan_dp/stream_counters.py"
spec = importlib.util.spec_from_file_location("stream_counters", drv)
sc = importlib.util.module_from_spec(spec); spec.loader.exec_module(sc)
orig = subprocess.run
target = str(sc.HERE / "sim_nxn.cpp")
def run(cmd, *a, **k):
    if isinstance(cmd, list):
        cmd = [str(inst / "sim_nxn.cpp") if c == target else c for c in cmd]
    return orig(cmd, *a, **k)
sc.subprocess.run = run
sys.argv = [str(drv), "--work", str(work)] + sys.argv[4:]
try:
    sc.main()
except RuntimeError as e:
    print("DRIVER VERDICT:", e)
