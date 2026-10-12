#!/usr/bin/env python3
"""R624-9: recompute the lane's headline grades from the per-block grade receipts, independently of the
author's figures check and of each receipt's own summary.

usage: spot_check.py <author packet root> <out.json>
Reads summary/<run>/c-b9-grade.json (blocks) for b0-2, bcrf and baaf, summary/<run>/align-*.json and the
round 2 poll receipts. Floor rule as the page states it: an event-free block within 3 dB of the median.
"""
import json
import statistics
import sys
from pathlib import Path

ROOT, OUT = Path(sys.argv[1]), sys.argv[2]
res = {}


def runs(idx):
    out, start = [], None
    for i, b in enumerate(idx):
        if start is None:
            start = b
        if i + 1 == len(idx) or idx[i + 1] != b + 1:
            out.append([start, b])
            start = None
    return out


for run in ("b0-2", "bcrf", "baaf"):
    g = json.load(open(ROOT / f"summary/{run}/c-b9-grade.json"))
    blocks = g["blocks"]
    r = dict(blocks=len(blocks), events=len(g["events"]), phase_net_frames=g["phase_net_frames"])
    floor_both = None
    for ch in ("ch0", "ch1"):
        v = [b[ch]["thdn_db"] for b in blocks]
        med = statistics.median(v)
        fl = [b[ch]["thdn_db"] for b in blocks if b["events"] == 0 and b[ch]["thdn_db"] <= med + 3.0]
        r[ch] = dict(median_all=round(med, 2), worst_all=round(max(v), 2), floor_n=len(fl),
                     floor_median=round(statistics.median(fl), 2), floor_worst=round(max(fl), 2),
                     ppm_largest=round(max(abs(b[ch]["ppm"]) for b in blocks), 3))
    # degraded: a block off the floor on either tone, as the receipt's list counts them
    deg = sorted(set(b["block"] for b in blocks for ch in ("ch0", "ch1")
                     if b[ch]["thdn_db"] > statistics.median([x[ch]["thdn_db"] for x in blocks]) + 3.0))
    r["degraded_n"], r["degraded_runs"] = len(deg), runs(deg)
    r["degraded_inside_blocks_0_33"] = len([b for b in deg if b <= 33])
    r["receipt_summary_degraded"] = len(g["summary"]["degraded_event_free_blocks"])
    for side in ("a", "b"):
        f = ROOT / f"summary/{run}/align-{side}-c.json"
        if f.exists():
            r[f"align_{side}_c"] = json.load(open(f))
    res[run] = r
for run in ("bcrf", "baaf"):
    p = json.load(open(ROOT / f"r2/{run}-poll-receipt.json"))
    res[run]["locked"] = p["locked"]
    res[run]["slip_lb_steps"] = [(s["span"], s["dups"], s["servo"]) for s in p["slip_lb_steps"]]
json.dump(res, open(OUT, "w"), indent=1)
for run, r in res.items():
    print(run, {k: r[k] for k in ("blocks", "events", "ch0", "ch1", "degraded_n", "degraded_runs",
                                   "degraded_inside_blocks_0_33", "receipt_summary_degraded")})
    print("   align", {k: v for k, v in r.items() if k.startswith("align")})
    if "locked" in r:
        print("   locked", r["locked"], "slips", r["slip_lb_steps"])
