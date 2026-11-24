# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Planted defects of the Talker registrations SRP keeps for StreamIDs no binding holds (#969).

ACMP initiates the SRP reservation only once the talker answers its probe (Milan v1.2 5.5.3.5.18 step 4), and a
talker declares once and then stays quiet until a LeaveAll (IEEE 802.1Q-2018 Table 10-3). So the receive filter keeps
a Talker of a StreamID no binding holds (srp_mbx.c keep_talker), at most one for each STREAM_INPUT of the shape, and a
binding made later takes its registration in the walk it owes and declares within one transmit (Milan v1.2 5.3.8.5).
One defect a rule, for each order: registration then binding (the filter ignores it, the shipped firmware's state,
also on a bind while bound); binding then registration with the kept attributes at their bound (the binding's own
Talker found for its first sink only); the bound itself (none, or a New of the other kind of a kept StreamID, which
registers beside it, taken as kept); the count made before a receive (it forgets the registered, or adds to the count
before it), an unbinding's registration counted against the bound (no count owed by the binding), and a kept attribute
that left, counted until mrp_reclaim frees its block (the count skips it) and uncounted once freed (no count owed by
the block's return); what makes that count exact below the bound as at it (a reset's count not zeroed with
the old count, a kept registration's end or a kept attribute with no registration owing no count, a left one the
count saw leaving none owed, a refresh counted again); and the latest kind of two registered before the binding
(#925), held for a StreamID no binding has.
srp_mutants.py plants each with the rest of its table, and the named test must fail on its own words. Every name
starts with PREFIX, so both interface counts' campaigns and the 8x8/1if one plant it
(test_ctrl_firmware.run_srp_mutants).
"""
from __future__ import annotations

from typing import Callable, TypeVar

T = TypeVar("T")

PREFIX = "feedback-early-"

EARLY = "SrpEarlyTalker."
BEFORE = EARLY + "ARegistrationMadeBeforeItsBindingIsDeclaredWithinOneTransmitOnEveryInput"
REBIND = EARLY + "ARebindWhileBoundToAStreamDeclaredAllAlongIsDeclaredWithinOneTransmit"
AFTER = EARLY + "ABindingMadeBeforeItsRegistrationIsDeclaredWithinAJoinTimeOnEveryInput"
BOUNDED = EARLY + "RegistrationsKeptBeforeABindingAreBoundedByTheInputs"
LEFT = EARLY + "AKeptRegistrationThatLeftHoldsItsPlaceUntilItsBlockIsFreed"
LATEST = EARLY + "ABindingTakesTheLatestOfTwoKindsRegisteredBeforeIt"
UNBOUND = EARLY + "AnUnboundRegistrationIsKeptAndCountedAgainstTheBound"
RESET_TEST = EARLY + "AResetLeavesNoKeptRegistrationCounted"
FREED = EARLY + "AKeptRegistrationWhoseBlockIsFreedIsCountedNoMore"
NEVER = EARLY + "AKeptLeaveOfAStreamNeverRegisteredIsCountedNoMoreOnceFreed"
REFRESHED = EARLY + "AKeptRegistrationRefreshedIsCountedOnce"
#: srp_mbx.c's receive filter for a Talker no binding holds, and its search of the bindings, as it holds them.
KEEPS = "    return keep_talker(i,type,value);\n"
SEARCH = ("        for (unsigned n = i->lane_first[id[7] % SRP_SINK_LANES]; n != 0u; n = i->lane_next[n - 1u]) {\n"
          "            if (i->sinks[n - 1u].stream_id.bytes[7] == id[7] && "
          "same(i->sinks[n - 1u].stream_id.bytes,id,8)) {\n")
#: keep_talker's bound, its search of the kept list, its listing of one kept now and the count it leaves pending.
FULL = "    if (*count >= SRP_KEPT_TALKERS) {\n        return false;\n    }\n"
KIND = ("        if (kept[n].kind == kind && kept[n].stream_id.bytes[7] == stream_id[7] &&\n"
        "            same(kept[n].stream_id.bytes,stream_id,8)) {\n")
LISTS = "    memcpy(kept[*count].stream_id.bytes,stream_id,8);\n    kept[(*count)++].kind = kind;\n"
KEPT_PENDING = "    kept[(*count)++].kind = kind;\n    m->kept_due[i->index] |= SRP_KEPT_PENDING;\n"
#: count_kept's count before a receive: when it is owed (a binding changed, or a block returned while one may have
#: ended), its start, and the attributes it counts (a Talker no binding holds, the participant not declaring it, any
#: Registrar), one left among them leaving it pending.
OWED_BINDING = "    m->kept_due[interface] |= SRP_KEPT_BOUND;\n"
RETURNED = "((due & SRP_KEPT_PENDING) != 0u && m->kept_returned[n] != ctrl_pool_returned)"
RECOUNT = "        m->kept_count[n] = 0u;\n"
COUNTED = "        (SRP_UNDECLARED_APPL >> status->appl & 1u) != 0u && !bound_stream(i,id)) {\n"
VISIT_PENDING = ("        if (status->reg == MRP_REG_STATE_MT) {\n"
                 "            m->kept_due[i->index] |= SRP_KEPT_PENDING;\n        }\n")
#: talker_changed's pending count at the end of a registration no binding has, and reset_interface's zeroed count.
LEFT_PENDING = "    if (!bound && !registered) {\n        m->kept_due[i->index] |= SRP_KEPT_PENDING;\n    }\n"
RESET = "    m->kept_count[i->index] = 0u;\n"
#: talker_changed's hold of a StreamID no binding has, from a registration it was kept for.
HOLDS = "    if (registered && !bound && h == NULL && m->held_count < SRP_HELD_STREAMS) {\n"


def defects(kind: Callable[..., T]) -> tuple[T, ...]:
    """Every defect of the rule, built with srp_mutants.Defect."""
    return (
        # registration then binding: the filter before #969 ignores a Talker no binding holds
        kind("feedback-early-talker-ignored", BEFORE, KEEPS, KEEPS.replace("return ", "return false && "),
             "an Advertise registered before its binding"),
        kind("feedback-early-rebind-ignored", REBIND, KEEPS, KEEPS.replace("return ", "return false && "),
             "a rebind to a stream declared all along"),
        # binding then registration, the kept attributes at their bound: the binding's own Talker, first sink only
        kind("feedback-early-bound-first-sink-only", AFTER, SEARCH, SEARCH.replace("n != 0u;", "n == 1u;"),
             "a binding made before its registration"),
        # the bound
        kind("feedback-early-unbounded", BOUNDED, FULL, "", "a registration past the bound takes no block"),
        kind("feedback-early-any-kind-kept", BOUNDED, KIND, KIND.replace("kept[n].kind == kind && ", ""),
             "the other kind of a kept StreamID, past the bound"),
        # what the count before a receive counts, and when it is made
        kind("feedback-early-count-forgets", BOUNDED, COUNTED,
             COUNTED.replace("(SRP_UNDECLARED_APPL", "status->reg == MRP_REG_STATE_MT && (SRP_UNDECLARED_APPL"),
             "counted again, they are still kept"),
        kind("feedback-early-count-adds", LEFT, RECOUNT, "", "once its block is freed, another is kept"),
        kind("feedback-early-left-uncounted", LEFT, COUNTED,
             COUNTED.replace("(SRP_UNDECLARED_APPL", "status->reg != MRP_REG_STATE_MT && (SRP_UNDECLARED_APPL"),
             "a kept registration that left is counted until its block is freed"),
        kind("feedback-early-freed-uncounted", LEFT, RETURNED, "false",
             "once its block is freed, another is kept"),
        kind("feedback-early-unbinding-uncounted", UNBOUND, OWED_BINDING, "",
             "an unbound registration is kept and counted"),
        # what makes the count exact below the bound: a reset, a registration's end, one never registered, a left
        # one the count saw, a refresh
        kind("feedback-early-reset-counted", RESET_TEST, RESET, "",
             "after a reset, one vector of every input is kept whole"),
        kind("feedback-early-end-unowed", FREED, LEFT_PENDING, "",
             "a kept one freed below the bound: one vector of every input is kept"),
        kind("feedback-early-unregistered-unowed", NEVER, KEPT_PENDING, "    kept[(*count)++].kind = kind;\n",
             "a Leave kept for a StreamID never registered"),
        kind("feedback-early-left-seen-unowed", LEFT, VISIT_PENDING, "", "once its block is freed, another is kept"),
        kind("feedback-early-refresh-counted-again", REFRESHED, LISTS, "    ++*count;\n",
             "a kept registration refreshed in one receive"),
        # the latest of two kinds registered before the binding: nothing held, so Failed whatever came latest
        kind("feedback-early-latest-unheld", LATEST, HOLDS, HOLDS.replace("if (registered &&", "if (false &&"),
             "the latest of two kinds registered before the binding"),
    )
