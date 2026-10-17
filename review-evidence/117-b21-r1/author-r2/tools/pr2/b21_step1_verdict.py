#!/usr/bin/env python3
"""Lane B21 PR round 2: step 1's mechanical verdict on the McASP self-test, with planted losses (offline).

usage: b21_step1_verdict.py <name-reads.u16|u32> <name-reads.json> <out_json>

CLEAN needs all four:
  overruns     arecord logged no overrun (reads.json arecord_overruns = 0);
  stamper      the stamper dropped no byte (dropped_bytes=0 in its log line);
  one period   every read inside the window delivered one period (reads_not_one_period empty);
  block floor  the deficit's floor over consecutive 10 s blocks (1,000 reads), less its linear fit,
               changes by at most LIMIT frames from one block to the next. LIMIT is lane B5's match
               tolerance, 4 frames (b5_attrib.TOL), fixed before the planted controls ran.
Planted controls: a loss of k frames after sampling delays every later read's frames by k/48000 s
against the read clock, so the record's time is advanced by that much from one read on. Each plant
must turn the verdict to NOT CLEAN through the block-floor test alone (the other three inputs are
unchanged by a plant).
"""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import b5_attrib as b5  # noqa: E402

LIMIT = b5.TOL
rec, meta, out = sys.argv[1:4]
enc = "<u2" if rec.endswith(".u16") else "<u4"
d = np.fromfile(rec, dtype=enc).astype(np.int64)
m = json.load(open(meta))


def block_change(t):
    D = t * b5.FS - b5.PER * np.arange(len(t))
    wn = 1000
    starts = list(range(0, len(D) - wn + 1, wn))
    fl = np.array([D[a:a + wn].min() for a in starts])
    tc = np.array([t[a] for a in starts])
    s, i = np.polyfit(tc, fl, 1)
    r = fl - (s * tc + i)
    return float(np.abs(np.diff(r)).max()), float(r.min()), float(r.max())


def verdict(t):
    ch, lo, hi = block_change(t)
    checks = dict(overruns=m["arecord_overruns"] == 0, stamper="dropped_bytes=0" in m["stamper"],
                  one_period=not m["reads_not_one_period"], block_floor=ch <= LIMIT)
    return dict(clean=all(checks.values()), checks=checks, block_change_frames=round(ch, 2),
                block_residual_frames=[round(lo, 2), round(hi, 2)], limit_frames=LIMIT)


t0 = np.concatenate(([0], np.cumsum(d))) / 1e6
res = dict(record=dict(file=Path(rec).name, sha256=b5.sha256(Path(rec)), reads=int(len(d))),
           as_recorded=verdict(t0), controls=[])
ok = res["as_recorded"]["clean"]
for k in (6, 12, 48):
    for frac in (0.25, 0.5, 0.75):
        r0 = int(len(t0) * frac)
        t = t0.copy()
        t[r0:] += k / b5.FS
        v = verdict(t)
        res["controls"].append(dict(planted_frames=k, at_read=r0, clean=v["clean"], block_change_frames=v["block_change_frames"]))
        ok &= not v["clean"]
res["as_recorded_clean_and_every_plant_caught"] = ok
json.dump(res, open(out, "w"), indent=1)
print(json.dumps(res, indent=1))
sys.exit(0 if ok else 1)
