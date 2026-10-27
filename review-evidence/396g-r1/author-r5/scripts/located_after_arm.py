#!/usr/bin/env python3
"""Whole-block (and short) DUT slips k = -64..64 samples from each arm, F = 8192 and 16384, tolerance 2:
verdict, and whether every DUT slip's located_within holds the true sample. Usage: located_after_arm.py <tools> [jobs]"""
import sys, json, collections
from multiprocessing import get_context
sys.path.insert(0, sys.argv[1])
JOBS = int(sys.argv[2]) if len(sys.argv) > 2 else 8
sys.argv = [sys.argv[0], sys.argv[1]]
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
from arm_d4 import arms, grade

def case(args):
    F, ai, k, n = args
    at = arms(F)[ai][1] + k
    v, d = grade(F, [dict(kind="drop" if n > 0 else "repeat", index=at, n=abs(n))])
    dut = [e for e in d["events"] if e["attribution"] == "dut"]
    outside = [(e["channel"], e["capture_index"], e.get("located_within")) for e in dut
               if e["class"] in ("dropped", "repeated") and not (
                   e.get("located_within", [e["capture_index"]] * 2)[0] <= at <= e.get("located_within", [e["capture_index"]] * 2)[1])]
    sizes = sorted((e["channel"], e["n"]) for e in dut if e["class"] in ("dropped", "repeated"))
    return args, v, [a["index"] for a in d["planted_missed"]], outside, sizes == [(c, abs(n)) for c in range(4)]

if __name__ == "__main__":
    cases = [(F, ai, k, n) for F in (8192, 16384) for ai in range(6) for k in list(range(-64, 0)) + list(range(1, 65))
             for n in (2048, -2048, 4096, -4096, 8192)]
    with get_context("fork").Pool(JOBS) as pool:
        res = pool.map(case, cases, chunksize=16)
    c = collections.Counter()
    for args, v, missed, outside, sized in res:
        F, ai, k, n = args
        key = (arms(F)[ai][0], "after" if k > 0 else "before")
        c[key + ("total",)] += 1
        if v != "FAIL" or missed: c[key + ("notfail",)] += 1; print("NOTFAIL", args, v, missed)
        if outside: c[key + ("outside",)] += 1; print("OUTSIDE", args, outside)
        if not sized: c[key + ("size",)] += 1; print("SIZE", args)
    for k in sorted(c): print("SUMMARY", k, c[k])
