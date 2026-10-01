#!/usr/bin/env python3
"""Planted-defect probe of the published grader's step classifier (grade_a.py steps_in),
extracted by AST and run on synthetic 24-bit pairs. usage: probe_grader_steps.py <grade_a.py>"""
import ast, sys
import numpy as np
src = open(sys.argv[1]).read()
fn = [n for n in ast.parse(src).body if isinstance(n, ast.FunctionDef) and n.name == "steps_in"][0]
ns = {"np": np, "FS": 48000}
def run(L, R):
    L = np.array(L, dtype=np.int64); R = np.array(R, dtype=np.int64)
    g = dict(ns, valid=((L >> 16) == 1) & ((R >> 16) == 2) & ((L & 0xFFFF) == (R & 0xFFFF)),
             torn=((L >> 16) == 1) & ((R >> 16) == 2) & ((L & 0xFFFF) != (R & 0xFFFF)),
             zero=(L == 0) & (R == 0), ordn=L & 0xFFFF)
    exec(compile(ast.Module(body=[fn], type_ignores=[]), "steps_in", "exec"), g)
    return g["steps_in"](0, len(L))
def pat(ns_):
    return [(1 << 16) | (n & 0xFFFF) if n is not None else 0 for n in ns_], [(2 << 16) | (n & 0xFFFF) if n is not None else 0 for n in ns_]
cases = {
    "clean 0..999": (list(range(1000)), dict(repeats=0, skip_events=0, torn=0, zero_frames=0, invalid_nonzero=0, backward=0)),
    "one repeat": (list(range(10)) + [9] + list(range(10, 20)), dict(repeats=1, skip_events=0)),
    "one-frame skip": (list(range(10)) + list(range(11, 20)), dict(skip_events=1, skip_single_frame=1, skipped_frames=1)),
    "six-frame skip": (list(range(10)) + list(range(16, 20)), dict(skip_events=1, skip_whole_packets=1, skipped_frames=6)),
    "backward": (list(range(10)) + list(range(5, 20)), dict(backward=1)),
    "wrap 65535->0": (list(range(65530, 65536)) + list(range(0, 6)), dict(skip_events=0, repeats=0, backward=0)),
    "zero frame inserted": (list(range(10)) + [None] + list(range(10, 20)), dict(zero_frames=1, skip_events=0)),
    "zero frame replacing (hidden skip)": (list(range(10)) + [None] + list(range(11, 20)), dict(zero_frames=1, skip_events=0)),
}
ok = True
for name, (seq, want) in cases.items():
    L, R = pat(seq); out = run(L, R)
    got = {k: out[k] for k in want}
    res = "OK" if got == want else "MISMATCH"; ok &= got == want
    print(f"{name}: {got} {res}")
L, R = pat(list(range(20))); R[7] = (2 << 16) | 99
out = run(L, R); print("torn frame:", out["torn"], "invalid_nonzero", out["invalid_nonzero"], "OK" if out["torn"] == 1 else "MISMATCH"); ok &= out["torn"] == 1
L, R = pat(list(range(20))); L[7] = (3 << 16) | 7
out = run(L, R); print("wrong tag:", out["invalid_nonzero"], "OK" if out["invalid_nonzero"] == 1 else "MISMATCH"); ok &= out["invalid_nonzero"] == 1
L, R = pat(list(range(20))); L[7] ^= 1; R[7] ^= 1
out = run(L, R); print("both ordinals flipped (bit error in both words):", {k: out[k] for k in ("repeats", "skip_events", "backward")},
                       "detected" if out["skip_events"] or out["backward"] or out["repeats"] else "NOT DETECTED")
print("ALL PLANTED CASES AS EXPECTED" if ok else "PROBE FAILED")
print("note: a zero frame that replaces a content frame is not graded as a skip (transitions next to it are ungraded)")
