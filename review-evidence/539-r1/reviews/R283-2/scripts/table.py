#!/usr/bin/env python3
"""Tabulate receipts/probes/*.log: exit, failed-check count, failing tags, summary."""
import glob
import os
import re
import sys

pkt = sys.argv[1]
rows = []
for f in sorted(glob.glob(os.path.join(pkt, "receipts/probes/*.log"))):
    name = os.path.basename(f)[:-4]
    lines = open(f, encoding="utf-8", errors="replace").read().splitlines()
    ex = lines[-1] if lines else "EXIT ?"
    fails = [ln for ln in lines if "[FAIL]" in ln]
    tags = sorted({m.group(1) for ln in fails for m in [re.search(r"\[(U\d+|P\d+[a-z]?)[\] ]", ln)] if m})
    summ = ""
    for ln in lines:
        if re.search(r"checks", ln) and re.search(r"failures", ln):
            summ = ln.strip()
    rows.append(f"{name:<30} {ex:<7} fails={len(fails):<4} {' '.join('['+t+']' for t in tags):<40} | {summ}")
print("\n".join(rows))
