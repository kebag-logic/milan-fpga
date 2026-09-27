#!/usr/bin/env python3
"""R363-2 reviewer probe: grade the #593 round-2 oracles against expectations
derived from the issue #593 round-2 assignment, REQ-VER-06 and TESTING 6d.

Usage: probe_r2.py <path/to/torture_campaign.py>
Exit 0 when every case meets its expectation; 1 otherwise. Output: one line per case.
"""
from __future__ import annotations

import importlib.util
import sys

spec = importlib.util.spec_from_file_location("tc", sys.argv[1])
tc = importlib.util.module_from_spec(spec)
sys.modules["tc"] = tc
spec.loader.exec_module(tc)
TU, HIST, MR, CAP = tc.check_release_tu, tc.check_release_tu_history, tc.check_release_mr, tc.ReleaseCapture

cases: list[tuple[str, str, object]] = []


def case(name, expected, thunk, check=None):
    try:
        verdict, detail = thunk()
    except Exception as exc:  # a crash is never a verdict
        verdict, detail = f"EXC {type(exc).__name__}: {exc}", {}
    ok = verdict == expected and (check is None or check(detail))
    cases.append((name, expected, verdict, ok, detail))


def tu(interval, disc, gm, r=0.001):
    return lambda: TU(interval, disc, holdover_bound_s=0.5, observation_resolution_s=r,
                      capture_complete=True, gm_changes_s=gm)


def hist(intervals, disc, gm, r=0.001, complete=True):
    return lambda: HIST(intervals, disc, observation_resolution_s=r, capture_complete=complete,
                        gm_changes_s=gm)


# 8 kHz stream, 40 PDUs from t=-1.2 s; toggles at the given PDU indices.
def trace(toggles, n=40, t0=-1.2, period=0.05, sid="stream-a"):
    level, out = 0, []
    for i in range(n):
        if i in toggles:
            level ^= 1
        out.append({"stream_id": sid, "timestamp_s": round(t0 + i * period, 9), "pdu_index": i, "mr": level})
    return out


def cause(t, kind="CRF disruption", sid="stream-a"):
    return {"stream_id": sid, "timestamp_s": t, "kind": kind}


def reads(*pairs, sid="stream-a"):
    return [{"stream_id": sid, "timestamp_s": t, "value": v} for t, v in pairs]


def mr(pdus, causes, rd, r=0.001, capture=None):
    cap = CAP((-2, 2)) if capture is None else capture
    return lambda: MR("stream-a", pdus, causes, rd, observation_resolution_s=r, capture_complete=cap)


# Item 1: a tu interval that rises before its first recorded discontinuity fails.
case("I1a rise 10 s before lone event (single entry)", "FAIL", tu((0, 10.4), [10], []))
case("I1b rise 10 s before lone event (history)", "FAIL", hist([(0, 10.4)], [10], []))
case("I1c first event at start+R passes", "PASS", tu((0, 0.3), [0.001], []))
case("I1d first event just after start+R fails", "FAIL", tu((0, 0.3), [0.0011], []))
case("I1e event R before observed start passes", "PASS", tu((0, 0.3), [-0.001], []))
case("I1f GM change is the rise event (history)", "PASS", hist([(0, 0.3)], [], [0]))
case("I1g second interval rising early fails (history)", "FAIL", hist([(0, 0.3), (2, 2.4)], [0, 2.3], []))
case("I1h rise explained, later chained PHC in bound", "PASS", tu((0, 0.62), [0, 0.2], [0]))

# Item 2: every recorded GM change graded; never set, or cleared at that instant, fails.
case("I2a GM change with tu never set", "FAIL", hist([], [], [5]))
case("I2b GM change at the clear instant", "FAIL", hist([(0, 0.3)], [0], [0, 0.3]))
case("I2c GM change held 0.3 s", "PASS", hist([(0, 0.3)], [], [0]))
case("I2d GM change held 0.2 s", "FAIL", hist([(0, 0.2)], [], [0]))
case("I2e third GM change uncovered", "FAIL", hist([(0, 0.3), (5, 5.3)], [], [0, 5, 7]))
case("I2f GM mid-interval after PHC rise, clears 0.2 s later", "FAIL", hist([(0, 0.3)], [0], [0.1]))
case("I2g GM 2R before rise is uncovered", "FAIL", hist([(0, 0.3)], [0], [-0.002]))
case("I2h missing GM history", "NOT RUN", hist([(0, 0.3)], [0], None))
case("I2i missing interval list", "NOT RUN", hist(None, [0], [0]))
case("I2j lists as intervals", "PASS", hist([[0, 0.3]], [], [0]))
case("I2k clear within R of minimum", "PASS", hist([(0, 0.249)], [], [0]))
case("I2l clear beyond R of minimum", "FAIL", hist([(0, 0.2489)], [], [0]))
case("I2m single entry grades GM at clear", "FAIL", tu((0, 0.3), [0], [0, 0.3]))

# Item 3: resolution too coarse to decide the limits is NOT RUN, with the limit stated.
lim = lambda value: (lambda d: d.get("resolution_limit_s") == value and "observation_resolution_s" in d)
case("I3a tu R = 0.25", "NOT RUN", tu((0, 0.3), [0], [0], r=0.25), lim(0.25))
case("I3b tu R just below 0.25 decides", "PASS", tu((0, 0.3), [0], [0], r=0.2499), lim(0.25))
case("I3c history R = 0.25, no intervals", "NOT RUN", hist([], [], [], r=0.25), lim(0.25))
case("I3d history R = 60 (periodic read cadence)", "NOT RUN", hist([(0, 0.3)], [0], [0], r=60), lim(0.25))
case("I3e mr R = 0.5", "NOT RUN", mr(trace({30}), [cause(0.3)], reads((0, 0), (0.9, 1)), r=0.5), lim(0.5))
case("I3f mr R just below 0.5 decides", "PASS", mr(trace({30}), [cause(0.3)], reads((0, 0), (0.9, 1)), r=0.4999), lim(0.5))
case("I3g tu NaN R", "NOT RUN", tu((0, 0.3), [0], [0], r=float("nan")))
case("I3h mr NaN R", "NOT RUN", mr(trace({30}), [cause(0.3)], reads((0, 0), (0.9, 1)), r=float("nan")))

# Item 4: one cause excuses at most one mr toggle per stream.
case("I4a one cause, two toggles 9 PDUs apart", "FAIL",
     mr(trace({30, 39}, n=48, period=0.001, t0=0.27), [cause(0.3045)], reads((0, 0), (0.9, 2)), r=0.005))
case("I4b two causes, two toggles", "PASS",
     mr(trace({30, 39}, n=48, period=0.001, t0=0.27), [cause(0.3), cause(0.309)], reads((0, 0), (0.9, 2)), r=0.005,
        capture=CAP((-2, 2))))
case("I4c causes recorded out of order", "PASS",
     mr(trace({30, 39}, n=48, period=0.001, t0=0.27), [cause(0.309), cause(0.3)], reads((0, 0), (0.9, 2)), r=0.005))
case("I4d earliest-feasible choice keeps later-only cause", "PASS",
     mr(trace({30, 39}, n=48, period=0.001, t0=0.27), [cause(0.3045), cause(0.296)], reads((0, 0), (0.9, 2)), r=0.005))
case("I4e foreign-stream second cause does not count", "FAIL",
     mr(trace({30, 39}, n=48, period=0.001, t0=0.27), [cause(0.3), cause(0.309, sid="stream-b")],
        reads((0, 0), (0.9, 2)), r=0.005))
case("I4f GM record inside window is not consumed as cause", "PASS",
     mr(trace({30}), [cause(0.3, "GM-identity edge"), cause(0.3)], reads((0, 0), (0.9, 1))))

# Item 6: PHC-only and GM-only causes stay rejected (#602 ruling).
for kind in ("PHC settime/adjtime", "PHC step", "GM-identity edge", "GM time-source change",
             "presentation-time re-base"):
    case(f"I6 {kind} alone is no mr cause", "FAIL", mr(trace({30}), [cause(0.3, kind)], reads((0, 0), (0.9, 1))))

# Item 7: capture must span the counter window; decrease is a reset, not a wrap.
case("I7a window starts at first read - 1 s (no R)", "NOT RUN",
     mr(trace({30}, t0=-0.9), [cause(0.6)], reads((0, 0), (0.9, 1)), capture=CAP((-1.0, 2))))
case("I7b window starts at first read - 1 s - R", "PASS",
     mr(trace({30}, t0=-0.9), [cause(0.6)], reads((0, 0), (0.9, 1)), capture=CAP((-1.001, 2))))
case("I7c window ends before last read", "NOT RUN",
     mr(trace({30}), [cause(0.3)], reads((0, 0), (0.9, 1)), capture=CAP((-2, 0.8))))
case("I7d boolean capture, PDUs start after required start", "NOT RUN",
     mr(trace({30}, t0=-0.5), [cause(1.0)], reads((0, 0), (0.9, 1)), capture=True))
case("I7e boolean capture, PDUs span the window", "PASS",
     mr(trace({30}), [cause(0.3)], reads((0, 0), (0.75, 1)), capture=True))
case("I7f silent capture with explicit window and flat counter", "PASS",
     mr([], [], reads((0, 0), (0.9, 0)), capture=CAP((-1.5, 1))))
case("I7g silent capture with counter increase", "FAIL",
     mr([], [], reads((0, 0), (0.9, 1)), capture=CAP((-1.5, 1))))
case("I7h silent capture without window", "NOT RUN", mr([], [], reads((0, 0), (0.9, 0)), capture=True))
case("I7i incomplete capture metadata", "NOT RUN",
     mr(trace({30}), [cause(0.3)], reads((0, 0), (0.9, 1)), capture=CAP((-2, 2), complete=False)))
case("I7j inverted window", "NOT RUN",
     mr(trace({30}), [cause(0.3)], reads((0, 0), (0.9, 1)), capture=CAP((2, -2))))
reset_detail = lambda d: "reset" in d.get("why", "") and "delta" not in d
case("I7k decrease 5 -> 2 is reported as a reset", "FAIL",
     mr(trace({30}), [cause(0.3)], reads((0, 5), (0.9, 2))), reset_detail)
case("I7l decrease 2^32-1 -> 0 is reported as a reset", "FAIL",
     mr(trace({30}), [cause(0.3)], reads((0, 2**32 - 1), (0.9, 0))), reset_detail)
case("I7m increase with caused toggle", "PASS", mr(trace({30}), [cause(0.3)], reads((0, 0), (0.9, 1))))
case("I7n PDU outside explicit window", "NOT RUN",
     mr(trace({30}), [cause(0.3)], reads((0, 0), (0.9, 1)), capture=CAP((-1.1, 2))))

# Carried #586/round-1 arms (spot checks).
case("C1 hold of 7 PDUs fails", "FAIL",
     mr(trace({30, 37}, n=48, period=0.001, t0=0.27), [cause(0.3), cause(0.307)], reads((0, 0), (0.9, 2)), r=0.0005))
case("C2 unfinished tail is NOT RUN", "NOT RUN", mr(trace({36}), [cause(0.6)], reads((0, 0), (0.62, 1))))
case("C3 increment without toggle fails", "FAIL", mr(trace(set()), [], reads((0, 0), (0.9, 1))))
case("C4 tu chained events clear at 0.62 passes", "PASS", tu((0, 0.62), [0.2], [0]))
case("C5 tu chained events clear at 0.8 fails", "FAIL", tu((0, 0.8), [0.2], [0]))

bad = 0
for name, expected, verdict, ok, detail in cases:
    bad += not ok
    extra = {k: detail.get(k) for k in ("why", "resolution_limit_s") if k in detail}
    print(f"{'MET  ' if ok else 'UNMET'} {name}: expected {expected}, got {verdict} {extra}")
print(f"probe: {len(cases) - bad}/{len(cases)} met")
sys.exit(1 if bad else 0)
