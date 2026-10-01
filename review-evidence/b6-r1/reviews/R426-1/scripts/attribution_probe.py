#!/usr/bin/env python3
"""Disposable probe of the B6 grader's attribution (grade_b6.py) on a synthetic run.

The peer's output sequence carries planted events of known cause:
  beat     a one-frame repeat every 93,990 source frames (the DUT's talker beat);
  listener one-frame drops every 58,000 frames (about 17 ppm), plus
    L_beat   one listener one-frame REPEAT 20 frames after one beat repeat,
    L_adj    a listener drop at the exact frame where a capture-path loss starts (one merged step),
    L_near   a listener drop 5 frames after a capture-path loss,
    L_multi  a 60-frame listener skip 200 ms after an 18 ms read gap that loses nothing,
    L_multi2 a 60-frame listener skip with no read gap near it.
The capture path then loses whole runs of 48 n + 12 device frames. Device time is exact
(48 kHz); the host reads every 10 ms, with a 30 ms read gap at each loss and one lossless
18 ms gap; each read delivers every frame the device produced by then less the frames lost.
The grader is run unmodified and every planted event's classification is printed.
usage: attribution_probe.py <tools_dir> <work_dir>"""
import json, os, subprocess, sys
import numpy as np
tools, work = sys.argv[1], sys.argv[2]
sys.path.insert(0, tools)
import b6_tone as T
FS = 48000
run_dir = os.path.join(work, "run"); raw_dir = os.path.join(work, "raw")
os.makedirs(run_dir, exist_ok=True); os.makedirs(raw_dir, exist_ok=True)
SECS = 120
# 1. peer output sequence (ordinals), events placed by output index
out, truth = [], {}
k = 0
beat_next, drop_next, lbeat_done = 50000, 30000, False
pending_lbeat = None
while len(out) < SECS * FS:
    k += 1
    if k == beat_next:
        out.append((k - 1) % T.N); truth[len(out) - 1] = "beat"
        beat_next += 93990
        if not lbeat_done and len(out) > 20 * FS:
            pending_lbeat = len(out) + 20; lbeat_done = True
    if pending_lbeat is not None and len(out) == pending_lbeat:
        out.append((k - 1) % T.N); truth[len(out) - 1] = "L_beat listener repeat"; pending_lbeat = None
    if k == drop_next:
        drop_next += 58000; truth[len(out)] = "listener drop"; continue
    out.append(k % T.N)
seq = np.array(out, dtype=np.int64)
def skip_listener(arr, at, n, label):
    truth[at] = label
    return np.delete(arr, np.arange(at, at + n))
LOSS = {int(10.3 * FS): 1164, int(25.7 * FS): 60, int(40.1 * FS): 540, int(55.5 * FS): 1260, int(70.9 * FS): 204}
# listener events placed relative to capture-path losses (output index space, before capture)
seq = skip_listener(seq, int(40.1 * FS) + 540, 1, "L_adj")            # merged with the 540 loss
seq = skip_listener(seq, int(55.5 * FS) + 1260 + 5, 1, "L_near")
seq = skip_listener(seq, int(85.0 * FS), 60, "L_multi")
seq = skip_listener(seq, int(100.0 * FS), 60, "L_multi2")
# 2. capture-path loss mask in device frames
lost = np.zeros(len(seq), bool)
for p, m in LOSS.items():
    lost[p:p + m] = True
cap = seq[~lost]
cum_lost = np.concatenate([[0], np.cumsum(lost)])
lp = T.loop()
c0, c1 = lp[cap, 0], lp[cap, 1]
def s24(x):
    x = x & 0xFFFFFF
    return np.stack([x & 0xFF, (x >> 8) & 0xFF, (x >> 16) & 0xFF], axis=1).astype(np.uint8)
np.concatenate([s24(c0)[:, None, :], s24(c1)[:, None, :]], axis=1).reshape(-1).tofile(os.path.join(raw_dir, "cap-lr.raw"))
# 3. host reads
t0 = 1000.0
gaps = {p / FS: 0.030 for p in LOSS}          # a 30 ms read gap where each loss starts
gaps[84.8] = 0.018                             # a lossless 18 ms read gap 200 ms before L_multi
rt, rf = [], []
t = 0.0
gl = sorted(gaps.items())
while t < len(seq) / FS - 0.05:
    step = 0.010
    for gt, g in gl:
        if t < gt <= t + step:
            step = g
    t += step
    x = min(int(t * FS), len(seq))
    rt.append(t0 + t); rf.append(x - int(cum_lost[x]))
ts = np.zeros(len(rt), dtype=np.dtype([("f", "<i8"), ("rt", "<f8"), ("raw", "<i8")]))
ts["f"] = rf; ts["rt"] = rt; ts["raw"] = np.round(np.array(rt) * 1e9).astype(np.int64)
ts.tofile(os.path.join(raw_dir, "cap-ts.bin"))
open(os.path.join(raw_dir, "samples.txt"), "w").close()
w0, w1 = 48000, len(cap) - 48000
with open(os.path.join(run_dir, "events.jsonl"), "w") as fh:
    for e in (dict(kind="start", case="PROBE", name="probe", t=0.0),
              dict(kind="window-start", frame=w0, mono_raw_ns=int(ts["raw"][0]), t=0.0),
              dict(kind="window-end", frame=w1, mono_raw_ns=int(ts["raw"][-1]), t=1.0)):
        fh.write(json.dumps(e) + "\n")
out_json = os.path.join(work, "grade.json")
r = subprocess.run([sys.executable, os.path.join(tools, "grade_b6.py"), run_dir, raw_dir, out_json],
                   capture_output=True, text=True)
print("grade rc", r.returncode, r.stderr[-1500:])
g = json.load(open(out_json))
evl = g["events_list"]
print("attribution:", {k_: (v["events"], v.get("skips"), v.get("repeats")) for k_, v in g["attribution"].items()})
for c in g["skip_clusters"]:
    print("cluster", c["steps"], c["basis"], "capture_path", c["capture_path"], "rise_ms", c["read_rise_ms"],
          "lost_ms", c["lost_ms"], "gap_ms", c["recent_read_gap_ms"])
cap_of_dev = lambda x: x - int(cum_lost[x])
for idx, label in sorted(truth.items()):
    if label in ("beat", "listener drop"):
        continue
    cf = cap_of_dev(idx)
    hit = [(e["capture_frame"], e["kind"], e["step"], e["cause"]) for e in evl if abs(e["capture_frame"] - cf) <= 30]
    print(f"{label:24} planted at capture frame ~{cf}: {hit}")
plain = sum(1 for v in truth.values() if v == "listener drop")
print("plain listener drops planted (whole run):", plain, "; listener-cause events in window:",
      sum(1 for e in evl if e["cause"] == "listener"), "; beat-cause:", sum(1 for e in evl if e["cause"] == "DUT beat"),
      "; beats planted:", sum(1 for v in truth.values() if v == "beat"))
