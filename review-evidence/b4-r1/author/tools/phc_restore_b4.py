#!/usr/bin/env python3
"""Put the controller NIC's PHC back on the frequency and trajectory recorded
before this lane's first slave-only gPTP run (controller host, under sudo; the
caller holds the bench lock). Lane B1's recorded method (packet b1-a438,
tools/phc_restore.py), as lane B3 copied it, with lane B4's readings.

usage: phc_restore.py <phc_ctl> <iface>

The two readings below are phc_ctl `freq cmp` outputs taken at the first
session's end snapshot and at the second session's start baseline, both
before any gPTP daemon ran: monotonic stamp (s) and PHC offset from
CLOCK_REALTIME (ns), at 0.000000 ppb, the frequency found.
"""
import re
import subprocess
import sys

PC, IFACE = sys.argv[1], sys.argv[2]
FREQ = "0"
M1, X1 = 38267.069, 2303090729
M2, X2 = 39772.619, 2357630234


def run(*a):
    r = subprocess.run(["sudo", "-n", PC, IFACE, *a], capture_output=True, text=True, timeout=20)
    print(r.stdout.strip())
    assert r.returncode == 0, r.stderr
    return r.stdout


rate = (X2 - X1) / (M2 - M1)
run("freq", "cmp")
run("freq", FREQ)
out = run("cmp")
m = float(re.findall(r"phc_ctl\[([0-9.]+)\]", out)[-1])
x = int(re.findall(r"is (-?\d+)ns", out)[-1])
target = X2 + rate * (m - M2)
d = (x - target) / 1e9
print(f"rate_ns_per_s={rate:.3f} now_offset={x} target_offset={target:.0f} adjust_s={d:.9f}")
run("adj", f"{d:.9f}")
out = run("freq", "cmp")
m = float(re.findall(r"phc_ctl\[([0-9.]+)\]", out)[-1])
x = int(re.findall(r"is (-?\d+)ns", out)[-1])
print(f"residual_from_original_trajectory_ns={x - (X2 + rate * (m - M2)):.0f}")
