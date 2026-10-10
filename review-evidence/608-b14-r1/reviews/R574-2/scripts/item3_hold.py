#!/usr/bin/env python3
"""Classify MSRP events inside each item-3 hold and time the DUT Talker Advertise Lv.

Usage: item3_hold.py <packet-author-dir>
Reads item3/cycles/cycle-NNN/{msrp.tsv,analysis.json} and item3/cycles.tsv only.
"""
import collections, csv, json, statistics, sys
from pathlib import Path

root = Path(sys.argv[1]) / "item3"
rows = {r["cycle"]: r for r in csv.DictReader(open(root / "cycles.tsv"), delimiter="\t")}
profiles = collections.Counter()
ta_lv = []
reg = collections.Counter()
lvs = []
for cdir in sorted(p for p in (root / "cycles").iterdir() if p.is_dir()):
    a = json.load(open(cdir / "analysis.json"))
    t0, t1 = a["disconnect_response_s"], a["connect_command_s"]
    bridge_lv = t0 + a["bridge_lv_after_disconnect_s"]
    ev = list(csv.DictReader(open(cdir / "msrp.tsv"), delimiter="\t"))
    hold = [e for e in ev if t0 <= float(e["t_s"]) <= t1]
    kinds = frozenset((e["sender"], e["type"], e["event"]) for e in hold)
    graded = rows[cdir.name]["graded"] == "True"
    if graded:
        profiles[kinds] += 1
        reg[a["registrar_at_lv"]] += 1
        lvs.append((a["bridge_lv_after_disconnect_s"], cdir.name))
    for e in ev:
        if e["sender"] == "DUT" and e["type"] == "TalkerAdvertise" and e["event"] == "Lv":
            t = float(e["t_s"])
            ta_lv.append((cdir.name, graded, e["stream_id"], round(t - bridge_lv, 4), round(t - t0, 4)))
print("graded cycles:", sum(profiles.values()))
for k, n in profiles.most_common():
    print(n, sorted(k))
print("registrar_at_lv (graded):", dict(reg))
print("DUT TA Lv anywhere in capture (cycle, graded, stream, after bridge Lv s, after response s):")
for x in ta_lv:
    print(" ", x)
v = sorted(x[0] for x in lvs)
print("bridge Lv after response ms: min %.3f max %.3f median %.3f" % (v[0]*1e3, v[-1]*1e3, statistics.median(v)*1e3))
print("over 50 ms:", [(c, round(t*1e3, 3)) for t, c in lvs if t > 0.05])
