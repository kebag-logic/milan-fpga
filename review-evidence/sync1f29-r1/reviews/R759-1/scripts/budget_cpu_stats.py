#!/usr/bin/env python3
"""Summarise a budget arm's results directory: CPU cycles per instruction and the flash window and refill costs over every group's summary. usage: budget_cpu_stats.py <results dir>"""
import glob, json, sys
tot_cpu = tot_instr = 0
keys = {}
for f in sorted(glob.glob(sys.argv[1] + "/*.json")):
    if f.endswith(("results.json", "build.json")):
        continue
    s = json.load(open(f)).get("summary", {})
    tot_cpu += int(s.get("cpu", 0)); tot_instr += int(s.get("instr", 0))
    for k, v in s.items():
        if "/" in str(v):
            keys.setdefault(k, []).append(v)
print("CPI over groups", round(tot_cpu / tot_instr, 2) if tot_instr else None)
for k, vs in keys.items():
    # count/sum/min/max per group, as the testbench prints them
    p = [tuple(int(x) for x in v.split("/")) for v in vs if v.count("/") == 3]
    if p:
        n = sum(x[0] for x in p); s = sum(x[1] for x in p)
        print(k, "count", n, "mean", round(s / n, 2) if n else "-", "min", min(x[2] for x in p if x[0]) if n else "-", "max", max(x[3] for x in p) if n else "-")
