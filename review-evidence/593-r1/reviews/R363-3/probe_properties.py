#!/usr/bin/env python3
"""R363-3 behavioural probes of the #593 tu/mr oracles at a given checkout.

Usage: probe_properties.py <repo>
Imports tb/tools/torture_campaign.py read-only (python3 -B) and prints one
line per probe: PROBE <id> <expected> <observed> <OK|MISMATCH>, then a summary.
Exit status 0 iff every probe matches.
"""
from __future__ import annotations

import importlib.util
import itertools
import sys
from decimal import Decimal
from pathlib import Path

sys.dont_write_bytecode = True
repo = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("tc", repo / "tb/tools/torture_campaign.py")
tc = importlib.util.module_from_spec(spec)
sys.modules["tc"] = tc
spec.loader.exec_module(tc)
tu, hist, mr, Cap = tc.check_release_tu, tc.check_release_tu_history, tc.check_release_mr, tc.ReleaseCapture
bad = 0


def probe(pid: str, expected, observed) -> None:
    global bad
    ok = observed == expected if not callable(expected) else expected(observed)
    bad += not ok
    exp = expected if not callable(expected) else getattr(expected, "__doc__", "predicate")
    print(f"PROBE {pid}\texpected={exp}\tobserved={observed}\t{'OK' if ok else 'MISMATCH'}")


# ---- P1: two-sided minimum. A true instant clear (d = 0) observed anywhere in
# [0, R] must never PASS, for every deciding R; R >= 0.125 is NOT RUN.
worst = set()
for r_us in list(range(0, 125000, 997)) + [124999, 124990, 1000, 62500]:
    R = r_us / 1e6
    for frac in (0.0, 0.25, 0.5, 0.999, 1.0):
        h = R * frac
        if h <= 0:
            h = 1e-6 if R >= 1e-6 else 1e-9
            if h > R and R > 0:
                continue
        for oracle in ("single", "history"):
            if oracle == "single":
                v = tu((0, h), [], gm_changes_s=[0], holdover_bound_s=0.5,
                       observation_resolution_s=R, capture_complete=True)[0]
            else:
                v = hist([(0, h)], [], gm_changes_s=[0], observation_resolution_s=R, capture_complete=True)[0]
            worst.add(v)
probe("P1 instant clear (d=0, h<=R) never PASS for R<0.125", {"FAIL"}, worst)

# GM change with tu never set (no interval) fails in history.
probe("P1b GM with no interval", "FAIL",
      hist([], [], gm_changes_s=[0], observation_resolution_s=0.001, capture_complete=True)[0])

# ---- P2: minimum soundness over an error model. Observed h = d + e, |e| <= R.
# PASS must imply d >= 0.25 - 2R; FAIL on the minimum must imply d < 0.25.
viol_pass = viol_fail = 0
for R, d, e in itertools.product((0, 0.001, 0.05, 0.1, 0.124999),
                                 (0.0, 0.01, 0.1, 0.12, 0.2, 0.249, 0.25, 0.3),
                                 (-1, -0.5, 0, 0.5, 1)):
    h = d + e * R
    if h <= 0:
        continue
    v = hist([(0, h)], [], gm_changes_s=[0], observation_resolution_s=R, capture_complete=True)[0]
    if v == "PASS" and Decimal(str(d)) < Decimal("0.25") - 2 * Decimal(str(R)):
        viol_pass += 1
    if v == "FAIL" and Decimal(str(d)) >= Decimal("0.25"):
        viol_fail += 1
probe("P2a minimum PASS implies d >= 0.25-2R", 0, viol_pass)
probe("P2b minimum FAIL implies d < 0.25", 0, viol_fail)

# ---- P3: upper bound. PASS must not admit a true hold beyond 0.5 + R.
viol = 0
for R, h in itertools.product((0, 0.001, 0.05, 0.124999),
                              (0.3, 0.49, 0.5, 0.500001, 0.51, 0.55, 0.62)):
    v = hist([(0, h)], [0], gm_changes_s=[], observation_resolution_s=R, capture_complete=True)[0]
    worst_d = Decimal(str(h)) + Decimal(str(R))
    if v == "PASS" and worst_d > Decimal("0.5") + Decimal(str(R)):
        viol += 1
probe("P3 upper PASS never admits d > 0.5+R", 0, viol)
probe("P3b h=0.5 R=0.1 PASS", "PASS",
      hist([(0, 0.5)], [0], gm_changes_s=[], observation_resolution_s=0.1, capture_complete=True)[0])
probe("P3c h=0.5000001 R=0.1 FAIL", "FAIL",
      hist([(0, 0.5000001)], [0], gm_changes_s=[], observation_resolution_s=0.1, capture_complete=True)[0])
# Upper measured from the LAST discontinuity (chained).
probe("P3d chained last disc 0.2, clear 0.7 PASS", "PASS",
      hist([(0, 0.7)], [0, 0.2], gm_changes_s=[], observation_resolution_s=0.001, capture_complete=True)[0])
probe("P3e chained last disc 0.2, clear 0.701 FAIL", "FAIL",
      hist([(0, 0.701)], [0, 0.2], gm_changes_s=[], observation_resolution_s=0.001, capture_complete=True)[0])

# ---- P4: resolution gate, both oracles, including an empty history.
for R, exp in ((0.124999, "PASS"), (0.125, "NOT RUN"), (0.2, "NOT RUN"), (0.25, "NOT RUN")):
    probe(f"P4 empty history R={R}", exp,
          hist([], [], gm_changes_s=[], observation_resolution_s=R, capture_complete=True)[0])

# ---- P5: every NOT RUN (and every verdict) carries resolution_limit_s and R.
def has_meta(result, limit, R):
    v, d = result
    return (d.get("resolution_limit_s") == limit and d.get("observation_resolution_s") == R, v)

single = dict(interval_s=(0, 0.3), discontinuities_s=[0], gm_changes_s=[0],
              holdover_bound_s=0.5, observation_resolution_s=0.001, capture_complete=True)
tu_cases = {
    "tu capture False": dict(capture_complete=False), "tu gm None": dict(gm_changes_s=None),
    "tu interval None": dict(interval_s=None), "tu disc None": dict(discontinuities_s=None),
    "tu interval len1": dict(interval_s=(0,)), "tu nonfinite event": dict(discontinuities_s=[float("nan")]),
    "tu zero interval": dict(interval_s=(0, 0)), "tu bound 5": dict(holdover_bound_s=5),
    "tu R=-1": dict(observation_resolution_s=-1), "tu R=0.125": dict(observation_resolution_s=0.125),
    "tu R=None": dict(observation_resolution_s=None),
    "tu uncorrelated FAIL": dict(discontinuities_s=[], gm_changes_s=[], interval_s=(1, 1.1)),
    "tu rise FAIL": dict(interval_s=(0, 0.3), discontinuities_s=[0.1], gm_changes_s=[]),
    "tu min FAIL": dict(interval_s=(0, 0.1)), "tu upper FAIL": dict(interval_s=(0, 0.6)),
    "tu PASS": dict(),
}
for name, over in tu_cases.items():
    args = dict(single, **over)
    R = args["observation_resolution_s"]
    meta, v = has_meta(tu(**args), 0.125, R)
    probe(f"P5 {name} [{v}] carries limit+R", True, meta)

hargs = dict(intervals_s=[(0, 0.3)], discontinuities_s=[0], gm_changes_s=[0],
             observation_resolution_s=0.001, capture_complete=True)
h_cases = {
    "hist capture False": dict(capture_complete=False), "hist intervals None": dict(intervals_s=None),
    "hist disc None": dict(discontinuities_s=None), "hist gm None": dict(gm_changes_s=None),
    "hist R None": dict(observation_resolution_s=None), "hist R 0.2": dict(observation_resolution_s=0.2),
    "hist nonfinite": dict(gm_changes_s=[float("inf")]), "hist bad interval": dict(intervals_s=[(0, "x")]),
    "hist touching": dict(intervals_s=[(0, 0.3), (0.3, 0.6)]), "hist nested FAIL": dict(intervals_s=[(0, 0.1)]),
    "hist uncovered GM FAIL": dict(gm_changes_s=[0, 5]), "hist PASS": dict(),
}
for name, over in h_cases.items():
    args = dict(hargs, **over)
    R = args["observation_resolution_s"]
    meta, v = has_meta(hist(**args), 0.125, R)
    probe(f"P5 {name} [{v}] carries limit+R", True, meta)


def trace(n=20, toggle_at=1):
    return [{"stream_id": "s", "timestamp_s": i / 100, "pdu_index": i, "mr": int(i >= toggle_at)}
            for i in range(n)]


margs = dict(stream_id="s", pdus=trace(), causes=[{"stream_id": "s", "timestamp_s": 0.01,
                                                   "kind": "CRF disruption"}],
             media_reset_reads=[{"stream_id": "s", "timestamp_s": 0, "value": 0},
                                {"stream_id": "s", "timestamp_s": 0.19, "value": 1}],
             observation_resolution_s=0.001, capture_complete=Cap((-2, 2)))
m_cases = {
    "mr capture False": dict(capture_complete=False), "mr empty stream": dict(stream_id=""),
    "mr pdus None": dict(pdus=None), "mr causes None": dict(causes=None),
    "mr reads None": dict(media_reset_reads=None), "mr R None": dict(observation_resolution_s=None),
    "mr R 0.5": dict(observation_resolution_s=0.5),
    "mr invalid record": dict(pdus=[dict(trace()[0], mr=2)] + trace()[1:]),
    "mr one read": dict(media_reset_reads=[{"stream_id": "s", "timestamp_s": 0, "value": 0}]),
    "mr bool capture no pdus": dict(pdus=[], capture_complete=True),
    "mr nonfinite window": dict(capture_complete=Cap((float("nan"), 2))),
    "mr short span": dict(capture_complete=Cap((-0.5, 2))),
    "mr pdu gap": dict(pdus=trace()[:5] + trace()[6:]),
    "mr unfinished tail": dict(pdus=trace(n=5)),
    "mr unordered reads": dict(media_reset_reads=[{"stream_id": "s", "timestamp_s": 0.19, "value": 0},
                                                  {"stream_id": "s", "timestamp_s": 0.1, "value": 1}]),
    "mr uncaused FAIL": dict(causes=[]), "mr PASS": dict(),
}
for name, over in m_cases.items():
    args = dict(margs, **over)
    R = args["observation_resolution_s"]
    meta, v = has_meta(mr(**args), 0.5, R)
    probe(f"P5 {name} [{v}] carries limit+R", True, meta)

# ---- P6: boundary semantics this report relies on.
probe("P6a equal consecutive PDU timestamps accepted", "PASS",
      mr(**dict(margs, pdus=[dict(p, timestamp_s=0.05 if p["pdu_index"] == 6 else p["timestamp_s"])
                             for p in trace()]))[0])
probe("P6b pdu_index -1 rejected (NOT RUN)", "NOT RUN",
      mr(**dict(margs, pdus=[dict(p, pdu_index=p["pdu_index"] - 1) for p in trace()]))[0])
probe("P6c GM exactly at start-R covered and graded (long hold PASS)", "PASS",
      hist([(0.3005, 0.7)], [], gm_changes_s=[0.3], observation_resolution_s=0.0005, capture_complete=True)[0])

print(f"SUMMARY mismatches={bad}")
raise SystemExit(1 if bad else 0)
