#!/usr/bin/env python3
"""Put the controller NIC's PHC back on the frequency and trajectory recorded
before this lane's first slave-only gPTP run (controller host, under sudo; the
caller holds the bench lock). Lane B1's recorded method (packet b1-a438,
tools/phc_restore.py) with this lane's readings.

usage: phc_restore.py <phc_ctl> <iface>

The two readings below are phc_ctl `freq cmp` outputs taken at the identity
gate and at the start baseline, both before any gPTP daemon ran: monotonic
stamp (s) and PHC offset from CLOCK_REALTIME (ns), at 28062.332153 ppb.
"""
import re
import subprocess
import sys

PC, IFACE = sys.argv[1], sys.argv[2]
FREQ = "28062.332153"
M1, X1 = 160966.373, 1790532372171772086
M2, X2 = 161057.606, 1790532372172467118


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
