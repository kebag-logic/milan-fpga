#!/usr/bin/env python3
"""Where do the 2..59-frame skips sit relative to the >=60-frame skips (capture stalls)?
Uses continuity-events.csv only. usage: small_skip_context.py <author dir>"""
import csv, json, statistics, sys
from collections import Counter
from pathlib import Path
A = Path(sys.argv[1]); FS = 48000
ev = [dict(frame=int(r["frame"]), kind=r["kind"], frames=int(r["frames"]))
      for r in csv.DictReader(open(A / "summary/a-long/continuity-events.csv"))]
large = [e["frame"] for e in ev if e["kind"] == "skip" and e["frames"] >= 60]
small = [e for e in ev if e["kind"] == "skip" and 2 <= e["frames"] < 60]
import bisect
def dist(f):
    i = bisect.bisect_left(large, f)
    c = [abs(f - large[j]) for j in (i - 1, i) if 0 <= j < len(large)]
    return min(c)
d = [dist(e["frame"]) for e in small]
for lim in (480, 4800, 24000, 48000):
    n = sum(1 for x in d if x <= lim)
    print(f"small skips within {lim/FS*1000:.0f} ms of a >=60-frame skip: {n} of {len(small)}, frames "
          f"{sum(e['frames'] for e, x in zip(small, d) if x <= lim)}")
six = [e for e in small if e["frames"] == 6]
d6 = [dist(e["frame"]) for e in six]
print("six-frame skips:", len(six), "median distance to nearest large skip, s", statistics.median(d6) / FS)
# expected median distance if uniform in time, given large-skip spacing
gaps = [b - a for a, b in zip(large, large[1:])]
print("large-skip spacing median s", statistics.median(gaps) / FS, "-> uniform expectation of median distance about",
      statistics.median(gaps) / FS / 4, "s")
# clustering of small skips among themselves
sf = [e["frame"] for e in small]
sg = [b - a for a, b in zip(sf, sf[1:])]
print("small-skip spacing: median s", statistics.median(sg) / FS, "share within 50 ms of previous small skip",
      sum(1 for g in sg if g < 2400) / len(sg))
print("small skip size histogram", sorted(Counter(e["frames"] for e in small).items()))
# window-level frame accounting from summary.json
s = json.load(open(A / "summary/a-long/summary.json")); c = s["continuity"]
T = c["window_time"][1] - c["window_time"][0]
lost2 = sum(e["frames"] for e in ev if e["kind"] == "skip" and e["frames"] >= 2)
print(f"window host time {T:.6f} s; captured {c['frames']}; host-clock frames {T*FS:.1f}; "
      f"captured deficit {T*FS - c['frames']:.1f}; skipped >=2 {lost2}; difference {T*FS - c['frames'] - lost2:.1f} "
      f"(= {1e6*(T*FS - c['frames'] - lost2)/(T*FS):.2f} ppm of the window, the peer output's rate offset if every >=2 skip is a capture loss)")
print("page figure 115,614 implies captured deficit short of the >=2 skips by", lost2 - 115614,
      "frames; adding a 17.3 ppm peer offset (", round(17.3e-6 * T * FS), "frames ) leaves", lost2 - 115614 + round(17.3e-6 * T * FS))
