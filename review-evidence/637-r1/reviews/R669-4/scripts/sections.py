#!/usr/bin/env python3
"""Tally an obj_dynmap leg log by section: preamble, [DYNMAP], [762-DP], [MAPREC].
Usage: python3 -I sections.py <leg log>"""
import re, sys
order = ["preamble", "DYNMAP", "762-DP", "MAPREC"]
heads = [(re.compile(r"^-- \[DYNMAP\]"), "DYNMAP"),
         (re.compile(r"^-- \[762-DP\] the AX7101 1x1 TDM8 geometry"), "762-DP"),
         (re.compile(r"^-- \[MAPREC\] #637: the channel-map records"), "MAPREC")]
cur = "preamble"; tally = {k: [0, 0] for k in order}; fails = []; leg = None
for line in open(sys.argv[1], errors="replace"):
    for rx, name in heads:
        if rx.match(line) and order.index(name) > order.index(cur):
            cur = name
    m = re.match(r"^\s*\[(ok|FAIL)\]\s", line)
    if m:
        tally[cur][0] += 1
        if m.group(1) == "FAIL":
            tally[cur][1] += 1; fails.append(f"{cur}: {line.strip()}")
    m = re.match(r"^checks: (\d+)\s+failures: (\d+)", line)
    if m: leg = (int(m.group(1)), int(m.group(2)))
for k in order: print(f"section {k}: {tally[k][0]} checks, {tally[k][1]} failures")
print(f"sum: {sum(v[0] for v in tally.values())}/{sum(v[1] for v in tally.values())}; leg line: {leg}")
for f in fails: print("  " + f)
