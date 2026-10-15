#!/usr/bin/env python3
"""R635-1: compare each printed poll figure of the B17 table (first poll, last poll, slip interval edges) with the
raw counter log rounded once to two decimals (round half to even and half up both shown).
usage: python3 -I check_printed_rounding.py <author_dir> <findings_page>"""
import json, re, sys
from decimal import Decimal, ROUND_HALF_UP
A, PAGE = sys.argv[1], sys.argv[2]
def jl(p): return [json.loads(x) for x in open(p) if x.startswith("{")]
def r2(x): return Decimal(repr(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
rows = {m.group(1): m.group(0) for m in re.finditer(r"^\| (c\d\d) \|.*$", open(PAGE).read(), re.M) if "Undefined" in m.group(0)}
bad = 0
for c in range(1, 11):
    tag = f"c{c:02d}"
    ev = jl(f"{A}/cycles/{tag}/events.jsonl"); po = sorted(jl(f"{A}/cycles/{tag}/poll.jsonl"), key=lambda r: r["n"])
    tb = [e for e in ev if e["kind"] == "bind-time"][0]["t_bind_local"]
    prev = None; lo = hi = None
    for r in po:
        lb = int(r["words"]["0x8d4"], 16)
        if prev is not None and lb != prev[0]: lo, hi = prev[1] - tb, r["t1"] - tb
        prev = (lb, r["t0"])
    raw = dict(first=po[0]["t0"] - tb, last=po[-1]["t1"] - tb, lo=lo, hi=hi)
    cells = rows[tag].split("|")
    m1 = re.search(r"80, ([+-]?\d+\.\d\d) to \+(\d+\.\d\d)", cells[4]); m2 = re.search(r"(\d+\.\d\d) to (\d+\.\d\d)", cells[6])
    printed = dict(first=Decimal(m1.group(1)), last=Decimal(m1.group(2)), lo=Decimal(m2.group(1)), hi=Decimal(m2.group(2)))
    for k in raw:
        ok = printed[k] == r2(raw[k])
        bad += not ok
        print(f"{tag} {k:5s} raw {raw[k]:+.6f} once-rounded {r2(raw[k])} printed {printed[k]} {'OK' if ok else 'MISMATCH'}")
print("mismatches:", bad)
