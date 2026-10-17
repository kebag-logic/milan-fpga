#!/usr/bin/env python3
"""Lane B21 PR round 2: step 1's short floor-test groups against the board sampler (offline).

usage: B5_W=110 b21_floor_groups.py <reads_u16> <name.ts> <name.samp> <out_txt>

<reads_u16> is the published derived read record (b21_mcasp_ana.py: per read, the time since the
previous read in us); <name.ts> gives its monotonic origin (read 0) and <name.samp> the 1 Hz board
sampler, whose /proc/uptime stamps share the reads' monotonic timeline (the first sample is within
40 ms of read 0). The floor test is b21_mcasp_ana.py's (lane B5's definitions from b5_attrib.py,
W from B5_W): the step at read a is min D[a+GA .. a+GA+W] - min D[a-GB-W .. a-GB], with the delivery
deficit D(r) = t(r) * 48000 - 480 r.

For every sampler wake: the dip it leaves in the deficit, the minimum of the detrended deficit from
50 ms before to 300 ms after the wake, less the median over the second around it. For every group the
floor test flags: the wakes inside each of its two windows at the group's largest step, and their dips.
Then a mechanical check of one rule for both signs: a window's floor is set by its deepest dip, so the
sign of (deepest dip before - deepest dip after) must equal the sign of (step - drift) in every group.
"""
import os
import re
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import b5_attrib as b5  # noqa: E402

W, GB, GA, TOL, JOIN = b5.W, b5.GB, b5.GA, b5.TOL, b5.JOIN
rec, tsf, samp, out = sys.argv[1:5]
d = np.fromfile(rec, dtype="<u2").astype(np.int64)
ts = np.fromfile(tsf, dtype=np.dtype([("f", "<i8"), ("rt", "<f8"), ("mono", "<i8")]))
mono0 = ts["mono"][0] / 1e9
t = np.concatenate(([0], np.cumsum(d))) / 1e6
R = len(d)
D = t * b5.FS - b5.PER * np.arange(R + 1)
lines = []
p = lines.append
p(f"inputs: {Path(rec).name} sha256 {b5.sha256(Path(rec))}; {Path(tsf).name} sha256 {b5.sha256(Path(tsf))}; "
  f"{Path(samp).name} sha256 {b5.sha256(Path(samp))}; W={W} GB={GB} GA={GA} TOL={TOL}")
up = np.array([float(m.group(1)) for m in (re.match(r"^([0-9.]+) [0-9.]+$", ln) for ln in open(samp)) if m]) - mono0
p(f"sampler wakes: {len(up)}; first at {up[0]:+.3f} s from read 0; spacing s, percentiles 0/1/50/99/100: "
  f"{b5.pct(np.diff(up), (0, 1, 50, 99, 100))}; longest {np.diff(up).max():.3f} s; window span {W * 0.01 + 0.01:.2f} s")
pos = np.arange(GB + W, R - GA - W)
mn = np.lib.stride_tricks.sliding_window_view(D, W + 1).min(axis=1)
x = mn[pos + GA] - mn[pos - GB - W]
drift = float(np.median(x))
big = np.flatnonzero(np.abs(x - drift) > TOL)
grp = []
for i in big:
    if grp and pos[i] - grp[-1][-1] <= 2 * JOIN:
        grp[-1].append(int(pos[i]))
    else:
        grp.append([int(pos[i])])
s, i0 = np.polyfit(t, D, 1)
Rz = D - (s * t + i0)
dip = np.full(len(up), np.nan)
for k, u in enumerate(up):
    a, b = np.searchsorted(t, u - 0.05), np.searchsorted(t, u + 0.3)
    c, e = np.searchsorted(t, u - 0.5), np.searchsorted(t, u + 0.5)
    if b > a and e > c:
        dip[k] = Rz[a:b].min() - np.median(Rz[c:e])
p(f"drift over one floor test (median step) {drift:+.3f} frames; groups {len(grp)}")
p(f"sampler dips, frames, percentiles 0/1/50/99/100: {b5.pct(dip[~np.isnan(dip)], (0, 1, 50, 99, 100))}")
p(f"windows holding no sampler wake: {int(sum(((up >= t[a]) & (up <= t[a + W])).sum() == 0 for a in range(0, R - W, 5)))} "
  f"of {len(range(0, R - W, 5))} (every 5th window start)")
ok = True
for g in grp:
    a = max(g, key=lambda r: abs(x[r - GB - W] - drift))
    st = float(x[a - GB - W])
    bw, aw = (t[a - GB - W], t[a - GB]), (t[a + GA], t[a + GA + W])
    db = dip[(up >= bw[0]) & (up <= bw[1])]
    da = dip[(up >= aw[0]) & (up <= aw[1])]
    pred = np.sign(np.nanmin(db) - np.nanmin(da)) * -1 if len(db) and len(da) else 0
    agree = bool(len(db) and len(da) and np.sign(st - drift) == pred)
    ok &= agree
    p(f"group reads {g[0]} .. {g[-1]} (t {t[g[0]]:.3f} s): largest step {st:+.1f} ({st - drift:+.1f} against the drift) at read {a}; "
      f"wakes before {len(db)}, dips {np.round(db, 1).tolist()}; after {len(da)}, dips {np.round(da, 1).tolist()}; "
      f"deepest before - deepest after {np.nanmin(db) - np.nanmin(da):+.1f}; sign rule {'holds' if agree else 'FAILS'}")
p(f"sign rule holds in every group: {ok}")
Path(out).write_text("\n".join(lines) + "\n")
print("\n".join(lines))
sys.exit(0 if ok else 1)
