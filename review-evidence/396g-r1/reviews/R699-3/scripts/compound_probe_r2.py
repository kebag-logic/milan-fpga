#!/usr/bin/env python3
"""Compound events: a slip followed within one 64-sample window by another event.

Usage: python3 -I compound_probe_r2.py <path-to-tb/tools> <dir holding grader_probe_r2.py>
Documented rule 3 (TESTING.md 6d): one word that leaves the track and returns
at once is a bit-flip, unless it equals a neighbouring received word. Each line:
    <id> <OK|DEVIATION> <channel 2 DUT events>
OK means channel 2 shows the slip, then the second event in its documented class.
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
F, C, AT = gp.F, gp.C, gp.AT


def ch2(ops):
    v, d, _ = gp.grade(F, C, ops)
    return v, [(e["capture_index"], e["class"], e.get("n"), e.get("mask")) for e in gp.full(d) if e["channel"] == 2]


for first_name, first in (("drop3", ('shift', AT, 3)), ("repeat2", ('shift', AT, -2)),
                          ("drop4096", ('shift', AT, 4096))):
    for gap in (5, 40, 100):
        second_at = AT + gap
        for mask in (0x80000, 0x40000, 0x100):
            v, ev = ch2([first, ('xor', second_at, 2, mask)])
            flips = [e for e in ev if e[1] == "bit-flip"]
            ok = len(flips) == 1 and flips[0][0] == second_at and flips[0][3] == f"0x{mask:08X}" and \
                sum(1 for e in ev if e[1] in ("dropped", "repeated")) == 1
            gp.line(f"K-{first_name}-then-flip-{mask:#x}-gap-{gap}", ok, [v, ev])
# Without a preceding slip (control): the same flip alone.
for mask in (0x80000, 0x40000):
    v, ev = ch2([('xor', AT + 5, 2, mask)])
    gp.line(f"K-control-flip-{mask:#x}-alone", ev == [(AT + 5, "bit-flip", 1, f"0x{mask:08X}")], [v, ev])
# A two-word burst with one mask after a slip (documented rule 4).
v, ev = ch2([('shift', AT, 3), ('xor', AT + 5, 2, 0x80000), ('xor', AT + 6, 2, 0x80000)])
gp.line("K-drop3-then-burst-0x80000x2-gap-5",
        [e[1] for e in ev] == ["dropped", "bit-flip"] and ev[1][2] == 2, [v, ev])
