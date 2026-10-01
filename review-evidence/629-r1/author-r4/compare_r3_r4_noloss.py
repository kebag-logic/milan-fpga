#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Compare the round-4 model's no-loss E8-P2 shape cases with the round-3
model's published output (meter_rules_model_r3.out, round 3 packet), field by
field: valid, restarts, open_max, closed<2ppm, closed_max, drops, t_lock_s."""
import re
import sys

r3_path, r4_path = sys.argv[1], sys.argv[2]
pat3 = re.compile(r"^(\S+)\s+J=\s*(\d+) ppm=\s*(\d+) E8 -P2 valid=\s*([\d.]+) "
                  r"restarts=\s*(\d+) open<2ppm=\s*[\d.]+ open_max=\s*(\d+) "
                  r"lock4=\s*[\d.]+ \| closed<2ppm=\s*([\d.]+) "
                  r"closed_max=\s*(\d+) drops=\s*(\d+) t_lock_s=\s*(\S+)")
pat4 = re.compile(r"^(\S+)\s+J=\s*(\d+) ppm=\s*(\d+) g=1.0 loss=none\s+E8-P2-b "
                  r"valid=\s*([\d.]+) restarts=\s*(\d+) lossvoids=\s*\d+ "
                  r"fills=\s*\d+ open_max=\s*(\d+) \| closed<2ppm=\s*([\d.]+) "
                  r"closed_max=\s*(\d+) drops=\s*(\d+) lockedfrac=\s*[\d.]+ "
                  r"t_lock_s=\s*(\S+)")
r3 = {}
for line in open(r3_path):
    m = pat3.match(line)
    if m:
        r3[m.group(1, 2, 3)] = m.groups()[3:]
n = same = 0
for line in open(r4_path):
    m = pat4.match(line)
    if not m:
        continue
    key = m.group(1, 2, 3)
    n += 1
    a, b = r3.get(key), m.groups()[3:]
    ok = a == b
    same += ok
    print(f"{' '.join(key):22s} r3={a} r4={b} {'match' if ok else 'DIFFERS'}")
print(f"compared {n} cases; identical {same}")
sys.exit(0 if n and n == same else 1)
