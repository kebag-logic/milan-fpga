#!/usr/bin/env python3
"""Independent box 4 receive-counter figures, decoded from the GET_COUNTERS payload
bytes (not the transcript's decoded field). Usage: probe_box4.py RAW_ROOT"""
import json, struct, sys
from pathlib import Path
root = Path(sys.argv[1])
def cnt(r, i):
    b = bytes.fromhex(r["response"]["payload"])
    dtype, didx, valid = struct.unpack(">HHI", b[:8])
    return dtype, didx, struct.unpack(">I", b[8 + 4 * i:12 + 4 * i])[0]
def polls(name, role, what):
    out = []
    for l in open(root / name / "controller.jsonl"):
        if l.strip():
            r = json.loads(l)
            if r.get("role") == role and r.get("what") == what and r["response"].get("status") == "SUCCESS":
                out.append(r)
    return out
p8 = polls("retention", "peer", "counter-5-8")
d61 = polls("retention", "dut", "counter-6-1")
assert all(cnt(r, 0)[:2] == (5, 8) for r in p8) and all(cnt(r, 0)[:2] == (6, 1) for r in d61)
span = p8[-1]["t"] - p8[0]["t"]
print("peer input 8 FRAMES_RX delta", cnt(p8[-1], 11)[2] - cnt(p8[0], 11)[2], "polls", len(p8), f"rate {(cnt(p8[-1],11)[2]-cnt(p8[0],11)[2])/span:.2f}/s")
print("dut output 1 FRAMES_TX delta", cnt(d61[-1], 4)[2] - cnt(d61[0], 4)[2], "polls", len(d61))
acts = ["firstreach", "retention"] + [f"cycle{i:02d}" for i in range(1, 7)] + [f"gm{i:02d}" for i in range(1, 6)]
ends, allv, mism = [], [], 0
for a in acts:
    s = polls(a, "dut", "counter-5-0")
    lag = []
    for r in s:
        _, _, tv = cnt(r, 6); _, _, fr = cnt(r, 11)
        mism += (tv != r["response"]["counters"]["6"]) + (fr != r["response"]["counters"]["11"])
        lag.append(tv - fr)
    ends += [lag[0], lag[-1]]; allv += lag
print("first/last reads", len(ends), min(ends), max(ends), "| every poll", len(allv), min(allv), max(allv), "negative", sum(x < 0 for x in allv), "| payload/decoded mismatches", mism)
