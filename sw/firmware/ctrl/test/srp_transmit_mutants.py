# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Planted defects of the SRP adapter's side of THE TRANSMIT (#665, ctrl_loop.h): the MRPDU build, and the
declarations it sends, out of the poll and into the loop's call, which takes no pass that takes a record; the hold
a centisecond, a record or a binding makes, reported owed; its age, counted on the centiseconds dispatched while it
is held and never beside an owed frame; one frame a pass; and the reclaim, after the declarations in the build's
pass and in the poll in every other pass.

srp_mutants.py plants them with the rest of its table: each must fail its named observable, never only a build.
"""
from __future__ import annotations

from typing import Callable, TypeVar

T = TypeVar("T")

WAITS = "TransmitWaitsForAPassThatTakesNoRecord"
AGES = "AHeldBuildTakesAPassOfItsOwnPastItsAge"
OWED = "AnOwedFrameComesBeforeTheBuild"
RETAINED = "SrpRetry.OversizedValidRecordExpiresOnceAndReleasesOtherInterfaceAndBinding"
#: The binding's end, after the withdrawals it holds a build for.
BIND_END = "    m->busy = false;\n    return true;\n}\n\nstatic bool rx_order_ready"
#: The poll's end: a held build reported owed.
POLL_END = "    owed = owed || m->tx_held;\n    m->busy = false;\n    return owed;\n}\n"
#: The build's declarations, which run in its call, before its MRPDU.
DECLARE = ("    if (!m->owed_len) {\n        for (unsigned n = 0; n < MBX_N_IF; ++n) {\n"
           "            if (m->ifs[n].msrp) {\n"
           "                owed = prepare_declarations(&m->ifs[n]) || owed;\n"
           "            }\n        }\n    }\n")
#: The poll's reclaim, in a pass whose build does not follow.
POLL_RECLAIM = ("    if (!m->loop->tx_pass) {\n        for (unsigned n = 0; n < MBX_N_IF; ++n) {\n"
                "            if (m->ifs[n].msrp) {\n                reclaim(&m->ifs[n]);\n            }\n"
                "        }\n    }\n")


def defects(kind: Callable[..., T]) -> tuple[T, ...]:
    """Every defect of the adapter's side of THE TRANSMIT, built with srp_mutants.Defect."""
    return (
        kind("transmit-built-by-the-poll", WAITS, POLL_END,
             "    m->busy = false;\n    owed = transmit(m) || owed || m->tx_held;\n    return owed;\n}\n",
             "a pass that takes a record builds no MRPDU"),
        kind("transmit-hold-unreported", WAITS, "    owed = owed || m->tx_held;\n", "",
             "a held build is reported owed"),
        kind("transmit-centisecond-holds-nothing", WAITS,
             "    m->tx_age += m->tx_held ? 1u : 0u;\n    m->tx_held = true;\n",
             "    m->tx_age += m->tx_held ? 1u : 0u;\n", "a centisecond holds a build"),
        kind("transmit-record-holds-nothing", WAITS,
             "    // a received record can make an MRPDU owed: THE TRANSMIT builds it once the pass's input is taken\n"
             "    m->tx_held = true;\n", "", "a received record holds a build"),
        kind("transmit-unbinding-holds-nothing", WAITS,
             "            m->tx_held = m->tx_held || old.declared != 0u;\n", "",
             "an unbinding that withdraws a declaration holds the build that sends it"),
        kind("transmit-binding-holds-a-build", WAITS, BIND_END, "    m->tx_held = true;\n" + BIND_END,
             "a binding holds no build itself"),
        kind("transmit-walk-holds-nothing", WAITS,
             "        i->owner->tx_held = i->owner->tx_held || i->sinks[k].desired != previous[k];\n", "",
             "the walk that finds its declaration holds the build that declares it"),
        kind("transmit-reentry-unguarded", "ReentryFromOutputIsRefusedAndCounted",
             "    if (!enter(m)) {\n        return false;\n    }\n    bool reclaims = false;\n",
             "    bool reclaims = false;\n", "adapter.reentries"),
        kind("transmit-not-bound", WAITS, "        (void)ctrl_loop_set_transmit(loop,transmit,transmit_aged,m);\n",
             "        (void)transmit; (void)transmit_aged;\n", "the next pass that takes no record builds one"),
        kind("transmit-attaches-over-a-bound-client", "AttachmentFailureIsAtomicAndDetachesAfterLoopReset",
             " &&\n              !loop->transmit;", ";", "a loop whose THE TRANSMIT client is bound is refused"),
        kind("transmit-kept-by-destroy", "AttachmentFailureIsAtomicAndDetachesAfterLoopReset",
             "        if (l->transmit_ctx == m) {\n            l->transmit = NULL;\n",
             "        if (l->transmit_ctx == NULL) {\n            l->transmit = NULL;\n",
             "destroy detaches THE TRANSMIT's client"),
        # the age (ctrl_loop.h, CTRL_LOOP_TX_AGE): counted while held, past the limit, restarted by a build
        kind("transmit-age-counts-unheld", AGES, "    m->tx_age += m->tx_held ? 1u : 0u;\n", "    m->tx_age += 1u;\n",
             "the build's pass follows the one that dispatches the centisecond past its age, counted from its hold"),
        kind("transmit-aged-at-its-limit", AGES, "m->tx_age > CTRL_LOOP_TX_AGE;", "m->tx_age >= CTRL_LOOP_TX_AGE;",
             "the build's pass follows the one that dispatches the centisecond past its age, counted from its hold"),
        kind("transmit-age-kept-by-a-build", AGES, "    m->tx_age = 0;\n    bool owed = false;\n",
             "    bool owed = false;\n", "two builds' passes stand more than CTRL_LOOP_TX_AGE centiseconds apart"),
        kind("transmit-aged-beside-an-owed-frame", OWED, "return m->tx_held && !m->owed_len && m->tx_age >",
             "return m->tx_held && m->tx_age >", "no held build takes a pass of its own while a frame is owed"),
        kind("transmit-builds-beside-the-owed-frame", OWED, "    if (m->resent_pass == m->loop->stats.passes || (",
             "    if ((", "the pass whose poll sends the owed frame builds no other"),
        # the declarations with the build: a Domain adopted in the poll leaves its VID unlicensed to the next poll
        kind("transmit-declarations-in-the-poll", "OwnDeclarationsThatRewriteARegisteredValueAreCopied", DECLARE, "",
             "over-saturated", also=((POLL_RECLAIM, DECLARE + POLL_RECLAIM),)),
        # the reclaim: after the declarations in the build's pass, in the poll in every other
        kind("transmit-reclaim-before-the-declarations", RETAINED, POLL_RECLAIM,
             POLL_RECLAIM.replace("    if (!m->loop->tx_pass) {", "    if (true) {"), "Change(0, 0, false)",
             suite="srp_rx_retry.cpp"),
        kind("transmit-reclaim-only-with-the-build", RETAINED, POLL_RECLAIM, "", "adapter.received",
             suite="srp_rx_retry.cpp"),
    )
