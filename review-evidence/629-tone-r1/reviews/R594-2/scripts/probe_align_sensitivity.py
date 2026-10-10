#!/usr/bin/env python3
"""Disposable probes of the lane B15 alignment and presence tools (no bench data).

usage: probe_align_sensitivity.py <dir holding align_b15.py, tone_points_b15.py, b6_thdn.py,
                                   b6_tone.py, b9_tone.py> <out.json>

Part A, alignment (align_b15.compare) on a synthetic idle floor shaped like the published
summaries (values -2..+1, about 54 % non-zero, 1,151,052 stream frames, 4 channels), with a
480,000-frame "recording" cut from it:
  A1 exact copy -> SAMPLE-EXACT, first window unique
  A2 one frame dropped / A3 repeated / A4 one sample +1 LSB / A5 another stretch -> detected
  A6 a +256 LSB offset on channel 0 (outside the 8-bit key) -> reveals whether the key is lossy
  A7 a recording that runs past the stream's end -> whether the uncompared tail is counted
  A8 the per-channel key is injective on [-128, 127]: so with the published ranges (-2..+1 at
     the taps, -2..0 at McASP) A6's blind spot cannot apply to the lane's two verdicts.
Part B, presence (tone_points_b15.channel_rows): a 997 Hz tone added to the same floor at
-120, -140, -150 and -160 dBFS (24-bit full scale, rounded to integers like a converter) and
the share within 5 Hz compared with the flat floor's 0.04 %.
"""
import json
import sys

import numpy as np

sys.path.insert(0, sys.argv[1])
import align_b15 as AL  # noqa: E402
import tone_points_b15 as TP  # noqa: E402

rng = np.random.default_rng(629594)
N, NCH = 1151052, 4
p = [0.0012, 0.54, 0.4576, 0.0012]  # -2, -1, 0, +1
s = rng.choice(np.array([-2, -1, 0, 1]), size=(N, NCH), p=p).astype(np.int64)
out = dict(partA={}, partB={})


def run(label, m):
    r = AL.compare(s, m, NCH, 0)
    out["partA"][label] = {k: r.get(k) for k in ("verdict", "matches_of_first_window", "compared_equal",
                                                  "frames_differing", "slips", "mcasp_frames")}


base = s[182213:182213 + 480000].copy()
run("A1 exact copy", base)
run("A2 one frame dropped", np.delete(s[182213:182213 + 480001], 200000, axis=0))
run("A3 one frame repeated", np.insert(s[182213:182213 + 479999], 250000, s[182213 + 249999], axis=0))
m = base.copy(); m[300000, 2] += 1
run("A4 one sample +1 LSB", m)
run("A5 another stretch", s[600000:1080000].copy())
m = base.copy(); m[:, 0] += 256
run("A6 channel 0 offset by +256 LSB", m)
m = s[N - 300000:].copy(); m = np.concatenate([m, rng.integers(-2, 2, size=(180000, NCH))])
run("A7 recording runs 180,000 frames past the stream end", m)
vals = np.arange(-128, 128)
k = AL.key(np.stack([vals] * NCH, axis=1))
out["partA"]["A8 key injective on [-128,127] per channel"] = bool(len(np.unique(k)) == 256)

fl = s[:480000, 0].astype(np.float64)
r0 = TP.channel_rows(fl[:, None])[0]
out["partB"]["floor only"] = dict(rms_dbfs=r0["rms_dbfs"], share_997=r0["share_997"])
t = np.arange(len(fl)) / 48000.0
for lv in (-120, -140, -150, -160):
    a = (2 ** 23) * 10 ** (lv / 20) * np.sqrt(2)
    x = np.round(fl + a * np.sin(2 * np.pi * 997 * t))
    r = TP.channel_rows(x[:, None])[0]
    out["partB"][f"tone {lv} dBFS"] = dict(rms_dbfs=r["rms_dbfs"], share_997=r["share_997"],
                                          tone_flagged="tone_997" in r)
json.dump(out, open(sys.argv[2], "w"), indent=1)
print(json.dumps(out, indent=1))
