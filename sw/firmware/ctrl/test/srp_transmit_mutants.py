# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Planted defects of the SRP adapter's side of THE TRANSMIT (#665, ctrl_loop.h): the MRPDU build, and the
declarations it sends, out of the poll and into a pass given whole; what owes that pass, a join count's end, a LeaveAll
with no join timer running, a declaration or an Applicant moved with its own join timer idle, each reported owed; the
count, restarted by what a build sent; a frame owed ahead of a build; both of an interface's MRPDUs a pass.

srp_mutants.py plants them with the rest of its table: each must fail its named observable, never only a build.
"""
from __future__ import annotations

from typing import Callable, TypeVar

T = TypeVar("T")

WAITS = "AnOwedMrpduTakesAPassOfItsOwn"
COUNT = "TheJoinCountFollowsWhatABuildSent"
OWED = "AnOwedFrameComesBeforeTheBuild"
RETAINED = "SrpRetry.OversizedValidRecordExpiresOnceAndReleasesOtherInterfaceAndBinding"
#: The poll's end: an owed build reported owed.
POLL_END = "    owed = owed || m->tx_due != 0u;\n    m->busy = false;\n    return owed;\n}\n"
#: The centisecond's end of a join count, and a LeaveAll's.
ENDS = "if (m->join_left[slot] != 0u ? --m->join_left[slot] == 0u : la == MRP_LA_STATE_ACTIVE) {"
#: An interface's declarations, which wait for a retained receive and are tried again at the JoinTime.
DECLARE = ("        if (i->msrp && (m->pending_rx.len != 0u || prepare_declarations(i)) && "
           "m->join_left[2u * n] == 0u) {\n            m->join_left[2u * n] = SRP_JOIN_CS;\n        }\n")
#: A build's result, which restarts the count of the participant that sent.
SENT = "    if (result > 0) {\n        m->join_left[slot] = SRP_JOIN_CS;\n    }\n"


def defects(kind: Callable[..., T]) -> tuple[T, ...]:
    """Every defect of the adapter's side of THE TRANSMIT, built with srp_mutants.Defect."""
    return (
        kind("transmit-built-by-the-poll", WAITS, POLL_END,
             "    m->busy = false;\n    transmit(m);\n    return owed || m->tx_due != 0u;\n}\n",
             "and no poll builds it"),
        kind("transmit-due-unreported", WAITS, "    owed = owed || m->tx_due != 0u;\n", "",
             "an owed MRPDU is reported owed"),
        kind("transmit-join-end-owes-nothing", WAITS, ENDS,
             "if (m->join_left[slot] != 0u ? --m->join_left[slot] == 0xffu : la == MRP_LA_STATE_ACTIVE) {",
             "the centisecond that ends a join timer owes its interface's MRPDUs"),
        kind("transmit-leaveall-owes-nothing", COUNT, ENDS,
             "if (m->join_left[slot] != 0u ? --m->join_left[slot] == 0u : false) {",
             "a LeaveAll timer's end owes its LeaveAll"),
        kind("transmit-every-centisecond-owes", WAITS, ENDS, "if (m->join_left[slot] != 0u ? true : true) {",
             "no centisecond before a join timer's end owes one"),
        kind("transmit-unbinding-holds-nothing", WAITS,
             "            if (old.declared != 0u) {\n                hold(i);\n            }\n", "",
             "an unbinding that withdraws a declaration owes the MRPDU that sends it"),
        kind("transmit-binding-holds-a-build", WAITS,
             "    i->stale = true; // snapshot matches registrations against the bindings (#665)\n",
             "    i->stale = true; // snapshot matches registrations against the bindings (#665)\n    hold(i);\n",
             "a binding owes no MRPDU itself"),
        kind("transmit-walk-holds-nothing", WAITS,
             "        if (i->sinks[k].desired != previous[k]) {\n            hold(i);\n        }\n", "",
             "the walk that finds its declaration owes the MRPDU that declares it"),
        kind("transmit-first-link-up-owes-nothing", "StartupDeclaresTalkersDomainAndVlan",
             "        } else {\n            hold(i);\n        }\n        i->link_seen = true;\n",
             "        }\n        i->link_seen = true;\n", "adapter.transmitted"),
        kind("transmit-reentry-unguarded", "ReentryFromOutputIsRefusedAndCounted",
             "    if (!enter(m)) {\n        return;\n    }\n    const unsigned first =",
             "    const unsigned first =",
             "adapter.reentries"),
        kind("transmit-second-interface-starved", WAITS, "const unsigned first = (m->tx_due & 1u) != 0u ? 0u : 1u;",
             "const unsigned first = 0u;", "the next such pass the next interface's"),
        kind("transmit-not-bound", WAITS, "        (void)ctrl_loop_set_transmit(loop,transmit,transmit_aged,m);\n",
             "        (void)transmit; (void)transmit_aged;\n", "the pass goes to the build"),
        kind("transmit-attaches-over-a-bound-client", "AttachmentFailureIsAtomicAndDetachesAfterLoopReset",
             " &&\n              !loop->transmit;", ";", "a loop whose THE TRANSMIT client is bound is refused"),
        kind("transmit-kept-by-destroy", "AttachmentFailureIsAtomicAndDetachesAfterLoopReset",
             "        if (l->transmit_ctx == m) {\n            l->transmit = NULL;\n",
             "        if (l->transmit_ctx == NULL) {\n            l->transmit = NULL;\n",
             "destroy detaches THE TRANSMIT's client"),
        # the count: restarted by what a build sent, and by nothing else
        kind("transmit-count-unset", COUNT, SENT, "    (void)slot;\n",
             "a sent MRPDU restarts its participant's count at the JoinTime"),
        kind("transmit-count-from-any-build", COUNT, SENT, "    m->join_left[slot] = SRP_JOIN_CS;\n",
             "a build that sends nothing leaves the count"),
        kind("transmit-count-not-kept", COUNT, ENDS,
             "if (m->join_left[slot] != 0u ? (m->join_left[slot] = 0u) != 0u : la == MRP_LA_STATE_ACTIVE) {",
             "each centisecond takes one off it"),
        # a pass a JoinTime: an Applicant moved owes one only with its own join timer idle, a first VLAN send one
        kind("transmit-moved-by-either-timer", "AnApplicantMovedOwesAPassWithItsOwnJoinTimerIdle",
             "t->appl_from != t->appl_to && m->join_left[2u * i->index + slot] == 0u",
             "t->appl_from != t->appl_to && (m->join_left[2u * i->index] == 0u || "
             "m->join_left[2u * i->index + slot] == 0u)", "not while its own runs, the other's idle or not"),
        kind("transmit-moved-owes-nothing", "AnApplicantMovedOwesAPassWithItsOwnJoinTimerIdle",
             "t->appl_from != t->appl_to && m->join_left[2u * i->index + slot] == 0u",
             "t->appl_from == t->appl_to && m->join_left[2u * i->index + slot] == 0u",
             "an Applicant moved with its own join timer idle owes a pass"),
        kind("transmit-first-vlan-send-declares-nothing", "AFirstVlanSendDeclaresWhatItLicensesInItsPass",
             "        if (i->msrp && (m->pending_rx.len != 0u || prepare_declarations(i)) &&",
             "        if (k < MBX_N_IF && i->msrp && (m->pending_rx.len != 0u || prepare_declarations(i)) &&",
             "the pass that sent it declares what it licensed"),
        kind("transmit-hold-beside-a-join-timer", "AJoinTimeOwesAnInterfaceAPass",
             "if (m->join_left[2u * i->index] == 0u || !m->loop->retry_queued) {", "if (m != NULL) {",
             "an interface's passes given whole, a JoinTime"),
        # a frame owed comes first
        kind("transmit-aged-beside-an-owed-frame", OWED, "return m->tx_due != 0u && !m->owed_len;",
             "return m->tx_due != 0u;", "no pass goes to the build while a frame is owed"),
        kind("transmit-due-cleared-with-a-frame-owed", OWED,
             "            if (!m->owed_len) {\n                m->tx_due &= (uint8_t)~(1u << n);\n            }\n",
             "            m->tx_due &= (uint8_t)~(1u << n);\n", "the interface stays due"),
        # the declarations with the build, none while a retained receive waits, a refusal tried again at the JoinTime
        kind("transmit-declares-beside-a-retained-receive", RETAINED, DECLARE,
             DECLARE.replace("(m->pending_rx.len != 0u || prepare_declarations(i))", "prepare_declarations(i)"),
             "a refused adoption takes no room a retained receive waits for", suite="srp_rx_retry.cpp"),
        kind("transmit-refusal-tried-no-more", "DomainExhaustionPreservesOldDeclarationUntilRetry", DECLARE,
             DECLARE.replace("            m->join_left[2u * n] = SRP_JOIN_CS;\n", ""),
             "a refused declaration is tried again when the join count ends"),
    )
