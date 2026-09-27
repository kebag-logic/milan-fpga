#!/usr/bin/env python3
"""R362-1 independent oracle probe for issue #593 (check_release_mr / check_release_tu).

Usage: oracle_probe.py /path/to/checkout
Imports tb/tools/torture_campaign.py from the given checkout and grades each
case against the expectation derived from the #593 scope (issue items 1-2,
assignment decisions 5858876858 and the scope note 5858887057).
Each line: ID, result (MET or NOT-MET), expected, actual, note.
Exit 0 always; the report reads the NOT-MET lines.
"""
import importlib.util
import itertools
import random
import sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
spec = importlib.util.spec_from_file_location("tc", root / "tb/tools/torture_campaign.py")
tc = importlib.util.module_from_spec(spec)
sys.modules["tc"] = tc
spec.loader.exec_module(tc)

rows = []


def expect(case_id, expected, actual, note):
    verdict = actual[0] if isinstance(actual, tuple) else actual
    ok = verdict in expected if isinstance(expected, (set, frozenset)) else verdict == expected
    rows.append((case_id, "MET" if ok else "NOT-MET", expected, verdict, note))


def trace(stream="s", n=40, toggles=(), dt=0.001, start_mr=0):
    """Contiguous PDUs; mr flips at every PDU index listed in toggles."""
    out, level = [], start_mr
    for i in range(n):
        if i in toggles:
            level ^= 1
        out.append({"stream_id": stream, "timestamp_s": round(i * dt, 9), "pdu_index": i, "mr": level})
    return out


def cause(t, kind="media-clock-source change", stream="s"):
    return {"stream_id": stream, "timestamp_s": t, "kind": kind}


def reads(*pairs, stream="s"):
    return [{"stream_id": stream, "timestamp_s": t, "value": v} for t, v in pairs]


def mr(pdus, causes, rd, r=0.0005, complete=True, stream="s"):
    return tc.check_release_mr(stream, pdus, causes, rd, observation_resolution_s=r,
                               capture_complete=complete)


def tu(interval, events, gm, r=0.001, complete=True, bound=0.5):
    return tc.check_release_tu(interval, events, holdover_bound_s=bound, observation_resolution_s=r,
                               capture_complete=complete, gm_changes_s=gm)


RD1 = reads((0, 0), (1.5, 1))
# ---- issue item 2 arms --------------------------------------------------------------
expect("A1 toggle + clock-source change", "PASS", mr(trace(toggles=[5]), [cause(0.005)], RD1), "item 2 arm 1")
expect("A2 toggle + CRF disruption", "PASS", mr(trace(toggles=[5]), [cause(0.005, "CRF disruption")], RD1), "item 2 arm 2")
expect("A2b toggle + received CRF mr toggle", "PASS", mr(trace(toggles=[5]), [cause(0.005, "CRF mr toggle")], RD1), "item 1 cause 3")
expect("A3 toggle without cause", "FAIL", mr(trace(toggles=[5]), [], RD1), "item 2 arm 3")
expect("A4 toggle on GM change alone", "FAIL", mr(trace(toggles=[5]), [cause(0.005, "GM-identity edge")], RD1), "item 2 arm 4")
expect("A4b toggle on PHC step alone", "FAIL", mr(trace(toggles=[5]), [cause(0.005, "PHC settime/adjtime")], RD1), "corrected rule")
expect("A5 toggle held 7 PDUs", "FAIL", mr(trace(toggles=[5, 12]), [cause(0.005), cause(0.012)], reads((0, 0), (1.5, 1))), "item 2 arm 5")
expect("A5b toggle held 8 PDUs", "PASS", mr(trace(toggles=[5, 13]), [cause(0.005), cause(0.013)], reads((0, 0), (1.5, 1))), "boundary")
expect("A6 MEDIA_RESET increment without cause", "FAIL", mr(trace(), [], RD1), "item 2 arm 6")
expect("A7 tu 0.24 s after GM change", "FAIL", tu((0, 0.24), [], [0]), "item 2 arm 7")
expect("A7b tu 0.25 s after GM change", "PASS", tu((0, 0.25), [], [0], r=0), "boundary")

# ---- derived window, not a literal ----------------------------------------------------
for r in (0.0001, 0.001, 0.01, 0.1):
    inside = mr(trace(toggles=[5]), [cause(round(0.005 + r, 9))], RD1, r=r)
    outside = mr(trace(toggles=[5]), [cause(round(0.005 + r * 1.5, 9))], RD1, r=r)
    expect(f"W1 cause at +R (R={r})", "PASS", inside, "window scales with R")
    expect(f"W2 cause at +1.5R (R={r})", "FAIL", outside, "window scales with R")
    expect(f"W3 cause at -R (R={r})", "PASS", mr(trace(toggles=[5]), [cause(round(0.005 - r, 9))], RD1, r=r), "symmetric")

# ---- 8-PDU hold counts the carrying stream only ---------------------------------------
a = trace("a", toggles=[5, 10])
b = trace("b", n=40)
mixed = []
for pa, pb in itertools.zip_longest(a, b):
    for p in (pa, pb):
        if p:
            mixed.append(p)
for extra in range(3):  # extra foreign PDUs between the two toggles
    mixed.append(dict(b[0], pdu_index=100 + extra, timestamp_s=0.007))
mixed.sort(key=lambda p: (p["timestamp_s"], p["stream_id"]))
expect("H1 5-PDU hold with foreign PDUs interleaved", "FAIL",
       mr(mixed, [cause(0.005, stream="a"), cause(0.010, stream="a")], reads((0, 0), (1.5, 1), stream="a"),
          stream="a"), "only stream a PDUs count")
expect("H2 toggle on foreign stream only", "PASS",
       mr(trace("a") + trace("b", toggles=[5]), [], reads((0, 0), (1.5, 0), stream="a"), stream="a"),
       "b's toggle is not a's")
expect("H3 foreign-stream cause", "FAIL",
       mr(trace("a", toggles=[5]), [cause(0.005, stream="b")], reads((0, 0), (1.5, 1), stream="a"), stream="a"),
       "cause scoped to stream")

# ---- MEDIA_RESET ----------------------------------------------------------------------
expect("M1 two toggles one interval, one increment", "PASS",
       mr(trace(toggles=[5, 20]), [cause(0.005), cause(0.020)], reads((0, 0), (1.5, 1))), "Tables 5.4/5.6")
expect("M2 one toggle two increments", "FAIL", mr(trace(toggles=[5]), [cause(0.005)], reads((0, 0), (1.5, 2))), "distinct")
expect("M3 increment with delayed update 0.9 s", "PASS",
       mr(trace(toggles=[5]), [cause(0.005)], reads((0.5, 0), (0.9, 1))), "update lag <= 1 s")
expect("M4 increment whose only toggle is 1.2 s before the prior read", "FAIL",
       mr(trace(toggles=[5]), [cause(0.005)], reads((1.3, 0), (1.5, 1))), "outside [before-1-R, after+R]")
expect("M5 single MEDIA_RESET read", "NOT RUN", mr(trace(), [], reads((0, 0))), "baseline and endpoint required")
expect("M6 foreign-stream counter reads only", "NOT RUN",
       mr(trace(), [], reads((0, 0), (1, 5), stream="other")), "reads scoped to stream")
expect("M7 unordered reads", "NOT RUN", mr(trace(), [], reads((1, 0), (0.5, 0))), "ordered reads")
expect("M8 wrap 2^32-1 -> 0 with one toggle", "PASS",
       mr(trace(toggles=[5]), [cause(0.005)], reads((0, 2**32 - 1), (1.5, 0))), "32-bit wrap")

# ---- NOT RUN on missing evidence, never PASS --------------------------------------------
base_args = dict(stream_id="s", pdus=trace(toggles=[5]), causes=[cause(0.005)], media_reset_reads=RD1,
                 observation_resolution_s=0.0005, capture_complete=True)
for key, value in (("pdus", None), ("causes", None), ("media_reset_reads", None), ("capture_complete", False),
                   ("capture_complete", 1), ("observation_resolution_s", None),
                   ("observation_resolution_s", float("inf")), ("stream_id", "")):
    expect(f"N-mr {key}={value!r}", "NOT RUN", tc.check_release_mr(**dict(base_args, **{key: value})), "item 3")
expect("N-mr tail 7 PDUs after final toggle", "NOT RUN", mr(trace(n=12, toggles=[5]), [cause(0.005)], RD1), "unfinished tail")
expect("N-mr packet gap", "NOT RUN", mr([p for p in trace(toggles=[5]) if p["pdu_index"] != 20], [cause(0.005)], RD1), "gap")
for label, args in (("interval None", ((None), [0], [0])), ("events None", ((0, 0.3), None, [0])),
                    ("gm None", ((0, 0.3), [0], None))):
    expect(f"N-tu {label}", "NOT RUN", tu(*args), "item 3")
expect("N-tu resolution None", "NOT RUN", tu((0, 0.3), [0], [0], r=None), "item 3")
expect("N-tu incomplete capture", "NOT RUN", tu((0, 0.3), [0], [0], complete=False), "item 3")

rng = random.Random(593)
never_pass = 0
for _ in range(2000):
    args = dict(base_args)
    key = rng.choice(["pdus", "causes", "media_reset_reads", "observation_resolution_s", "capture_complete"])
    args[key] = rng.choice([None, float("nan"), "x", -1, False]) if key != "capture_complete" else rng.choice([False, None, 0, "yes"])
    try:
        verdict = tc.check_release_mr(**args)[0]
    except Exception as exc:  # a crash is not a PASS
        verdict = "EXC:" + type(exc).__name__
    never_pass += verdict == "PASS"
rows.append(("N-mr fuzz 2000 corrupted inputs", "MET" if never_pass == 0 else "NOT-MET", "no PASS", f"{never_pass} PASS", "item 3"))

# ---- tu: routed #396 suggestions ------------------------------------------------------------
expect("S-R347-5-S1 tu rises 10 s before its first discontinuity", "FAIL", tu((0, 10.4), [10], []),
       "scope note 5858887057: must fail the containment check")
expect("S-R347-5-S1b tu rises 1 s before its first discontinuity", "FAIL", tu((0, 1.2), [1.0], []),
       "scope note 5858887057")
expect("S-R347-5-S1c GM change 5 s after tu rose, clear 0.3 s later", "FAIL", tu((0, 5.3), [], [5.0]),
       "scope note 5858887057")
expect("S-R346-3-S1 60 s periodic cadence used as resolution; tu held 60 s", {"FAIL", "NOT RUN"},
       tu((0, 60), [0], [], r=60), "resolution must be wire/event, not the periodic read")
expect("S-R346-3-S1b resolution 0.3 s; tu 0.01 s after GM change", {"FAIL", "NOT RUN"},
       tu((0, 0.01), [], [0], r=0.3), "coarse resolution makes the 0.25 s minimum vacuous")
expect("S-R346-3-S1c mr cause 0.9 s away, R=1 s", {"FAIL", "NOT RUN"},
       mr(trace(n=2000, toggles=[1500], dt=0.001), [cause(0.6)], reads((0, 0), (3, 1)), r=1.0),
       "coarse resolution widens the cause window to +/-1 s")
expect("S-R346-3-S2 tu 0.2 s after GM change, R=0.001", "FAIL", tu((0, 0.2), [0], [0]), "0.25 s lower bound")

# ---- B.1.1 coverage of GM changes ------------------------------------------------------------
expect("B1 GM change after tu cleared, no new tu interval (interval graded)", {"FAIL", "NOT RUN"},
       tu((0, 0.3), [0], [0, 0.5]), "a GM change at 0.5 s with no tu after it is never graded")
expect("B2 GM edge supplied only as a discontinuity, gm history []", {"FAIL", "NOT RUN"},
       tu((0, 0.1), [0], []), "unkinded discontinuities bypass the GM minimum if history omits the edge")

# ---- other edges ------------------------------------------------------------------------------
t2 = trace(toggles=[5, 13])
expect("E1 one cause explains two toggles (net level unchanged)", {"FAIL", "NOT RUN"},
       mr(t2, [cause(0.009)], reads((0, 0), (1.5, 1)), r=0.005), "one restart per cause")
expect("E2 caused toggle with no MEDIA_RESET increment", {"FAIL", "NOT RUN"},
       mr(trace(toggles=[5]), [cause(0.005)], reads((0, 0), (1.5, 0))), "counter under-count")
expect("E3 talker restart resets MEDIA_RESET to 0 (Table 5.4)", {"NOT RUN", "FAIL"},
       mr(trace(), [], reads((0, 3), (1.5, 0))), "reported cause label checked in report")
e3 = mr(trace(), [], reads((0, 3), (1.5, 0)))
rows.append(("E3-detail", "INFO", "-", e3[0], str({k: e3[1].get(k) for k in ("why", "delta")})))
e4 = tu((0, 0.3), [0], [0])
rows.append(("E4 verdict carries R", "MET" if e4[1].get("observation_resolution_s") == 0.001 else "NOT-MET",
             "R in detail", str(e4[1].get("observation_resolution_s")), "decision: resolution part of verdict"))

for row in rows:
    print(" | ".join(str(x) for x in row))
print(f"TOTAL {len(rows)} MET {sum(r[1] == 'MET' for r in rows)} NOT-MET {sum(r[1] == 'NOT-MET' for r in rows)}")
