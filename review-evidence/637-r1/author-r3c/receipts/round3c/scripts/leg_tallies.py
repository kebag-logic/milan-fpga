#!/usr/bin/env python3
"""Each sim leg's own tally in one milan_dp suite log: the executable a
run line names, then the next 'checks: N failures: M' (or 'NAME: N checks,
M failures') line, with the RESULT line after it.
usage: leg_tallies.py <log>"""
import re
import sys

cur = None
for line in open(sys.argv[1], errors="replace"):
    m = re.match(r'\s*\./(obj_[A-Za-z0-9_]+)/(V\w+)', line)
    if m:
        cur = m.group(1)
        continue
    m = re.match(r'checks: (\d+)\s+failures: (\d+)', line) or \
        re.match(r'[\w./-]+: (\d+) checks, (\d+) failures', line)
    if m and cur:
        print(f"{cur}\t{m.group(1)}\t{m.group(2)}")
        cur = None
