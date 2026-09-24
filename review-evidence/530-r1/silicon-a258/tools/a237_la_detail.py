#!/usr/bin/env python3
"""LeaveAll MRPDU detail on the DUT link (issue 530, A237, offline, read-only).

Per phase (before bind, bound, after unbind) and per sender: LeaveAll MRPDU count, the
types flagged, which of them are NumberOfValues-0 vectors, and how many of the DUT's
MRPDUs carry more than one Domain vector.

usage: a237_la_detail.py <tap.pcap> <analysis.json>
"""
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import a237_analyze as an  # noqa: E402
import wire_summary as ws  # noqa: E402


def main():
    js = json.load(open(sys.argv[2]))
    tb, tu = js["acceptance"]["bind_t"], js["acceptance"]["unbind_t"]
    recs = sorted(ws.records(sys.argv[1]), key=lambda r: r["tap_ns"])
    t0 = recs[0]["tap_ns"]
    la, dom, tot = Counter(), Counter(), Counter()
    for r in recs:
        if ws.decode(r).get("kind") != "MSRP":
            continue
        t = (r["tap_ns"] - t0) / 1e9
        ph = "before" if t < tb else ("bound" if t <= tu else "after")
        who = "DUT" if r["port"] == 3 else "switch"
        vec = an.msrp_decode(r["frame"])
        tot[(ph, who)] += 1
        nd = sum(1 for v in vec if v["attr"] == "Domain")
        if nd > 1:
            dom[(ph, who, nd, bool(any(v["la"] for v in vec)))] += 1
        if any(v["la"] for v in vec):
            la[(ph, who, tuple(sorted({v["attr"] for v in vec if v["la"]})),
                tuple(sorted({v["attr"] for v in vec if v["la"] and v["nv"] == 0})))] += 1
    print("MRPDUs per phase/sender:", dict(tot))
    print("LeaveAll MRPDUs (phase, sender, flagged types, NumberOfValues-0 types): count")
    for k in sorted(la):
        print("  ", k, la[k])
    print("MRPDUs with more than one Domain vector (phase, sender, n Domain vectors, LeaveAll PDU): count")
    for k in sorted(dom):
        print("  ", k, dom[k])
    return 0


if __name__ == "__main__":
    sys.exit(main())
