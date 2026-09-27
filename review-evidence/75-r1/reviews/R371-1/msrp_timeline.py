#!/usr/bin/env python3
"""Print the published target-stream MSRP timeline for selected captures.

Usage: msrp_timeline.py <packet author dir> <capture name>...
Uses only the public per-capture analysis.json and msrp.tsv. For each capture
it prints the ACMP anchors, every event on the target stream plus Listener
LeaveAll vectors, and (for numbered cycles) a restart decomposition:
response -> first peer-side declaration -> Ready -> first valid CRF.
"""
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
for name in sys.argv[2:]:
    a = json.loads((root / name / "analysis.json").read_text())
    sid = a["stream_id"]
    anchors = {k: a.get(k) for k in ("disconnect_response_ns", "connect_command_ns", "response_ns",
                                     "first_advertise_since_connect_ns", "first_ready_since_connect_ns",
                                     "first_avtp_ns")}
    print(f"== {name} ({a['direction']}), latency {a['latency_s']} s")
    for k, v in anchors.items():
        if v is not None:
            print(f"   {k:34s} {v / 1e9:12.6f} s")
    rows = [l.rstrip("\n").split("\t") for l in (root / name / "msrp.tsv").read_text().splitlines()[1:]]
    for ns, sender, typ, ev, s, lst, fv in rows:
        if s == sid or (ev == "LeaveAll" and typ in ("Listener", "TalkerAdvertise")):
            # Stream identifiers embed station addresses; print a role label instead.
            label = "target-stream" if s == sid else "-"
            print(f"   {int(ns) / 1e9:12.6f} {sender:6s} {typ:15s} {ev:8s} {label} {lst}")
    first_bridge = next((int(r[0]) for r in rows if r[1] == "bridge"), None)
    print(f"   first bridge MSRP event of any type: {first_bridge / 1e9 if first_bridge else None} s")
    per_sender = {s: v["pdus"] for s, v in a["msrp"]["before"].items()}
    print(f"   MSRP PDUs before the response window by sender: {per_sender}")
    if a["direction"] == "listener" and a.get("response_ns") is not None:
        ta = next((int(r[0]) for r in rows if r[4] == sid and r[1] == "bridge" and r[3] in ("New", "JoinMt", "JoinIn")
                   and int(r[0]) >= a["response_ns"]), None)
        if ta is not None and a.get("first_ready_since_connect_ns"):
            print(f"   decomposition: response->bridge TA {(ta - a['response_ns']) / 1e6:.3f} ms; "
                  f"bridge TA->DUT Ready {(a['first_ready_since_connect_ns'] - ta) / 1e6:.3f} ms; "
                  f"DUT Ready->first CRF {(a['first_avtp_ns'] - a['first_ready_since_connect_ns']) / 1e6:.3f} ms")
    if a["direction"] == "talker" and a.get("first_ready_since_connect_ns"):
        print(f"   decomposition: response->bridge Ready {a['response_to_ready_s'] * 1e3:.3f} ms; "
              f"bridge Ready->first CRF {a['ready_to_first_avtp_s'] * 1e3:.3f} ms")
