# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Planted defects of the SRP cut (#665's ruling of 2026-11-20, item 3): lwSRP's reclaim owed only where an attribute
may be freed, the receive filter's pass over the sinks made only from a Talker's indication on, a Listener's StreamID
matched against a source's only where their last bytes agree, and the walk-free snapshot's capture made in place.

srp_mutants.py plants each into a copy of sw/firmware/ctrl with the rest of its table, and the named test must fail
on its own words: srp_listeners.cpp's reclaim tests, srp_mbx.cpp's comparison test and srp_feedback.hpp's withdrawal
tests (test_acmp_mbx.cpp). The one-interface campaigns plant them at 1x1/1if and at 8x8/1if
(ENTITY; test_ctrl_firmware.run_srp_mutants), the two-interface campaign at 8x8/2if.
"""
from __future__ import annotations

from typing import Callable, TypeVar

T = TypeVar("T")

SUITE = "srp_listeners.cpp"
#: The entity of the one-interface campaign at 8x8/1if and of the two-interface campaign.
ENTITY = "endstation_ax7101_8x8"
#: The name every defect here starts with, which the one-interface campaigns select them by.
PREFIX = "srp-cut-"
STEADY = ("Listeners.SteadyListenerRecordsAndBuildsWalkNoAttributes",
          "a registered Listener's JoinIn and THE TRANSMIT's builds walk no attributes")
CREATED = ("Listeners.AListenerLeftAsCreatedIsReclaimed",
           "an attribute a receive created and left as created is reclaimed")
BESIDE = ("Listeners.AListenerLeftAsCreatedBesideAnotherChangeIsReclaimed",
          "an attribute a receive created and left as created beside another change is reclaimed")
LEAVING = ("Listeners.ALeavingListenerIsReclaimed", "an attribute changed into a state mrp_reclaim frees is reclaimed")
#: srp_feedback.hpp's (test_acmp_mbx.cpp): a Talker's Lv then its New in one PDU is two events, the withdrawal retained.
TWO_EVENTS = ("SrpFeedback.SinglePduWithdrawalThenRegistrationRetainsTheFirstEvent", "retained withdrawal reprobes")
#: srp_feedback.hpp's: a kind registered after a withdrawal is not delivered before it.
RETAINED = ("SrpFeedback.LaterKindAfterWithdrawalIsNotReported", "retained pre-withdrawal kind")
#: srp_mbx.c's sites, as it holds them.
FREEABLE = "    if (t->reg_to == MRP_REG_STATE_MT && (SRP_FREED_APPL >> t->appl_to & 1u) != 0u) {\n"
FREED = "#define SRP_FREED_APPL ((1u << MRP_APPL_STATE_VO) | (1u << MRP_APPL_STATE_AO) | (1u << MRP_APPL_STATE_QO))\n"
FRESH = "    if (t->appl_from == MRP_APPL_STATE_VO && t->reg_from == MRP_REG_STATE_MT) {\n"
CREATION = "    if (room > attribute_room(pool) + i->fresh) {\n"
SINKS = "    const unsigned sinks = i->stale ? CTRL_SRP_SINKS : 0u;\n"
SAME_ID = "        if (s[7] == id[7] && same(s,id,8)) {\n"
COPY = "            if (!i->sinks[k].withdrawn && i->sinks[k].desired) {\n"


def defects(kind: Callable[..., T]) -> tuple[T, ...]:
    """Every defect of the cut, built with srp_mutants.Defect, in srp_mbx.c's order."""
    def d(name: str, test: tuple[str, str], old: str, new: str, suite: str = SUITE) -> T:
        """One defect, named with PREFIX, which its test must fail on its words."""
        return kind(PREFIX + name, test[0], old, new, test[1], suite=suite, entity=ENTITY)
    return (
        # the match taken from the last byte alone: a StreamID that differs from a source's elsewhere is the source's
        d("same-id-last-byte-only", ("Srp.AListenerIsASourcesOnlyForItsStreamIDByteForByte",
                                     "differs from source 0's in byte 0 alone"),
          SAME_ID, "        if (s[7] == id[7]) {\n", suite="srp_mbx.cpp"),
        # the filter's pass never made: a Talker's change earlier in the MRPDU is not closed before the next value
        d("filter-pass-dropped", TWO_EVENTS, SINKS, "    const unsigned sinks = 0u;\n", suite="test_acmp_mbx.cpp"),
        # the pass made only while the interface is not stale: the changes it closes are those it skips
        d("filter-pass-inverted", TWO_EVENTS, SINKS, SINKS.replace("CTRL_SRP_SINKS : 0u", "0u : CTRL_SRP_SINKS"),
          suite="test_acmp_mbx.cpp"),
        # every change owes the reclaim, as before the cut
        d("reclaim-every-change", STEADY, FREEABLE, "    if (true) {\n"),
        # an Applicant's change owes it whatever its Registrar
        d("reclaim-any-registrar", STEADY, FREEABLE, FREEABLE.replace("t->reg_to == MRP_REG_STATE_MT && ", "")),
        # a change into VO and MT read as one that frees nothing
        d("reclaim-very-anxious-kept", LEAVING, FREED, FREED.replace("(1u << MRP_APPL_STATE_VO) | ", "")),
        # every change counted as one out of creation, so a created attribute left as created goes uncounted
        d("reclaim-every-change-fresh", BESIDE, FRESH, "    if (true) {\n"),
        # the receive's own count short by one: one attribute it created and left as created is not reclaimed
        d("reclaim-creation-unowed", CREATED, CREATION,
          CREATION.replace("> attribute_room(pool) + i->fresh", "> attribute_room(pool) + i->fresh + 1u")),
        # every receive owes the reclaim, as before the cut
        d("reclaim-every-receive", STEADY, CREATION,
          CREATION.replace("room > attribute_room(pool) + i->fresh", "room >= attribute_room(pool)")),
        # the walk-free snapshot's copy of a continuing kind made over a withdrawal not yet delivered
        d("snapshot-copy-over-withdrawal", RETAINED, COPY, COPY.replace("!i->sinks[k].withdrawn && ", ""),
          suite="test_acmp_mbx.cpp"),
    )
