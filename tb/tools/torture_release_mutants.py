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
     'Decimal(str(MILAN_MAX_OBSERVATION_INTERVAL_S))', 'Decimal(0)',
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
