#!/usr/bin/env python3
"""R699-3 F2(a)'s shape at every gap: a 100-word 0x80000 or 0x40000 excursion on channel 2 from 3000,
plus one 0x100 word 1 to 64 samples before its start or after its end.

Usage: python3 -I r4_cf_full.py <path-to-tb/tools> <dir holding r3_probe.py>
Oracle: one 100-word bit-flip with the mask at 3000, the 0x100 word as its own one-word bit-flip,
nothing else, FAIL with every arm found. Prints each deviation and a summary.
"""
import json
import sys

sys.path.insert(0, sys.argv[2])
sys.argv = [sys.argv[0], sys.argv[1]]
import r3_probe as p  # noqa: E402

bad = total = 0
for mask in (0x80000, 0x40000):
    for side in ("before", "after"):
        for gap in range(1, 65):
            flip = 3000 - gap if side == "before" else 3099 + gap
            ops = [("xor", 3000 + k, 2, mask) for k in range(100)] + [("xor", flip, 2, 0x100)]
            v, d, dut = p.grade(16384, ops)
            got = sorted((e["channel"], e["capture_index"], e["class"], e.get("n"), e.get("mask")) for e in dut)
            want = sorted([(2, 3000, "bit-flip", 100, f"0x{mask:08X}"), (2, flip, "bit-flip", 1, "0x00000100")])
            total += 1
            if v != "FAIL" or d["planted_missed"] or got != want:
                bad += 1
                print("DEVIATION", f"0x{mask:X}", side, gap, v, json.dumps(got))
print("SUMMARY", total, "cases", bad, "deviations")
