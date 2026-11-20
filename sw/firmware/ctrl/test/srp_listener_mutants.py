# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Planted defects of SRP's Listener copies (#930), one a site that copies a change where lwSRP reports it or marks
the registrar walk owed for it.

A Listener's indication copies its declaration (listener) and lwSRP's transition observer its presence (moved,
listener_moved), with no walk; a Registrar change owes none, since each change of what the walk copies comes with an
indication, and a Talker's marks the walk owed (talker_changed). srp_mutants.py plants each into a copy of
sw/firmware/ctrl with the rest of its table, and srp_listeners.cpp's differential, whose reference run restores the
walk's schedule as #665 left it, must fail on its own words. The one-interface campaigns plant them at 1x1/1if and
at 8x8/1if (ENTITY; test_ctrl_firmware.run_srp_mutants), the two-interface campaign at 8x8/2if.
"""
from __future__ import annotations

from typing import Callable, TypeVar

T = TypeVar("T")

SUITE = "srp_listeners.cpp"
#: The entity of the one-interface campaign at 8x8/1if and of the two-interface campaign.
ENTITY = "endstation_ax7101_8x8"
#: The name every defect here starts with, which the one-interface campaigns select them by.
PREFIX = "listener-copy-"
TEST = "Listeners.RandomRecordsMatchTheReferenceWalk"
NEEDLE = "the copied run makes the reference run's mailbox writes and licence calls, in order"
#: srp_mbx.c's copies and marks, as it holds them.
DECLARATION = ("            i->registered[n] = declaration == MSRP_LISTENER_DECL_READY ||\n"
               "                               declaration == MSRP_LISTENER_DECL_READY_FAILED;\n")
PRESENCE = "            i->listener_present[n] = t->reg_to != MRP_REG_STATE_MT;\n"
DISPATCH = "    if (slot == 0u && t->attr_type == MSRP_ATTR_TYPE_LISTENER && t->reg_from != t->reg_to) {\n"
TALKER = "    i->stale = true; // what an indication writes, snapshot copies (#665)\n"


def defects(kind: Callable[..., T]) -> tuple[T, ...]:
    """Every Listener copy defect, built with srp_mutants.Defect, in srp_mbx.c's order."""
    def d(name: str, old: str, new: str) -> T:
        """One defect, named with PREFIX, which the differential must fail on its words."""
        return kind(PREFIX + name, TEST, old, new, NEEDLE, suite=SUITE, entity=ENTITY)
    return (
        d("talker-indication-unwalked", TALKER, ""),
        d("declaration-lost", DECLARATION, "            (void)declaration;\n"),
        d("presence-lost", PRESENCE, ""),
        d("leaving-counted-absent", PRESENCE, PRESENCE.replace("!= MRP_REG_STATE_MT", "== MRP_REG_STATE_IN")),
        d("departure-dropped", DISPATCH,
          DISPATCH.replace("t->reg_from != t->reg_to", "t->reg_from == MRP_REG_STATE_MT")),
    )
