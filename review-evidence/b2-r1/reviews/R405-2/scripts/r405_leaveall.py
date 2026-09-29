#!/usr/bin/env python3
"""R405-2: independent re-derivation from the archived msrp.tsv of every B2
capture of (a) cycle 22's LeaveAll gap, (b) the session count of DUT LeaveAll
PDUs less than 10 s after a received bridge LeaveAll in the same capture, and
(c) the minimum capture time before the bridge's Listener Lv (the inference
bound).  Usage: r405_leaveall.py <author-dir>"""
import glob, json, os, statistics, sys

root = sys.argv[1]
STREAM = "0200000000010001"

def rows(p):
    with open(p) as f:
        hdr = f.readline().rstrip("\n").split("\t")
        for line in f:
            yield dict(zip(hdr, line.rstrip("\n").split("\t")))

caps = sorted(glob.glob(os.path.join(root, "**", "msrp.tsv"), recursive=True))
print("captures:", len(caps))
pairs = []; caps_hit = set(); dut_la_total = 0; bridge_la_total = 0
lv_min = []
for p in caps:
    name = os.path.relpath(os.path.dirname(p), root)
    R = list(rows(p))
    dut_la = sorted({float(r["t_s"]) for r in R if r["sender"] == "DUT" and r["event"] == "LeaveAll"})
    br_la = sorted({float(r["t_s"]) for r in R if r["sender"] == "bridge" and r["event"] == "LeaveAll"})
    dut_la_total += len(dut_la); bridge_la_total += len(br_la)
    for t in dut_la:
        prior = [b for b in br_la if b < t]
        if prior and t - prior[-1] < 10.0:
            pairs.append((name, t - prior[-1], prior[-1], t)); caps_hit.add(name)
    if name.startswith("cycles/"):
        lv = [float(r["t_s"]) for r in R if r["sender"] == "bridge" and r["type"] == "Listener"
              and r["event"] == "Lv" and r["stream_id"] == STREAM]
        if lv: lv_min.append((lv[0], name))
gaps = sorted(g for _, g, _, _ in pairs)
print("DUT LeaveAll PDUs (distinct times):", dut_la_total, " bridge LeaveAll PDUs:", bridge_la_total)
print("DUT LeaveAll PDUs < 10 s after a prior bridge LeaveAll in the same capture:", len(pairs))
print("captures holding at least one such PDU:", len(caps_hit), "of", len(caps))
print("gap min/median/max: %.6f %.6f %.6f" % (gaps[0], statistics.median(gaps), gaps[-1]), " under 1 s:", sum(g < 1 for g in gaps))
for n, g, b, t in pairs:
    if n.endswith("cycle-022"):
        print("cycle-022 pair: bridge LA %.9f DUT LA %.9f gap %.9f" % (b, t, g))
# cycle 22 relative to the tapped DISCONNECT_RX response
acmp = list(rows(os.path.join(root, "cycles/cycle-022/acmp.tsv")))
resp = [float(r["t_s"]) for r in acmp if r["mt"] == "9"][0]
R = list(rows(os.path.join(root, "cycles/cycle-022/msrp.tsv")))
for label, cond in (("bridge LA", lambda r: r["sender"] == "bridge" and r["event"] == "LeaveAll"),
                    ("DUT LA", lambda r: r["sender"] == "DUT" and r["event"] == "LeaveAll"),
                    ("bridge Listener Lv", lambda r: r["sender"] == "bridge" and r["event"] == "Lv" and r["type"] == "Listener")):
    t = min(float(r["t_s"]) for r in R if cond(r))
    print("cycle-022 %s after DISCONNECT_RX response: %+.6f s" % (label, t - resp))
lv_min.sort()
print("minimum capture time before the bridge Listener Lv over 100 cycles: %.9f s (%s)" % lv_min[0])
print("  -> printed 3 d.p. truncated: %.3f floor, rounded: %.3f" % (int(lv_min[0][0] * 1000) / 1000, round(lv_min[0][0], 3)))
