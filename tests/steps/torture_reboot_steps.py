# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Issue #787: the #396 power area's soft resets as AECP REBOOTs, and their two oracles."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING

from behave import then, when

if TYPE_CHECKING:
    from behave.runner import Context

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tb" / "tools"))
import torture_campaign as tp  # noqa: E402

#: Issue #787: the assertions only the soft resets owe, beside RELEASE_REQUIRED.
SOFT_RESET_REQUIRED = {"power.reboot-reset", "power.gptp-relock"}


@then("the soft resets send an AECP REBOOT of ENTITY 0 and require SUCCESS")
def step_tp_release_reboot_method(context: Context) -> None:
    """IEEE 1722.1-2021 7.4.43: the reset command, its answer and its bound."""
    reset = next(s for s in _release_repeats(context.tp_plan) if s.sid == "power.soft_reset")
    assert reset.args["reset_command"] == {"message_type": "AEM_COMMAND", "command_type": "REBOOT",
                                           "descriptor_type": "ENTITY", "descriptor_index": 0}
    assert reset.args["reset_response_required"] == "SUCCESS"
    assert reset.args["reset_link_down_s"] == 11
    assert reset.args["reset_oracle"] == "check_release_reboot"
    assert reset.args["gptp_relock_oracle"] == "check_release_gptp_relock"
    assert "reboot_exchange" in reset.args["evidence"]


@then("the soft resets owe the REBOOT exchange and the gPTP relock, and the cold cuts do not")
def step_tp_release_reboot_asserts(context: Context) -> None:
    """The two checks sit on the soft-reset repeat alone, at SHALL."""
    for step in _release_repeats(context.tp_plan):
        shall = {a.name for a in step.asserts if a.severity == "SHALL"}
        if step.sid == "power.soft_reset":
            assert SOFT_RESET_REQUIRED <= shall, SOFT_RESET_REQUIRED - shall
        else:
            assert not SOFT_RESET_REQUIRED & {a.name for a in step.asserts}, step.sid


#: defect: the change to one complete, passing REBOOT exchange.
_REBOOT_CASES = {
    "nothing": {},
    "a status other than SUCCESS": {"status": 11},
    "no ENTITY_DEPARTING": {"departing_s": None},
    "a link still up after 11 s": {"link_down_s": 111.5},
    "an incomplete capture": {"capture_complete": False},
}


@when("a soft reset's REBOOT exchange shows {defect}")
def step_tp_release_reboot_case(context: Context, defect: str) -> None:
    """One exchange on the T0 clock, T0 = 100 s, through the plan's own oracle."""
    exchange = {"t0_s": 100.0, "response_s": 100.01, "status": 0, "departing_s": 100.02,
                "link_down_s": 103.6, "capture_complete": True}
    exchange.update(_REBOOT_CASES[defect])
    reset = next(s for s in tp.build_plan(["power"]) if s.sid == "power.soft_reset")
    oracle = getattr(tp, reset.args["reset_oracle"])
    context.release_reboot_result = oracle(exchange, reset.args["reset_link_down_s"])


@then("the REBOOT oracle grades it {verdict}")
def step_tp_release_reboot_verdict(context: Context, verdict: str) -> None:
    """The verdict issue #787 owes the case."""
    actual, detail = context.release_reboot_result
    assert actual == verdict, detail


#: defect: (pre-reset change, post-reset change) to one passing pair of readings.
_RELOCK_CASES = {
    "nothing": ({}, {}),
    "no asCapable by the deadline": ({}, {"as_capable": False}),
    "the peer's link delay moved 50 ns": ({}, {"peer_delay_ns": 660}),
    "the DUT's link delay moved 50 ns": ({}, {"dut_delay_ns": 550}),
    "an unlocked pre-reset reading": ({"as_capable": False}, {}),
}


@when("a soft reset's gPTP readings show {defect}")
def step_tp_release_relock_case(context: Context, defect: str) -> None:
    """Readings before the REBOOT and 25 s after T0, through the plan's own oracle."""
    pre_change, post_change = _RELOCK_CASES[defect]
    pre = dict({"as_capable": True, "dut_delay_ns": 600, "peer_delay_ns": 610}, **pre_change)
    post = dict({"as_capable": True, "dut_delay_ns": 605, "peer_delay_ns": 612,
                 "elapsed_s": 25.0}, **post_change)
    reset = next(s for s in tp.build_plan(["power"]) if s.sid == "power.soft_reset")
    oracle = getattr(tp, reset.args["gptp_relock_oracle"])
    context.release_relock_result = oracle(pre, post, deadline_s=reset.args["boot_observation_s"],
                                           tolerance_ns=reset.args["gptp_delay_tolerance_ns"])


@then("the gPTP relock oracle grades it {verdict}")
def step_tp_release_relock_verdict(context: Context, verdict: str) -> None:
    """The verdict issue #787 owes the case."""
    actual, detail = context.release_relock_result
    assert actual == verdict, detail


def _release_repeats(plan: list) -> list:
    """The planner's own release repeat operations."""
    return [s for s in plan if s.op in tp.RELEASE_REQUIRED_ASSERTS]
