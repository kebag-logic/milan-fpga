# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Value types shared by service stimulus and trace grading."""
from __future__ import annotations

from dataclasses import dataclass

@dataclass
class Probe:
    """One measured path instance."""
    name: str            # e.g. adp.discover.if0
    row: str             # the table row it measures
    family: str          # key of CEILING_MS
    start: str
    ends: list[str]      # every listed end must occur; the path ends at the last of them
    wait_ms: float = 0.0  # a normative wait W the path may include (3.4.1: elapsed <= W + its budget)
    expect: str = ''     # an expected response check, see grade.py
    accesses: int | None = None  # the host model's measured or bound accesses in the pass, for comparison
    until: str = ''      # a later mark bounding the search; '' is the next mark
    also_from: str = ''  # a mark the interval is also reported from (the row's own origin)
    #: A notification's required recipients: (controller entity_id, interface), each
    #: registered for unsolicited notifications on that interface (IEEE 1722.1-2021 7.5.2).
    recipients: tuple[tuple[int, int], ...] = ()
    path: str = ''       # the path it is an instance of; '' is the name without .if<n>
    #: The sequence_ids of the responses owed ahead of the probe's: exactly these, in this
    #: order, must be committed on its channel between its input and its response.
    owed: tuple[int, ...] = ()
    #: An admitted command the firmware may take and never answer under the load: a missing
    #: response is then a measured finding, never answered (unbounded), not a refusal.
    may_drop: bool = False

    def path_key(self) -> tuple[str, int]:
        """The path and interface this probe measures; the tables report each one's worst instance."""
        base, _, suffix = self.name.rpartition('.if')
        return (self.path or base, int(suffix) if suffix.isdigit() else 0)


@dataclass(frozen=True)
class Point:
    """A measured shape: its config, AVB interface count and identity."""
    label: str
    shape: str
    interfaces: int
    entity_id: int
    mac: int
    sources: int
    sinks: int
