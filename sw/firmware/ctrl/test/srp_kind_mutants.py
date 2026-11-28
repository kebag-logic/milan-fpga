# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Planted defects of the Listener declaration a stream's Talker Advertise and Talker Failed decide (#925).

A talker declares one of the two for a stream and moves directly between them (IEEE 802.1Q-2018 35.1.2.1). A received
JoinIn or JoinMt of one replaces a registered other (35.2.6), but lwSRP registers a New beside it. 35.2.6's informative
NOTE would give the Failed precedence; Milan v1.2 5.3.8.5 and the ruling on #925 have the latest decide while both are
registered (srp_mbx.c's listener_kind), and the other once the latest leaves. One defect a rule: an Advertise New over
a registered Failed is Ready within a JoinTime, in the registrar walk and in the receive filter's copy (the kind a
withdrawal inside one MRPDU retains, and the kind ACMP sees); a Failed New over a registered Advertise asks Failed; each
New in turn decides, also one beside the other kind; the latest leaving hands the declaration to the other; coincident
registrations in one MRPDU follow their order; a declaration the filter's copy changes is owed whatever follows it in
the MRPDU, on the wire and in ACMP's view; a binding made later takes the StreamID's latest from any binding of it,
whatever that one's destination, and one replaced in place keeps it; and a StreamID none binds holds its latest while
both stay registered, for its next binding and no other StreamID's, until either leaves or the interface resets, and
for its own interface only; past the table's bound, both registered with no latest known take Failed.
srp_mutants.py plants each with the rest of its table, and the named test must fail on its own words. A name that
starts with "feedback-" is planted in both interface counts' campaigns (test_ctrl_firmware.run_srp_mutants); the two
"held-latest-" defects of another interface, in the two-interface one.
"""
from __future__ import annotations

from typing import Callable, TypeVar

T = TypeVar("T")

KINDS = "SrpTalkerKinds."
COMPOSED = "test_acmp_mbx.cpp"
#: listener_kind's rule, as srp_mbx.c holds it.
LATEST = "const uint8_t kinds = (s->registered_kinds & s->latest_kind) != 0u ? s->latest_kind : s->registered_kinds;"
#: talker_changed's record of the StreamID's latest registration.
RECORD = "s->latest_kind = registered ? kind : s->latest_kind;"
#: the receive filter's hold of a declaration its copy changed.
FILTER_HOLDS = "        if (s->desired != previous) {\n            hold(i);\n        }\n"
#: srp_mbx_bind's hold of a StreamID its last binding leaves with both kinds registered.
STORE = "            if (old.stream_kinds == 3u && m->held_count < SRP_HELD_STREAMS) {"
HELD = KINDS + "AFinalUnbindingKeepsTheLatestWhileBothStayRegistered"
ENDS = KINDS + "AHeldStreamEndsWithEitherRegistrationOrAReset"
#: held_scan's match of an interface's StreamID, the last byte first (#977), and the test of a StreamID whose last
#: octet a held one's shares.
OWN_STREAM = "held[7] == stream_id[7] && m->held[n].interface == interface && same(held,stream_id,8)"
TWIN = "SrpEarlyTalker.ABindingOfAStreamIDOfAHeldOnesLastOctetTakesNoneOfIt"


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
             RECORD, "s->latest_kind = registered && (s->registered_kinds & (3u ^ kind)) == 0u ? kind : "
             "s->latest_kind;",
             "Failed then Advertise in one MRPDU"),
        kind("feedback-latest-not-carried", KINDS + "ABindingMadeLaterTakesTheLatestFromAnyBindingOfTheStream",
             "                replacement.latest_kind = r->latest_kind;\n", "",
             "the shared declaration stays Ready, not ReadyFailed"),
        # recorded only for a registration of the binding's own destination and VID
        kind("feedback-latest-matching-only", KINDS + "ABindingMadeLaterTakesTheLatestFromAnyBindingOfTheStream",
             RECORD, "s->latest_kind = registered && same(s->dest_mac,v->dest_mac,6) && s->vid == v->vlan_id ? kind : "
             "s->latest_kind;", "a later binding takes the latest registration"),
        # a New of a kind the binding holds beside the other is not recorded: the first conflict alone decides
        kind("feedback-latest-renew-not-recorded", KINDS + "EachNewInTurnDecidesWhileBothAreRegistered",
             RECORD, "s->latest_kind = registered && (held & kind) == 0u ? kind : s->latest_kind;",
             "a Failed New beside the Advertise decides again",
             also=(("s->registered_kinds &= (uint8_t)~kind;",
                    "const uint8_t held = s->registered_kinds; s->registered_kinds &= (uint8_t)~kind;"),)),
        # both registered with no latest known withdraws, past the held table's bound
        kind("feedback-latest-unknown-withdraws", KINDS + "AFullHeldTableHoldsNothingMore",
             "return (kinds & 1u) != 0u ? 1u : kinds;", "return kinds == 3u ? 0u : kinds;", "no latest known: Failed"),
        # a binding replaced in place does not carry its own latest
        kind("feedback-latest-not-carried-in-place", KINDS + "ABindingMadeLaterTakesTheLatestFromAnyBindingOfTheStream",
             "                replacement.latest_kind = r->latest_kind;\n",
             "                replacement.latest_kind = k == sink ? replacement.latest_kind : r->latest_kind;\n",
             "one in place too"),
        # the walk alone owes a changed declaration: one the filter's copy changed waits for unrelated work
        kind("feedback-latest-filter-holds-nothing",
             KINDS + "AReplacementBeforeAMessageThatChangesNothingIsDeclaredWithinAJoinTime", FILTER_HOLDS, "",
             "a New before a message that changes nothing"),
        kind("feedback-latest-filter-holds-nothing-acmp",
             "SrpFeedback.AnAdvertiseNewBeforeAnUnchangedDomainUpdatesBothWireViews", FILTER_HOLDS, "",
             "Listener Ready on the wire within a JoinTime", suite=COMPOSED),
        # the order kept per binding, the exception before the StreamID held it
        kind("feedback-latest-not-held", HELD, STORE, "            if (false) {",
             "a final unbinding keeps the latest registration"),
        kind("feedback-latest-held-not-taken", HELD, "            replacement.latest_kind = h->latest_kind;\n", "",
             "a final unbinding keeps the latest registration"),
        # the talker's MAC alone compared: another StreamID of the same talker takes it; the table is scanned only for
        # a StreamID ending in an octet one held ends in (#977, held_octets), so the test's is the same talker's twin
        kind("feedback-latest-held-for-another-stream", TWIN, OWN_STREAM,
             "m->held[n].interface == interface && same(held,stream_id,6)",
             "stream 0 keeps its latest Advertise past its twin's binding"),
        kind("feedback-latest-held-with-one-kind", ENDS, "old.stream_kinds == 3u &&", "old.stream_kinds != 0u &&",
             "one kind registered holds nothing"),
        kind("feedback-latest-held-past-a-leave", ENDS,
             "    } else if (h != NULL) {\n        release_held(m,h);\n    }\n", "    }\n",
             "a registration's end or a reset ends the hold"),
        kind("feedback-latest-held-past-a-reset", ENDS, "        if (m->held[n].interface == i->index) {",
             "        if (false) {", "a registration's end or a reset ends the hold"),
        # held whatever the interface, at two interfaces (no "feedback-" name: the two-interface campaign alone)
        kind("held-latest-any-interface", KINDS + "AStreamIsHeldForItsOwnInterface",
             "m->held[n].interface == interface && same",
             "(m->held[n].interface == interface || MBX_N_IF > 1u) && same",
             "another interface's binding takes none of it"),
        kind("held-latest-reset-any-interface", KINDS + "AStreamIsHeldForItsOwnInterface",
             "        if (m->held[n].interface == i->index) {", "        if (true) {",
             "another interface's reset leaves it"),
        kind("feedback-latest-stream-kinds-kept", "HeldRegistrationsAreWhatAWalkCopiesAfterEveryStep",
             "        i->sinks[k].stream_kinds = 0;\n    }\n", "    }\n", "holds what a walk copies"),
        # the receive filter recomputes the sinks only from a Talker's indication in the MRPDU on (#665's ruling of
        # 2026-11-20, item 3), so this copy is held by the cut's differential: its reference recomputes every sink at
        # every filter call, as the adapter before the cut did, which a copy other than listener_kind's makes differ
        kind("feedback-latest-filter-failed-first", "Listeners.RandomRecordsMatchTheReferenceReclaim",
             "        s->desired = listener_kind(s);",
             "        s->desired = (s->registered_kinds & 1u) ? 1u : s->registered_kinds;",
             "the copied run makes the reference run's mailbox writes and licence calls, in order, and holds its state",
             suite="srp_listeners.cpp"),
        kind("feedback-latest-acmp-failed-first",
             "SrpFeedback.AdvertiseNewOverARegisteredFailedUpdatesTheSettledWireView",
             LATEST, "const uint8_t kinds = s->registered_kinds;", "current kind reaches ACMP", suite=COMPOSED),
    )
