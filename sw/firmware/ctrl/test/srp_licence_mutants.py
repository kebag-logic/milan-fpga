# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Planted defects of the poll's skipped licence scan (#872, srp_mbx.c poll): the scan runs only where its interface is
marked stale (licence_stale), each writer of what it reads marking it. Each defect drops a writer's mark, or inverts
the skip, so a skipped scan would have changed a licence, and srp_mbx.cpp's
ALicenceScanIsSkippedOnlyWhereItWouldChangeNothing, built with CTRL_SRP_LICENCE_CHECK (srp_arms.py), must fail on its
own words. The other marks (the declarations' admission, the walk, the VLAN's first send, an adopted Domain's VID, the
link, an interface's open, reset and destroy) are each made, in every path the suites reach, together with another
mark before the same scan (a declaration marks its interface stale, whose walk marks it; a re-declared Talker's
Listener is indicated again), so a defect of one alone changes nothing there and is not planted; every SRP arm checks
each skip's premise (srp_licence_check.cpp).

srp_mutants.py plants each into a copy of sw/firmware/ctrl with the rest of its table.
"""
from __future__ import annotations

from typing import Callable, TypeVar

T = TypeVar("T")

#: The name every defect here starts with.
PREFIX = "srp-licence-"
TEST = ("Srp.ALicenceScanIsSkippedOnlyWhereItWouldChangeNothing", "a skipped licence scan would have changed a licence")
#: srp_mbx.c's sites, as it holds them.
LISTENER = "    if (of != 0u) {\n        i->licence_stale = true;\n    }\n"
SKIP = "        if (!i->licence_stale) {\n#ifdef CTRL_SRP_LICENCE_CHECK\n"


def defects(kind: Callable[..., T]) -> tuple[T, ...]:
    """Every defect of the skip, built with srp_mutants.Defect, in srp_mbx.c's order."""
    def d(name: str, old: str, new: str) -> T:
        return kind(PREFIX + name, TEST[0], old, new, TEST[1])
    return (
        # a Listener's Ready, AskingFailed or leave not marked: its licence waits for an unrelated mark
        d("listener-unmarked", LISTENER, ""),
        # the skip inverted: a marked scan is skipped, an unmarked one run
        d("skip-inverted", SKIP, SKIP.replace("if (!i->licence_stale)", "if (i->licence_stale)")),
    )
