# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""L3 release-plan coverage against issue #396's recorded decisions."""

from __future__ import annotations

import sys
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
        assert step.args["boot_observation_s"] >= 480
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
