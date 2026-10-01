#!/usr/bin/env python3
"""Disposable probe of the published grade_b6.py attribution on a synthetic run.

Builds a 60 s two-channel S24_3LE capture of the published tone loop with a read-time
record (480 frames per 10 ms read), plants events, runs grade_b6.py and prints each
planted event's cause. Planted:
  P1 listener skip of 12 frames, no read stall, no deficit rise      (expected: listener)
  P2 listener skip of 2 frames, no read stall, no deficit rise       (expected: listener)
  P3 listener skip of 48 frames, no read stall, no deficit rise      (expected: listener)
  P4 listener skip of 60 frames, no read stall, no deficit rise      (expected: listener)
  P5 listener drop of 1 frame                                        (expected: listener)
  P6 capture loss of 108 frames: a 30 ms read stall and a 2.25 ms deficit rise (expected: capture path)
usage: probe_attribution.py <tools dir> <work dir>
"""
import json, os, subprocess, sys
import numpy as np
tools, work = sys.argv[1], sys.argv[2]
sys.path.insert(0, tools)
import b6_tone as T
FS = 48000
lp = T.loop()
secs = 60
n_src = secs * FS + 2000
plants = {  # capture frame -> (kind, size)
    20 * FS + 1111: ("listener-skip", 12),
    26 * FS + 2222: ("listener-skip", 2),
    32 * FS + 3333: ("listener-skip", 48),
    38 * FS + 4444: ("listener-skip", 60),
    44 * FS + 5555: ("listener-skip", 1),
    50 * FS + 6666: ("capture-loss", 108),
}
# build captured ordinal sequence
ords = []
src = 777
k = 0
cap_loss_at = {}
while len(ords) < secs * FS:
    f = len(ords)
    if f in plants:
        kind, m = plants[f]
        src += m
        if kind == "capture-loss":
            cap_loss_at[f] = m
    ords.append(src % T.N)
    src += 1
ords = np.array(ords)
c0, c1 = lp[ords, 0], lp[ords, 1]
raw = os.path.join(work, "raw"); run = os.path.join(work, "run")
os.makedirs(raw, exist_ok=True); os.makedirs(run, exist_ok=True)
w = np.stack([c0, c1], axis=1).astype(np.int64) & 0xFFFFFF
b = np.zeros((len(w), 2, 3), dtype=np.uint8)
for i in range(3):
    b[:, :, i] = (w >> (8 * i)) & 0xFF
b.tofile(os.path.join(raw, "cap-lr.raw"))
# read-time record: a read every 10 ms delivering 480 frames; the capture loss delays
# delivery (the deficit D = t - frames/fs rises by the lost duration) after a 30 ms stall
t0 = 1_000_000_000_000
recs = []
t = t0
fr = 0
lossf = sorted(cap_loss_at)
rng = np.random.default_rng(1)
while fr < len(ords):
    fr_next = min(fr + 480, len(ords))
    t += 10_000_000 + int(rng.integers(-20_000, 20_000))
    for lf in lossf:
        if fr < lf <= fr_next:
            t += 20_000_000 + int(cap_loss_at[lf] / FS * 1e9)  # stall, then the lost audio's time
    recs.append((fr_next, 0.0, t))
    fr = fr_next
ts = np.array(recs, dtype=np.dtype([("f", "<i8"), ("rt", "<f8"), ("raw", "<i8")]))
ts.tofile(os.path.join(raw, "cap-ts.bin"))
open(os.path.join(raw, "samples.txt"), "w").close()
ev = [dict(kind="start", case="PROBE", name="probe", t=0, mono_raw_ns=t0),
      dict(kind="window-start", frame=0, t=0, mono_raw_ns=t0),
      dict(kind="window-end", frame=len(ords), t=0, mono_raw_ns=int(t))]
with open(os.path.join(run, "events.jsonl"), "w") as fh:
    for e in ev:
        fh.write(json.dumps(e) + "\n")
out = os.path.join(work, "grade.json")
p = subprocess.run([sys.executable, os.path.join(tools, "grade_b6.py"), run, raw, out], capture_output=True, text=True)
print("grade_b6.py rc", p.returncode, (p.stderr.strip().splitlines() or [""])[-1][:200])
g = json.load(open(out))
byf = {e["capture_frame"]: e for e in g["events_list"]}
for f, (kind, m) in sorted(plants.items()):
    e = byf.get(f)
    exp = "capture path" if kind == "capture-loss" else "listener"
    got = e["cause"] if e else "NOT FOUND"
    cl = next((x for x in g["skip_clusters"] if x["first_frame"] == f), None)
    print(f"planted {kind:14s} {m:4d} frames at {f}: cause={got:13s} expected={exp:13s} {'OK' if got == exp else 'MISATTRIBUTED'}"
          + (f"  [rise {cl['read_rise_ms']} ms, gap {cl['recent_read_gap_ms']} ms, basis {cl['basis']}]" if cl else ""))
