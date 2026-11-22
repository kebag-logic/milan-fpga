# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Planted defects of SRP's link level in a loop pass (#973): the level SRP's poll takes, and the loop's record of the
level its LINK records carried (ctrl_loop_link_up).

SRP's poll takes a DOWN as the LINK register reads it and an UP only once the loop has dispatched one or while the
interface holds one (srp_mbx.c, poll). srp_mutants.py plants each into a copy of sw/firmware/ctrl with the rest of
its table, and the named test must fail on its own words: srp_link_pass.cpp's for the level a link that comes up
inside a pass shows, srp_mbx.cpp's for the DOWN that fails closed and for the UP recovered from the level. The
one-interface campaigns plant them at 1x1/1if and at 8x8/1if (test_ctrl_firmware.run_srp_mutants), the
two-interface campaign at 1x1/2if.
"""
from __future__ import annotations

from typing import Callable, TypeVar

T = TypeVar("T")

#: The name every defect here starts with, which the one-interface campaigns select them by.
PREFIX = "link-pass-"
SUITE = "srp_link_pass.cpp"
INSIDE = "SrpLinkPass.AfterTheEventsBeforeSrpsPoll"
#: srp_mbx.c's poll, the level it takes for each interface, as it holds it.
POLL = "        links[n] = mbx_link_up(n) && (m->ifs[n].link || ctrl_loop_link_up(m->loop, n));\n"
#: The loop's record of the level a LINK record carries (ctrl_loop.c, service_events), and its reader (ctrl_loop.h).
RECORD = "\t\t\tl->link_level = ev.link_up ? l->link_level | bit : l->link_level & ~bit;\n"
READ = "\treturn ((l->link_level >> interface) & 1u) != 0u;\n"
#: on_event's first UP, which keeps the startup participants.
FIRST_UP = "        if (i->link_seen || !event->link_up) {\n"


def defects(kind: Callable[..., T]) -> tuple[T, ...]:
    """Every link level defect, built with srp_mutants.Defect."""
    return (
        # the fix reverted: the poll takes the register's UP, which a LINK has not carried yet, and resets on it; the
        # LINK the next pass dispatches is then a repeated UP, which resets the interface again
        kind(PREFIX + "poll-takes-the-register", INSIDE, POLL, "        links[n] = mbx_link_up(n);\n",
             "a first UP resets nothing", suite=SUITE),
        # a double reset through the loop: its level read from the register, not from the LINK records it dispatched
        kind(PREFIX + "loop-level-is-the-register", INSIDE, READ, "\t(void)l;\n\treturn mbx_link_up(interface);\n",
             "SRP's poll reset the interface on a level no LINK had carried", path="loop/ctrl_loop.h", suite=SUITE),
        # a first UP that resets the interface, so the startup participants are lost at any phase
        kind(PREFIX + "first-up-resets", "SrpLinkPass.BeforeAPass", FIRST_UP, "        if (true) {\n",
             "a first UP keeps the startup participants", suite=SUITE),
        # the loop never records a LINK's level: an UP whose record a held ring cancelled is never recovered
        kind(PREFIX + "level-never-recorded", "CancelledLinkRecordRecoversFromLevelAndFencesOldReceive", RECORD,
             "\t\t\t(void)bit;\n", "adapter.ifs[i].link", path="loop/ctrl_loop.c"),
        # the two-hart form taken whole, without the register's LINK it reads each pass: a link lost while a full
        # ring holds its record back no longer fails closed
        kind(PREFIX + "down-waits-for-its-record", "LinkLevelLossAndFirstDownEventAreFailClosed", POLL,
             "        links[n] = ctrl_loop_link_up(m->loop, n);\n", "adapter.ifs[0].active[0]"),
    )
