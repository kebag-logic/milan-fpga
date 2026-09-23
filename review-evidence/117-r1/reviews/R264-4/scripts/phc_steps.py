#!/usr/bin/env python3
"""Observation 7: DUT PHC step at each adoption (console TAI_NS) against the
interval between consecutive switch power-on commands (power-strip logs; the
attempt 1 guard's early ON counts as that attempt's power-on).
usage: phc_steps.py <bench-a202 root>"""
import os
import re
import sys
from datetime import datetime, timezone

root = os.path.join(sys.argv[1], "bench")
ons = [float(re.findall(r"^(\d{10}\.\d+)\nOUT4 -> ON", open(os.path.join(root, "attempt1-aborted", "lock.txt")).read(), re.M)[0])]
for c in range(1, 7):
    ons.append(float(re.search(r"T_ON_CMD (\S+)", open(os.path.join(root, f"cycle{c}", "powerstrip.txt")).read()).group(1)))
for c in range(1, 7):
    txt = open(os.path.join(root, f"cycle{c}", "console.txt"), errors="replace").read()
    S = []
    for b in re.split(r"^### ", txt, flags=re.M)[1:]:
        m = re.match(r"(\S+) cmd='milan_status'", b)
        if m and "TAI_NS=" in b:
            t = datetime.strptime(m.group(1), "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc).timestamp()
            S.append((t, int(re.search(r"TAI_NS=(0x[0-9a-f]+)", b).group(1), 16) / 1e9, re.search(r"GPTP_GM=(\w+)", b).group(1)))
    steps = []
    for (t1, p1, g1), (t2, p2, g2) in zip(S, S[1:]):
        d = (p2 - p1) - (t2 - t1)
        if abs(d) > 1.0:
            steps.append((round(d, 2), g1, g2))
    print(f"cycle {c}: PHC steps {steps}; interval between on commands {ons[c] - ons[c - 1]:.2f} s")
