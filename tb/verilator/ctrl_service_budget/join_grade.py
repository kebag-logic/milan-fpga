# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The join intervals (#894's contingent ruling issuecomment-6858269025, item 4): with the join timer armed at
CTRL_LOOP_JOIN_CS (ctrl_loop.h), each participant's MRPDUs on the wire keep Milan v1.2 Table 4.3's JoinTime, 180 to
240 ms. A participant is an interface and an MRP application, told by its MRPDU's EtherType (MSRP or MVRP). A join
interval is the time from one of its MRPDUs' commit to the next, where a join timer ran out between them (lwSRP's
on_join_timer, mrp_mad.c) and neither the periodic nor the LeaveAll timer did: the next transmit opportunity the join
timer armed at the first commit gave. The harness reports each group's shortest and longest (run.py, JOINS), and a
group with one under LEAST_MS or over MOST_MS fails the run whatever findings it records.
"""
from __future__ import annotations

from bisect import bisect_left

import grade
import scenario

#: Table 4.3's JoinTime range, in ms.
LEAST_MS, MOST_MS = 180.0, 240.0
#: The MRP applications by their MRPDUs' EtherType (IEEE 802.1Q-2018 Table 10-2, 35.2.2.1).
APPLICATIONS = {0x22EA: 'MSRP', 0x88F5: 'MVRP'}
#: The lwSRP callbacks a timer's run-out enters (mrp_mad.c): the join timer's, and the two whose MRPDUs are not join's.
JOIN, OTHERS = 'on_join_timer', ('on_pt_timer', 'on_la_timer')


def intervals(log: grade.Log) -> list[tuple[float, str, int]]:
    """Each join interval of the log in ms, with its participant (`if<n> MSRP`) and the bus cycle it ended."""
    srp = scenario.CH['srp']
    joins = sorted(c for c, name in log.entries if name == JOIN)
    others = sorted(c for c, name in log.entries if name in OTHERS)
    sent: dict[str, list[int]] = {}
    for cycle, ch, interface, frame in log.tx:
        kind = APPLICATIONS.get(frame[12] << 8 | frame[13]) if ch == srp and len(frame) > 14 else None
        if kind:
            sent.setdefault(f'if{interface} {kind}', []).append(cycle)
    out = []
    for who, cycles in sent.items():
        cycles.sort()
        for a, b in zip(cycles, cycles[1:]):
            if bisect_left(joins, b) > bisect_left(joins, a) and bisect_left(others, b) == bisect_left(others, a):
                out.append(((b - a) * 1000 / log.sys_hz, who, b))
    return sorted(out)


def held(log: grade.Log) -> dict:
    """The group's join intervals: how many, the shortest and the longest in ms, and each outside LEAST_MS to
    MOST_MS."""
    every = intervals(log)
    over = [dict(ms=round(ms, 3), who=who, end_sys=end) for ms, who, end in every if not LEAST_MS <= ms <= MOST_MS]
    return dict(count=len(every), shortest=round(every[0][0], 3) if every else None,
                longest=round(every[-1][0], 3) if every else None, over=over)
