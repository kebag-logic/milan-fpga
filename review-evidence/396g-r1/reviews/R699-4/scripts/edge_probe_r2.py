#!/usr/bin/env python3
"""Edge sweep for whole-block slips near the capture end and near other events.

Usage: python3 -I edge_probe_r2.py <path-to-tb/tools> <dir holding grader_probe_r2.py>
Prints one line per case with the DUT events the grader reports.
"""
import io
import json
import sys
import contextlib

tools, here = sys.argv[1], sys.argv[2]
sys.path.insert(0, here)
sys.argv = [sys.argv[0], tools]
with contextlib.redirect_stdout(io.StringIO()):
    import grader_probe_r2 as gp  # noqa: E402  (its own lines are discarded)

F, C = gp.F, gp.C


def show(name, ops, **kw):
    v, d, dut = gp.grade(F, C, ops, **kw)
    ev = gp.full(d)
    print(f"{name} {json.dumps([v, len(ev), ev[:2]])}", flush=True)


for back in (20, 40, 62, 63, 64, 70, 90, 100, 130):
    show(f"X1-block-slip-4096-at-end-minus-{back}", [('shift', F - back, 4096)])
for back in (20, 62, 63, 64, 100):
    show(f"X2-drop-3-at-end-minus-{back}", [('shift', F - back, 3)])
# A whole-block slip followed within 64 samples by a one-word flip.
for gap in (5, 30, 63, 64, 80):
    show(f"X3-block-slip-then-flip-gap-{gap}", [('shift', 8205, 4096), ('xor', 8205 + gap, 2, 0x80000)])
# A capture loss of a whole block in the last 63 samples.
show("X4-loss-4096-at-end-minus-30", [('shift', F - 30, 4096)], losses=[{"index": F - 30, "frames": 4096}])
