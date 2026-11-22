# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Planted defects of the Talker registrations SRP keeps for StreamIDs no binding holds (#969).

ACMP initiates the SRP reservation only once the talker answers its probe (Milan v1.2 5.5.3.5.18 step 4), and a
talker declares once and then stays quiet until a LeaveAll (IEEE 802.1Q-2018 Table 10-3). So the receive filter keeps
a Talker of a StreamID no binding holds (srp_mbx.c keep_talker), at most one for each STREAM_INPUT of the shape, and a
binding made later takes its registration in the walk it owes and declares within one transmit (Milan v1.2 5.3.8.5).
One defect a rule, for each order: registration then binding (the filter ignores it, the shipped firmware's state,
also on a bind while bound); binding then registration with the kept attributes at their bound (the binding's own
Talker found for its first sink only); the bound itself (none, or a New of the other kind of a kept StreamID, which registers beside it, taken as kept);
the count a walk makes (it forgets them, or adds to the count before it); a kept attribute that left, counted until
mrp_reclaim frees its block (the walk skips it) and uncounted once freed (no walk owed for the block's return); and
the latest kind of two registered before the binding (#925), held for a StreamID no binding has.
srp_mutants.py plants each with the rest of its table, and the named test must fail on its own words. Every name
starts with "feedback-", so both interface counts' campaigns plant it (test_ctrl_firmware.run_srp_mutants).
"""
from __future__ import annotations

from typing import Callable, TypeVar

T = TypeVar("T")

EARLY = "SrpEarlyTalker."
BEFORE = EARLY + "ARegistrationMadeBeforeItsBindingIsDeclaredWithinOneTransmitOnEveryInput"
REBIND = EARLY + "ARebindWhileBoundToAStreamDeclaredAllAlongIsDeclaredWithinOneTransmit"
AFTER = EARLY + "ABindingMadeBeforeItsRegistrationIsDeclaredWithinAJoinTimeOnEveryInput"
BOUNDED = EARLY + "RegistrationsKeptBeforeABindingAreBoundedByTheInputs"
LEFT = EARLY + "AKeptRegistrationThatLeftHoldsItsPlaceUntilItsBlockIsFreed"
LATEST = EARLY + "ABindingTakesTheLatestOfTwoKindsRegisteredBeforeIt"
#: srp_mbx.c's receive filter for a Talker no binding holds, and its search of the bindings, as it holds them.
KEEPS = "    return (type == MSRP_ATTR_TYPE_TALKER_ADV || type == MSRP_ATTR_TYPE_TALKER_FAILED) && keep_talker(i,type,value);\n"
SEARCH = ("        for (unsigned n = 0; n < CTRL_SRP_SINKS; ++n) {\n"
          "            if (i->sinks[n].bound && same(i->sinks[n].stream_id.bytes,value,8)) {\n")
#: keep_talker's bound and its search of the kept list.
FULL = "    if (i->kept_count >= SRP_KEPT_TALKERS) {\n        return false;\n    }\n"
KIND = "        if (kept[n].kind == kind && same(kept[n].stream_id.bytes,stream_id,8)) {\n"
#: the walk's count: its start, a registered Talker no binding holds, and one that left whose block is not yet freed.
RECOUNT = "    i->kept_count = 0u;\n"
WALKED = "        if (!bound) {\n            kept_walked(i,status->attr_type,v->stream_id.bytes);\n        }\n"
UNFREED = "        if (talker && (SRP_UNDECLARED_APPL >> status->appl & 1u) != 0u &&\n"
#: the walk a block's return owes while the interface keeps one.
RETURNED = "        i->stale = i->stale || (i->kept_count != 0u && ctrl_pool_returned != returned);\n"
#: talker_changed's hold of a StreamID no binding has, from a registration it was kept for.
HOLDS = "    if (registered && !bound && h == NULL && m->held_count < SRP_HELD_STREAMS) {\n"


def defects(kind: Callable[..., T]) -> tuple[T, ...]:
    """Every defect of the rule, built with srp_mutants.Defect."""
    return (
        # registration then binding: the filter before #969 ignores a Talker no binding holds
        kind("feedback-early-talker-ignored", BEFORE, KEEPS, KEEPS.replace("return (", "return false && ("),
             "an Advertise registered before its binding"),
        kind("feedback-early-rebind-ignored", REBIND, KEEPS, KEEPS.replace("return (", "return false && ("),
             "a rebind to a stream declared all along"),
        # binding then registration, the kept attributes at their bound: the binding's own Talker, first sink only
        kind("feedback-early-bound-first-sink-only", AFTER, SEARCH, SEARCH.replace("n < CTRL_SRP_SINKS", "n < 1u"),
             "a binding made before its registration"),
        # the bound
        kind("feedback-early-unbounded", BOUNDED, FULL, "", "a registration past the bound takes no block"),
        kind("feedback-early-any-kind-kept", BOUNDED, KIND, KIND.replace("kept[n].kind == kind && ", ""),
             "the other kind of a kept StreamID, past the bound"),
        # what a walk counts
        kind("feedback-early-walk-forgets", BOUNDED, WALKED, "        (void)bound;\n", "a walk keeps counting them"),
        kind("feedback-early-walk-adds", LEFT, RECOUNT, "", "once its block is freed, another is kept"),
        kind("feedback-early-left-uncounted", LEFT, UNFREED, "        if (false &&\n",
             "a kept registration that left is counted until its block is freed"),
        kind("feedback-early-freed-unwalked", LEFT, RETURNED, "        (void)returned;\n",
             "once its block is freed, another is kept"),
        # the latest of two kinds registered before the binding: nothing held, so Failed whatever came latest
        kind("feedback-early-latest-unheld", LATEST, HOLDS, HOLDS.replace("if (registered &&", "if (false &&"),
             "the latest of two kinds registered before the binding"),
    )
