#!/usr/bin/env python3
"""Per cycle: CLKV_TUCNT delta (console mem_read 0x90000780) and the span with tu=1.

Usage: step3_tucnt.py <evidence-root>
"""
import datetime as dt
import os
import re
import sys

root = sys.argv[1]
for c in range(1, 7):
    txt = open(os.path.join(root, "bench-a202", "bench", f"cycle{c}", "console.txt"), errors="replace").read()
    tucnt = [int("".join(m.group(1).split()[::-1]), 16) for m in
             re.finditer(r"cmd='mem_read 0x90000780 4'.*?\n0x90000780  ((?:[0-9a-f]{2} ){4})", txt, re.S)]
    tus = []
    for m in re.finditer(r"^### (\S+) cmd='milan_status'[^\n]*\n(.*?)(?=^### |\Z)", txt, re.M | re.S):
        f = dict(re.findall(r"(\w+)=(\S+)", m.group(2)))
        if "TU" in f:
            ts = dt.datetime.strptime(m.group(1), "%Y-%m-%dT%H:%M:%S.%fZ").timestamp()
            tus.append((ts, f["TU"]))
    ones = [t for t, v in tus if v == "1"]
    print(f"cycle {c}: CLKV_TUCNT first {tucnt[0]} last {tucnt[-1]} delta {tucnt[-1]-tucnt[0]}; tu=1 samples {len(ones)} span {ones[-1]-ones[0]:.2f} s")
