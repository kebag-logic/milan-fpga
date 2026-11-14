# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The join intervals (#894's contingent ruling of 2026-11-13, item 4): with the join timer armed at
CTRL_LOOP_JOIN_CS (ctrl_loop.h), each participant's MRPDUs on the wire keep Milan v1.2 Table 4.3's JoinTime, 180 to
240 ms, so commit to commit, as the harness sees them, LEAST_MS to MOST_MS, since either frame may wait T_egress to
leave. A participant is an interface and an MRP application, told by its MRPDU's EtherType (MSRP or MVRP). A join
interval is the time from one of its MRPDUs' commit to the next, where that next is a frame a join timer's run-out
between them released (lwSRP's on_join_timer, mrp_mad.c; the frames of the builds after it, mrpdu_grade.released, with
no horizon) and neither the periodic nor the LeaveAll timer ran out between them: the transmit opportunity the join
timer armed at the first commit gave, since lwSRP arms it at a commit alone. A run-out with nothing to send releases
nothing, and the MRPDU a later request then sends at once (its join timer idle) ends no interval. The harness reports
each group's shortest and longest and its MRP timers' run-outs by outcome (run.py, JOINS); a group with an interval
under LEAST_MS or over MOST_MS, or a run-out whose build is late or absent (mrpdu_grade.FAILING), fails the run
whatever findings it records.
"""
from __future__ import annotations

from bisect import bisect_left
from pathlib import Path

import grade
import mrpdu_grade
import scenario
from tier1_rows import allowance

#: Table 4.3's JoinTime range on the wire, in ms, the bench capture's (FR_NFR.md 3.4.1).
WIRE_MS = (180.0, 240.0)
#: T_egress, ctrl_loop.h's CTRL_LOOP_T_EGRESS_MS, in ms: a commit's frame is on the wire within it.
EGRESS_MS = allowance((Path(__file__).resolve().parents[3] / 'sw/firmware/ctrl/loop/ctrl_loop.h').read_text(),
                      'CTRL_LOOP_T_EGRESS_MS')
#: The range a join interval is held to commit to commit: the wire's narrowed by T_egress at each end, 181.0 to
#: 239.0 ms (#894's egress ruling of 2026-11-13, item 1).
LEAST_MS, MOST_MS = WIRE_MS[0] + EGRESS_MS, WIRE_MS[1] - EGRESS_MS
#: The MRP applications by their MRPDUs' EtherType (IEEE 802.1Q-2018 Table 10-2, 35.2.2.1).
APPLICATIONS = {0x22EA: 'MSRP', 0x88F5: 'MVRP'}
#: The lwSRP callbacks a timer's run-out enters (mrp_mad.c): the join timer's, and the two whose MRPDUs are not join's.
JOIN, OTHERS = 'on_join_timer', ('on_pt_timer', 'on_la_timer')


def released(log: grade.Log) -> dict[int, int]:
    """Each MRPDU a join timer's run-out released, late or not, by its commit's bus cycle: the latest such run-out's
    (mrpdu_grade.released, which has no horizon)."""
    joins = sorted(c for c, name in log.entries if name == JOIN)
    return {cycle: entry for entry in joins for cycle, _ in mrpdu_grade.released(log, entry)}


def intervals(log: grade.Log) -> list[tuple[float, str, int]]:
    """Each join interval of the log in ms, with its participant (`if<n> MSRP`) and the bus cycle it ended."""
    srp = scenario.CH['srp']
    others = sorted(c for c, name in log.entries if name in OTHERS)
    by = released(log)
    sent: dict[str, list[int]] = {}
    for cycle, ch, interface, frame in log.tx:
        kind = APPLICATIONS.get(frame[12] << 8 | frame[13]) if ch == srp and len(frame) > 14 else None
        if kind:
            sent.setdefault(f'if{interface} {kind}', []).append(cycle)
    out = []
    for who, cycles in sent.items():
        cycles.sort()
        for a, b in zip(cycles, cycles[1:]):
            if a < by.get(b, a) and bisect_left(others, b) == bisect_left(others, a):
                out.append(((b - a) * 1000 / log.sys_hz, who, b))
    return sorted(out)


def held(log: grade.Log) -> dict:
    """The group's join intervals: how many, the shortest and the longest in ms, and each outside LEAST_MS to
    MOST_MS; and every MRP timer's run-out by its outcome (mrpdu_grade.resolve, no horizon), each late or absent one
    named with its timer, its time and how far its first frame or build, or the log's end, lies past it."""
    every = intervals(log)
    over = [dict(ms=round(ms, 3), who=who, end_sys=end) for ms, who, end in every if not LEAST_MS <= ms <= MOST_MS]
    builds, _, sent, last = mrpdu_grade.index(log)
    runs, failing = dict.fromkeys(mrpdu_grade.OUTCOMES, 0), []
    for entry, kind, outcome in mrpdu_grade.outcomes(log):
        runs[outcome] += 1
        if outcome in mrpdu_grade.FAILING:
            frames = mrpdu_grade.released(log, entry)
            after = frames[0][0] if frames else next((b for b in builds if b > entry), last)
            failing.append(dict(kind=kind, outcome=outcome, at_ms=round(entry * 1000 / log.sys_hz, 3),
                                after_ms=round((after - entry) * 1000 / log.sys_hz, 3)))
    return dict(count=len(every), shortest=round(every[0][0], 3) if every else None,
                longest=round(every[-1][0], 3) if every else None, over=over, runs=runs, failing=failing)
