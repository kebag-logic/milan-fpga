#!/usr/bin/env python3
"""Re-derive the continuity attributions of 117_AUDIO_CONTINUITY.md from the
published packet only (summary/a-long/summary.json, continuity-events.csv).

usage: rederive_continuity.py <packet author dir> [ZADV=1|2]
"""
import csv, json, sys, statistics as st
from pathlib import Path

A = Path(sys.argv[1])
s = json.load(open(A / "summary/a-long/summary.json"))
c = s["continuity"]
ev = list(csv.DictReader(open(A / "summary/a-long/continuity-events.csv")))
for e in ev:
    e["frame"] = int(e["frame"]); e["step"] = int(e["step"]); e["frames"] = int(e["frames"])
c0, c1 = c["window"]
zeros = [z["start"] for z in c["silent_stretches"]]
FS = 48000
print("window frames", c1 - c0, "summary frames", c["frames"])
print("events", len(ev), "repeat", sum(e["kind"] == "repeat" for e in ev),
      "skip", sum(e["kind"] == "skip" for e in ev))

# content position: cumulative ordinal advance from the window start, assuming a step of 1
# across the 12 transitions that touch a zero frame (unknown; at most a few frames each)
# ZADV: ordinal advance across each zero frame (2 transitions); 1 = the zero was inserted
# between consecutive ordinals (the page's "removes one frame"), 2 = it replaced one.
ZADV = int(sys.argv[2]) if len(sys.argv) > 2 else 1
def content(k, upto):
    return (k - c0) + sum(e["step"] - 1 for e in upto) + (ZADV - 2) * sum(1 for z in zeros if z < k)

pos = []
done = []
for e in ev:
    pos.append(content(e["frame"], done)); done.append(e)

reps = [p for p, e in zip(pos, ev) if e["kind"] == "repeat"]
dr = [b - a for a, b in zip(reps, reps[1:])]
single = sorted(x for x in dr if x < 140000)
dbl = [x for x in dr if x >= 140000]
print("repeat spacing, content frames: n", len(dr), "min", min(single), "max", max(single),
      "doubles", len(dbl), dbl)
capsp = c["repeat_spacing_frames"]
print("summary repeat spacing (capture frames): min", min(capsp), "max", max(capsp))

one = [(p, e) for p, e in zip(pos, ev) if e["kind"] == "skip" and e["frames"] == 1]
# group one-frame skips into slip events: skip, zero, skip within 12 frames counts once
slips = []
for p, e in one:
    if slips and e["frame"] - slips[-1][1]["frame"] <= 12:
        slips[-1][2].append(e); continue
    slips.append([p, e, [e]])
pairs = [x for x in slips if len(x[2]) == 2]
print("one-frame skips", len(one), "slip events", len(slips), "paired", len(pairs))
pz = 0
for x in pairs:
    a, b = x[2][0]["frame"], x[2][1]["frame"]
    if any(a <= z < b for z in zeros):
        pz += 1
print("paired events with a zero frame between", pz, "gap frames", [x[2][1]["frame"] - x[2][0]["frame"] for x in pairs])
sp = [b[0] - a[0] for a, b in zip(slips, slips[1:])]
spn = sorted(x for x in sp if x < 100000)
print("slip spacing content frames: n", len(sp), "min", spn[0], "max", spn[-1], "median", st.median(spn),
      "doubles", [x for x in sp if x >= 100000])
med = st.median(spn)
print("slip period s", round(med / FS, 4), "ppm", round(1e6 / med, 2))
print("beat period s", round(st.median(single) / FS, 4), "ppm", round(1e6 / st.median(single), 2))

# rates on the bench host clock (uncalibrated) from the window end times
T = c["window_time"][1] - c["window_time"][0]
skips = [e for e in ev if e["kind"] == "skip"]
content_adv = c["in_order_steps"] + sum(e["step"] for e in skips) + 6 * ZADV  # transitions touching the six zero frames
stream = content_adv + c["repeats"]
peer_out = stream - len(slips)
nom = FS * T
print("T s", round(T, 6), "nominal frames", round(nom, 1))
for name, n in (("content (TDM source)", content_adv), ("stream", stream), ("peer output", peer_out)):
    print(f"{name}: {n} frames, {1e6 * (n - nom) / nom:+.2f} ppm vs 48 kHz on the bench host clock")
print("captured", c["frames"], "deficit vs nominal", round(nom - c["frames"], 1))
multi = [e for e in skips if e["frames"] >= 2]
print("multi-frame skip frames", sum(e["frames"] for e in multi), "events", len(multi))
print("peer_out - captured", peer_out - c["frames"], "(identity check against multi-frame skip frames)")
sm = [e for e in skips if 2 <= e["frames"] < 60]
lg = [e for e in skips if e["frames"] >= 60]
print("2..59:", len(sm), sum(e["frames"] for e in sm), " >=60:", len(lg), sum(e["frames"] for e in lg))
hist = {}
for e in sm:
    hist[e["frames"]] = hist.get(e["frames"], 0) + 1
print("2..59 histogram", dict(sorted(hist.items())))
print("2..59 multiples of 6:", sum(v for k, v in hist.items() if k % 6 == 0), "of", len(sm))
# spacing of the large skips (proxy for stall recurrence)
lp = [p for p, e in zip(pos, ev) if e["kind"] == "skip" and e["frames"] >= 60]
ls = sorted(b - a for a, b in zip(lp, lp[1:]))
print("large-skip spacing content frames median", st.median(ls), "s", round(st.median(ls) / FS, 3))
# small-skip spacing
spos = [p for p, e in zip(pos, ev) if e["kind"] == "skip" and 2 <= e["frames"] < 60]
ss = sorted(b - a for a, b in zip(spos, spos[1:]))
print("small-skip spacing content frames p10/median/p90", ss[len(ss)//10], st.median(ss), ss[9*len(ss)//10])
# small skips adjacent to a large skip (within 0.1 s)
near = 0
for p in spos:
    if any(abs(p - q) < 4800 for q in lp):
        near += 1
print("small skips within 0.1 s of a large skip", near, "of", len(spos))
# peer counters: packets per second between window reads
pc = [x for x in s["counters"] if x["role"] == "peer"]
for a, b in zip(pc, pc[1:]):
    fa, fb = a["nonzero"].get("11", 0), b["nonzero"].get("11", 0)
    if fb > fa:
        print("peer FRAMES_RX rate", round((fb - fa) / (b["t"] - a["t"]), 3), "per s over", round(b["t"] - a["t"], 2), "s")
print("peer counter indices seen non-zero", sorted({k for x in pc for k in x["nonzero"]}, key=int))
