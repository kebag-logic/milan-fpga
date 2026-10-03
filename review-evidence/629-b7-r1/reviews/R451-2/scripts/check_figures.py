#!/usr/bin/env python3
"""Recompute the round-2 figures from the published grades: the capture drift range
(48 kHz less the external capture's fitted rate, per case) and the conservative count
(frames each off-signature cluster is short, per case, from summary/checks/absorb.jsonl).
usage: check_figures.py <packet author dir>"""
import json, sys
a = sys.argv[1]
d = {}
for c in ["a0", "a1", "a2", "b0", "bcrf", "baaf"]:
    g = json.load(open(f"{a}/summary/{c}/grade.json"))
    d[c] = 48000 - g["frame_rate_ratio"]["external_capture"]["rate"]
    print(f"{c:5} capture deficit {d[c]:.3f} frames/s")
print(f"range {min(d.values()):.2f} to {max(d.values()):.2f} frames/s")
for l in open(f"{a}/summary/checks/absorb.jsonl"):
    r = json.loads(l)
    off = [x["frames_off"] for x in r["item1_clusters_net_off"]]
    print(f"{r['case']:5} {r['segment']:9} clusters {r['clusters']:3} off-signature {len(off)} frames_off {off} conservative listener frames {sum(abs(x) for x in off)} smallest loss {r['smallest_capture_loss']}")
