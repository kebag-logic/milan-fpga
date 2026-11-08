#!/usr/bin/env python3
"""Reviewer check: every register the split placement ties in g_sp_amr (milan_datapath.sv) against
the value its all-fabric twin in g_af_amr takes in reset. Prints each pair and every departure.

Usage: amr_tie_check.py <repo checkout>
"""
import re
import sys
from pathlib import Path

src = (Path(sys.argv[1]) / "hdl/milan/milan_datapath.sv").read_text().splitlines()
start = next(i for i, l in enumerate(src) if "begin : g_af_amr" in l)
split = next(i for i, l in enumerate(src) if "begin : g_sp_amr" in l)
end = next(i for i in range(split, len(src)) if "end endgenerate" in src[i])


def norm(v: str) -> str:
    v = v.strip()
    if v in ("'0", "'b0"):
        return "0"
    m = re.fullmatch(r"(\d+)?'([bdh])([0-9a-fA-F_]+)", v)
    if m:
        return str(int(m.group(3).replace("_", ""), {"b": 2, "d": 10, "h": 16}[m.group(2)]))
    return v


resets, depth, in_reset = {}, 0, False
for line in src[start:split]:
    if re.search(r"if\s*\(\s*!axis_resetn\s*\)", line):
        in_reset, depth = True, 0
    if in_reset:
        depth += len(re.findall(r"\bbegin\b", line)) - len(re.findall(r"\bend\b", line))
        for name, val in re.findall(r"\b(amr_\w+)\s*<=\s*([^;]+);", line):
            resets.setdefault(name, norm(val))
        if "else" in line and depth <= 0:
            in_reset = False
ties = {n: norm(v) for n, v in (re.findall(r"assign\s+(amr_\w+)\s*=\s*([^;]+);", "\n".join(src[split:end])))}
bad = []
for n, v in sorted(ties.items()):
    r = resets.get(n)
    flag = "" if r == v else ("   <-- no reset value found" if r is None else "   <-- differs")
    print(f"{n:18s} split {v:8s} reset {str(r):8s}{flag}")
    if flag:
        bad.append(n)
print(f"\n{len(ties)} ties, {len(ties) - len(bad)} equal to the all-fabric reset value; departures: {', '.join(bad) or 'none'}")
