#!/usr/bin/env python3
"""Per-instance LUT/FF delta between two Vivado hierarchical utilization reports."""
import sys
def rows(p):
    out, stack = {}, []
    for l in open(p):
        c = l.split("|")
        if len(c) > 7 and c[3].strip().isdigit():
            depth = (len(c[1]) - len(c[1].lstrip(" "))) // 2
            stack = stack[:depth] + [c[1].strip()]
            out["/".join(stack)] = (int(c[3]), int(c[7]))
    return out
b, n = rows(sys.argv[1]), rows(sys.argv[2])
print(f"{'instance':32} {'dLUT':>6} {'dFF':>6}")
for k in n:
    if k in b and n[k] != b[k]:
        print(f"{k:32} {n[k][0]-b[k][0]:>6} {n[k][1]-b[k][1]:>6}")
