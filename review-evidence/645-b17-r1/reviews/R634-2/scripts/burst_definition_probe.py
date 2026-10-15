#!/usr/bin/env python3
"""Reviewer probe: lane B17 burst figures under two burst definitions (offline, read-only).

usage: burst_definition_probe.py <author_packet_dir>

A: the summary tool's rule, late PDUs (> 20 us) grouped while less than 1 ms apart.
B: the page's wording, "consecutive PDUs": grouped only while adjacent at the 125 us PDU period
   (gap < 187.5 us, i.e. no PDU at or under 20 us between them).
Prints, per definition, the per-cycle counts and the ranges the page prints, plus every burst under A
that contains a gap of more than one PDU period.
"""
import json
import sys
from pathlib import Path

P = Path(sys.argv[1])


def jl(p):
    return [json.loads(x) for x in open(p) if x.strip()]


def group(lp, gap):
    b = []
    for x in lp:
        if x["late_us"] <= 20.0:
            continue
        if b and x["s"] - b[-1]["last"] < gap:
            b[-1]["gaps"].append(x["s"] - b[-1]["last"])
            b[-1]["last"] = x["s"]; b[-1]["peak"] = max(b[-1]["peak"], x["late_us"]); b[-1]["n"] += 1
        else:
            b.append(dict(s=x["s"], last=x["s"], peak=x["late_us"], n=1, gaps=[]))
    return b


res = {}
for name, gap in (("A_1ms", 1e-3), ("B_consecutive", 187.5e-6)):
    cyc = []
    for c in range(1, 11):
        cd = P / "cycles" / f"c{c:02d}"
        ev = jl(cd / "events.jsonl")
        tb = [e for e in ev if e["kind"] == "bind"][0]["t_cmd_local"]
        pl = sorted(jl(cd / "poll.jsonl"), key=lambda r: r["n"])
        last = pl[-1]["t1"] - tb
        lb = [int(r["words"]["0x8d4"], 16) for r in pl]
        i = next(k for k in range(1, len(pl)) if lb[k] != lb[k - 1])
        lo, hi = pl[i - 1]["t0"] - tb, pl[i]["t1"] - tb
        lp = json.load(open(P / "summary" / f"c{c:02d}.json"))["tap"]["late_pdus"]
        b = group(lp, gap)
        ins = [z for z in b if lo <= z["s"] <= hi]
        row = dict(cycle=f"c{c:02d}", per_last=len([z for z in b if z["s"] <= last]), per_cap=len(b),
                   after_last=len([z for z in b if hi < z["s"] <= last]), after_cap=len([z for z in b if z["s"] > hi]),
                   pdus=[min(z["n"] for z in b), max(z["n"] for z in b)],
                   larger_last=any(z["peak"] > ins[0]["peak"] for z in b if hi < z["s"] <= last),
                   gapped=[dict(s=round(z["s"], 6), n=z["n"], max_gap_us=round(max(z["gaps"]) * 1e6, 1))
                           for z in b if z["gaps"] and max(z["gaps"]) > 187.5e-6])
        cyc.append(row)
    rng = lambda k: [min(r[k] for r in cyc), max(r[k] for r in cyc)]
    res[name] = dict(cycles=cyc, ranges=dict(per_last=rng("per_last"), per_cap=rng("per_cap"), after_last=rng("after_last"),
                                             after_cap=rng("after_cap"),
                                             pdus=[min(r["pdus"][0] for r in cyc), max(r["pdus"][1] for r in cyc)],
                                             larger_last=sum(r["larger_last"] for r in cyc)))
print(json.dumps(res, indent=1))
