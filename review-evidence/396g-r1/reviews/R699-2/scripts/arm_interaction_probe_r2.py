#!/usr/bin/env python3
"""Planted arms next to other events within one 64-sample window.

Usage: python3 -I arm_interaction_probe_r2.py <path-to-tb/tools> <dir holding grader_probe_r2.py>
Round-1 F1's required outcome: a DUT defect with every planted arm present must
not void the run. Each line: <id> <OK|DEVIATION> [verdict, why, missed arms, DUT events].
"""
import contextlib
import io
import json
import sys

tools, here = sys.argv[1], sys.argv[2]
sys.path.insert(0, here)
sys.argv = [sys.argv[0], tools]
with contextlib.redirect_stdout(io.StringIO()):
    import grader_probe_r2 as gp  # noqa: E402
F, C = gp.F, gp.C


def arms_at(starts, gap):
    ops, log = [], []
    for s in starts:
        ops += [('shift', s, 3), ('shift', s + gap, -2), ('xor', s + 2 * gap, 1, 0x100)]
        log += [{"class": "dropped", "index": s, "n": 3}, {"class": "repeated", "index": s + gap, "n": 2},
                {"class": "bit-flip", "index": s + 2 * gap, "mask": 0x100, "channel": 1}]
    return ops, log


def show(pid, ops, log, want):
    v, d, _ = gp.grade(F, C, ops, ops_arms=False, log=log)
    dut = [(e["channel"], e["capture_index"], e["class"], e.get("n"), e.get("mask")) for e in gp.full(d)]
    gp.line(pid, v == want, [v, d.get("why"), [(a["class"], a["index"]) for a in d.get("planted_missed", [])], dut[:6]])


for gap in (10, 40, 63, 64, 70, 100, 200):
    ops, log = arms_at((100, F - 900), gap)
    show(f"A1-arms-{gap}-apart-clean", ops, log, "PASS")
ops, log = arms_at((100, F - 900), 200)
for at in (495, 498, 470, 440, 430):
    show(f"A2-dut-drop1-all-channels-at-{at}-before-flip-arm-500", ops + [('shift', at, 1)], log, "FAIL")
show("A3-dut-drop1-all-channels-at-505-after-flip-arm", ops + [('shift', 505, 1)], log, "FAIL")
show("A4-dut-pos-flip-ch0-at-110-after-drop-arm", ops + [('xor', 110, 0, 0x80000)], log, "FAIL")
show("A5-dut-pos-flip-ch1-at-320-after-repeat-arm", ops + [('xor', 320, 1, 0x80000)], log, "FAIL")
