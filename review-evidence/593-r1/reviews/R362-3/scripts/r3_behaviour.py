#!/usr/bin/env python3
"""[R362] round-3 behavioural probes for PR #601 (issue #593) under the round-3 decision.

usage: python3 -B r3_behaviour.py <tree-with-tb/tools>
Prints PROBE <id> <OK|UNEXPECTED> expected=<v> actual=<v> <note>. Expectations come from
issue 593 comment 5859532913 (two-sided model), TESTING 6d and REQ-VER-06, not from the tests.
"""
import itertools, sys
from decimal import Decimal
from pathlib import Path
sys.path.insert(0, str(Path(sys.argv[1]).resolve() / "tb" / "tools"))
import torture_campaign as tp

ok = bad = 0
def probe(pid, expected, got, note, detail=None):
    global ok, bad
    good = got in expected if isinstance(expected, (set, frozenset)) else got == expected
    ok += good; bad += not good
    print(f"PROBE {pid} {'OK' if good else 'UNEXPECTED'} expected={expected} actual={got} {note}"
          + (f" {detail}" if detail is not None and not good else ""))

def hist(intervals, events, gm, r):
    return tp.check_release_tu_history(intervals, events, gm_changes_s=gm,
                                       observation_resolution_s=r, capture_complete=True)
def single(interval, events, gm, r):
    return tp.check_release_tu(interval, events, gm_changes_s=gm, holdover_bound_s=0.5,
                               observation_resolution_s=r, capture_complete=True)

# Round-2 probes under the round-3 decision
for pid, iv, r, exp in (("I3e", (0, 0.002), 0.249, {"FAIL", "NOT RUN"}), ("I3f", (0, 0.06), 0.2, {"FAIL", "NOT RUN"}),
                        ("I3g", (0, 0.13), 0.125, {"FAIL", "NOT RUN"}), ("I3h", (0, 0.124), 0.124, "FAIL")):
    v, d = hist([iv], [], [0], r)
    probe(pid, exp, v, f"GM 0, tu {iv}, R={r} (must not PASS; I3h FAIL)", d)

# D0: instant-clear soundness sweep. True d=0 is observed as h in (0, R]; every R < 0.125 must FAIL,
# every R >= 0.125 must be NOT RUN. Both oracles.
grid_r = [0, 1e-6, 0.001, 0.01, 0.05, 0.1, 0.12, 0.124, 0.124999, 0.125, 0.125001, 0.2, 0.249, 0.25, 1]
viol = []
for r in grid_r:
    for frac in (0.001, 0.25, 0.5, 0.999, 1.0):
        h = r * frac if r > 0 else 1e-6
        if h <= 0: continue
        for name, fn in (("hist", lambda: hist([(0, h)], [], [0], r)), ("single", lambda: single((0, h), [], [0], r))):
            v, _ = fn()
            want = "FAIL" if r < 0.125 else "NOT RUN"
            if v != want: viol.append((name, r, h, v))
probe("D0", [], viol, "instant true clear never PASSes; NOT RUN iff R >= 0.125")

# D1: minimum PASS soundness: any PASS implies h + R >= 0.25, so d >= 0.25 - 2R > 0
viol = []
for r in (0, 0.001, 0.05, 0.1, 0.124999):
    for h in [x / 1000 for x in range(1, 520)]:
        v, _ = hist([(0, h)], [], [0], r)
        if v == "PASS" and Decimal(str(h)) + Decimal(str(r)) < Decimal("0.25"): viol.append((r, h))
        if v != "PASS" and Decimal(str(h)) + Decimal(str(r)) >= Decimal("0.25") and h <= 0.5: viol.append((r, h, v))
probe("D1", [], viol, "minimum decided exactly at h + R >= 0.25 (h <= 0.5)")

# D2: upper PASS soundness: PASS iff h <= 0.5 after the last discontinuity, independent of R (< limit)
viol = []
for r in (0, 0.001, 0.05, 0.124999):
    for h in (0.4, 0.499999, 0.5, 0.500001, 0.51, 0.5 + r, 0.5 + 2 * r):
        v, d = hist([(0, h)], [0], [], r)
        want = "PASS" if Decimal(str(h)) <= Decimal("0.5") else "FAIL"
        if v != want: viol.append((r, h, v))
probe("D2", [], viol, "upper: PASS iff observed hold h <= 0.5 s, so true d <= 0.5 + R")

# D3: the #586 arm (clear 0.76, events 0 and 0.25, R 0.01) is FAIL now: h = 0.51 > 0.5
probe("D3", "FAIL", single((0, 0.76), [0, 0.25], [], 0.01)[0], "PR #586 arm now FAIL under the two-sided upper bound")
probe("D3b", "PASS", single((0, 0.75), [0, 0.25], [], 0.01)[0], "h = 0.5 at R 0.01 passes")

# D4: GM then PHC step: minimum from GM, upper from the step
probe("D4a", "PASS", hist([(0, 0.62)], [0.2], [0], 0.001)[0], "TESTING example: GM 0, step 0.2, clear 0.62")
probe("D4b", "FAIL", hist([(0, 0.8)], [0.2], [0], 0.001)[0], "TESTING example: clear 0.8")
probe("D4c", "FAIL", hist([(0, 0.24)], [], [0], 0.001)[0], "TESTING: 0.24 s after GM fails at R 0.001")
probe("D4d", "PASS", hist([(0, 0.249)], [], [0], 0.001)[0], "TESTING: 0.249 s meets minimum at R 0.001")
# D5: GM at an interval's clear instant belongs to no preceding interval
probe("D5", "FAIL", hist([(0, 0.3)], [0], [0, 0.3], 0.001)[0], "GM at clear, no later interval")
# D6: never-set tu after a GM change fails
probe("D6", "FAIL", hist([], [], [5.0], 0.001)[0], "GM with tu never set")
probe("D6b", "NOT RUN", hist([], [], [5.0], 0.125)[0], "GM with tu never set at R = limit")
# D7: empty history at coarse R is NOT RUN; at fine R PASS
probe("D7a", "PASS", hist([], [], [], 0.124999)[0], "empty history, R just below limit")
probe("D7b", "NOT RUN", hist([], [], [], 0.125)[0], "empty history, R at limit")

# N: every NOT RUN verdict records resolution_limit_s and observation_resolution_s (R363-2 S1)
def mr(**kw):
    base = dict(stream_id="s", pdus=[{"stream_id": "s", "timestamp_s": i / 100, "pdu_index": i, "mr": 0} for i in range(20)],
                causes=[], media_reset_reads=[{"stream_id": "s", "timestamp_s": 0.05, "value": 0},
                                              {"stream_id": "s", "timestamp_s": 0.15, "value": 0}],
                observation_resolution_s=0.001, capture_complete=tp.ReleaseCapture((-2, 2)))
    base.update(kw); return tp.check_release_mr(**base)
pd = [{"stream_id": "s", "timestamp_s": i / 100, "pdu_index": i, "mr": 0} for i in range(20)]
gap = pd[:5] + pd[6:]
tail = [dict(p, mr=1 if i >= 17 else 0) for i, p in enumerate(pd)]
cases = {
  "mr-gap": mr(pdus=gap),
  "mr-tail": mr(pdus=tail, causes=[{"stream_id": "s", "timestamp_s": 0.17, "kind": "CRF disruption"}]),
  "mr-invalid": mr(causes=[{"stream_id": "s", "timestamp_s": 0.1, "kind": 3}]),
  "mr-span": mr(capture_complete=tp.ReleaseCapture((0.0, 2))),
  "mr-unordered-reads": mr(media_reset_reads=[{"stream_id": "s", "timestamp_s": 0.15, "value": 0},
                                              {"stream_id": "s", "timestamp_s": 0.05, "value": 0}]),
  "mr-one-read": mr(media_reset_reads=[{"stream_id": "s", "timestamp_s": 0.05, "value": 0}]),
  "mr-coarse": mr(observation_resolution_s=0.5),
  "mr-none": mr(pdus=None),
  "tu-coarse": single((0, 0.3), [0], [0], 0.2),
  "tu-none": tp.check_release_tu((0, 0.3), [0], gm_changes_s=None, holdover_bound_s=0.5, observation_resolution_s=0.001, capture_complete=True),
  "tu-nan": single((0, float("nan")), [0], [0], 0.001),
  "tu-order": single((0.3, 0.3), [0], [0], 0.001),
  "hist-coarse": hist([], [], [], 0.2),
  "hist-inf": hist([], [float("inf")], [], 0.001),
  "hist-bad-interval": hist([(0,)], [], [], 0.001),
  "hist-touching": hist([(0, 0.3), (0.3, 0.6)], [0, 0.3], [], 0.001),
}
for name, (v, d) in cases.items():
    good = v == "NOT RUN" and "resolution_limit_s" in d and "observation_resolution_s" in d
    probe(f"N-{name}", True, good, f"verdict={v} limit={d.get('resolution_limit_s')} R={d.get('observation_resolution_s')}")
# F: FAIL verdicts carry R too ("Resolution appears in every timing verdict")
fails = {"tu-uncorrelated": single((0, 0.3), [], [], 0.001), "tu-rise": single((0, 10.4), [10], [], 0.001),
         "tu-min": hist([(0, 0.1)], [], [0], 0.001), "hist-uncovered": hist([], [], [1], 0.001),
         "mr-uncaused": mr(pdus=[dict(p, mr=1 if i >= 5 else 0) for i, p in enumerate(pd)])}
for name, (v, d) in fails.items():
    carried = "observation_resolution_s" in d or "observation_resolution_s" in d.get("evidence", {})
    probe(f"F-{name}", True, v == "FAIL" and carried, f"verdict={v} R-recorded={carried} limit={d.get('resolution_limit_s')}")
print(f"SUMMARY ok={ok} unexpected={bad} total={ok + bad}")
