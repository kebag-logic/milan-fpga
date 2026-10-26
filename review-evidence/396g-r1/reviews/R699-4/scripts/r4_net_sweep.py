#!/usr/bin/env python3
"""Round-4: per-channel net of reported DUT slips against the true net, over r4_probe group C and r4_regress_sweep cases.

Usage: python3 -I r4_net_sweep.py <path-to-tb/tools> <scripts dir> [jobs]
The documented limit says a cluster's total is exact; a case is UNBALANCED when
a channel's reported slips do not sum to its true net shift.
"""
import json
import sys
from multiprocessing import get_context

TOOLS, HERE = sys.argv[1], sys.argv[2]
JOBS = int(sys.argv[3]) if len(sys.argv) > 3 else 8
sys.path.insert(0, HERE)
sys.argv = [sys.argv[0], TOOLS, HERE]
import r4_probe as q  # noqa: E402
sys.argv = [sys.argv[0], TOOLS, HERE]
import r4_regress_sweep as rs  # noqa: E402

p = q.p


def ops_of(args):
    mask, length, begin, gap, side, nb = args
    ops = [("xor", begin + k, 2, mask) for k in range(length)]
    nmask = 0x100 if mask != 0x100 else 0x80000
    sites = ([begin - gap] if side in ("before", "both") else []) + \
            ([begin + length - 1 + gap] if side in ("after", "both") else [])
    for s in sites:
        ops.append(("xor", s, 2, nmask) if nb == "flip" else ("shift", s, 3 if nb == "slip3" else -2))
    return ops


def one(args):
    ops = ops_of(args)
    v, d, dut = p.grade(16384, ops)
    bad = []
    for c in range(p.C):
        net = sum(o[2] for o in ops if o[0] == "shift" and (len(o) < 4 or o[3] == c))
        got = sum(e["n"] if e["class"] == "dropped" else -e["n"] for e in dut
                  if e["channel"] == c and e["class"] in ("dropped", "repeated"))
        if net != got and not any(e["channel"] == c and e["class"] == "unresolved" for e in dut):
            bad.append((c, net, got))
    return args, v, bad


def main():
    cases = sorted(set(q.c_cases()) | set(rs.cases()))
    with get_context("fork").Pool(JOBS) as pool:
        res = pool.map(one, cases, chunksize=8)
    n = 0
    for args, v, bad in res:
        if bad:
            n += 1
            print("UNBALANCED", json.dumps(list(args)), v, json.dumps(bad))
    print("SUMMARY cases", len(res), "unbalanced", n)


if __name__ == "__main__":
    main()
