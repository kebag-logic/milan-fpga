#!/usr/bin/env python3
"""R363-1 behavioural probe of check_release_mr / check_release_tu.

Usage: python3 -B oracle_probe.py <repo-root>
Imports the planner read-only from <repo-root>/tb/tools and prints one line
per case: id, verdict, expected-by-rule, and OK/GAP. Exit 0 always; the log
is the evidence.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(sys.argv[1]).resolve() / "tb" / "tools"))
import torture_campaign as tp  # noqa: E402

rows = []


def case(case_id, got, expected, note):
    verdict = got[0]
    rows.append((case_id, verdict, expected, "OK" if verdict == expected else "GAP", note, got[1]))


def trace(toggle_indices, n=40, period=0.000125, stream="s"):
    level, out = 0, []
    for i in range(n):
        if i in toggle_indices:
            level ^= 1
        out.append({"stream_id": stream, "timestamp_s": round(i * period, 9), "pdu_index": i, "mr": level})
    return out


def reads(t0, t1, v0, v1, stream="s"):
    return [{"stream_id": stream, "timestamp_s": t0, "value": v0},
            {"stream_id": stream, "timestamp_s": t1, "value": v1}]


def mr(pdus, causes, rd, r):
    return tp.check_release_mr("s", pdus, causes, rd, observation_resolution_s=r, capture_complete=tp.ReleaseCapture((-2, 4)))


cause = lambda t, k="media-clock-source change": {"stream_id": "s", "timestamp_s": t, "kind": k}

# --- A. tu: interval that rises long before its first recorded discontinuity (R347-5 S1)
case("A1 tu rises 10 s before its only discontinuity",
     tp.check_release_tu((0, 10.4), [10], holdover_bound_s=0.5, observation_resolution_s=0.001,
                         capture_complete=True, gm_changes_s=[]), "FAIL",
     "scope note 5858887057: rising before first recorded discontinuity must fail containment")
case("A2 tu rises 1 s before its only GM change",
     tp.check_release_tu((0, 1.3), [], holdover_bound_s=0.5, observation_resolution_s=0.001,
                         capture_complete=True, gm_changes_s=[1.0]), "FAIL",
     "same, with the discontinuity being a GM change")
case("A3 control: event within resolution of start",
     tp.check_release_tu((0, 0.3), [0.0005], holdover_bound_s=0.5, observation_resolution_s=0.001,
                         capture_complete=True, gm_changes_s=[]), "PASS", "control")

# --- B. tu: GM change with no tu set afterwards (held 0 s)
case("B1 GM change 0.05 s after the only interval clears (tu never re-set)",
     tp.check_release_tu((0, 0.3), [0], holdover_bound_s=0.5, observation_resolution_s=0.001,
                         capture_complete=True, gm_changes_s=[0.35]), "FAIL",
     "B.1.1/REQ-VER-06: after every GM change tu set for 0.25 s; per-interval oracle never sees this GM change")
case("B2 GM change exactly at the clear instant",
     tp.check_release_tu((0, 0.3), [0], holdover_bound_s=0.5, observation_resolution_s=0.001,
                         capture_complete=True, gm_changes_s=[0.3]), "FAIL",
     "tu cleared at the GM change; held 0 s after it")

# --- C. coarse resolution makes the new GM minimum and the tu bound vacuous (R346-3 S1)
case("C1 R=0.25: tu clears 1 ms after GM change",
     tp.check_release_tu((0, 0.001), [], holdover_bound_s=0.5, observation_resolution_s=0.25,
                         capture_complete=True, gm_changes_s=[0]), "NOT RUN",
     "minimum undecidable at R>=0.25; PASS here means the minimum cannot fail")
case("C2 R=60 (periodic publication cadence): 60 s tu interval",
     tp.check_release_tu((0, 60.0), [], holdover_bound_s=0.5, observation_resolution_s=60,
                         capture_complete=True, gm_changes_s=[0]), "NOT RUN",
     "R346-3 S1 routed in scope: resolution must not be the 60 s periodic read")

# --- D. one cause explaining several mr toggles
case("D1 one source change, two toggles 8 PDUs apart, R=0.002",
     mr(trace({1, 9}), [cause(0.000125)], reads(0, 0.004, 0, 1), 0.002), "FAIL",
     "second toggle has no distinct recorded cause (1722-2016 4.4.4.3: toggled each time a restart is needed)")
case("D2 one source change, four toggles at 8-PDU spacing, R=0.004",
     mr(trace({1, 9, 17, 25}), [cause(0.000125)], reads(0, 0.004, 0, 1), 0.004), "FAIL", "flapping talker")
case("D3 control: two toggles, two causes",
     mr(trace({1, 9}), [cause(0.000125), cause(0.001125)], reads(0, 0.004, 0, 1), 0.0001), "PASS", "control")

# --- E. capture span shorter than counter window
case("E1 capture covers 5 ms of a 3600 s counter window",
     mr(trace(set()), [], reads(0, 3600, 0, 0), 0.001), "NOT RUN",
     "missing packet evidence for most of the window; oracle trusts capture_complete")
case("E2 empty PDU list, counter window 3600 s",
     mr([], [], reads(0, 3600, 0, 0), 0.001), "NOT RUN", "the explicit span also cannot attest a 3600 s silent capture")

# --- F. talker-start counter reset (Table 5.6: reset to 0 on stream start)
case("F1 MEDIA_RESET 3 -> 0 decoded as wrap",
     mr(trace(set()), [], reads(0, 0.004, 3, 0), 0.001), "FAIL",
     "fails (fail-safe) but reason is 'increment without caused toggle' with delta 2**32-3")

# --- G. GM-only / PHC-only mr toggles
for kind in ("GM-identity edge", "GM time-source change", "PHC settime/adjtime", "fabric discontinuity"):
    case(f"G {kind} alone", mr(trace({1}), [cause(0.000125, kind)], reads(0, 0.004, 0, 1), 0.001), "FAIL",
         "B.1.2 / corrected decision")

# --- H. hold boundaries at a different stream rate
case("H1 7-PDU hold", mr(trace({1, 8}), [cause(0.000125), cause(0.001)], reads(0, 0.004, 0, 1), 0.00001),
     "FAIL", "4.4.4.3 minimum eight")
case("H2 8-PDU hold", mr(trace({1, 9}), [cause(0.000125), cause(0.001125)], reads(0, 0.004, 0, 1), 0.00001),
     "PASS", "4.4.4.3 minimum eight")
case("H3 tail of 7 PDUs after last toggle", mr(trace({33}), [cause(0.004125)], reads(0, 0.005, 0, 1), 0.00001),
     "NOT RUN", "unfinished tail")
case("H4 toggle on first captured PDU unobservable (prior level unknown)",
     mr(trace({0}), [], reads(0, 0.004, 0, 0), 0.001), "PASS",
     "documented: first captured PDU establishes the prior level")

for row in rows:
    print(f"{row[3]:4} | {row[0]} | got={row[1]} want={row[2]} | {row[4]}")
    print(f"     detail={row[5]}")
print("GAPS:", sum(row[3] == "GAP" for row in rows), "of", len(rows))
