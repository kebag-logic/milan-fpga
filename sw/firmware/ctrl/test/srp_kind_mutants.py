# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Planted defects of the Listener declaration a stream's Talker Advertise and Talker Failed decide (#925).

A talker declares one of the two for a stream (IEEE 802.1Q-2018 35.2.4) and a registration of the other kind replaces
the one held (35.2.6). lwSRP withdraws the old one for a received JoinIn or JoinMt but registers a New beside it, so
while both are registered the latest decides (srp_mbx.c's listener_kind), and the other once the latest leaves. One
defect a rule: an Advertise New over a registered Failed is Ready within a JoinTime, in the registrar walk and in
the receive filter's copy (the kind a withdrawal inside one MRPDU retains, and the kind ACMP sees); a Failed New over a
registered Advertise asks Failed; the latest leaving hands the declaration to the other; coincident registrations in
one MRPDU follow their order; a binding made later takes the StreamID's latest from any binding of it, whatever that
one's destination; and one that saw neither registration takes Failed. srp_mutants.py plants each with the rest of its
table, and the named test must fail on its own words. Each name starts with "feedback-", so both interface counts'
campaigns plant it (test_ctrl_firmware.run_srp_mutants).
"""
from __future__ import annotations

from typing import Callable, TypeVar

T = TypeVar("T")

KINDS = "SrpTalkerKinds."
COMPOSED = "test_acmp_mbx.cpp"
#: listener_kind's two lines, as srp_mbx.c holds them.
LATEST = "const uint8_t kinds = (s->registered_kinds & s->latest_kind) != 0u ? s->latest_kind : s->registered_kinds;"
FAILED_FIRST = "return (kinds & 1u) != 0u ? 1u : kinds;"
#: talker_changed's record of the StreamID's latest registration.
RECORD = "s->latest_kind = registered ? kind : s->latest_kind;"


def defects(kind: Callable[..., T]) -> tuple[T, ...]:
    """Every defect of the rule, built with srp_mutants.Defect."""
    return (
        # the rule before #925: Failed first whatever registered latest
        kind("feedback-latest-failed-first", KINDS + "AnAdvertiseNewReplacesARegisteredFailedWithinAJoinTime",
             LATEST, "const uint8_t kinds = s->registered_kinds;", "an Advertise New replaces the registered Failed"),
        kind("feedback-latest-walk-failed-first", KINDS + "AnAdvertiseNewReplacesARegisteredFailedWithinAJoinTime",
             "        i->sinks[k].desired = listener_kind(&i->sinks[k]);",
             "        i->sinks[k].desired = (i->sinks[k].registered_kinds & 1u) ? 1u : i->sinks[k].registered_kinds;",
             "an Advertise New replaces the registered Failed"),
        # only an Advertise's New replaces: a Failed New over an Advertise stays Ready
        kind("feedback-latest-advertise-only", KINDS + "AFailedNewReplacesARegisteredAdvertiseWithinAJoinTime",
             RECORD, "s->latest_kind = registered && kind == 2u ? kind : s->latest_kind;",
             "a Failed New replaces the registered Advertise"),
        kind("feedback-latest-decides-unregistered", KINDS + "LeaveOfEitherKindLeavesTheOtherDeciding",
             "(s->registered_kinds & s->latest_kind) != 0u ?", "s->latest_kind != 0u ?",
             "the latest leaves: the other decides"),
        # the earliest registered decides: a New beside a registered other kind is not recorded
        kind("feedback-latest-earliest-decides", KINDS + "CoincidentRegistrationsInOneMrpduFollowTheirOrder",
             RECORD, "s->latest_kind = registered && (s->registered_kinds & (3u ^ kind)) == 0u ? kind : s->latest_kind;",
             "Failed then Advertise in one MRPDU"),
        kind("feedback-latest-not-carried", KINDS + "ABindingMadeLaterTakesTheLatestFromAnyBindingOfTheStream",
             "                replacement.latest_kind = r->latest_kind;\n", "",
             "the shared declaration stays Ready, not ReadyFailed"),
        # recorded only for a registration of the binding's own destination and VID
        kind("feedback-latest-matching-only", KINDS + "ABindingMadeLaterTakesTheLatestFromAnyBindingOfTheStream",
             RECORD, "s->latest_kind = registered && same(s->dest_mac,v->dest_mac,6) && s->vid == v->vlan_id ? kind : "
             "s->latest_kind;", "a later binding takes the latest registration"),
        kind("feedback-latest-unknown-advertise", KINDS + "ABindingThatSawNeitherRegistrationTakesFailedFirst",
             FAILED_FIRST, "return kinds == 3u ? 2u : kinds;", "neither registration seen: Failed first"),
        kind("feedback-latest-filter-failed-first", "SrpFeedback.AWithdrawalInsideOneMrpduRetainsTheLatestKind",
             "        s->desired = listener_kind(s);",
             "        s->desired = (s->registered_kinds & 1u) ? 1u : s->registered_kinds;",
             "the latest kind precedes the withdrawal", suite=COMPOSED),
        kind("feedback-latest-acmp-failed-first",
             "SrpFeedback.AdvertiseNewOverARegisteredFailedUpdatesTheSettledWireView",
             LATEST, "const uint8_t kinds = s->registered_kinds;", "current kind reaches ACMP", suite=COMPOSED),
    )
