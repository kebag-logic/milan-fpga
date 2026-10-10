#!/usr/bin/env python3
"""Reviewer probes of the lane B15 decoders (offline, synthetic data only).

usage: probe_b15_tools.py <tools-dir> <out.json>

<tools-dir> holds the published tone_points_b15.py (with its synthetic IDs unmasked), align_b15.py,
b6_thdn.py, b6_tone.py, b9_thdn.py and b9_tone.py from the lane packet.

P1  presence sensitivity: a synthetic idle floor shaped like the captured one (values -1/0, about half
    nonzero, the size of the recorded -141.5 dBFS) with a 997 Hz tone added at a range of levels and
    rounded to 24 bits; the published channel_rows/verdict give the share and the verdict. Shows how far
    below the -40 dBFS gate a tone still moves the share off the 0.04 % flat-floor value.
P2  alignment probes on a synthetic floor stream of 1,151,052 frames x 4 channels (the size of pts1 at (b)):
    exact, one dropped frame, one repeated frame, one changed sample, two channels swapped (a channel-map
    defect), a constant-zero recording (a dead render), a recording from another stretch, and the number of
    stream offsets the first 256-frame window matches.
"""
import json
import os
import sys

import numpy as np

TOOLS = os.path.abspath(sys.argv[1])
sys.path.insert(0, TOOLS)
import tone_points_b15_unmasked as TP  # noqa: E402
import align_b15 as AL  # noqa: E402

FS = 48000
rng = np.random.default_rng(629015)
out = {}

# P1
N = 1151058
floor = -(rng.random(N) < 0.5).astype(np.float64)  # values -1 / 0
rows0 = TP.channel_rows(floor[:, None])
p1 = dict(floor_only=dict(rms_dbfs=rows0[0]["rms_dbfs"], share_997=rows0[0]["share_997"],
                          verdict=TP.verdict(rows0)[1]), with_tone=[])
k = np.arange(N)
for lvl in (-20, -40, -45, -60, -80, -100, -120, -130, -135, -140):
    amp = (2 ** 23) * 10 ** (lvl / 20)
    x = np.round(floor + amp * np.sin(2 * np.pi * 997 * k / FS))
    r = TP.channel_rows(x[:, None])
    p1["with_tone"].append(dict(tone_dbfs_peak=lvl, rms_dbfs=r[0]["rms_dbfs"], share_997=r[0]["share_997"],
                                verdict=TP.verdict(r)[1]))
out["P1_presence_sensitivity"] = p1

# P2
S = 1151052
s = rng.integers(-2, 2, size=(S, 4)).astype(np.int64)
s[:, 2:] = -(rng.random((S, 2)) < 0.5).astype(np.int64)
base = s[100000:580000].copy()
cases = []


def run(label, m, want):
    r = AL.compare(s, m, 4, 0)
    ok = bool(want(r))
    cases.append(dict(probe=label, verdict=r.get("verdict"), matches_of_first_window=r.get("matches_of_first_window"),
                      slips=r.get("slips"), frames_differing=r.get("frames_differing"),
                      compared_equal=r.get("compared_equal"), result="PASS" if ok else "FAIL"))


run("exact copy", base, lambda r: r["verdict"] == "SAMPLE-EXACT" and r["matches_of_first_window"] == 1
    and r["compared_equal"] == 480000)
m = np.delete(s[100000:580001], 200000, axis=0)
run("one frame dropped", m, lambda r: r["verdict"] == "DIFFERENT" and len(r["slips"]) == 1 and r["slips"][0]["step"] == 1)
m = np.insert(s[100000:579999], 250000, s[100000 + 249999], axis=0)
run("one frame repeated", m, lambda r: r["verdict"] == "DIFFERENT" and len(r["slips"]) == 1 and r["slips"][0]["step"] == -1)
m = base.copy()
m[300000, 3] -= 1
run("one sample changed", m, lambda r: r["verdict"] == "DIFFERENT" and r["frames_differing"] == 1)
m = base[:, [1, 0, 2, 3]].copy()
run("channels 0 and 1 swapped", m, lambda r: r["verdict"] != "SAMPLE-EXACT")
m = base[:, [0, 1, 3, 2]].copy()
run("channels 2 and 3 swapped", m, lambda r: r["verdict"] != "SAMPLE-EXACT")
m = np.zeros_like(base)
run("constant zero recording", m, lambda r: r["verdict"] != "SAMPLE-EXACT")
m = s[300007:780007].copy()
m[:, 0] = -m[:, 0]
run("another stretch, channel 0 negated", m, lambda r: r["verdict"] != "SAMPLE-EXACT")
m = base.copy()
m[:, 1] = 0
run("channel 1 dead", m, lambda r: r["verdict"] != "SAMPLE-EXACT")
out["P2_alignment"] = dict(cases=cases, all_pass=all(c["result"] == "PASS" for c in cases))

json.dump(out, open(sys.argv[2], "w"), indent=1)
print(json.dumps(out, indent=1))
sys.exit(0 if out["P2_alignment"]["all_pass"] else 1)
