#!/usr/bin/env python3
"""Print the full DUT event list, and byte-identity checks, for named round-4 cases.

Usage: python3 -I r4_detail.py <path-to-tb/tools> <dir holding r3_probe.py>
"""
import json
import sys

sys.path.insert(0, sys.argv[2])
sys.argv = [sys.argv[0], sys.argv[1]]
import r3_probe as p  # noqa: E402


def xs(begin, length, ch, mask):
    return [("xor", begin + k, ch, mask) for k in range(length)]


F = 16384
CASES = {
    # A DUT slip (all channels) shortly before a constant-mask excursion on channel 2.
    "slip3-17-before-0x80000-L100-b3000": [("shift", 2983, 3)] + xs(3000, 100, 2, 0x80000),
    "slip-2-1-before-0x100-L100-b3000": [("shift", 2999, -2)] + xs(3000, 100, 2, 0x100),
    "slip3-63-before-0x40000-L300-b3000": [("shift", 2937, 3)] + xs(3000, 300, 2, 0x40000),
    "slip3-17-before-0x80000-L100-b3000-ch2-only": [("shift", 2983, 3, 2)] + xs(3000, 100, 2, 0x80000),
    "slip100-17-before-0x80000-L100-b3000": [("shift", 2983, 100)] + xs(3000, 100, 2, 0x80000),
    "slip3-64-before-0x80000-L100-b3000 (control)": [("shift", 2936, 3)] + xs(3000, 100, 2, 0x80000),
    "no-slip-0x80000-L100-b3000 (control)": xs(3000, 100, 2, 0x80000),
    # A one-word corruption adjacent to (or one clean word from) a constant-mask excursion.
    "0x100-adjacent-before-0x80000-L100-b4089": [("xor", 4088, 2, 0x100)] + xs(4089, 100, 2, 0x80000),
    "0x80000-adjacent-before-0x80100-L100-b3000": [("xor", 2999, 2, 0x80000)] + xs(3000, 100, 2, 0x80100),
    "0x80000-gap2-before-0x80100-L100-b4089": [("xor", 4087, 2, 0x80000)] + xs(4089, 100, 2, 0x80100),
    "0x100-adjacent-before-0xF00F00-L100-b3000": [("xor", 2999, 2, 0x100)] + xs(3000, 100, 2, 0x00F00F00),
}
for name, ops in CASES.items():
    v, d, dut = p.grade(F, ops)
    print(name, v, d.get("why"), json.dumps(d.get("planted_missed")))
    for e in dut:
        print("   ", json.dumps(p.brief(e)))
# Byte identities offered by the grader's readings.
same = lambda a, b: p.build(F, p.arms(F)[0] + a) == p.build(F, p.arms(F)[0] + b)  # noqa: E731
print("IDENTITY 0x100@4088 == drop2048@4088+repeat2048@4089 on ch2:",
      same([("xor", 4088, 2, 0x100)], [("shift", 4088, 2048, 2), ("shift", 4089, -2048, 2)]))
