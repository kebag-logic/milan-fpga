#!/usr/bin/env python3
"""Per cycle: the console interval in which LINKG_STAT (0x774) went 0x83 ->
0x03, relative to the switch's last frame on the DUT link (tap port 2).
usage: linkg_brackets.py <bench-a202 root>"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rederive_step3 import console, offsets, ptp_records  # noqa: E402

root = os.path.join(sys.argv[1], "bench")
for c in range(1, 7):
    d = os.path.join(root, f"cycle{c}")
    off = offsets(os.path.join(d, "clock-before.jsonl"))
    t0 = float(re.search(r"T_OFF_CMD (\S+)", open(os.path.join(d, "powerstrip.txt")).read()).group(1)) - off["pi"]
    srv = [v for k, v in off.items() if k.startswith("ubuntu")][0]
    S, _ = console(os.path.join(d, "console.txt"))
    L = [(s["t"] - t0, s.get("0x774")) for s in S if s.get("0x774") is not None]
    i = next(k for k, (t, v) in enumerate(L) if t > 0 and v == 0x03)
    last = max(t - srv - t0 for t, port, fr in ptp_records(os.path.join(d, f"tap-c{c}.pcap")) if port == 2 and t - srv - t0 < 20)
    print(f"cycle {c}: switch last frame {last:.2f} s; LINKG 0x83 at {L[i-1][0]:.2f}, 0x03 at {L[i][0]:.2f}; "
          f"edge after last frame in ({L[i-1][0]-last:.2f}, {L[i][0]-last:.2f}] s")
