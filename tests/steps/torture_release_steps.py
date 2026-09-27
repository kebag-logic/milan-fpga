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


def _plan(context: Context, areas: list[str]) -> None:
    context.tp_dut, context.tp_peer = tp.ARTY, tp.PEER
    context.tp_plan = tp.build_plan(areas)
    context.tp_cov = tp.plan_covers_every_index(context.tp_plan)


@when("the {area} release area is planned")
def step_tp_release_area(context: Context, area: str) -> None:
    """Plan each release area alone, so another area cannot supply its coverage."""
    assert area in ("soak", "power")
    _plan(context, [area])


@then("every release repeat observes every index including each CRF sink")
def step_tp_release_observations(context: Context) -> None:
    """L3 oracle: the descriptor topology, independent of the plan's audit."""
    for step in context.tp_plan:
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
    for step in context.tp_plan:
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
    step = next(s for s in context.tp_plan if s.area == area)
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


@then("the soak lasts seven days with periodic and endpoint observations")
def step_tp_release_soak_defaults(context: Context) -> None:
    """Issue #396 fixes seven days; interval sampling must include both ends."""
    steps = [s for s in context.tp_plan if s.area == "soak"]
    assert len(steps) == 1
    args = steps[0].args
    assert args["duration_s"] == 7 * 24 * 60 * 60
    assert args["interval_s"] == 60
    assert args["sample_at_start"] and args["sample_at_end"]
    assert args["continuous_evidence"] == ["asCapable_transitions", "tu_intervals",
                                           "stream_flow", "uptime"]


@then("power repeats 160 idle and 40 journal-commit cold cuts")
def step_tp_release_power_defaults(context: Context) -> None:
    """Issue #396 excludes warm resets and requires measured commit-window cuts."""
    steps = [s for s in context.tp_plan if s.area == "power"]
    assert [(s.args["phase"], s.args["cycles"]) for s in steps] == [
        ("idle", 160), ("journal_commit", 40)]
    for step in steps:
        assert step.args["cold"] and not step.args["count_resets"]
        assert step.args["total_cycles"] == 200
        assert step.args["persisted_items"] == ["stream_binding"]
        assert step.args["restore_bound_s"] == 30
        assert step.args["boot_margin_s"] == 5
        assert step.args["boot_observation_s"] == 35
        assert step.args["power_off_hold_s"] == 8
        assert step.args["restore_start"] == "T0"
        assert step.args["restore_end"] == "first valid AVTP PDU of each persisted binding"
        assert step.args["rebind_limit_s"] == 1 and step.args["rebind_limit_exclusive"]
    assert steps[0].args["snapshot_policy"] == "exact pre-cut committed snapshot"
    assert steps[1].args["snapshot_policy"] == "complete old or new committed snapshot"
    assert steps[1].args["cut_requires"] == "journal_commit_window"


@then("release assertions require complete measured evidence")
def step_tp_release_evidence(context: Context) -> None:
    """Desk coverage is never a substitute for completed physical evidence."""
    for step in context.tp_plan:
        if step.area not in ("soak", "power"):
            continue
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
    settings = tp.ReleaseSettings(125, 17, 10, 8, 2, ("stream_binding", "clock_source"),
                                  restore_bound_s=23, boot_margin_s=7, power_off_hold_s=13)
    context.tp_plan = tp.build_plan(["soak", "power"], release=settings)


@then("every release repeat preserves those parameters and its timing origins")
def step_tp_release_parameter_results(context: Context) -> None:
    """L3 #396 round 3: T0 starts the ADP window after the recorded hold."""
    soak, idle, commit = context.tp_plan
    assert (soak.args["duration_s"], soak.args["interval_s"]) == (125, 17)
    assert (idle.args["cycles"], commit.args["cycles"]) == (8, 2)
    for step in (idle, commit):
        args = step.args
        assert args["total_cycles"] == 10
        assert args["restore_bound_s"] == 23 and args["boot_margin_s"] == 7
        assert args["boot_observation_s"] == 30
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
    assert all(not step.args["release_eligible"] for step in context.tp_plan)


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
        [sys.executable, "-B", "tb/tools/torture_campaign.py", "--plan", "--areas", "soak,power",
         "--json", "--dut", specs[0], "--peer", specs[1]],
        cwd=root, capture_output=True, text=True, check=True, timeout=600)
    context.release_cli_steps = json.loads(result.stdout)


@then("every release repeat reports diagnostic topology")
def step_tp_release_partial_result(context: Context) -> None:
    """Require all three emitted repeats to reject the partial CLI shape."""
    assert len(context.release_cli_steps) == 3
    for step in context.release_cli_steps:
        assert step["args"]["topology_explicit"] is False
        assert step["args"]["release_eligible"] is False


@when("an explicit release profile uses a restoration bound of {seconds:d} seconds")
def step_tp_release_restore_bound(context: Context, seconds: int) -> None:
    """L3 #396 round 3 varies only restoration, keeping other prerequisites valid."""
    context.tp_plan = tp.build_plan(
        ["soak", "power"], release=tp.ReleaseSettings(topology_explicit=True, restore_bound_s=seconds))


@then("every release repeat is {eligibility} for release")
def step_tp_release_eligible(context: Context, eligibility: str) -> None:
    """The independent 29/30/31-second examples pin the inclusive ceiling."""
    assert len(context.tp_plan) == 3
    for step in context.tp_plan:
        assert step.args["release_eligible"] is (eligibility == "eligible")


@then("uncertainty is correlated and bounded by half a second plus observation resolution")
def step_tp_release_tu_bound(context: Context) -> None:
    """L3 #396 round 4 measures holdover from the interval's last event."""
    args = context.tp_plan[0].args
    assert args["tu_holdover_bound_s"] == 0.5
    assert args["tu_time_origin"] == "last recorded discontinuity before tu clears"
    assert args["tu_discontinuity_kinds"] == ["PHC settime/adjtime", "fabric discontinuity", "GM-identity edge"]
    assert args["tu_uncorrelated"] == "fail"
    assert args["tu_observation_resolution"] == \
        "record wire-capture and correlated event-timestamp resolution in seconds"


@then("a chained discontinuity clearing at {seconds:g} seconds is {verdict}")
def step_tp_release_tu_chain(context: Context, seconds: float, verdict: str) -> None:
    """L3 #396 round 4: GM edge at zero, followed by PHC step at 0.2 s."""
    actual, evidence = tp.check_release_tu(
        (0, seconds), [0, 0.2], holdover_bound_s=context.tp_plan[0].args["tu_holdover_bound_s"],
        observation_resolution_s=0.001, capture_complete=True)
    assert actual == verdict, evidence


@then("an uncertainty interval without a discontinuity fails")
def step_tp_release_tu_no_event(context: Context) -> None:
    """L3 #396 round 4: complete capture cannot excuse uncorrelated tu."""
    actual, evidence = tp.check_release_tu(
        (0, 0.62), [], holdover_bound_s=context.tp_plan[0].args["tu_holdover_bound_s"],
        observation_resolution_s=0.001, capture_complete=True)
    assert actual == "FAIL", evidence
