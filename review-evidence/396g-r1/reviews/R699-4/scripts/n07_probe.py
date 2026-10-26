#!/usr/bin/env python3
"""N07 equivalence check and block-slip-then-flip detail.

Usage: python3 -I n07_probe.py <path-to-tb/tools> <dir holding grader_probe_r2.py>
Prints the events at the loss index (their acquisition index must include the
loss logged at that index), then channel 2's events for a whole-block slip
followed by a one-word flip.
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
AT, F, C, RATE = gp.AT, gp.F, gp.C, gp.RATE
anchors = [(4096, 4096 / RATE, 4096 / RATE), (F, (F + 9) / RATE, (F + 9) / RATE)]
v, d, _ = gp.grade(F, C, [('shift', AT, 9), ('xor', AT, 2, 0x80000)], losses=[{"index": AT, "frames": 9}],
                   anchors=anchors, steps=())
for e in d["events"]:
    if e["capture_index"] == AT:
        print(json.dumps({k: e.get(k) for k in ("channel", "class", "attribution", "acquisition_index", "wall_s")}))
print("want acquisition_index", AT + 9, "wall", (AT + 9) / RATE)
for gap in (5, 80):
    v, d, _ = gp.grade(F, C, [('shift', 8205, 4096), ('xor', 8205 + gap, 2, 0x80000)])
    print("block-slip-then-flip gap", gap, json.dumps([e for e in gp.full(d) if e["channel"] == 2]))
