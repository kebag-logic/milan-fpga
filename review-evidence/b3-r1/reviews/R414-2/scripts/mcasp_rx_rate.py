#!/usr/bin/env python3
"""Re-derive the McASP0 receive DMA period rate and capture-restart count from
the published SoC status logs: the 485c0100 chan1 Edge line (192-frame receive
periods) and chan1 Level line, each bracketed by the /proc/uptime read taken
just before the interrupt read.
usage: mcasp_rx_rate.py <status-before.log> <status-after.log> [...pairs]"""
import re, sys
def read(p):
    t = re.sub(r"\x1b\[[0-9;]*m", "", open(p, errors="replace").read())
    ups = [float(m.group(1)) for m in re.finditer(r"^(\d+\.\d+) \d+\.\d+$", t, re.M)]
    edge = int(re.search(r"^\s*125:\s+(\d+).*chan1$", t, re.M).group(1))
    level = int(re.search(r"^\s*143:\s+(\d+).*chan1$", t, re.M).group(1))
    return ups[-1], edge, level
a = sys.argv[1:]
for i in range(0, len(a), 2):
    (u0, e0, l0), (u1, e1, l1) = read(a[i]), read(a[i + 1])
    dt = u1 - u0
    print(f"{a[i]} -> {a[i+1]}: interval {dt:.2f} s, rx periods {e1-e0}, rate {(e1-e0)/dt:.2f} periods/s "
          f"({(e1-e0)*192/dt:.0f} frames/s), level (restart) delta {l1-l0}")
