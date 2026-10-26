#!/usr/bin/env python3
"""Round-4 spot checks.

Usage: python3 -I r4_checks.py <path-to-tb/tools> <dir holding r3_probe.py>

1. The arm-adjacent void (one DUT corruption one sample beside a planted arm)
   at arm tolerance 0 as well as 2.
2. Whether the reading "one-word corruption = unbalanced dropped 2048" is
   byte-consistent: the bytes after the excursion against a +2048 track.
"""
import json
import struct
import sys

sys.path.insert(0, sys.argv[2])
sys.argv = [sys.argv[0], sys.argv[1]]
import r3_probe as p  # noqa: E402

t = p.tc()
F = 16384


def grade(ops, tol):
    aops, alog = p.arms(F)
    out = p.build(F, aops + ops)
    cap = struct.pack(">" + "I" * (p.C * F), *(w for f in out for w in f))
    v, d = t.grade_audio_counter_capture(cap, t.CounterCapture(p.C, "big", 48000, 0.0, 0.0),
                                         t.CounterRunLog(alog, [], tol), required_s=(F - 126) / 48000)
    return v, [a["index"] for a in d.get("planted_missed", [])], [p.brief(e) for e in d["events"] if e["attribution"] == "dut"]


for tol in (0, 2):
    for ops in ([("xor", 299, 0, 0x40000)], [("xor", 299, 2, 0x200)], [("xor", 499, 1, 0x80000)],
                [("xor", 699, 1, 0x100000)], [("xor", 701, 1, 0x01000000)], [("xor", 16183, 1, 0x200)],
                [("xor", 298, 0, 0x40000)], [("xor", 297, 0, 0x40000)]):
        print("ADJ tol", tol, json.dumps(ops), json.dumps(grade(ops, tol)))
ops = [("xor", 4085, 2, 0x100)] + [("xor", 4088 + k, 2, 0x80000) for k in range(100)]
v, missed, dut = grade(ops, 2)
print("UNBALANCED", v, json.dumps(dut))
a = p.build(F, p.arms(F)[0] + ops)
b = p.build(F, p.arms(F)[0] + ops + [("shift", 4085, 2048, 2)])
diff = sum(a[i][2] != b[i][2] for i in range(4200, 15000))
print("UNBALANCED words 4200..14999 on ch2 that differ between the capture and a +2048 track:", diff)
net = sum(e["n"] if e["class"] == "dropped" else -e["n"] for e in dut if e["channel"] == 2 and e["class"] in ("dropped", "repeated"))
print("UNBALANCED net DUT slip reported on ch2:", net, "true net: 0")
