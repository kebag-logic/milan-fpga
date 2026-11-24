# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Immutable choices for the control-service tier models."""
from __future__ import annotations

from typing import NamedTuple

LONG_RULES = ('buffer', 'slot-552')

class Fix(NamedTuple):
    """The corrected model's corrections, each a count at its source's own rule; AS_BUILT is rows_grade.demand."""

    retained: bool = True
    window: bool = True
    datapath: bool = True
    notify: bool = False


class Design(NamedTuple):
    """A tier design (TIERS): tier 2's slice in microseconds (0: the tree's at each point, CTRL_LOOP_SLICE_US, resolved
    by at_point), tier 1's and tier 2's order, AECP's rule, and whether the datapath events are counted (a report's
    choice, to show what they add; every bound counts them); the others' cap a pass (0: CTRL_LOOP_RX_PER_PASS), each
    tier-1 channel's quota a pass in TIER1's order under QUOTA_ORDERS (aecp-quota's AECP 0: the time the others' leave),
    and the rule for a notice longer than a slot (LONG_RULES)."""

    slice_us: int
    tier1: str = 'turn'
    tier2: str = 'srp-first'
    aecp: str = 'notify'
    datapath: bool = True
    cap: int = 0
    quota: tuple[int, ...] = ()
    long: str = 'buffer'

    def label(self) -> str:
        """The design as the tables name it."""
        shown = f'{self.slice_us} us' if self.slice_us else 'CTRL_LOOP_SLICE_US'
        return (f'slice {shown}, tier 1 {self.tier1}, tier 2 {self.tier2}, AECP {self.aecp}' +
                (f', cap {self.cap}' if self.cap else '') +
                (f', quotas {"/".join(map(str, self.quota))}' if self.quota else '') +
                ('' if self.long == LONG_RULES[0] else f', long notices {self.long}') +
                ('' if self.datapath else ', datapath events left out'))

