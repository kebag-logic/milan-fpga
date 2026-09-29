#!/usr/bin/env python3
"""Drill-down for two page numbers: the pre-Lv capture bound and the
LeaveAll re-declaration bound. Usage: drill_b2.py <packet author dir>"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import replay_b2 as R
pkt = Path(sys.argv[1])
pre = []
slow = []
count = {"pre": 0, "post": 0}
for n in range(1, 101):
    d = pkt / "cycles" / f"cycle-{n:03d}"
    msrp = R.tsv(d / "msrp.tsv")
    acmp = R.tsv(d / "acmp.tsv")
    an = json.load(open(d / "analysis.json"))
    disc = an["disconnect_response_s"]; conn = an["response_s"]
    lv = disc + an["bridge_lv_after_disconnect_s"]
    first_any = min([msrp[0]["t"]] + [acmp[0]["t"]])
    pre.append((lv, n, round(msrp[0]["t"], 6), round(first_any, 6), an["capture_span_s"], round(disc, 6)))
    for sender, delay, t in R.redeclare_bound(msrp, 0.0, lv):
        count["pre"] += 1
        if delay is None or delay > 0.088:
            slow.append((n, "pre", sender, round(t, 6), round(lv - t, 6), delay))
    rd = [r["t"] for r in msrp if r["sender"] == "bridge" and r["type"] == "Listener"
          and r["stream_id"] == R.SID and r["event"] in R.DECL and r["t"] > conn]
    if rd:
        for sender, delay, t in R.redeclare_bound(msrp, rd[0], 1e9):
            count["post"] += 1
            if delay is None or delay > 0.088:
                slow.append((n, "post", sender, round(t, 6), None, delay))
pre.sort()
print("smallest Lv tap times (Lv, cycle, first msrp t, first record t, span, disc):")
for p in pre[:6]:
    print(" ", [round(p[0], 6)] + list(p[1:]))
print("LeaveAll windows counted", count)
print("LeaveAlls with bridge re-declaration later than 0.088 s or never:")
for s in slow:
    print(" ", s)

# Cycle-only bound excluding the cycle-22 LV LeaveAll, by sender.
from collections import Counter
allb = []
for n in range(1, 101):
    d = pkt / "cycles" / f"cycle-{n:03d}"
    msrp = R.tsv(d / "msrp.tsv")
    an = json.load(open(d / "analysis.json"))
    lv = an["disconnect_response_s"] + an["bridge_lv_after_disconnect_s"]
    conn = an["response_s"]
    allb += [(n, s, dl) for s, dl, t in R.redeclare_bound(msrp, 0.0, lv)]
    rd = [r["t"] for r in msrp if r["sender"] == "bridge" and r["type"] == "Listener"
          and r["stream_id"] == R.SID and r["event"] in R.DECL and r["t"] > conn]
    if rd:
        allb += [(n, s, dl) for s, dl, t in R.redeclare_bound(msrp, rd[0], 1e9)]
ex = [b for b in allb if not (b[0] == 22 and b[2] is not None and b[2] > 1)]
print("cycles-only LeaveAlls while registered (excluding the cycle-22 LV one):", len(ex),
      dict(Counter(b[1] for b in ex)), "max re-declaration delay", round(max(b[2] for b in ex), 6))
