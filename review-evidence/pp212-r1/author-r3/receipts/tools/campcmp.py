#!/usr/bin/env python3
"""campcmp.py <old camp log> <new camp log>: per arm entry (label, in order), the failure count and tags of
each run; prints the entries whose count or tags differ, and the entries only in one run."""
import re
import sys
from collections import defaultdict

def load(path):
    out = defaultdict(list)
    for line in open(path):
        m = re.match(r"^(\S+): rc=(\d+) failures=(\d+) (KILLED|UNPROVEN) tags=(.*)$", line.strip())
        if m:
            out[m.group(1)].append((int(m.group(3)), m.group(4), m.group(5)))
    return out

old, new = load(sys.argv[1]), load(sys.argv[2])
for label in sorted(set(old) | set(new)):
    a, b = old.get(label), new.get(label)
    if a is None:
        print(f"NEW   {label}: {b}")
    elif b is None:
        print(f"GONE  {label}: {a}")
    elif a != b:
        print(f"MOVED {label}: {a} -> {b}")
print(f"old {sum(len(v) for v in old.values())} entries, new {sum(len(v) for v in new.values())} entries")
