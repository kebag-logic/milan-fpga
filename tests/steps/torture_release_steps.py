# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""L3 release-plan coverage against issue #396's recorded decisions."""

from __future__ import annotations

import sys
import json
import subprocess
from pathlib import Path
from typing import TYPE_CHECKING

from behave import then, when

if TYPE_CHECKING:
    from behave.runner import Context

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tb" / "tools"))
import torture_campaign as tp  # noqa: E402


#: Issue #396's release repeats and the assertions each owes, stated here
#: independently of the planner's own table so that the audit has an oracle.
RELEASE_REQUIRED = {
    "release_soak": {
        "release.complete-evidence", "soak.continuous-duration", "soak.bound-both-directions",
        "soak.counter-walk", "soak.no-counter-errors", "soak.mr-causes-and-hold",
        "soak.gptp-continuity", "soak.tu-within-holdover", "soak.timestamp-margin",
        "soak.uptime-monotonic"},
    "release_audio_integrity": {
        "release.complete-evidence", "audio.inside-soak-window",
        "audio.counter-every-digital-path", "audio.counter-classified",
        "audio.planted-arms-found", "audio.capture-losses-apart", "audio.event-record",
        "audio.analog-sine-pair", "audio.zero-dut-glitches"},
    "release_power_cycles": {
        "release.complete-evidence", "power.cycle-count-and-phase", "power.state-restored",
        "power.adp-valid-time", "power.automatic-restore-bound", "power.rebind-bound",
        "power.single-boot", "power.counter-walk"},
}
#: The eight Milan v1.2 saved-state items of issue #70 and the binding.
EIGHT_ITEMS_AND_BINDING = [
    "configuration", "sampling_rate", "stream_format", "presentation_time_offset",
    "channel_mappings", "clock_source", "entity_names", "object_names", "stream_binding"]


def _plan(context: Context, areas: list[str]) -> None:
    context.tp_dut, context.tp_peer = tp.ARTY, tp.PEER
    context.tp_plan = tp.build_plan(areas)
    context.tp_cov = tp.plan_covers_every_index(context.tp_plan)


def _repeats(plan: list) -> list:
    """The release repeat operations, without identity steps or controls."""
    return [s for s in plan if s.op in RELEASE_REQUIRED]


@when("the {area} release area is planned")
def step_tp_release_area(context: Context, area: str) -> None:
    """Plan each release area alone, so another area cannot supply its coverage."""
    assert area in ("soak", "audio", "power")
    _plan(context, [area])


@then("every release repeat observes every index including each CRF sink")
def step_tp_release_observations(context: Context) -> None:
    """L3 oracle: the descriptor topology, independent of the plan's audit."""
    assert _repeats(context.tp_plan)
    for step in _repeats(context.tp_plan):
        actual = {(t["entity"], t["descriptor"], t["index"])
                  for t in step.args["counter_targets"]}
        expected = set()
        for device in (context.tp_dut, context.tp_peer):
            expected.update((device.entity_id, "stream_output", i)
                            for i in device.talker_indices())
            expected.update((device.entity_id, "stream_input", i)
                            for i in device.listener_indices())
            assert (device.entity_id, "stream_input", device.crf_in) in actual
        assert actual == expected, (step.sid, actual, expected)


@then("every release repeat binds compatible AAF and CRF in both directions")
def step_tp_release_bindings(context: Context) -> None:
    """One listener cannot be rebound by a second simultaneous pair."""
    dut, peer = context.tp_dut, context.tp_peer
    assert _repeats(context.tp_plan)
    for step in _repeats(context.tp_plan):
        pairs = step.args["pairs"]
        sinks = [(p["listener"], p["listener_index"]) for p in pairs]
        assert len(sinks) == len(set(sinks)), sinks
        for talker, listener in ((dut, peer), (peer, dut)):
            direction = [p for p in pairs if p["talker"] == talker.entity_id
                         and p["listener"] == listener.entity_id]
            assert any(p["talker_index"] in talker.talker_indices(False)
                       and p["listener_index"] in listener.listener_indices(False)
                       for p in direction), step.sid
            assert any(p["talker_index"] == talker.crf_out
                       and p["listener_index"] == listener.crf_in
                       for p in direction), step.sid
            for pair in direction:
                assert talker.is_crf_talker(pair["talker_index"]) == \
                    listener.is_crf_listener(pair["listener_index"])


@when("the {area} release plan loses its {missing}")
def step_tp_release_omission(context: Context, area: str, missing: str) -> None:
    """Plant one omission in one repeat while retaining a full matrix."""
    _plan(context, ["matrix", area])
    context.tp_release_area = area
    step = next(s for s in _repeats(context.tp_plan) if s.area == area)
    dut, peer = context.tp_dut, context.tp_peer
    if missing == "direction":
        step.args["pairs"] = [p for p in step.args["pairs"]
                              if p["talker"] != peer.entity_id]
    else:
        index = 1 if missing == "index" else dut.crf_in
        step.args["counter_targets"] = [
            t for t in step.args["counter_targets"]
            if not (t["entity"] == dut.entity_id
                    and t["descriptor"] == "stream_input" and t["index"] == index)]


@then("that release area fails its own audit")
def step_tp_release_audit_refuses(context: Context) -> None:
    """The per-area audit must detect the omission by its own verdict."""
    ok, detail = tp.area_covers_every_index(context.tp_plan, context.tp_release_area)
    assert not ok, detail
    assert detail["missing"], detail


@then("the complete matrix still passes its audit")
def step_tp_release_matrix_still_complete(context: Context) -> None:
    """The matrix cannot mask a release area's missing observation or binding."""
    ok, detail = tp.area_covers_every_index(context.tp_plan, "matrix")
    assert ok, detail


@then("the soak lasts 24 hours with periodic and endpoint observations")
def step_tp_release_soak_defaults(context: Context) -> None:
    """Issue #396 2026-10-26 fixes 24 hours; interval sampling must include both ends."""
    steps = [s for s in context.tp_plan if s.area == "soak"]
    assert len(steps) == 1
    args = steps[0].args
    assert args["duration_s"] == 24 * 60 * 60
    assert args["interval_s"] == 60
    assert args["sample_at_start"] and args["sample_at_end"]
    assert args["continuous_evidence"] == ["asCapable_transitions", "tu_intervals",
                                           "stream_flow", "uptime", "mr_pdus", "media_clock_events",
                                           "MEDIA_RESET_reads", "gptp_discontinuities", "gm_changes",
                                           "planted_events"]
    assert args["zero_growth_counters"] == ["SEQ_NUM_MISMATCH", "STREAM_INTERRUPTED",
                                            "LATE_TIMESTAMP", "EARLY_TIMESTAMP"]


@then("the audio run lasts the whole soak window inside it")
def step_tp_release_audio_defaults(context: Context) -> None:
    """Issue #396 decision 2026-10-04 as amended: the audio run rides inside the soak."""
    audio = [s for s in _repeats(context.tp_plan) if s.area == "audio"]
    assert [s.sid for s in audio] == ["audio.integrity"]
    args = audio[0].args
    assert args["window"] == "soak.continuous"
    assert args["duration_s"] == 24 * 60 * 60
    assert {p["path"] for p in args["digital_paths"]} == {"outbound", "return", "dut-tdm-loop"}
    assert [a["class"] for a in args["planted_arms"]] == ["dropped", "repeated", "bit-flip"]
    assert args["analog"]["tones_hz"] == [997, 9973]


@then("power repeats 100 idle and 50 journal-commit cold cuts and 50 soft resets")
def step_tp_release_power_defaults(context: Context) -> None:
    """Issue #396 2026-10-26: 150 cold cuts, a third in a commit, and 50 soft resets."""
    steps = _repeats([s for s in context.tp_plan if s.area == "power"])
    assert [(s.args["phase"], s.args["cycles"], s.args["cold"]) for s in steps] == [
        ("idle", 100, True), ("journal_commit", 50, True), ("soft_reset", 50, False)]
    for step in steps:
        assert step.args["total_cycles"] == 200
        assert step.args["persisted_items"] == EIGHT_ITEMS_AND_BINDING
        assert step.args["restore_bound_s"] == 30
        assert step.args["boot_margin_s"] == 5
        assert step.args["boot_observation_s"] == 35
        assert step.args["restore_start"] == "T0"
        assert step.args["restore_end"] == "first valid AVTP PDU of each persisted binding"
        assert step.args["rebind_limit_s"] == 1 and step.args["rebind_limit_exclusive"]
    assert [s.args.get("power_off_hold_s") for s in steps] == [8, 8, None]
    assert steps[2].args["time_origin"] == "T0: reset command, host monotonic clock"
    assert steps[0].args["snapshot_policy"] == "exact pre-cut committed snapshot"
    assert steps[1].args["snapshot_policy"] == "complete old or new committed snapshot"
    assert steps[1].args["cut_requires"] == "journal_commit_window"


@then("release assertions require complete measured evidence")
def step_tp_release_evidence(context: Context) -> None:
    """Desk coverage is never a substitute for completed physical evidence."""
    assert len(_repeats(context.tp_plan)) == 5
    for step in _repeats(context.tp_plan):
        specs = {a.name: a for a in step.asserts}
        assert "release.complete-evidence" in specs
        assert all(a.severity == "SHALL" for a in specs.values())
        assert "SKIP" in specs["release.complete-evidence"].clause
        assert {"image_hashes", "uart_transcript", "wire_captures",
                "verdict_jsonl", "temperature_log"} <= set(step.args["evidence"])


@when("release repeat {repeat} loses {role} {missing}")
def step_tp_release_repeat_omission(context: Context, repeat: str, role: str, missing: str) -> None:
    """L3: each repeat owns both devices' counters and both traffic directions."""
    area = repeat.split(".")[0]
    _plan(context, ["matrix", area])
    context.tp_release_area = area
    step = next(s for s in context.tp_plan if s.sid == repeat)
    device = context.tp_dut if role == "DUT" else context.tp_peer
    if missing in ("AAF direction", "CRF direction"):
        step.args["pairs"] = [
            pair for pair in step.args["pairs"]
            if not (pair["talker"] == device.entity_id and
                    (pair["talker_index"] == device.crf_out) == (missing == "CRF direction"))]
    else:
        descriptor = "stream_output" if missing == "talker index" else "stream_input"
        index = (device.talker_indices(False)[-1] if missing == "talker index"
                 else device.crf_in if missing == "CRF sink"
                 else device.listener_indices(False)[-1])
        step.args["counter_targets"] = [
            target for target in step.args["counter_targets"]
            if not (target["entity"] == device.entity_id and
                    target["descriptor"] == descriptor and target["index"] == index)]


@when("a diagnostic release profile uses non-default timing and counts")
def step_tp_release_parameters(context: Context) -> None:
    """Non-default inputs are an independent oracle for the emitted parameters."""
    settings = tp.ReleaseSettings(
        soak_duration_s=125, soak_interval_s=17, power_cycles=10, idle_cycles=6,
        commit_cycles=2, reset_cycles=2, persisted_items=("stream_binding", "clock_source"),
        restore_bound_s=23, boot_margin_s=7, power_off_hold_s=13, audio_duration_s=100,
        audio_context_s=3)
    context.tp_plan = tp.build_plan(["soak", "audio", "power"], release=settings)


@then("every release repeat preserves those parameters and its timing origins")
def step_tp_release_parameter_results(context: Context) -> None:
    """L3 #396 / REQ-VER-06: T0 follows the cycle kind; the hold is recorded separately."""
    repeats = {s.sid: s for s in _repeats(context.tp_plan)}
    soak, audio = repeats["soak.continuous"], repeats["audio.integrity"]
    idle, commit, reset = (repeats["power." + p] for p in ("idle", "journal_commit", "soft_reset"))
    assert (soak.args["duration_s"], soak.args["interval_s"]) == (125, 17)
    assert (audio.args["duration_s"], audio.args["context_s"]) == (100, 3)
    assert (idle.args["cycles"], commit.args["cycles"], reset.args["cycles"]) == (6, 2, 2)
    assert reset.args["time_origin"] == "T0: reset command, host monotonic clock"
    assert "power_off_hold_s" not in reset.args
    for step in (idle, commit, reset):
        assert step.args["total_cycles"] == 10
        assert step.args["restore_bound_s"] == 23 and step.args["boot_margin_s"] == 7
        assert step.args["boot_observation_s"] == 30
        assert step.args["adp_start"] == "T0"
    for step in (idle, commit):
        args = step.args
        assert args["power_off_hold_s"] == 13
        assert args["power_off_hold_in_adp_window"] is False
        assert args["time_origin"] == "T0: power-strip ON command, host monotonic clock"
        assert args["adp_start"] == "T0"
        assert args["adp_required_valid_time"] == 10
        assert args["adp_deadline"] == "2 * pre_cut_valid_time"
        assert args["adp_elapsed"] == "first_post_cut_available_host_s - t0_host_s"
        assert args["adp_limit_exclusive"]
        assert args["rebind_requires"] == "automatic restoration passed for every persisted binding"
        assert {"power.automatic-restore-bound", "power.rebind-bound", "power.single-boot"} <= {
            spec.name for spec in step.asserts}
    assert all(not step.args["release_eligible"] for step in repeats.values())


@then("the first-boot restart control fails the release boot assertion")
def step_tp_release_boot_control(context: Context) -> None:
    """L3 #366: a later healthy prompt cannot erase an earlier BIOS restart."""
    assert tp.check_release_boot(1, 0, capture_complete=True)[0] == "PASS"
    assert tp.check_release_boot(2, 1, capture_complete=True)[0] == "FAIL"
    assert tp.check_release_boot(1, 0, capture_complete=False)[0] == "SKIP"


@when("the release CLI omits only {shape} from the {role} topology")
def step_tp_release_partial_cli(context: Context, shape: str, role: str) -> None:
    """L3 #396 round 3: valid inherited shapes must not attest provenance."""
    specs = ["entity=0011223344556677,mac=001122334455,talkers=2,listeners=2,crf_out=16,crf_in=16",
             "entity=8899aabbccddeeff,mac=8899aabbccdd,talkers=2,listeners=2,crf_out=16,crf_in=16"]
    position = 0 if role == "DUT" else 1
    missing = {"crf_in", "crf_out"} if shape == "CRF keys" else {"listeners"}
    specs[position] = ",".join(part for part in specs[position].split(",")
                               if part.split("=", 1)[0] not in missing)
    root = Path(__file__).resolve().parents[2]
    result = subprocess.run(
        [sys.executable, "-B", "tb/tools/torture_campaign.py", "--plan", "--areas", "soak,audio,power",
         "--json", "--dut", specs[0], "--peer", specs[1]],
        cwd=root, capture_output=True, text=True, check=True, timeout=600)
    context.release_cli_steps = [step for step in json.loads(result.stdout)
                                 if step["op"] in RELEASE_REQUIRED]


@then("every release repeat reports diagnostic topology")
def step_tp_release_partial_result(context: Context) -> None:
    """Require all five emitted repeats to reject the partial CLI shape."""
    assert len(context.release_cli_steps) == 5
    for step in context.release_cli_steps:
        assert step["args"]["topology_explicit"] is False
        assert step["args"]["release_eligible"] is False


@when("an explicit release profile uses a restoration bound of {seconds:d} seconds")
def step_tp_release_restore_bound(context: Context, seconds: int) -> None:
    """L3 #396 round 3 varies only restoration, keeping other prerequisites valid."""
    context.tp_plan = tp.build_plan(
        ["soak", "audio", "power"],
        release=tp.ReleaseSettings(topology_explicit=True, restore_bound_s=seconds))


@then("every release repeat is {eligibility} for release")
def step_tp_release_eligible(context: Context, eligibility: str) -> None:
    """The independent 29/30/31-second examples pin the inclusive ceiling."""
    assert len(_repeats(context.tp_plan)) == 5
    for step in _repeats(context.tp_plan):
        assert step.args["release_eligible"] is (eligibility == "eligible")


@then("uncertainty is correlated and bounded by half a second plus observation resolution")
def step_tp_release_tu_bound(context: Context) -> None:
    """L3 #396 round 4 measures holdover from the interval's last event."""
    args = context.tp_plan[0].args
    assert args["tu_holdover_bound_s"] == 0.5
    assert args["tu_time_origin"] == "last recorded discontinuity before tu clears"
    assert args["tu_event_window"] == "[observed_start - observation_resolution_s, clear)"
    assert args["tu_discontinuity_kinds"] == [
        "PHC settime/adjtime", "fabric discontinuity", "GM-identity edge",
        "GM time-source change", "other detected gPTP discontinuity"]
    assert args["tu_uncorrelated"] == "fail"
    assert args["tu_observation_resolution"] == \
        "record wire-capture and correlated event-timestamp resolution in seconds"


@then("a chained discontinuity clearing at {seconds:g} seconds is {verdict}")
def step_tp_release_tu_chain(context: Context, seconds: float, verdict: str) -> None:
    """L3 #396 round 4: GM edge at zero, followed by PHC step at 0.2 s."""
    actual, evidence = tp.check_release_tu(
        (0, seconds), [0, 0.2], holdover_bound_s=context.tp_plan[0].args["tu_holdover_bound_s"],
        observation_resolution_s=0.001, capture_complete=True, gm_changes_s=[0])
    assert actual == verdict, evidence


@then("an uncertainty interval without a discontinuity fails")
def step_tp_release_tu_no_event(context: Context) -> None:
    """L3 #396 round 4: complete capture cannot excuse uncorrelated tu."""
    actual, evidence = tp.check_release_tu(
        (0, 0.62), [], holdover_bound_s=context.tp_plan[0].args["tu_holdover_bound_s"],
        observation_resolution_s=0.001, capture_complete=True, gm_changes_s=[])
    assert actual == "FAIL", evidence


@then("a lone discontinuity at {event_s:g} seconds with {resolution_s:g} second resolution is {verdict}")
def step_tp_release_tu_start(context: Context, event_s: float, resolution_s: float, verdict: str) -> None:
    """L3 #396 round 5: the observed interval is [0, 0.4) seconds."""
    actual, evidence = tp.check_release_tu(
        (0, 0.4), [event_s], holdover_bound_s=context.tp_plan[0].args["tu_holdover_bound_s"],
        observation_resolution_s=resolution_s, capture_complete=True, gm_changes_s=[])
    assert actual == verdict, evidence


@then("the planned uncertainty oracle rejects missing holds for every GM change")
def step_tp_release_tu_history(context: Context) -> None:
    """A later unserved GM edge cannot hide behind an earlier valid interval."""
    name = context.tp_plan[0].args["tu_oracle"]
    assert name == "check_release_tu_history"
    oracle = getattr(tp, name)
    for intervals, gm, expected in (([], [0], "FAIL"), (None, [0], "NOT RUN"),
                                    ([(0, 0.3)], [0, 0.3], "FAIL"),
                                    ([(0, 0.3)], [0, 0.35], "FAIL"),
                                    ([(0, 0.3), (1, 1.3)], [0, 1], "PASS")):
        verdict, evidence = oracle(intervals, [], gm_changes_s=gm,
                                   observation_resolution_s=0.001, capture_complete=True)
        assert verdict == expected, evidence


# ------------------------------------------- issue #396 decisions 2026-10-26 --
@then("the power phases add up to 200 cycles")
def step_tp_release_cycle_total(context: Context) -> None:
    """The decided mix, read from the plan and summed here, not by the audit."""
    steps = _repeats(context.tp_plan)
    assert sum(s.args["cycles"] for s in steps) == 200, [s.args["cycles"] for s in steps]
    assert {s.args["total_cycles"] for s in steps} == {200}
    assert sorted(s.args["phase"] for s in steps) == ["idle", "journal_commit", "soft_reset"]


@then("150 of them are cold cuts and a third of those land in a journal commit")
def step_tp_release_cold_share(context: Context) -> None:
    """Owner decision 2026-10-26 item 2: 150 cold, 50 of them inside a commit."""
    cycles = {s.args["phase"]: (s.args["cycles"], s.args["cold"]) for s in _repeats(context.tp_plan)}
    cold = sum(count for count, is_cold in cycles.values() if is_cold)
    assert cold == 150 and cycles["journal_commit"] == (50, True), cycles
    assert cycles["soft_reset"] == (50, False), cycles


@then("every cycle restores the eight Milan items and the binding")
def step_tp_release_items(context: Context) -> None:
    """Owner decision 2026-10-26 item 3: the eight items, not the binding alone."""
    for step in _repeats(context.tp_plan):
        assert step.args["persisted_items"] == EIGHT_ITEMS_AND_BINDING, step.sid
        assert step.args["state_oracle"] == "check_release_state_restored"
        assert "power.state-restored" in {a.name for a in step.asserts}


@when("the power release plan loses one {phase} cycle")
def step_tp_release_lose_cycle(context: Context, phase: str) -> None:
    """Plant a 199-cycle mix in one phase while the matrix stays complete."""
    _plan(context, ["matrix", "power"])
    context.tp_release_area = "power"
    step = next(s for s in _repeats(context.tp_plan) if s.args["phase"] == phase)
    step.args["cycles"] -= 1


@then("every release repeat carries its area's required assertions at SHALL severity")
def step_tp_release_required(context: Context) -> None:
    """Against the independent table above; one repeat of each kind at least."""
    repeats = _repeats(context.tp_plan)
    assert {s.op for s in repeats} == set(RELEASE_REQUIRED)
    for step in repeats:
        shall = {a.name for a in step.asserts if a.severity == "SHALL"}
        assert RELEASE_REQUIRED[step.op] <= shall, (step.sid, RELEASE_REQUIRED[step.op] - shall)


@then("every release repeat refuses an unsupported operation instead of skipping it")
def step_tp_release_refuses(context: Context) -> None:
    """A runner that cannot perform a repeat reports it, never a silent PASS."""
    for step in _repeats(context.tp_plan):
        assert step.args["unsupported_operation"] == "refuse; never skip or claim PASS", step.sid
        assert "SKIP" in {a.name: a.clause for a in step.asserts}["release.complete-evidence"]


@when("release repeat {repeat} has its {assertion} assertion {change}")
def step_tp_release_lose_assertion(context: Context, repeat: str, assertion: str, change: str) -> None:
    """Drop an assertion, or downgrade it to INFO, in one repeat only."""
    from dataclasses import replace
    area = repeat.split(".")[0]
    _plan(context, ["matrix", area])
    context.tp_release_area = area
    step = next(s for s in context.tp_plan if s.sid == repeat)
    assert assertion in {a.name for a in step.asserts}
    if change == "dropped":
        step.asserts = tuple(a for a in step.asserts if a.name != assertion)
    else:
        assert change == "downgraded"
        step.asserts = tuple(replace(a, severity="INFO") if a.name == assertion else a
                             for a in step.asserts)


#: growth: (counter increments, planted windows, read interval the growth lands in).
_GROWTH = {
    "nothing": ({}, [], 2),
    "one SEQ_NUM_MISMATCH": ({"SEQ_NUM_MISMATCH": 1}, [], 2),
    "one STREAM_INTERRUPTED": ({"STREAM_INTERRUPTED": 1}, [], 2),
    "one LATE_TIMESTAMP": ({"LATE_TIMESTAMP": 1}, [], 2),
    "one EARLY_TIMESTAMP": ({"EARLY_TIMESTAMP": 1}, [], 2),
    "one MEDIA_UNLOCKED": ({"MEDIA_UNLOCKED": 1}, [], 2),
    "one MEDIA_UNLOCKED in a planted event": ({"MEDIA_UNLOCKED": 1}, [(20, 25)], 1),
    "one MEDIA_UNLOCKED beside a planted event": ({"MEDIA_UNLOCKED": 1}, [(20, 25)], 2),
    "two MEDIA_UNLOCKED in one planted event": ({"MEDIA_UNLOCKED": 2}, [(20, 25)], 1),
}


@when("an input's soak counter walk shows {growth}")
def step_tp_release_counter_walk(context: Context, growth: str) -> None:
    """Reads of one CRF Stream Input at 100, 120, 125 and 160 s, with the named growth.

    The runner reads the input at a planted window's start and end, so an
    unlock inside the window lands between the 120 and 125 s reads; one
    beside it lands in the next interval and stays unexcused (REQ-VER-06).
    """
    names = ("SEQ_NUM_MISMATCH", "STREAM_INTERRUPTED", "LATE_TIMESTAMP",
             "EARLY_TIMESTAMP", "MEDIA_UNLOCKED")
    delta, windows, landing = _GROWTH[growth]
    reads = []
    for k, timestamp in enumerate((100, 120, 125, 160)):
        grown = k > landing
        reads.append({"target": "dut/stream_input/4", "timestamp_s": timestamp,
                      "values": {name: 3 + (delta.get(name, 0) if grown else 0) for name in names}})
    planted = [{"target": "dut/stream_input/4", "kind": "CRF disruption",
                "window_s": (100 + start, 100 + end)} for start, end in windows]
    context.release_counter_verdict = tp.check_release_soak_counters(
        reads, planted, targets=["dut/stream_input/4"], capture_complete=True)


@then("the soak counter oracle grades it {verdict}")
def step_tp_release_counter_verdict(context: Context, verdict: str) -> None:
    """The verdict the decided rule owes; the named oracle is the plan's own."""
    actual, detail = context.release_counter_verdict
    assert actual == verdict, detail
    soak = tp.build_plan(["soak"])[0]
    assert soak.args["counter_oracle"] == "check_release_soak_counters"


@when("the {control} negative control is run at the desk")
def step_tp_release_control(context: Context, control: str) -> None:
    """Run the plan entry's own desk fixture through its own oracle."""
    plan = tp.build_plan([control.split(".")[0]])
    context.release_control = next(s for s in plan if s.sid == control)
    context.release_control_result = tp.run_release_control(context.release_control)


@then("the control fails {assertion}")
def step_tp_release_control_fails(context: Context, assertion: str) -> None:
    """The control carries the assertion it expects to fail, and the oracle fails."""
    step = context.release_control
    assert step.op == "release_negative_control"
    assert step.args["expected_failing_assertion"] == assertion
    assert assertion in {a.name for a in step.asserts}
    assert step.args["expected_verdict"] == "FAIL"
    verdict, detail = context.release_control_result
    assert verdict == "FAIL", detail


@then("the same oracle passes once the defect is removed")
def step_tp_release_control_clean(context: Context) -> None:
    """Without its defect the fixture passes, so the FAIL is the defect's alone."""
    args = context.release_control.args
    if args["oracle"] == "check_release_boot":
        verdict, detail = tp.check_release_boot(1, 0, capture_complete=True)
    elif args["oracle"] == "check_release_state_restored":
        fixture = args["desk_fixture"]
        verdict, detail = tp.check_release_state_restored(
            fixture["pre"], fixture["pre"], fixture["defaults"], items=fixture["items"], phase="idle")
    else:
        fixture = args["fixture"]
        verdict, detail = tp.grade_audio_counter_capture(
            tp.synthesize_counter_capture(fixture["frames"], fixture["channels"],
                                          events=fixture["source_events"]),
            tp.CounterCapture(fixture["channels"], "big", fixture["rate_hz"], 0.0, 0.0),
            tp.CounterRunLog(fixture["planted_arms"], [], 2))
    assert verdict == "PASS", detail


@when("the planted audio drop is graded on its synthetic capture")
def step_tp_release_audio_drop(context: Context) -> None:
    """The plan's own control entry, graded offline with no bench."""
    step = next(s for s in tp.build_plan(["audio"]) if s.sid == "audio.control.planted-drop")
    assert step.args["offline"] is True
    context.release_audio_fixture = step.args["fixture"]
    context.release_audio_result = tp.run_release_control(step)


@then("the grader finds one 5-sample drop at the planted sample on every channel")
def step_tp_release_audio_drop_found(context: Context) -> None:
    """Exact class, size, sample and channel set: nothing approximate."""
    verdict, detail = context.release_audio_result
    assert verdict == "FAIL", detail["why"]
    dut = [e for e in detail["events"] if e["attribution"] == "dut"]
    planted = context.release_audio_fixture["dut_event"]
    assert planted == {"kind": "drop", "index": 3 * 4096 + 7, "n": 5}
    assert sorted((e["channel"], e["class"], e["n"], e["capture_index"]) for e in dut) == [
        (channel, "dropped", 5, planted["index"]) for channel in range(8)]


@then("every planted arm is found and attributed apart from the DUT")
def step_tp_release_audio_arms(context: Context) -> None:
    """Three arms at each end; eight channels see each source-side slip."""
    verdict, detail = context.release_audio_result
    assert detail["planted_missed"] == []
    assert detail["counts"]["planted"] == {"dropped": 16, "repeated": 16, "bit-flip": 2}


def _counter_capture(extra: list, losses: list | None = None, arms_drop: int = 0) -> tuple:
    """A four-channel capture with the drop, repeat and flip arms at both ends."""
    frames = 4 * 4096
    sites = (200, 400, 600, frames - 800, frames - 500, frames - 200)
    source = [{"kind": "drop", "index": sites[0], "n": 3}, {"kind": "repeat", "index": sites[1], "n": 2},
              {"kind": "flip", "index": sites[2], "channel": 0, "mask": 0x100},
              {"kind": "drop", "index": sites[3], "n": 3}, {"kind": "repeat", "index": sites[4], "n": 2},
              {"kind": "flip", "index": sites[5], "channel": 1, "mask": 0x100}]
    arms = [{"class": "dropped", "index": sites[0], "n": 3}, {"class": "repeated", "index": sites[1], "n": 2},
            {"class": "bit-flip", "index": sites[2], "channel": 0, "mask": 0x100},
            {"class": "dropped", "index": sites[3], "n": 3}, {"class": "repeated", "index": sites[4], "n": 2},
            {"class": "bit-flip", "index": sites[5], "channel": 1, "mask": 0x100}]
    arms += [{"class": "dropped", "index": 9000, "n": arms_drop}] if arms_drop else []
    capture = tp.synthesize_counter_capture(frames, 4, events=source + extra)
    return tp.grade_audio_counter_capture(
        capture, tp.CounterCapture(4, "big", 48000, 0.0, 0.0),
        tp.CounterRunLog(arms, losses or [], 0))


_EVENTS = {
    "a 3-sample drop": {"kind": "drop", "index": 8000, "n": 3},
    "a 2-sample repeat": {"kind": "repeat", "index": 8000, "n": 2},
    "6 samples of silence": {"kind": "silence", "index": 8000, "n": 6},
    "a bit flip on one channel": {"kind": "flip", "index": 8000, "channel": 3, "mask": 0x00000800},
    "a swap of two channels": {"kind": "swap", "index": 8000, "n": 4, "channels": (1, 2)},
}


@when("a synthetic counter capture carries {event}")
def step_tp_release_counter_event(context: Context, event: str) -> None:
    """One unplanted event in the middle of an otherwise clean, armed capture."""
    context.release_counter_event = _EVENTS[event]
    context.release_counter_result = _counter_capture([_EVENTS[event]])


@then("the audio grader reports {cls} on {count:d} channels")
def step_tp_release_counter_class(context: Context, cls: str, count: int) -> None:
    """Class and sample exact, and nothing else attributed to the DUT."""
    verdict, detail = context.release_counter_result
    assert verdict == "FAIL", detail["why"]
    dut = [e for e in detail["events"] if e["attribution"] == "dut"]
    assert len(dut) == count, dut
    assert {(e["class"], e["capture_index"]) for e in dut} == {
        (cls, context.release_counter_event["index"])}


@when("a synthetic counter capture logs an arm the source never planted")
def step_tp_release_counter_missed(context: Context) -> None:
    """The log claims a drop at sample 9000; the capture has none there."""
    context.release_counter_result = _counter_capture([], arms_drop=4)


@then("the audio grader voids the run as NOT RUN")
def step_tp_release_counter_void(context: Context) -> None:
    """A grader that missed a control cannot be trusted with the rest."""
    verdict, detail = context.release_counter_result
    assert verdict == "NOT RUN", detail["why"]
    assert detail["why"] == "void: a planted arm was missed"
    assert [arm["index"] for arm in detail["planted_missed"]] == [9000]


@then("a logged capture loss is attributed to the capture, not the DUT")
def step_tp_release_counter_loss(context: Context) -> None:
    """The same slip passes when the capture tool logged it, and fails when not."""
    loss = {"kind": "drop", "index": 7000, "n": 11}
    verdict, detail = _counter_capture([loss], losses=[{"index": 7000, "frames": 11}])
    assert verdict == "PASS", detail["why"]
    assert detail["counts"]["capture"] == {"dropped": 4}
    assert _counter_capture([loss])[0] == "FAIL"


# ------------------------------------- the non-repeating counter, issue #396 --
def _counter_word(tag: int, n: int) -> int:
    """REQ-VER-06's counter layout restated here, apart from the planner: channel
    number in sample bits 15:12, n mod 2048 in bits 11:1, and in bit 0 bit n mod 32
    of block n div 2048's code, the block number times 0x9E3779B1 modulo 2^32."""
    code = ((n // 2048) * 0x9E3779B1) % 2**32
    return ((tag << 12) | ((n % 2048) << 1) | ((code >> (n % 32)) & 1)) << 8


def _independent_capture(frames: int, shifts: dict, flips: list) -> bytes:
    """Four big-endian S32 channels; `shifts` moves the source position from an
    index on, and each flip (index, channel, mask) XORs one word."""
    import struct
    rows, shift = [], 0
    for index in range(frames):
        shift += shifts.get(index, 0)
        rows.append([_counter_word(channel + 1, index + shift) for channel in range(4)])
    for index, channel, mask in flips:
        rows[index][channel] ^= mask
    return b"".join(struct.pack(">4I", *row) for row in rows)


#: Arms in the first and the last tenth of an 8192-frame capture.
_ARM_SHIFTS = {100: 3, 300: -2, 7492: 3, 7742: -2}
_ARMS = [{"class": "dropped", "index": 100, "n": 3}, {"class": "repeated", "index": 300, "n": 2},
         {"class": "bit-flip", "index": 500, "mask": 0x100, "channel": 1},
         {"class": "dropped", "index": 7492, "n": 3}, {"class": "repeated", "index": 7742, "n": 2},
         {"class": "bit-flip", "index": 7992, "mask": 0x100, "channel": 3}]


def _with_arms(shifts: dict) -> dict:
    """The arm shifts plus `shifts`, added where both move the same index."""
    merged = dict(_ARM_SHIFTS)
    for index, shift in shifts.items():
        merged[index] = merged.get(index, 0) + shift
    return merged


def _arm_edits() -> list:
    """The two planted flips of the code bit."""
    return [(500, 1, 0x100), (7992, 3, 0x100)]


def _grade_independent(shifts: dict, edits: list, **layout: object) -> tuple:
    capture = _independent_capture(8192, _with_arms(shifts), _arm_edits() + edits)
    return tp.grade_audio_counter_capture(capture, tp.CounterCapture(4, "big", 48000, 0.0, 0.0, **layout),
                                          tp.CounterRunLog(_ARMS, [], 0))


def _dut(detail: dict) -> list:
    return sorted((e["channel"], e["capture_index"], e["class"], e.get("n"), e.get("mask"), e.get("partner"))
                  for e in detail.get("events", []) if e["attribution"] == "dut")


@when("the counter capture shows a {n:d}-sample {kind}")
def step_tp_release_block_slip(context: Context, n: int, kind: str) -> None:
    """A slip at sample 3000; a counter repeating every 4096 samples would alias these sizes."""
    assert kind in ("drop", "repeat")
    context.release_slip = (3000, n)
    context.release_counter_result = _grade_independent({3000: n if kind == "drop" else -n}, [])


@then("the audio grader reports {cls} of {n:d} samples on {count:d} channels within 63 samples of the slip")
def step_tp_release_block_slip_found(context: Context, cls: str, n: int, count: int) -> None:
    """Sized exactly; a slip of whole blocks may be located to an interval of under 64 samples."""
    verdict, detail = context.release_counter_result
    assert verdict == "FAIL", detail["why"]
    at, size = context.release_slip
    dut = [e for e in detail["events"] if e["attribution"] == "dut"]
    assert len(dut) == count and {(e["class"], e["n"]) for e in dut} == {(cls, size)}, dut
    for event in dut:
        first, last = event.get("located_within", (event["capture_index"],) * 2)
        assert first <= at <= last < first + 64 and last == event["capture_index"], event


@when("a synthetic counter capture flips one channel-number bit on one channel")
def step_tp_release_tag_flip(context: Context) -> None:
    """Sample bit 12 of channel 2's word at 3000: its number 3 reads as channel 1's 2."""
    context.release_counter_result = _grade_independent({}, [(3000, 2, 0x00100000)])


@then("the audio grader reports one bit-flip with that mask and no swap")
def step_tp_release_tag_flip_found(context: Context) -> None:
    """Channel 1 keeps its own word, so nothing was exchanged."""
    verdict, detail = context.release_counter_result
    assert verdict == "FAIL", detail["why"]
    assert _dut(detail) == [(2, 3000, "bit-flip", 1, "0x00100000", None)], _dut(detail)


@when("a synthetic counter capture holds one sample on every channel")
def step_tp_release_hold(context: Context) -> None:
    """Sample 3000 repeats sample 2999 and sample 3001 follows on time."""
    context.release_counter_result = _grade_independent({3000: -1, 3001: 1}, [])


@then("the audio grader reports a 1-sample repeat and then a 1-sample drop on every channel")
def step_tp_release_hold_found(context: Context) -> None:
    """The hold is the slip pair it is, never a bit-corruption mask."""
    verdict, detail = context.release_counter_result
    assert verdict == "FAIL", detail["why"]
    assert _dut(detail) == sorted([(c, 3000, "repeated", 1, None, None) for c in range(4)]
                                  + [(c, 3001, "dropped", 1, None, None) for c in range(4)]), _dut(detail)


@when("a synthetic counter capture swaps two channels for the whole run")
def step_tp_release_static_swap(context: Context) -> None:
    """Channels 1 and 3 exchanged from the first frame, the flip arms planted on both."""
    capture = bytearray(_independent_capture(8192, _with_arms({}), _arm_edits()))
    for frame in range(8192):
        one, three = slice(16 * frame + 4, 16 * frame + 8), slice(16 * frame + 12, 16 * frame + 16)
        capture[one], capture[three] = capture[three], capture[one]
    context.release_counter_result = tp.grade_audio_counter_capture(
        bytes(capture), tp.CounterCapture(4, "big", 48000, 0.0, 0.0), tp.CounterRunLog(_ARMS, [], 0))


@then("the audio grader fails the run with two swaps and every planted arm found")
def step_tp_release_static_swap_found(context: Context) -> None:
    """A wrong channel map is a DUT finding, not a void measurement."""
    verdict, detail = context.release_counter_result
    assert verdict == "FAIL" and detail["planted_missed"] == [], detail["why"]
    assert _dut(detail) == [(1, 0, "swap", 8192, None, 3), (3, 0, "swap", 8192, None, 1)], _dut(detail)


@when("a synthetic counter capture loses frames at the capture before a corrupted sample")
def step_tp_release_loss_clock(context: Context) -> None:
    """409600 frames lost at stored index 2000, then sample 3000 corrupted, with and
    without the capture tool's end anchor."""
    lost, edits = 409600, [(3000, 0, 1)]
    capture = _independent_capture(8192, _with_arms({2000: lost}), _arm_edits() + edits)
    span = (8192 + lost) / 48000
    context.release_loss_results = [tp.grade_audio_counter_capture(
        capture, tp.CounterCapture(4, "big", 48000, 100.0, 200.0, **layout),
        tp.CounterRunLog(_ARMS, [{"index": 2000, "frames": lost}], 0))
        for layout in ({"anchors": ((8192, 100.0 + span, 200.0 + span),), "gptp_steps_wall_s": ()}, {})]


@then("the corrupted sample's wall and gPTP times include the lost frames")
def step_tp_release_loss_clock_found(context: Context) -> None:
    """(3000 + 409600) / 48000 s after the start: 8.6083 s, not 0.0625 s."""
    verdict, detail = context.release_loss_results[0]
    assert verdict == "FAIL", detail["why"]
    event = next(e for e in detail["events"] if e["attribution"] == "dut")
    assert event["acquisition_index"] == 3000 + 409600, event
    assert abs(event["wall_s"] - (100.0 + 412600 / 48000)) < 1e-6, event
    assert abs(event["gptp_s"] - (200.0 + 412600 / 48000)) < 1e-6, event
    assert detail["counts"]["capture"] == {"dropped": 4}, detail["counts"]


@then("without an anchor after the event its times are null, not invented")
def step_tp_release_loss_clock_unsupported(context: Context) -> None:
    """The start time alone cannot carry a later event through 8.6 s of unknowns."""
    verdict, detail = context.release_loss_results[1]
    event = next(e for e in detail["events"] if e["attribution"] == "dut")
    assert (event["wall_s"], event["gptp_s"]) == (None, None), event
    assert event["timing"] == "unsupported: no anchor after the event", event


@when("a synthetic counter capture plants every arm in the middle of the run")
def step_tp_release_mid_arms(context: Context) -> None:
    """The arms all within 300 samples of the midpoint of an 8192-frame capture."""
    shifts = {3796: 3, 3896: -2, 4196: 3, 4296: -2}
    arms = [{"class": "dropped", "index": 3796, "n": 3}, {"class": "repeated", "index": 3896, "n": 2},
            {"class": "bit-flip", "index": 3996, "mask": 0x100, "channel": 1},
            {"class": "dropped", "index": 4196, "n": 3}, {"class": "repeated", "index": 4296, "n": 2},
            {"class": "bit-flip", "index": 4396, "mask": 0x100, "channel": 1}]
    edits = [(3996, 1, 0x100), (4396, 1, 0x100)]
    context.release_counter_result = tp.grade_audio_counter_capture(
        _independent_capture(8192, shifts, edits), tp.CounterCapture(4, "big", 48000, 0.0, 0.0),
        tp.CounterRunLog(arms, [], 0))


@then("the audio grader voids the run as NOT RUN for arms outside the first and the last tenth")
def step_tp_release_mid_arms_void(context: Context) -> None:
    """Every arm is found, so only their placement voids the run."""
    verdict, detail = context.release_counter_result
    assert verdict == "NOT RUN" and detail["planted_missed"] == [], detail["why"]
    assert "first and the last tenth" in detail["why"], detail["why"]


_COMMIT_ITEMS = EIGHT_ITEMS_AND_BINDING
_PRE = {item: f"set-{item}" for item in _COMMIT_ITEMS}
_NEW = {item: f"new-{item}" for item in _COMMIT_ITEMS}
_DEFAULTS = {item: f"default-{item}" for item in _COMMIT_ITEMS}
#: case: (readback, pending snapshot, commit window, cut instant)
_COMMIT_CASES = {
    "restores the new snapshot inside its commit window": (_NEW, _NEW, (40.0, 40.4), 40.1),
    "restores the old snapshot inside its commit window": (_PRE, _NEW, (40.0, 40.4), 40.1),
    "restores a mix of old and new values": (dict(_PRE, clock_source=_NEW["clock_source"]), _NEW,
                                             (40.0, 40.4), 40.1),
    "pends default values while persistence is disabled": (_DEFAULTS, _DEFAULTS, (40.0, 40.4), 40.1),
    "pends one default value": (_NEW, dict(_NEW, entity_names=_DEFAULTS["entity_names"]), (40.0, 40.4), 40.1),
    "lands after its commit window closed": (_NEW, _NEW, (40.0, 40.4), 40.4),
    "has no cut-phase evidence": (_NEW, _NEW, None, None),
}


@when("a journal-commit cut {case}")
def step_tp_release_commit_case(context: Context, case: str) -> None:
    """One commit cut of the nine-item inventory, through the plan's own state oracle."""
    post, pending, window, cut_s = _COMMIT_CASES[case]
    oracle = getattr(tp, next(s for s in tp.build_plan(["power"])
                              if s.sid == "power.journal_commit").args["state_oracle"])
    committed = pending if window is None else tp.ReleaseCommitCut(pending, window, cut_s)
    context.release_commit_result = oracle(_PRE, post, _DEFAULTS, items=_COMMIT_ITEMS,
                                           phase="journal_commit", committed=committed)


@then("the state oracle grades the commit cut {verdict}")
def step_tp_release_commit_verdict(context: Context, verdict: str) -> None:
    """The verdict REQ-VER-06 owes the case."""
    actual, detail = context.release_commit_result
    assert actual == verdict, detail
