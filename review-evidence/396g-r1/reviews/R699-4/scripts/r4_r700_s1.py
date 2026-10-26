#!/usr/bin/env python3
"""The other reviewer's round-3 S1 equalities on channel 2, rebuilt with r3_probe's encoder, and their readings here.

Usage: python3 -I r4_r700_s1.py <path-to-tb/tools> <dir holding r3_probe.py>
"""
import json
import sys

sys.path.insert(0, sys.argv[2])
sys.argv = [sys.argv[0], sys.argv[1]]
import r3_probe as p  # noqa: E402

F = 8192
others = [("shift", 3000, 4096, c) for c in (0, 1, 3)]
pairs = (([("shift", 3000, 4096, 2), ("xor", 3001, 2, 0x100)], [("shift", 3005, 4096, 2)]),
         ([("shift", 3000, 4096, 2), ("xor", 3001, 2, 0x80000)], [("shift", 3001, -1024, 2), ("shift", 3002, 5120, 2)]))
for a, b in pairs:
    same = p.build(F, p.arms(F)[0] + others + a) == p.build(F, p.arms(F)[0] + others + b)
    v, d, dut = p.grade(F, others + a)
    print("EQUAL" if same else "DIFFER", json.dumps(a), "==", json.dumps(b), "->", v, len(d["planted_missed"]),
          json.dumps([p.brief(e) for e in dut if e["channel"] == 2]))
