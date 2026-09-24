#!/usr/bin/env python3
"""Join the round-1 and round-2 mutation tables by probe name: exit and failed-check count."""
import re
import sys


def load(path):
    out = {}
    for ln in open(path, encoding="utf-8"):
        m = re.match(r"(\S+)\s+EXIT (\d+)\s+fails=(\d+)", ln)
        if m:
            out[m.group(1)] = (int(m.group(2)), int(m.group(3)))
    return out


r1, r2 = load(sys.argv[1]), load(sys.argv[2])
print(f"{'probe':<30} {'r1 exit/fails':<14} {'r2 exit/fails':<14} note")
for k in sorted(set(r1) | set(r2)):
    a, b = r1.get(k), r2.get(k)
    fa = f"{a[0]}/{a[1]}" if a else "-"
    fb = f"{b[0]}/{b[1]}" if b else "-"
    if a and b and a[0] == 0 and b[0] != 0:
        note = "round-1 survivor, now KILLED"
    elif a and b and a[0] != 0 and b[0] == 0:
        note = "REGRESSION: killed in round 1, survives now"
    elif not a:
        note = "round-2 addition"
    elif k.endswith("_phc") and a != b:
        note = "step-suite count differs"
    else:
        note = ""
    print(f"{k:<30} {fa:<14} {fb:<14} {note}")
