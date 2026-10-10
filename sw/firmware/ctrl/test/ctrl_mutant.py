# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""ctrl_mutant.py - the shape of one planted defect of the control-plane
firmware's campaign (ctrl_mutants.py), shared by its tables."""

from __future__ import annotations

from dataclasses import dataclass

#: The stack's files the tables plant into (#697): tsn-c-stack's sources and
#: public headers, named with ctrl_build.STACK_PREFIX. Every other path is the
#: ctrl tree's.
ADP_C = "tsn-c-stack/src/adp.c"
ACMP_C = "tsn-c-stack/src/acmp.c"
ACMP_H = "tsn-c-stack/include/acmp.h"
MAAP_C = "tsn-c-stack/src/maap.c"
MAAP_H = "tsn-c-stack/include/maap.h"


@dataclass(frozen=True)
class Mutant:
    """One planted defect."""

    name: str
    path: str
    old: str
    new: str
    arm: str
    test: str
    needle: str
    also: tuple[tuple[str, str, str], ...] = ()

    def kills(self) -> tuple[tuple[str, str, str], ...]:
        """Every (arm, test, words) that must fail on this defect."""
        return ((self.arm, self.test, self.needle), *self.also)
