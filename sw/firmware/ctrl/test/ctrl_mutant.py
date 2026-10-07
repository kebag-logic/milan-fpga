# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""ctrl_mutant.py - the shape of one planted defect of the control-plane
firmware's campaign (ctrl_mutants.py), shared by its tables."""

from __future__ import annotations

from dataclasses import dataclass


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
