#!/usr/bin/env python3
"""Grade the gmstep leg's PHC-only step with the merged release-soak oracles.

Usage: soak_phc_probe.py CLONE GMSTEP_LOG

Reads the clone's own tb/tools/torture_campaign.py (the #593 oracles as
merged) and the clean gmstep leg's log from this head. The leg's compressed
time is mapped to modelled seconds by its own convention: one quarter tick
(printed by the leg) stands for 0.25 s. From the log it takes the grandmaster
identity edge, the plane's step, the tu rise and fall, the talker interval,
and the graded facts that outgoing mr and MEDIA_RESET did not change.

Cases (each must produce the stated verdict, or the probe exits 1):
  A  post-602 wire: constant mr, flat MEDIA_RESET, no cause   -> mr PASS
  B  A plus a recorded PHC-step record offered as an mr cause -> mr PASS
     (a non-cause kind is ignored, not required)
  C  pre-602 wire: one toggle 116 cycles after the step, +1 MEDIA_RESET,
     only the PHC step and GM edge recorded                   -> mr FAIL
  D  C with the toggle excused by a genuine CRF mr toggle     -> mr PASS
  E  tu history with the PHC step recorded as a discontinuity -> tu PASS
  F  tu history without the PHC step (GM edge only)           -> tu FAIL
     (the step is what extends tu past 0.5 s of the GM edge)
  G  tu interval with no recorded discontinuity at all        -> tu FAIL
Limits: a model of recorded evidence built from the leg's graded outcome,
not a capture from hardware; compressed time; one stream.
"""
import json
import re
import sys
from pathlib import Path


def main() -> int:
    clone = Path(sys.argv[1]).resolve()
    log = Path(sys.argv[2]).read_text(errors="replace")
    sys.path.insert(0, str(clone / "tb/tools"))
    import torture_campaign as tc  # noqa: E402

    quarter = int(re.search(r"quarter tick (\d+) cycles", log).group(1))
    ev = re.search(r"EVENT: identity (\d+), counters read (\d+), step pulse (\d+), "
                   r"step (\d+) \((\d+) ns\), tu rise (\d+) fall (\d+)", log)
    identity, _, pulse, _, _, tu_rise, tu_fall = (int(x) for x in ev.groups())
    interval = float(re.search(r"TALKER: baseline interval ([\d.]+) cycles", log).group(1))
    assert "[ ok ] restart: a PHC-only step leaves outgoing mr unchanged got=0 exp=0" in log
    assert "[ ok ] restart: a PHC-only step adds no MEDIA_RESET got=0 exp=0" in log
    assert re.search(r"== gmstep: checks: \d+\s+failures: 0 ==", log)
    cyc_s = 0.25 / quarter            # modelled seconds per fabric cycle

    def t(cycles: float) -> float:
        return round(cycles * cyc_s, 9)

    R = 0.001                          # stated relative resolution for the model
    sid = "talker-0"
    gm_s, step_s = t(identity), t(pulse)
    # PDUs every talker interval from 1.2 s before the step to 1.2 s after it.
    first = pulse - int(1.2 / cyc_s)
    n = int(2.4 / cyc_s / interval)
    times = [t(first + k * interval) for k in range(n)]
    reads_s = [times[0] + 1.0 + 2 * R + 0.01, times[-1] - 0.001]
    window = tc.ReleaseCapture((times[0], times[-1]), complete=True)

    def pdus(toggle_at_s=None):
        out, level = [], 0
        for k, ts in enumerate(times):
            if toggle_at_s is not None and ts >= toggle_at_s:
                level = 1
            out.append({"stream_id": sid, "timestamp_s": ts, "pdu_index": k, "mr": level})
        return out

    def reads(delta):
        return [{"stream_id": sid, "timestamp_s": reads_s[0], "value": 7},
                {"stream_id": sid, "timestamp_s": reads_s[1], "value": 7 + delta}]

    phc = {"stream_id": sid, "timestamp_s": step_s, "kind": "PHC settime/adjtime"}
    gm = {"stream_id": sid, "timestamp_s": gm_s, "kind": "GM-identity edge"}
    toggle_s = t(pulse + 116)
    first_toggled = next(ts for ts in times if ts >= toggle_s)
    crf = {"stream_id": sid, "timestamp_s": first_toggled, "kind": "CRF mr toggle"}

    def mr(p, causes, delta):
        return tc.check_release_mr(sid, p, causes, reads(delta),
                                   observation_resolution_s=R, capture_complete=window)

    def tu(disc, gms, intervals=None):
        return tc.check_release_tu_history(
            intervals if intervals is not None else [(t(tu_rise), t(tu_fall))], disc,
            observation_resolution_s=R, capture_complete=True, gm_changes_s=gms)

    cases = [
        ("A post-602 wire, no cause", mr(pdus(), [], 0), "PASS"),
        ("B post-602 wire, PHC record offered as cause", mr(pdus(), [phc, gm], 0), "PASS"),
        ("C pre-602 wire, PHC step and GM edge only", mr(pdus(toggle_s), [phc, gm], 1), "FAIL"),
        ("D pre-602 wire excused by a genuine CRF toggle", mr(pdus(toggle_s), [crf], 1), "PASS"),
        ("E tu with PHC step recorded", tu([step_s], [gm_s]), "PASS"),
        ("F tu with GM edge only", tu([], [gm_s]), "FAIL"),
        ("G tu with no recorded discontinuity", tu([], []), "FAIL"),
    ]
    bad = 0
    print(json.dumps({"quarter_tick_cycles": quarter, "seconds_per_cycle": cyc_s,
                      "gm_edge_s": gm_s, "step_s": step_s, "tu_rise_s": t(tu_rise),
                      "tu_fall_s": t(tu_fall), "tu_after_step_s": t(tu_fall - pulse),
                      "tu_after_gm_s": t(tu_fall - identity), "talker_interval_cycles": interval,
                      "pdus": n, "resolution_s": R}, indent=1))
    for name, (verdict, detail), want in cases:
        ok = verdict == want
        bad += not ok
        why = detail.get("why") or detail.get("evidence", {}).get("why", "")
        print(f"[{'ok' if ok else 'FAIL'}] {name}: {verdict} (want {want}) {why}")
    print(f"{len(cases)} cases, {bad} unexpected")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
