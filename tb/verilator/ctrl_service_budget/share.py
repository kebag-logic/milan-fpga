# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The per-pass share (#665): the CPU time one pass of the control loop may take. grade.pass_share
holds every work pass to it, apart from the row verdicts, and run.py fails a run with a pass over it
even when every row fits, unless --record-share-findings is given.

A pass is the only opportunity to take an input. An input waits for the pass running when it
arrives, is taken in a later pass and answered in the pass that takes it. The deepest wait the loop
admits is ten passes (sw/firmware/ctrl/loop/ctrl_loop.h, THE SHARE; #397's one-hart rule), which must
fit the smallest bound every input shares. That bound is the least over the families of
min(T_svc, the family's ceiling) (FR_NFR.md 3.4.1), T_svc's 20 ms since the owner's ruling of
2026-11-06 relaxed SRP's. The share is that bound over the ten passes, 2.0 ms of CPU time at whatever
clock the build runs the CPU: 200,000 CPU cycles at the product's split CPU clock, sys, 100 MHz.
"""
from __future__ import annotations

from fractions import Fraction

import scenario

#: The passes that must fit the tightest bound (ctrl_loop.h, THE SHARE).
SHARE_PASSES = 10


def bound_ms() -> float:
    """The smallest bound every input shares: the least of min(T_svc, ceiling) over the families."""
    return min(min(scenario.T_SVC_MS, ceiling) for ceiling in scenario.CEILING_MS.values())


def share_ms() -> float:
    """The share: that bound over SHARE_PASSES passes, in ms of CPU time."""
    return bound_ms() / SHARE_PASSES


def share_cycles(cpu_hz: int) -> int:
    """The share in CPU cycles at cpu_hz: a pass of at most that many fits it."""
    return int(Fraction(str(bound_ms())) * cpu_hz / (1000 * SHARE_PASSES))
