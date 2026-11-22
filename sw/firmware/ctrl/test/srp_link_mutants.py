# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Planted defects of SRP's link level in a loop pass (#973): the level SRP's poll takes, and the level the last LINK
the loop dispatched carried (link_carried).

SRP's poll takes a DOWN as the LINK register reads it, and an UP only while the last LINK the loop dispatched carried
one; attach carries the register's level (srp_mbx.c, poll, on_event, srp_mbx_attach). srp_mutants.py plants each into
a copy of sw/firmware/ctrl with the rest of its table, and the named test must fail on its own words:
srp_link_pass.cpp's for the level a link that comes up inside a pass shows, srp_mbx.cpp's for the DOWN that fails
closed and for the level attach learns. The one-interface campaigns plant them at 1x1/1if and at 8x8/1if
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
POLL = "        links[n] = mbx_link_up(n) && m->ifs[n].link_carried;\n"
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
        kind(PREFIX + "poll-takes-the-register", INSIDE, POLL, "        links[n] = mbx_link_up(n);\n",
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
        # attach carries nothing: a link already up when SRP attaches, which no further LINK carries, is lost, and
        # with it the Talker declarations the reattached interface owes
        kind(PREFIX + "attach-carries-nothing", "ReattachLearnsAnAlreadyUpLinkWithoutAnotherRecord", ATTACH, "",
             "Value of: talker"),
        # the two-hart form taken whole, without the register's LINK its loop reads each pass: a link lost while a full
        # ring holds its record back no longer fails closed
        kind(PREFIX + "down-waits-for-its-record", "LinkLevelLossAndFirstDownEventAreFailClosed", POLL,
             "        links[n] = m->ifs[n].link_carried;\n", "adapter.ifs[0].active[0]"),
    )
