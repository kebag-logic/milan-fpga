#!/usr/bin/env python3
"""Time one census pass of the dev and head owners on this host's /proc.

usage: census_cost.py DIR (holding dev_owned_process.py and head_owned_process.py) ROUNDS
Interleaves the two, prints the process count and each one's median and p90 in ms.
"""
import importlib.util, os, statistics, sys, time
d, rounds = sys.argv[1], int(sys.argv[2])
def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(d, name + ".py"))
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod
mods = {n: load(n) for n in ("dev_owned_process", "head_owned_process")}
owners = {n: m.OwnedProcesses() for n, m in mods.items()}
times = {n: [] for n in mods}
for _ in range(rounds):
    for n, o in owners.items():
        t = time.perf_counter(); o._descendants(); times[n].append((time.perf_counter() - t) * 1000)
procs = sum(1 for e in os.scandir("/proc") if e.name.isdecimal())
print(f"processes visible {procs}, rounds {rounds}, loadavg {open('/proc/loadavg').read().split()[:3]}")
for n, v in times.items():
    v.sort(); print(f"{n}: median {statistics.median(v):.1f} ms, p90 {v[int(len(v)*0.9)]:.1f} ms")
