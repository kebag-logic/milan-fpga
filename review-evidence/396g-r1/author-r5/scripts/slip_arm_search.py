#!/usr/bin/env python3
"""Whole-block DUT slips near every arm, F = 8192 and 16384, tolerance 2: verdicts at two planner copies.

Usage: python3 -I slip_arm_search.py <tools A> <tools B> [jobs]   prints cases whose verdicts differ.
"""
import sys, json
from multiprocessing import get_context
A, B = sys.argv[1], sys.argv[2]
JOBS = int(sys.argv[3]) if len(sys.argv) > 3 else 8

def load(path):
    import importlib.util
    spec = importlib.util.spec_from_file_location("tc_" + str(abs(hash(path))), path + "/torture_campaign.py")
    mod = importlib.util.module_from_spec(spec); sys.modules[spec.name] = mod; spec.loader.exec_module(mod)
    return mod

MODS = {}
def arms(F):
    return [("dropped", 300, 3, None), ("repeated", 500, 2, None), ("bit-flip", 700, 0x100, 1),
            ("dropped", F - 700, 3, None), ("repeated", F - 450, 2, None), ("bit-flip", F - 200, 0x100, 1)]

def grade(t, F, extra):
    ev, log = [], []
    for cls, at, size, ch in arms(F):
        if cls == "bit-flip":
            ev.append(dict(kind="flip", index=at, channel=ch, mask=size)); log.append({"class": cls, "index": at, "mask": size, "channel": ch})
        else:
            ev.append(dict(kind="drop" if cls == "dropped" else "repeat", index=at, n=size)); log.append({"class": cls, "index": at, "n": size})
    cap = t.synthesize_counter_capture(F, 4, events=ev + extra)
    v, d = t.grade_audio_counter_capture(cap, t.CounterCapture(4, "big", 48000, 0.0, 0.0), t.CounterRunLog(log, [], 2),
                                         required_s=(F - 126) / 48000)
    return v, [a["index"] for a in d["planted_missed"]]

def case(args):
    F, ai, k, n, scope = args
    out = []
    for path in (A, B):
        if path not in MODS: MODS[path] = load(path)
        t = MODS[path]
        at = arms(F)[ai][1] + k
        extra = [dict(kind="drop" if n > 0 else "repeat", index=at, n=abs(n))] if scope == "all" else []
        if scope != "all":
            return args, None, None
        out.append(grade(t, F, extra))
    return args, out[0], out[1]

if __name__ == "__main__":
    cases = [(F, ai, k, n, "all") for F in (8192, 16384) for ai in range(6) for k in range(-4, 5)
             for n in (2048, -2048, 4096, -4096, 8192, 1, -1, 3, -2)]
    with get_context("fork").Pool(JOBS) as pool:
        res = pool.map(case, cases, chunksize=8)
    diff = 0
    for args, a, b in res:
        if a != b:
            diff += 1; print("DIFF", args, a, b)
    print("SUMMARY", len(res), "differ", diff)
