#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""L3 #396/#593 release controls: the unchanged self-test must reject each defect.

Run from any directory with the same interpreter as the planner self-test.
Only a temporary planner copy changes. A timeout or parser error is no kill;
each defect must fail the named behavioral test after a clean baseline passes.
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path


# These source anchors inject defects; expected behavior stays in the tests.
MUTANTS = (
    ("restore eligibility check removed",
     "            and settings.restore_bound_s <= RELEASE_RESTORE_BOUND_S\n", "",
     "test_release_eligibility_boundaries"),
    ("restore ceiling relaxed",
     "RELEASE_RESTORE_BOUND_S = 30\n", "RELEASE_RESTORE_BOUND_S = 31\n",
     "test_release_eligibility_boundaries"),
    ("power-off hold hardcoded",
     "power_off_hold_s=settings.power_off_hold_s,", "power_off_hold_s=8,",
     "test_release_timing_and_snapshot_contract"),
    ("power-off CLI value discarded",
     "power_off_hold_s=a.power_off_hold_s,", "power_off_hold_s=ReleaseSettings.power_off_hold_s,",
     "test_release_cli_parameters"),
    ("ADP window charged for pre-cut time",
     'adp_deadline="2 * pre_cut_valid_time",',
     'adp_deadline="pre_cut_last_available_host_s + 2 * pre_cut_valid_time - t0_host_s",',
     "test_release_timing_and_snapshot_contract"),
    ("missing ADP evidence skipped",
     'adp_missing_or_expired="fail; require captured valid_time=10 and arrival before T0 deadline",',
     'adp_missing_or_expired="skip",', "test_release_timing_and_snapshot_contract"),
    ("tu bound uses media-clock holdover",
     "tu_holdover_bound_s=0.5,", "tu_holdover_bound_s=5,", "test_release_tu_contract"),
    ("uncorrelated tu ignored",
     'tu_uncorrelated="fail",', 'tu_uncorrelated="ignore",', "test_release_tu_contract"),
    ("boot evidence ends before the next cut",
     'boot_evidence="complete UART/reset observation from T0 through next cut or campaign end; "',
     'boot_evidence="complete UART/reset observation from T0 through boot_observation_s; "',
     "test_release_boot_negative_control"),
    ("tu anchor uses the first discontinuity",
     "last_discontinuity_s = max(events_s)", "last_discontinuity_s = min(events_s)",
     "test_release_tu_chained_discontinuities"),
    ("tu clearing deadline ignores observation resolution",
     "last_discontinuity_s + holdover_bound_s + observation_resolution_s",
     "last_discontinuity_s + holdover_bound_s",
     "test_release_tu_chained_discontinuities"),
    ("tu oracle accepts an uncorrelated interval",
     'return "FAIL", {"why": "uncorrelated tu fails", **detail}',
     'return "PASS", {"why": "uncorrelated tu fails", **detail}',
     "test_release_tu_chained_discontinuities"),
    ("tu plan uses the first discontinuity",
     'tu_time_origin="last recorded discontinuity before tu clears",',
     'tu_time_origin="first recorded discontinuity",', "test_release_tu_contract"),
    ("tu plan drops capture resolution",
     'tu_observation_resolution="record wire-capture and correlated event-timestamp resolution in seconds",',
     'tu_observation_resolution="optional",', "test_release_tu_contract"),
    ("tu assertion allows five seconds",
     '"it clears within 0.5 s plus "', '"it clears within 5 s plus "', "test_release_assertion_text"),
    ("tu assertion drops uncorrelated failure",
     '"the stated observation resolution; uncorrelated tu fails; "',
     '"the stated observation resolution; "', "test_release_assertion_text"),
    ("ADP assertion uses the pre-cut anchor",
     "valid_time measured from T0, the host-timestamped power-strip ",
     "valid_time measured from the last pre-cut advertisement, the host-timestamped power-strip ",
     "test_release_assertion_text"),
    ("ADP assertion charges the off time",
     "pre-cut advertisement age are provenance, not charged to",
     "pre-cut advertisement age are charged to", "test_release_assertion_text"),
    ("CLI power hold default changes",
     "default=ReleaseSettings.power_off_hold_s", "default=5", "test_release_cli_power_hold_default"),
    ("tu containment drops the start allowance",
     "start_s = observed_start_s - observation_resolution_s", "start_s = observed_start_s",
     "test_release_tu_start_resolution"),
    ("tu containment doubles the start allowance",
     "start_s = observed_start_s - observation_resolution_s",
     "start_s = observed_start_s - 2 * observation_resolution_s",
     "test_release_tu_start_resolution"),
    ("tu containment excludes its inclusive start",
     "in discontinuities_s + gm_changes_s if start_s <= event_s < clear_s]",
     "in discontinuities_s + gm_changes_s if start_s < event_s < clear_s]",
     "test_release_tu_start_resolution"),
    ("tu containment includes the clear instant",
     "in discontinuities_s + gm_changes_s if start_s <= event_s < clear_s]",
     "in discontinuities_s + gm_changes_s if start_s <= event_s <= clear_s]",
     "test_release_tu_start_resolution"),
    ("tu assertion drops the event window",
     '"containment uses [observed_start - observation_resolution_s, clear); "', '""',
     "test_release_assertion_text"),
    ("tu plan drops the start allowance",
     'tu_event_window="[observed_start - observation_resolution_s, clear)",',
     'tu_event_window="[observed_start, clear)",', "test_release_tu_contract"),
    ("mr clock-source cause removed",
     'allowed = {"media-clock-source change", "CRF disruption", "CRF mr toggle"}',
     'allowed = {"CRF disruption", "CRF mr toggle"}', "test_release_mr_allowed_causes"),
    ("mr CRF disruption cause removed",
     'allowed = {"media-clock-source change", "CRF disruption", "CRF mr toggle"}',
     'allowed = {"media-clock-source change", "CRF mr toggle"}', "test_release_mr_allowed_causes"),
    ("mr received CRF toggle cause removed",
     'allowed = {"media-clock-source change", "CRF disruption", "CRF mr toggle"}',
     'allowed = {"media-clock-source change", "CRF disruption"}', "test_release_mr_allowed_causes"),
    ("mr uncorrelated toggle accepted",
     'return "FAIL", {"why": "mr toggle without a recorded media-clock cause", "toggle": toggle}',
     'return "PASS", {"toggles_s": [toggle["timestamp_s"] for toggle in toggles]}',
     "test_release_mr_no_cause"),
    ("mr GM-only toggle accepted",
     'allowed = {"media-clock-source change", "CRF disruption", "CRF mr toggle"}',
     'allowed = {"media-clock-source change", "CRF disruption", "CRF mr toggle", "GM-identity edge"}',
     "test_release_mr_gm_only"),
    ("mr cause time window removed",
     'abs(Decimal(str(event["timestamp_s"])) - Decimal(str(toggle["timestamp_s"])))',
     'Decimal(0)', "test_release_mr_resolution"),
    ("mr foreign-stream cause accepted",
     'stream_causes = [event for event in causes if event["stream_id"] == stream_id]',
     'stream_causes = causes', "test_release_mr_stream_scope"),
    ("mr eight-PDU minimum removed",
     'if current["pdu_index"] - previous["pdu_index"] < 8:',
     'if False:', "test_release_mr_eight_pdus"),
    ("mr terminal hold evidence ignored",
     "return \"NOT RUN\", {\"why\": \"capture ends before the final toggle's eighth PDU\"}",
     'return "PASS", {"toggles_s": [toggle["timestamp_s"] for toggle in toggles]}',
     "test_release_mr_eight_pdus"),
    ("MEDIA_RESET cause check removed",
     'if delta > len(matches_s):', 'if False:', "test_release_media_reset_no_cause"),
    ("MEDIA_RESET reuses a toggle for two increments",
     'unused_s.remove(event_s)', 'pass', "test_release_media_reset_intervals"),
    ("MEDIA_RESET interval update allowance removed",
     'Decimal(str(before["timestamp_s"])) - Decimal(str(MILAN_MAX_OBSERVATION_INTERVAL_S))',
     'Decimal(str(before["timestamp_s"]))',
     "test_release_media_reset_intervals"),
    ("tu GM minimum removed",
     'if minimum_clear_s is not None and clear_s + observation_resolution_s < minimum_clear_s:',
     'if False:', "test_release_tu_gm_minimum"),
    ("tu GM minimum anchored at the first GM change",
     'max(gm_events_s) + Decimal("0.25")', 'min(gm_events_s) + Decimal("0.25")',
     "test_release_tu_gm_minimum"),
    ("tu GM minimum drops recorded resolution",
     'clear_s + observation_resolution_s < minimum_clear_s', 'clear_s < minimum_clear_s',
     "test_release_tu_gm_minimum"),
    ("tu missing GM history accepted",
     'return "NOT RUN", dict(detail, why="complete interval, discontinuity and GM history required")',
     'return "PASS", dict(detail, why="complete interval, discontinuity and GM history required")',
     "test_release_tu_missing_gm_history"),
    ("mr missing evidence accepted",
     'return "NOT RUN", dict(detail, why="complete packet, cause, counter and resolution evidence required")',
     'return "PASS", dict(detail, why="complete packet, cause, counter and resolution evidence required")',
     "test_release_mr_missing_evidence"),
    ("mr plan hold weakened", 'mr_hold_pdus=8,', 'mr_hold_pdus=7,', "test_release_mr_plan_contract"),
    ("tu plan GM minimum removed", 'tu_gm_minimum_s=0.25,', 'tu_gm_minimum_s=0,',
     "test_release_mr_plan_contract"),
    (
        'tu rise correlation removed',
        'if min(events_s) > observed_start_s + observation_resolution_s:',
        'if False:',
        'test_release_tu_before_first_discontinuity',
    ),
    (
        'tu rise correlation made exclusive',
        'if min(events_s) > observed_start_s + observation_resolution_s:',
        'if min(events_s) >= observed_start_s + observation_resolution_s:',
        'test_release_tu_rise_boundary',
    ),
    (
        'tu resolution ceiling removed',
        'if observation_resolution_s >= resolution_limit_s:\n        return "NOT RUN", dict(det'
        'ail, why="resolution cannot decide the tu timing limits")',
        'if False:\n        return "NOT RUN", dict(detail, why="resolution cannot decide the tu timing limits")',
        'test_release_deciding_resolution',
    ),
    (
        'mr resolution ceiling removed',
        'if observation_resolution_s >= resolution_limit_s:\n        return "NOT RUN", dict(det'
        'ail, why="resolution cannot decide the mr cause window")',
        'if False:\n        return "NOT RUN", dict(detail, why="resolution cannot decide the mr cause window")',
        'test_release_deciding_resolution',
    ),
    (
        'GM history coverage removed',
        '    for event in gm_changes_s:\n        gm_s = Decimal(str(event))',
        '    for event in []:\n        gm_s = Decimal(str(event))',
        'test_release_tu_history',
    ),
    (
        'GM history check skips interval verdict',
        '        if verdict != "PASS":\n            return verdict, dict(detail, interval=inter'
        'val, evidence=evidence)',
        '        if False:\n            return verdict, dict(detail, interval=interval, evidence=evidence)',
        'test_release_tu_history',
    ),
    (
        'history coarse resolution accepted',
        'or not 0 <= observation_resolution_s < 0.25):',
        'or observation_resolution_s < 0):',
        'test_release_tu_history',
    ),
    (
        'history interval order ignored',
        'if clear_s <= start_s or (intervals and start_s <= intervals[-1][1]):',
        'if False:',
        'test_release_tu_history',
    ),
    (
        'single interval drops future GM changes',
        'gm_events_s = gm_changes_s',
        'gm_events_s = [event for event in gm_changes_s if event < clear_s]',
        'test_release_tu_history',
    ),
    (
        'mr reuses one cause',
        '        causes.remove(matches[0])',
        '        pass',
        'test_release_mr_distinct_causes',
    ),
    (
        'mr cause order ignored',
        'causes = sorted(causes, key=lambda event: event["timestamp_s"])',
        'causes = list(causes)',
        'test_release_mr_distinct_causes',
    ),
    (
        'mr cause window doubled',
        '                   <= Decimal(str(resolution_s))\n',
        '                   <= 2 * Decimal(str(resolution_s))\n',
        'test_release_mr_resolution',
    ),
    (
        'mr cause window strict',
        '                   <= Decimal(str(resolution_s))\n',
        '                   < Decimal(str(resolution_s))\n',
        'test_release_mr_resolution',
    ),
    (
        'mr cause first toggle skipped',
        '    for toggle in toggles:\n        matches =',
        '    for toggle in toggles[1:]:\n        matches =',
        'test_release_mr_no_cause',
    ),
    (
        'mr cause last toggle skipped',
        '    for toggle in toggles:\n        matches =',
        '    for toggle in toggles[:-1]:\n        matches =',
        'test_release_mr_no_cause',
    ),
    (
        'mr PDU time order ignored',
        'or current["timestamp_s"] < previous["timestamp_s"]):',
        'or False):',
        'test_release_mr_record_boundaries',
    ),
    (
        'counter stream filter removed',
        'reads = [read for read in media_reset_reads if read["stream_id"] == stream_id]',
        'reads = media_reset_reads',
        'test_release_mr_record_boundaries',
    ),
    (
        'counter endpoint optional',
        'if len(reads) < 2:',
        'if len(reads) < 1:',
        'test_release_mr_record_boundaries',
    ),
    (
        'counter read order ignored',
        'if after["timestamp_s"] <= before["timestamp_s"]:',
        'if False:',
        'test_release_mr_record_boundaries',
    ),
    (
        'counter reset ignored',
        'if after["value"] < before["value"]:',
        'if False:',
        'test_release_media_reset_decrease',
    ),
    (
        'counter upper window drops resolution',
        'upper_s = Decimal(str(after["timestamp_s"])) + Decimal(str(resolution_s))',
        'upper_s = Decimal(str(after["timestamp_s"]))',
        'test_release_media_reset_window_edges',
    ),
    (
        'counter upper window widened',
        'upper_s = Decimal(str(after["timestamp_s"])) + Decimal(str(resolution_s))',
        'upper_s = Decimal(str(after["timestamp_s"])) + 1 + Decimal(str(resolution_s))',
        'test_release_media_reset_window_edges',
    ),
    (
        'counter consumes latest toggle',
        'for event_s in matches_s[:delta]:',
        'for event_s in (matches_s[-delta:] if delta else []):',
        'test_release_media_reset_window_edges',
    ),
    (
        'counter range ignored',
        'if type(read.get("value")) is not int or not 0 <= read["value"] < 2**32:',
        'if type(read.get("value")) is not int:',
        'test_release_mr_record_boundaries',
    ),
    (
        'cause kind type ignored',
        'if not isinstance(event.get("kind"), str):',
        'if False:',
        'test_release_mr_record_boundaries',
    ),
    (
        'tu bound guard removed',
        'holdover_bound_s != 0.5 or',
        'False or',
        'test_release_deciding_resolution',
    ),
    (
        'tu zero interval accepted',
        'if clear_s <= observed_start_s or',
        'if clear_s < observed_start_s or',
        'test_release_deciding_resolution',
    ),
    (
        'capture start check removed',
        'or capture_start_s > required_start_s',
        'or False',
        'test_release_mr_capture_span',
    ),
    (
        'capture endpoint check removed',
        'or capture_end_s < Decimal(str(reads[-1]["timestamp_s"]))',
        'or False',
        'test_release_mr_capture_span',
    ),
    (
        'capture guard removed',
        'if (capture_start_s >= capture_end_s or capture_start_s > required_start_s',
        'if (False and capture_start_s >= capture_end_s or False',
        'test_release_mr_capture_span',
    ),
    (
        'tu minimum sentence',
        '"after each GM change, clear + observation_resolution_s must be at least "',
        '""',
        'test_release_assertion_text',
    ),
    (
        'tu minimum and missing history',
        '"GM change + 0.25 s (Annex B.1.1 minimum); missing GM history is NOT RUN; clock validity "',
        '""',
        'test_release_assertion_text',
    ),
    (
        'mr cause kinds',
        '"media-clock-source change, CRF disruption, or received CRF mr toggle "',
        '""',
        'test_release_mr_plan_contract',
    ),
    (
        'mr toggle and counter scope',
        '"every mr toggle and MEDIA_RESET increment needs a recorded "',
        '""',
        'test_release_mr_plan_contract',
    ),
    (
        'mr counter intervals',
        '"MEDIA_RESET counts observation intervals, not packets; "',
        '""',
        'test_release_mr_plan_contract',
    ),
    (
        'missing evidence verdict',
        '"need measured PASS records on the exact image; missing, NOT RUN, SKIP, INFO, "',
        '""',
        'test_release_assertion_text',
    ),
    (
        'mr distinct causes',
        '"each cause excuses at most one toggle per stream; "',
        '""',
        'test_release_mr_plan_contract',
    ),
    (
        'mr deciding resolution',
        '"2 * observation_resolution_s must be less than the 1 s counter interval ceiling; "',
        '""',
        'test_release_mr_plan_contract',
    ),
    (
        'mr capture span',
        '"capture must span [first read - 1 s - observation_resolution_s, last read]; "',
        '""',
        'test_release_mr_plan_contract',
    ),
    (
        'mr reset classification',
        '               "a MEDIA_RESET decrease is a counter reset, not a wrap"),',
        '               ""),',
        'test_release_mr_plan_contract',
    ),
    (
        'tu rise text',
        '"first discontinuity must be within observation_resolution_s of the rise; "',
        '""',
        'test_release_assertion_text',
    ),
    (
        'tu history text',
        '"grade every GM change against the complete tu interval history; "',
        '""',
        'test_release_assertion_text',
    ),
    (
        'tu uncovered GM text',
        '"a GM change with no covering interval fails; "',
        '""',
        'test_release_assertion_text',
    ),
    (
        'tu deciding resolution text',
        '"observation_resolution_s must be less than min(0.25 s, 0.5 s); "',
        '""',
        'test_release_assertion_text',
    ),
    (
        'tu coarse resolution text',
        '               "coarser resolution is NOT RUN"),',
        '               ""),',
        'test_release_assertion_text',
    ),
    (
        'plan mr_distinct_causes weakened',
        'mr_distinct_causes=True,',
        'mr_distinct_causes=False,',
        'test_release_round2_plan_contract',
    ),
    (
        'plan tu_oracle weakened',
        'tu_oracle="check_release_tu_history",',
        'tu_oracle="check_release_tu",',
        'test_release_round2_plan_contract',
    ),
    (
        'plan tu_resolution_limit_s weakened',
        'tu_resolution_limit_s=min(0.25, 0.5),',
        'tu_resolution_limit_s=1,',
        'test_release_round2_plan_contract',
    ),
    (
        'plan mr_resolution_limit_s weakened',
        'mr_resolution_limit_s=MILAN_MAX_OBSERVATION_INTERVAL_S / 2,',
        'mr_resolution_limit_s=1,',
        'test_release_round2_plan_contract',
    ),
    (
        'plan mr_capture_window weakened',
        'mr_capture_window="[first read - 1 s - observation_resolution_s, last read]",',
        'mr_capture_window="optional",',
        'test_release_round2_plan_contract',
    ),
    (
        'plan tu_rise_check weakened',
        'tu_rise_check="first discontinuity <= observed_start + observation_resolution_s",',
        'tu_rise_check="optional",',
        'test_release_round2_plan_contract',
    ),
    ("capture metadata completeness ignored",
     "capture_complete = capture_complete.complete", "capture_complete = True",
     "test_release_mr_capture_span"),
    ("capture metadata window ignored",
     "capture_window_s = capture_complete.window_s", "capture_window_s = None",
     "test_release_mr_capture_span"),
    (
        'history evidence refusal accepted',
        'return "NOT RUN", dict(detail, why="complete history and deciding resolution required")',
        'return "PASS", dict(detail, why="complete history and deciding resolution required")',
        'test_release_tu_history',
    ),
    (
        'history nonfinite event accepted',
        'return "NOT RUN", dict(detail, why="finite event history required")',
        'return "PASS", dict(detail, why="finite event history required")',
        'test_release_tu_history',
    ),
    (
        'history invalid interval accepted',
        'return "NOT RUN", dict(detail, why="finite interval endpoints required")',
        'return "PASS", dict(detail, why="finite interval endpoints required")',
        'test_release_tu_history',
    ),
    (
        'history invalid order accepted',
        'return "NOT RUN", dict(detail, why="ordered, separate positive intervals required")',
        'return "PASS", dict(detail, why="ordered, separate positive intervals required")',
        'test_release_tu_history',
    ),
    (
        'missing capture extent accepted',
        'return "NOT RUN", dict(detail, why="recorded capture window required")',
        'return "PASS", dict(detail, why="recorded capture window required")',
        'test_release_mr_capture_span',
    ),
    (
        'invalid mr records accepted',
        'return "NOT RUN", dict(detail, why="invalid recorded evidence")',
        'return "PASS", dict(detail, why="invalid recorded evidence")',
        'test_release_mr_record_boundaries',
    ),
    (
        'capture PDU extent check removed',
        'or any(not capture_start_s <= Decimal(str(pdu["timestamp_s"])) <= capture_end_s',
        'or any(False',
        'test_release_mr_capture_span',
    ),
    (
        'mr completeness guard removed',
        'if (capture_complete is not True or not stream_id or pdus is None',
        'if (not stream_id or pdus is None',
        'test_release_mr_missing_evidence',
    ),
    (
        'mr negative resolution guard removed',
        'or observation_resolution_s < 0):',
        'or False):',
        'test_release_mr_missing_evidence',
    ),

)


def main() -> int:
    """Require a clean baseline and a named test failure for every mutation."""
    source = Path(__file__).with_name("torture_campaign.py")
    original = source.read_bytes()
    text = original.decode("utf-8")
    with tempfile.TemporaryDirectory(prefix="release-controls-") as directory:
        candidate = Path(directory) / source.name
        candidate.write_bytes(original)
        command = [sys.executable, "-B", str(candidate), "--self-test"]
        clean = subprocess.run(command, capture_output=True, text=True, timeout=600)
        if clean.returncode != 0 or "\nOK\n" not in clean.stderr:
            print("FAIL: pristine planner self-test", clean.stdout, clean.stderr)
            return 1
        print("PASS: pristine planner self-test")
        for name, old, new, test in MUTANTS:
            if text.count(old) != 1:
                print(f"FAIL: {name}: expected one source anchor")
                return 1
            candidate.write_text(text.replace(old, new), encoding="utf-8")
            result = subprocess.run(command, capture_output=True, text=True, timeout=600)
            if result.returncode != 1 or f"FAIL: {test} " not in result.stderr:
                print(f"FAIL: {name}: no named behavioral failure", result.stdout, result.stderr)
                return 1
            print(f"KILLED: {name}: {test}")
    if source.read_bytes() != original:
        raise RuntimeError("planner source changed during controls")
    print(f"PASS: {len(MUTANTS)} mutations killed; source unchanged")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
