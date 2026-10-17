#!/usr/bin/env python3
"""Lane B21 host-evidence sampler: /proc/stat, /proc/interrupts and /proc/loadavg at a fixed rate.

usage: host_sampler_b21.py <out.bin> <hz>

Each record is one JSON line (written to <out.bin> despite the name, one line per sample):
monotonic ns, realtime, the aggregate cpu line's ten counters, the per-CPU steal counters,
every /proc/interrupts row's total (by its label), the 1-minute load, the three /proc/pressure
"some" and "full" totals (us) and the /proc/vmstat compaction, allocation-stall, swap and fault
counters (added after the first self-test, st-long). Reads only.
Stops on SIGINT.
"""
import json
import signal
import sys
import time

out, hz = sys.argv[1], float(sys.argv[2])
VMKEYS = {"compact_stall", "compact_fail", "compact_success", "allocstall_normal", "allocstall_movable",
          "pgmajfault", "pswpin", "pswpout", "thp_fault_alloc", "pgscan_direct", "pgsteal_direct"}
stop = False


def _stop(*_):
    global stop
    stop = True


signal.signal(signal.SIGINT, _stop)
signal.signal(signal.SIGTERM, _stop)
f = open(out, "w", buffering=1 << 16)
period = 1.0 / hz
nxt = time.monotonic()
while not stop:
    mono, rt = time.monotonic_ns(), time.time()
    cpu, steal = None, []
    for ln in open("/proc/stat"):
        if ln.startswith("cpu "):
            cpu = [int(x) for x in ln.split()[1:11]]
        elif ln.startswith("cpu"):
            steal.append(int(ln.split()[8]))
    irq = {}
    lines = open("/proc/interrupts").read().splitlines()
    ncpu = len(lines[0].split())
    for ln in lines[1:]:
        p = ln.split()
        if not p:
            continue
        lab = p[0].rstrip(":")
        tot = 0
        for x in p[1:1 + ncpu]:
            if x.isdigit():
                tot += int(x)
            else:
                break
        irq[lab + ("|" + " ".join(p[1 + ncpu:])[-40:] if lab.isdigit() else "")] = tot
    load = open("/proc/loadavg").read().split()[0]
    psi = {}
    for k in ("cpu", "memory", "io"):
        for ln in open(f"/proc/pressure/{k}"):
            q = ln.split()
            psi[f"{k}_{q[0]}"] = int(q[4].split("=")[1])
    vm = {}
    for ln in open("/proc/vmstat"):
        k, v = ln.split()
        if k in VMKEYS:
            vm[k] = int(v)
    f.write(json.dumps(dict(m=mono, t=round(rt, 6), cpu=cpu, steal=steal, irq=irq, load=load, psi=psi, vm=vm)) + "\n")
    nxt += period
    d = nxt - time.monotonic()
    if d > 0:
        time.sleep(d)
    else:
        nxt = time.monotonic()
f.close()
