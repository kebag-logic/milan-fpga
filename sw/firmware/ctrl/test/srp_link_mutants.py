# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Planted defects of SRP's link level in a loop pass (#973): the level SRP's poll takes, and the level the last LINK
the loop dispatched carried (link_carried).

SRP's poll takes a DOWN as the LINK register reads it, and an UP only while the last LINK the loop dispatched carried
one, or once no LINK is owed, a poll that reads a DOWN clearing the mark that the take of an UP no LINK carried rests
on; attach carries the register's level (srp_mbx.c, poll, carried_up, on_event, srp_mbx_attach). srp_mutants.py
plants each into a copy of sw/firmware/ctrl with the rest of its table, and the named test must fail on its own
words: srp_link_pass.cpp's for the level a link that comes up inside a pass or behind a full event ring shows, for a
fresh UP after an UP a DOWN elided, and for a re-attach whose DOWN record was elided, srp_mbx.cpp's for the DOWN that
fails closed and for the level attach learns. The one-interface campaigns plant them at 1x1/1if and at 8x8/1if
(test_ctrl_firmware.run_srp_mutants), the two-interface campaign at 1x1/2if.
"""
from __future__ import annotations

from typing import Callable, TypeVar

T = TypeVar("T")

#: The name every defect here starts with, which the one-interface campaigns select them by.
PREFIX = "link-pass-"
SUITE = "srp_link_pass.cpp"
INSIDE = "SrpLinkPass.AfterTheEventsBeforeSrpsPoll"
#: srp_mbx.c's poll, the level it takes for each interface, as it holds it.
POLL = "        links[n] = carried_up(m, &m->ifs[n], mbx_link_up(n));\n"
#: carried_up's mark and take of an UP no LINK carried, and its clearing of the mark on a DOWN (the mask).
UNOWED = "        c = ((c >> 1 & (m->loop->events_left ? 0u : 1u)) | 2u) & -(unsigned)up;\n"
#: carried_up's level: the carried UP the register reads.
TAKEN = "    return c & up;\n"
ELIDED = "Srp.AReattachWhoseDownRecordIsElidedFollowsTheLinkThatIsUp"
HELD = "SrpLinkPass.ALinkUpHeldBehindAFullEventRingIsTheFirstUp"
FRESH = "SrpLinkPassElided.AnElidedUpAuthorizesNoFreshFirstUp"
FRESH_LATER = "SrpLinkPassElided.AnElidedUpAuthorizesNoFreshLaterUp"
#: on_event's record of the level a LINK carried, and its first UP, which keeps the startup participants.
CARRIED = "        i->link_carried = event->link_up;\n"
FIRST_UP = "        if (i->link_seen || !event->link_up) {\n"
#: srp_mbx_attach's level, the register's.
ATTACH = "            m->ifs[n].link_carried = m->ifs[n].link;\n"


def defects(kind: Callable[..., T]) -> tuple[T, ...]:
    """Every link level defect, built with srp_mutants.Defect."""
    return (
        # the fix reverted: the poll takes the register's UP, which a LINK has not carried yet, and resets on it; the
        # LINK the next pass dispatches is then a repeated UP, which resets the interface again
        kind(PREFIX + "poll-takes-the-register", INSIDE, POLL,
             "        links[n] = mbx_link_up(n);\n        (void)carried_up;\n",
             "a first UP resets nothing", suite=SUITE),
        # a double reset at the first UP: attach carries an UP it did not read, so the poll takes the register's
        kind(PREFIX + "attach-carries-an-up", INSIDE, ATTACH, "            m->ifs[n].link_carried = true;\n",
             "SRP's poll reset the interface on a level no LINK had carried", suite=SUITE),
        # a double reset at a later UP: a DOWN's LINK leaves the carried level up
        kind(PREFIX + "carried-stays-up", INSIDE, CARRIED,
             "        i->link_carried = i->link_carried || event->link_up;\n",
             "a later UP resets the interface once", suite=SUITE),
        # a first UP that resets the interface, so the startup participants are lost at any phase
        kind(PREFIX + "first-up-resets", "SrpLinkPass.BeforeAPass", FIRST_UP, "        if (true) {\n",
             "a first UP keeps the startup participants", suite=SUITE),
        # no LINK's level carried: the poll undoes every UP the loop dispatched
        kind(PREFIX + "carried-never-recorded", "SrpLinkPass.BeforeAPass", CARRIED, "",
             "a first UP resets nothing", suite=SUITE),
        # attach carries nothing: a link already up when SRP attaches, which no further LINK carries, is dropped by
        # the first poll and taken back only once no LINK is owed, so the interface resets twice and loses the
        # Listener the reattached interface was offered
        kind(PREFIX + "attach-carries-nothing", "ReattachLearnsAnAlreadyUpLinkWithoutAnotherRecord", ATTACH, "",
             "adapter.ifs[i].active[0]"),
        # the two-hart form taken whole, without the register's LINK its loop reads each pass: a link lost while a full
        # ring holds its record back no longer fails closed
        kind(PREFIX + "down-waits-for-its-record", "LinkLevelLossAndFirstDownEventAreFailClosed", POLL,
             "        links[n] = (m->ifs[n].link_carried & 1u) != 0u;\n        (void)carried_up;\n",
             "adapter.ifs[0].active[0]"),
        # the register's level ORed with the carried one: a DOWN no longer fails closed
        kind(PREFIX + "poll-or-instead-of-and", "LinkLevelLossAndFirstDownEventAreFailClosed", TAKEN,
             "    return (c | up) & 1u;\n", "adapter.ifs[0].active[0]"),
        # an UP no LINK carries never taken: a re-attach whose DOWN record was elided never follows the link that is up
        kind(PREFIX + "unowed-up-never-taken", ELIDED, UNOWED, "        (void)m;\n        c = 2u & -(unsigned)up;\n",
             "SRP does not follow a link that is up", suite=SUITE),
        # a double reset: an uncarried UP taken at once, at a poll whose pass's take found the ring empty, though its
        # LINK was posted after that take
        kind(PREFIX + "unowed-up-taken-unmarked", INSIDE, UNOWED,
             "        c = (m->loop->events_left ? 2u : 3u) & -(unsigned)up;\n",
             "SRP's poll reset the interface on a level no LINK had carried", suite=SUITE),
        # a double reset: an uncarried UP taken at the poll after its mark whatever that pass's take left, though its
        # LINK still waits behind a full ring's records
        kind(PREFIX + "unowed-up-ignores-the-take", HELD, UNOWED,
             "        (void)m;\n        c = (c >> 1 | 2u) & -(unsigned)up;\n",
             "SRP took an UP from the register while its LINK waited behind the ring's records", suite=SUITE),
        # the fix of an elided UP's mark reverted: a DOWN the poll reads leaves the mark, so a fresh UP raised after a
        # later pass's take, owed a LINK of its own, is taken on the elided UP's observation: the first UP resets the
        # interface and loses the startup participants, and a later one resets it twice
        kind(PREFIX + "mark-survives-a-down", FRESH, UNOWED,
             "        c = (((c >> 1 & (m->loop->events_left ? 0u : 1u)) | 2u) & -(unsigned)up) | (c & 2u);\n",
             "SRP's poll took a fresh UP on an elided UP's observation", suite=SUITE),
        kind(PREFIX + "mark-survives-a-down-later", FRESH_LATER, UNOWED,
             "        c = (((c >> 1 & (m->loop->events_left ? 0u : 1u)) | 2u) & -(unsigned)up) | (c & 2u);\n",
             "a later UP resets the interface once", suite=SUITE),
        # the mask applied before the shift, not after it: a DOWN the poll reads sets the mark instead of clearing
        # it, so the fresh UP is taken on an observation made while the link was down
        kind(PREFIX + "mark-masked-before-the-shift", FRESH, UNOWED,
             "        c = ((c & -(unsigned)up) >> 1 & (m->loop->events_left ? 0u : 1u)) | 2u;\n",
             "SRP's poll took a fresh UP on an elided UP's observation", suite=SUITE),
    )
