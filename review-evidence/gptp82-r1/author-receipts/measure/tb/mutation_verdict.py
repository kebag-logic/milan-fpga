#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""How a suite's OWN output answers, read once for every mutation arm.

A mutation arm is only evidence if "caught" means the harness said so. A
non-zero exit on its own is not a catch: a mutant that makes the design abort,
hang, or die by a signal has told us nothing about the assertions - it has only
told us the mutant is broken, which we already knew. So the verdict is read
from the tally line and the FAIL lines both suites already print, and every
other outcome is named as what it is rather than counted as success.
"""

from __future__ import annotations

import re

#: `N checks: P PASS, F FAIL`, printed by tsngen_main/run_tsngen.py and by the
#: gasket sim_main.cpp alike.
TALLY = re.compile(r"^\s*(\d+)\s+checks:\s*(\d+)\s+PASS,\s*(\d+)\s+FAIL\s*$", re.M)
#: a per-check failure line, e.g. `FAIL size 64 delivered got 0 exp 1`
FAIL_LINE = re.compile(r"^\s*FAIL\s+\S", re.M)


def reports_failure(out: str) -> tuple[str, bool]:
    """(reason, the harness itself reported at least one failed check)."""
    tally = TALLY.search(out)
    if tally is not None:
        failed = int(tally.group(3))
        if failed:
            return f"the tally reports {failed} failed check(s)", True
        return "the tally reports no failed check", False
    if FAIL_LINE.search(out):
        return "a FAIL line was printed with no tally", True
    return "the harness printed no tally and no FAIL line", False


def verdict(rc: int, out: str) -> str:
    """'pass', 'caught', 'skipped', or why this run is not evidence.

    There is deliberately no host deadline here. Both harnesses bound their
    own waits in DUT CYCLES - the gasket harness so that a wedged gasket
    fails the suite instead of hanging it, and tsngen with an explicit tick
    ceiling on every wait - so a mutant that livelocks the design still
    returns, and returns a verdict. A wall-clock deadline would only add a
    second, machine-dependent answer to a question the DUT already answers.
    """
    if "SKIP:" in out:
        return "skipped"
    reason, failed = reports_failure(out)
    if rc == 0 and not failed:
        return "pass"
    if rc == 0 and failed:
        return f"exited 0 but {reason} - a masked verdict is not evidence"
    if failed:
        return "caught"
    if rc < 0:
        return f"died by signal {-rc} with no harness verdict - a crash is not a catch"
    return f"exited {rc} with no harness verdict - an abort is not a catch"
