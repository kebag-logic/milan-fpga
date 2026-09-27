#!/usr/bin/env python3
"""[R362] round-2 behavioural probes for PR #601 (issue #593).

Usage: python3 -B r362_2_behaviour.py <repo-checkout>

Imports tb/tools/torture_campaign.py read-only and prints one line per probe:
PROBE <id> <OK|UNEXPECTED> expected=<v> actual=<v> <note>. "expected" is what
the round-2 assignment / docs require; it is not the author's test oracle.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(sys.argv[1]).resolve() / "tb" / "tools"))
import torture_campaign as tp  # noqa: E402

results = []


def probe(pid, expected, got, note):
    verdict, detail = got
    ok = verdict == expected
    results.append(ok)
    extra = {k: detail.get(k) for k in ("why", "resolution_limit_s", "observation_resolution_s") if k in detail}
    print(f"PROBE {pid} {'OK' if ok else 'UNEXPECTED'} expected={expected} actual={verdict} {note} {extra}")


def tu(interval, events, gm, r):
    return tp.check_release_tu(interval, events, holdover_bound_s=0.5, observation_resolution_s=r,
                               capture_complete=True, gm_changes_s=gm)


def hist(intervals, events, gm, r):
    return tp.check_release_tu_history(intervals, events, observation_resolution_s=r,
                                       capture_complete=True, gm_changes_s=gm)


def trace(stream="s", toggles=(1,), n=40, dt=0.01, t0=0.0):
    level, out = 0, []
    for i in range(n):
        if i in toggles:
            level ^= 1
        out.append({"stream_id": stream, "timestamp_s": round(t0 + i * dt, 9), "pdu_index": i, "mr": level})
    return out


def cause(t, kind="media-clock-source change", stream="s"):
    return {"stream_id": stream, "timestamp_s": t, "kind": kind}


def reads(*pairs, stream="s"):
    return [{"stream_id": stream, "timestamp_s": t, "value": v} for t, v in pairs]


def mr(pdus, causes, rd, r=0.001, window=(-2.0, 2.0), stream="s"):
    cap = tp.ReleaseCapture(window) if window is not None else True
    return tp.check_release_mr(stream, pdus, causes, rd, observation_resolution_s=r, capture_complete=cap)


# ---- item 1: rise before first recorded discontinuity -----------------------------
probe("I1a", "FAIL", tu((0, 10.4), [10], [], 0.001), "rise at 0, lone event at 10 (R347-5 S1 case)")
probe("I1b", "FAIL", hist([(0, 10.4)], [10], [], 0.001), "same case through the planned history oracle")
probe("I1c", "PASS", tu((0, 0.3), [0.001], [], 0.001), "first event exactly R after rise")
probe("I1d", "FAIL", tu((0, 0.3), [0.0011], [], 0.001), "first event just beyond R after rise")
probe("I1e", "FAIL", tu((0, 0.6), [0.3, 0.0015], [], 0.001), "unordered event list; earliest still beyond R")

# ---- item 2: every GM change graded -------------------------------------------------
probe("I2a", "FAIL", hist([], [], [5.0], 0.001), "GM change, tu never set")
probe("I2b", "FAIL", hist([(5.0, 5.3)], [], [5.0, 5.3], 0.001), "second GM change exactly at clear")
probe("I2c", "FAIL", hist([(5.0, 5.0005)], [], [5.0], 0.001), "tu clears 0.5 ms after GM change")
probe("I2d", "FAIL", hist([(0, 0.3)], [0], [0, 10.0], 0.001), "later GM change with no interval")
probe("I2e", "PASS", hist([(0, 0.3), (10.0, 10.3)], [], [0, 10.0], 0.001), "two covered GM changes")
probe("I2f", "FAIL", hist([(0, 0.3), (10.0, 10.2)], [], [0, 10.0], 0.001), "second hold 0.2 s")

# ---- item 3: deciding resolution ------------------------------------------------------
probe("I3a", "NOT RUN", tu((0, 0.3), [0], [0], 0.25), "tu single-interval at R = 0.25")
probe("I3b", "NOT RUN", hist([], [], [], 0.25), "history at R = 0.25 with no intervals")
probe("I3c", "NOT RUN", mr(trace(), [cause(0.01)], reads((0, 0), (0.39, 1)), r=0.5), "mr at R = 0.5")
probe("I3d", "PASS", mr(trace(), [cause(0.01)], reads((0, 0), (0.39, 1)), r=0.499), "mr at R = 0.499")
# Resolution-vs-minimum decidability (finding F1): these are what the gate does, and
# "expected" states the result an instant-clear / short hold must have per item 2.
probe("I3e", "FAIL", hist([(0, 0.002)], [], [0], 0.249), "2 ms observed hold after GM, R = 0.249")
probe("I3f", "FAIL", hist([(0, 0.06)], [], [0], 0.2), "60 ms observed hold after GM, R = 0.2")
probe("I3g", "FAIL", hist([(0, 0.13)], [], [0], 0.125), "hold observed = R, R = 0.125 (true hold may be 0)")
probe("I3h", "FAIL", hist([(0, 0.124)], [], [0], 0.124), "hold observed = R, R = 0.124 (true hold may be 0)")
probe("I3i", "PASS", hist([(0, 0.3)], [], [0], 0.2), "compliant-looking 0.3 s hold at R = 0.2")
det = hist([(0, 0.3)], [], [0], 0.001)[1]
print(f"STATED history resolution_limit_s={det.get('resolution_limit_s')}")

# ---- item 4: one cause excuses at most one toggle per stream -------------------------
p = trace(toggles=(1, 9, 17), n=40, dt=0.0001)
probe("I4a", "FAIL", mr(p, [cause(0.0009)], reads((0, 0), (0.0039, 3)), r=0.001), "one cause, three toggles")
probe("I4b", "FAIL", mr(p, [cause(0.0005), cause(0.0013)], reads((0, 0), (0.0039, 3)), r=0.001),
      "two causes, three toggles")
probe("I4c", "PASS", mr(p, [cause(0.0001), cause(0.0009), cause(0.0017)], reads((0, 0), (0.0039, 3)), r=0.001),
      "three causes, three toggles")
two = trace("a") + trace("b")
cs = [cause(0.01, stream="a"), cause(0.01, stream="b")]
rd = reads((0, 0), (0.39, 1), stream="a") + reads((0, 0), (0.39, 1), stream="b")
probe("I4d", "PASS", mr(two, cs, rd, stream="a"), "per-stream causes, stream a")
probe("I4e", "PASS", mr(two, cs, rd, stream="b"), "per-stream causes, stream b")

# ---- item 6: PHC-only causes keep failing ------------------------------------------------
for kind in ("PHC settime/adjtime", "PHC step", "media re-base", "GM-identity edge", "GM time-source change"):
    probe("I6-" + kind.replace(" ", "_"), "FAIL", mr(trace(), [cause(0.01, kind)], reads((0, 0), (0.39, 1))),
          f"toggle with only '{kind}' cause")

# ---- item 7: capture span and MEDIA_RESET decrease --------------------------------------
probe("I7a", "NOT RUN", mr(trace(), [cause(0.01)], reads((0, 0), (0.39, 1)), window=(-0.5, 0.5)),
      "capture starts after first read - 1 s - R")
probe("I7b", "NOT RUN", mr(trace(), [cause(0.01)], reads((0, 0), (0.39, 1)), window=None),
      "boolean completeness, PDUs start at first read")
probe("I7c", "NOT RUN", mr(trace(), [cause(0.01)], reads((0, 0), (0.39, 1)), window=(-2, 0.3)),
      "capture ends before last read")
probe("I7d", "FAIL", mr(trace(), [cause(0.01)], reads((0, 5), (0.39, 0))), "MEDIA_RESET 5 -> 0")
print("  why:", mr(trace(), [cause(0.01)], reads((0, 5), (0.39, 0)))[1].get("why"))
probe("I7e", "FAIL", mr(trace(toggles=()), [], reads((0, 2**32 - 1), (0.39, 0))), "MEDIA_RESET max -> 0, no toggle")

# ---- survivor distinguishing inputs (finding F2) -----------------------------------------
probe("S-C06", "FAIL", hist([(0, 0.01)], [0], [-0.0005], 0.001),
      "GM inside start allowance, 10 ms hold (C06 mutant would PASS)")
probe("S-C07", "PASS", hist([(0, 0.3), (0.3005, 0.6)], [], [0, 0.3], 0.001),
      "GM at clear of #1, covered by #2's start allowance (C07 mutant would FAIL)")
probe("S-C09", "NOT RUN", hist([(0, 0.3), (0.3, 0.6)], [0], [0], 0.001),
      "touching intervals (C09 mutant grades them instead of refusing)")
probe("S-C10", "NOT RUN", hist([], [], [], -1.0), "negative resolution, empty history (C10 mutant would PASS)")
probe("S-C34", "NOT RUN", mr(trace(), [cause(0.01), cause(0.02, stream="")], reads((0, 0), (0.39, 1))),
      "empty stream_id record (C34 mutant would PASS)")
bad = trace()
bad_neg = [dict(x, pdu_index=x["pdu_index"] - 5) for x in bad]
probe("S-C35", "NOT RUN", mr(bad_neg, [cause(0.01)], reads((0, 0), (0.39, 1))),
      "negative pdu_index (C35 mutant would PASS)")

print(f"SUMMARY ok={sum(results)} unexpected={len(results) - sum(results)} total={len(results)}")
