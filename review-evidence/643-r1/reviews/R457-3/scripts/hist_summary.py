#!/usr/bin/env python3
"""R457-2: summarise receipts/hist/*.log (the sound design's --law-boundary
leg in three histories at both processors): per (processor, history) the
graded/NOT GRADABLE outcome per phase, graded failures, and the largest
offset range in any window. Prints a TSV table and the per-history summary.

usage: hist_summary.py <receipts/hist>
"""
import glob
import os
import re
import sys

d = sys.argv[1]
B = re.compile(r"\[BOUNDARY\] \+(\d+): (graded PASS|graded FAIL|NOT GRADABLE), (\d+) check")
W = re.compile(r"(T30 INTERNAL LAW \+(\d+)): over \d+ steady PDU ends the first pop after the end is "
               r"taken ([+-]\d+)\.\.([+-]\d+) cycles from it and the pop nearest the boundary "
               r"([+-]\d+)\.\.([+-]\d+) \(walk (\d+)\); the least clearance is (\d+)")
groups = {}
for f in sorted(glob.glob(os.path.join(d, "*.log"))):
    name = os.path.basename(f)[:-4]
    proc, hist = name.split("-", 1)
    hist = "alone" if hist.startswith("alone") else hist
    t = open(f, errors="replace").read()
    rc = open(f[:-4] + ".rc").read().strip()
    g = groups.setdefault((proc, hist), {"out": {}, "rng": 0, "walk": 0, "rc": set(), "fails": 0})
    g["rc"].add(rc)
    g["fails"] += t.count("[FAIL]")
    for m in B.finditer(t):
        g["out"][int(m[1])] = m[2]
    for m in W.finditer(t):
        n0, n1, d0, d1, w = (int(m[i]) for i in (3, 4, 5, 6, 7))
        rs = [x for x in (n1 - n0, d1 - d0) if x < 1000]
        g["rng"] = max(g["rng"], max(rs))
        g["walk"] = max(g["walk"], w)


def runs(ps):
    out, cur = [], None
    for p in sorted(ps):
        if cur and p == cur[1] + 1:
            cur[1] = p
        else:
            cur = [p, p]
            out.append(cur)
    return ", ".join(f"+{a}..+{b}" if a != b else f"+{a}" for a, b in out) or "none"


print("processor\thistory\tphases\tgraded_pass\tgraded_fail\tnot_gradable\tmax_reported_walk\tmax_offset_range\tFAIL_lines\trc")
for (proc, hist), g in sorted(groups.items()):
    o = g["out"]
    ng = [p for p, v in o.items() if v == "NOT GRADABLE"]
    print("\t".join(map(str, (proc, hist, len(o), sum(v == "graded PASS" for v in o.values()),
                              sum(v == "graded FAIL" for v in o.values()), runs(ng),
                              g["walk"], g["rng"], g["fails"], ",".join(sorted(g["rc"]))))))
