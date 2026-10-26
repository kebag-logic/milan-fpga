#!/usr/bin/env python3
"""Print the full DUT event list for named r3_probe cases.

Usage: python3 -I r3_detail.py <path-to-tb/tools> <dir holding r3_probe.py>
"""
import json
import sys

sys.path.insert(0, sys.argv[2])
sys.argv = [sys.argv[0], sys.argv[1]]
import r3_probe as p  # noqa: E402

CASES = {
    "E-4096-at-F-150": (8192, [("shift", 8192 - 150, 4096)]),
    "E--4096-at-F-150": (8192, [("shift", 8192 - 150, -4096)]),
    "E-clean-arms-only": (8192, []),
    "A-drop4096-5-after-flip": (16384, [("shift", 705, 4096)]),
    "A-drop4096-5-after-repeat": (16384, [("shift", 505, 4096)]),
    "A-drop1024-200-before-repeat": (16384, [("shift", 300, 1024)]),
    "A-ch1-0x80000x100-ends-5-before-flip": (16384, [("xor", 595 + k, 1, 0x80000) for k in range(100)]),
    "M-0x100-at-6143-n-2049": (16384, [("xor", 6143 + k, 2, 0x100) for k in range(2049)]),
}
for name, (frames, ops) in CASES.items():
    v, d, dut = p.grade(frames, ops)
    print(name, v, d.get("why"), json.dumps(d.get("planted_missed")))
    for e in dut:
        print("   ", json.dumps(p.brief(e)))
