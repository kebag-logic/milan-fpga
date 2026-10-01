#!/usr/bin/env python3
"""Re-derive the continuity, beat, slip and restart figures of the B5 page from the
published packet (summary.json and continuity-events.csv only; raw capture is not public).

usage: rederive_continuity.py <packet author dir>
"""
import csv, json, statistics, sys
from pathlib import Path

A = Path(sys.argv[1])
FS = 48000
s = json.load(open(A / "summary/a-long/summary.json"))
c = s["continuity"]
ev = list(csv.DictReader(open(A / "summary/a-long/continuity-events.csv")))
for e in ev:
    e["frame"] = int(e["frame"]); e["step"] = int(e["step"]); e["frames"] = int(e["frames"])
w0, w1 = c["window"]
print("window frames", w1 - w0, "=", c["frames"], "seconds", (w1 - w0) / FS)
print("valid", c["valid"], "torn", c["torn"], "invalid_nonzero", c["invalid_nonzero"], "zero", c["zero_frames"])
trans = c["in_order_steps"] + c["repeats"] + c["skip_events"]
print("graded transitions", trans, "of", c["frames"] - 1, "ungraded", c["frames"] - 1 - trans)
sk = [e for e in ev if e["kind"] == "skip"]
one = [e for e in sk if e["frames"] == 1]
small = [e for e in sk if 2 <= e["frames"] < 60]
large = [e for e in sk if e["frames"] >= 60]
rep = [e for e in ev if e["kind"] == "repeat"]
print("repeats", len(rep), "one", len(one), "small", len(small), sum(e["frames"] for e in small),
      "large", len(large), sum(e["frames"] for e in large), "total lost", sum(e["frames"] for e in sk))
print("rates/s over", c["seconds"], ":", [round(x / c["seconds"], 3) for x in (len(rep), len(one), len(small), len(large))])

# content position: ordinal advance from window start, per captured frame index k
# content(k) = (k - w0) + skipped frames in events at or before k - repeats at or before k
evs = sorted(ev, key=lambda e: e["frame"])
cum_skip = 0; cum_rep = 0; cpos = {}
for e in evs:
    if e["kind"] == "skip": cum_skip += e["frames"]
    elif e["kind"] == "repeat": cum_rep += 1
    cpos[(e["frame"], e["kind"])] = (e["frame"] - w0) + cum_skip - cum_rep
rp = [cpos[(e["frame"], "repeat")] for e in evs if e["kind"] == "repeat"]
rsp = [b - a for a, b in zip(rp, rp[1:])]
single = [x for x in rsp if x < 140000]
double = [x for x in rsp if x >= 140000]
print("repeat spacing content frames: n", len(rsp), "single min/max/median", min(single), max(single),
      statistics.median(single), "doubles", double)
cap_rsp = c["repeat_spacing_frames"]
print("repeat spacing CAPTURE frames (summary.json): min/max", min(cap_rsp), max(cap_rsp))
mb = statistics.median(single)
print("beat: median spacing", mb, "frames =", mb / FS, "s =", 1e6 / mb, "ppm")
print("beats in window incl hidden:", len(rep) + len(double), "per s", (len(rep) + len(double)) / ((w1 - w0) / FS))

# slip events: one-frame skips; pairs (skip, zero, skip) within 12 frames merge
ones = [e["frame"] for e in one]
zs = [z["start"] for z in c["silent_stretches"]]
events = []; i = 0
while i < len(ones):
    if i + 1 < len(ones) and ones[i + 1] - ones[i] <= 12:
        events.append((ones[i], ones[i + 1])); i += 2
    else:
        events.append((ones[i],)); i += 1
pairs = [e for e in events if len(e) == 2]
print("slip events", len(events), "singles", len(events) - len(pairs), "pairs", len(pairs))
for p in pairs:
    near = [z for z in zs if p[0] - 12 <= z <= p[1] + 12]
    print("  pair", p, "gap", p[1] - p[0], "zero frames at", near, "offsets", [z - p[0] for z in near])
print("zero frames not in a pair:", [z for z in zs if not any(p[0] - 12 <= z <= p[1] + 12 for p in pairs)])
sp = [cpos[(e[0], "skip")] for e in events]
ssp = [b - a for a, b in zip(sp, sp[1:])]
sng = [x for x in ssp if x < 100000]; dbl = [x for x in ssp if x >= 100000]
ms = statistics.median(sng)
print("slip spacing content frames: min/max/median", min(sng), max(sng), ms, "=", ms / FS, "s =", 1e6 / ms, "ppm; doubles", dbl)
# neighbourhood of events: does any one-frame skip sit next to a repeat or large skip?
allf = sorted((e["frame"], e["kind"], e["frames"]) for e in ev)
close = 0
for (a, ka, fa), (b, kb, fb) in zip(allf, allf[1:]):
    if b - a < 12 and not (ka == kb == "skip" and fa == fb == 1): close += 1
print("adjacent mixed events within 12 frames:", close)
# skip histogram residues mod 6
h = {int(k): v for k, v in c["skip_size_histogram"].items()}
res = {}
for k, v in h.items():
    if k > 1: res[k % 6] = res.get(k % 6, 0) + v
print("skip>1 residues mod 6:", dict(sorted(res.items())))

# restarts
cy = s.get("cycles")
if cy is None:
    print("cycles not in summary")

# detail: repeat spacings at the extremes and the events between them
from collections import Counter
print("repeat content spacing histogram (single):", sorted(Counter(single).items()))
for (a, b), sp_ in zip(zip(rp, rp[1:]), rsp):
    if sp_ == 93993:
        fa = [e for e in evs if e["kind"] == "repeat" and cpos[(e["frame"], "repeat")] == a][0]["frame"]
        fb = [e for e in evs if e["kind"] == "repeat" and cpos[(e["frame"], "repeat")] == b][0]["frame"]
        between = [(e["frame"], e["kind"], e["frames"]) for e in evs if fa < e["frame"] <= fb]
        zin = [z for z in zs if fa < z <= fb]
        print("93993 between capture frames", fa, fb, "zero frames inside", zin, "events", len(between),
              "one-frame skips", sum(1 for x in between if x[1] == "skip" and x[2] == 1))
