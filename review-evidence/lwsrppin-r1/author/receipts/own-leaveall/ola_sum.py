#!/usr/bin/env python3
"""Summarize OWN-LA lines per arm from an own_la.py log."""
import re, sys
arm = None; st = {}
for line in open(sys.argv[1], errors="replace"):
    if line.startswith("=== ARM"):
        arm = line.split()[2]; st[arm] = dict(w=0, none=0, worst=0, over=0, held=None)
    m = re.match(r"OWN-LA input=\d+ offset_ms=(\d+) leaveall_ms=\d+ withdrawn_ms=(\d+) lv_ms=(\S+)", line)
    if m and arm:
        s = st[arm]; s["w"] += 1
        if m.group(3).startswith("none"): s["none"] += 1
        else:
            d = int(m.group(3)) - int(m.group(2)); s["worst"] = max(s["worst"], d); s["over"] += d > 240
    if line.startswith("OWN-LA held") and arm: st[arm]["held"] = line.strip()[7:]
for a, s in st.items():
    print(f"{a}: withdrawals={s['w']} never_sent={s['none']} worst_ms={s['worst']} over_240={s['over']} | {s['held']}")
