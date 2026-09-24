#!/usr/bin/env python3
"""Cross-checks on one a237_analyze run (issue 530, A237, offline, read-only).

For the CRF stream: every DUT and switch MSRP event for it, binned as before the bind,
bound, and after the unbind; the pairing of switch and DUT LeaveAll MRPDUs (the delay
from each switch LeaveAll to the nearest DUT LeaveAll either side); and the acceptance
instants as UTC strings.

usage: a237_crosscheck.py <tap.pcap> <analysis.json>
"""
import datetime as dt
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import a237_analyze as an  # noqa: E402
import wire_summary as ws  # noqa: E402


def utc(h):
    return dt.datetime.fromtimestamp(h, dt.timezone.utc).strftime("%H:%M:%S.%f")


def main():
    pcap, js = sys.argv[1], json.load(open(sys.argv[2]))
    acc = js["acceptance"]
    tb, tu = acc["bind_t"], acc["unbind_t"]
    recs = sorted(ws.records(pcap), key=lambda r: r["tap_ns"])
    t0 = recs[0]["tap_ns"]
    ev = Counter()
    firsts = {}
    for r in recs:
        if ws.decode(r).get("kind") != "MSRP":
            continue
        t = (r["tap_ns"] - t0) / 1e9
        ph = "before" if t < tb else ("bound" if t <= tu else "after")
        for v in an.msrp_decode(r["frame"]):
            if v["attr"] not in ("TalkerAdvertise", "TalkerFailed", "Listener"):
                continue
            for sid, e, ld in an.sid_values(v):
                if sid != an.DUT_SID:
                    continue
                who = "DUT" if r["port"] == 3 else "switch"
                k = (ph, who, v["attr"], ("LA " if v["la"] else "") + e + ("/" + ld if ld else ""))
                ev[k] += 1
                firsts.setdefault(k, round(t, 6))
    print("== MSRP events for the CRF stream by phase (count, first tap s)")
    for k in sorted(ev):
        print(f"  {k[0]:6} {k[1]:6} {k[2]:15} {k[3]:22} n={ev[k]:4} first={firsts[k]}")
    sw = [x["t"] for x in js["leaveall"]["2"]]
    du = [x["t"] for x in js["leaveall"]["3"]]
    d = []
    for t in sw:
        near = min(du, key=lambda u: abs(u - t))
        d.append(round(near - t, 3))
    print("\n== nearest DUT LeaveAll minus each switch LeaveAll (s):")
    print("  ", Counter(d).most_common(12))
    print("   in bound window:", Counter(dd for t, dd in zip(sw, d) if tb <= t <= tu).most_common(12))
    print("\n== UTC (capture-server clock via the fit)")
    for k in ("bind_h", "first_listener_ready_h", "first_pdu_h", "unbind_h"):
        if k in acc:
            print(f"  {k}: {utc(acc[k])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
