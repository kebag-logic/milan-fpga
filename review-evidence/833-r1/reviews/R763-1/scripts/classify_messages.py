#!/usr/bin/env python3
"""Classify CLEANUP FAILED messages by the states they list.

Usage: classify_messages.py all-cleanup-failed-messages.txt
A listed process whose parent is not itself listed has the owner as parent:
the census lists every descendant, and a dead parent's child is re-parented.
"""
import re, sys
rows = []
for line in open(sys.argv[1]):
    m = re.search(r"CLEANUP FAILED: owned descendants remain after ([0-9.]+) s.*?: (.*)$", line)
    if not m:
        continue
    procs = [re.match(r"pid (\d+) \((.*?)\) state (\S) wchan (\S+) parent (\d+) \((.*?)\).*?, (.*)$", p.strip()).groups()
             for p in m.group(2).split("; ")]
    listed = {p[0] for p in procs}
    states = {p[2] for p in procs}
    cls = "D (uninterruptible after SIGKILL)" if "D" in states else (
          "T shell holding Z child" if "T" in states else "Z, parent is the owner")
    owner_parent = all(p[4] not in listed for p in procs if p[2] == "Z" and cls.startswith("Z"))
    rows.append((cls, line.split(":", 1)[0], m.group(1),
                 " | ".join(f"{p[1]} {p[2]} {p[3]} parent={'owner' if p[4] not in listed else p[4]} {p[6]}" for p in procs),
                 owner_parent))
from collections import Counter
for r in rows:
    print(f"{r[0]:36} {r[1]:55} {r[2]:>5}s  {r[3]}")
print(Counter(r[0] for r in rows), "total", len(rows))
