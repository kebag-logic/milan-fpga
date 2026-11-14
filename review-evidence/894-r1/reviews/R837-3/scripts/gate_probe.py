#!/usr/bin/env python3
"""Independent model of THE PACE gate (aecp_mbx.c ready: now - edited_ms >= P, whole ms; the stamp the
clock read as the record is taken): edits always waiting, the first taken at sub-ms phase phi, each next
at the first microsecond whose whole ms is P past the last stamp. For every window of 0.01 to 120 ms
(0.01 steps) and P of 1 to 13, the most edits any phase puts in a window opening at the first take,
against paced_rows.edits (argv[1] = the tree)."""
import math, sys
sys.path.insert(0, sys.argv[1] + '/tb/verilator/ctrl_service_budget')
import paced_rows

def takes(phi_us, pace, w_us):
    t, n = phi_us, 1                       # first take at phi within ms 0
    while True:
        stamp = t // 1000
        t = (stamp + pace) * 1000          # first us whose whole ms is P past the stamp
        if t - phi_us > w_us:
            return n
        n += 1

phases = sorted(set(range(0, 1000, 37)) | {998, 999})
bad = under = 0
for pace in range(1, 14):
    for h in range(1, 12001):
        w_us = 10 * h
        most = max(takes(phi, pace, w_us) for phi in phases)
        if most != paced_rows.edits(h / 100, pace):
            bad += 1
        if 1 + math.floor(h / 100 / pace) < most:
            under += 1
print(f"windows x paces checked: {13 * 12000}; edits() != simulated gate: {bad}; "
      f"earlier rule 1 + floor(w/P) under the gate: {under}")
