# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The self-test's checks of THE TRANSMIT's transmit opportunity and of the LeaveAll's (mrpdu_grade.py; #665's ruling
of 2026-11-16, Q1). An MRPDU a timer owes is timed from its participant's transmit opportunity: the TICK that runs
the participant's join timer out where that timer still runs at the run-out, the run-out's own TICK where it does not
(IEEE 802.1Q-2018 10.7.4.1). A LeaveAll goes out at its participant's first transmit opportunity after its timer runs
out, within THE TRANSMIT's bound of it. A participant whose first MRPDU after the run-out does not carry the LeaveAll
has skipped one, which is named and fails the run, as a late or an absent LeaveAll does."""
from __future__ import annotations

import argparse
from collections.abc import Callable

import grade
import join_grade
import mrpdu_grade
import run
import scenario

Check = tuple[str, bool, str]
MSRP, MVRP = 0x22EA, 0x88F5


def mrpdu(kind: int, leave_all: bool, listener: bool = False) -> bytes:
    """An Ethernet frame of one MRPDU, its VectorAttribute's LeaveAllEvent LeaveAll or not: MSRP's Domain (type 4,
    with its AttributeListLength), or with listener MSRP's Listener (type 3) whose first vector, with no LeaveAll, has
    a FourPackedEvents byte and whose second carries the LeaveAll; or MVRP's VID (type 1)."""
    header = ((1 << 13) if leave_all else 0) | 1
    if kind == MSRP and listener:
        first = (1).to_bytes(2, 'big') + bytes(8) + bytes([36]) + bytes([0])
        second = header.to_bytes(2, 'big') + bytes(8) + bytes([36]) + bytes([0])
        vectors = first + second
        body = bytes([0, 3, 8]) + (len(vectors) + 2).to_bytes(2, 'big') + vectors + bytes(4)
    elif kind == MSRP:
        vector = header.to_bytes(2, 'big') + bytes([6, 3, 0, 2]) + bytes([36])
        body = bytes([0, 4, 4]) + (len(vector) + 2).to_bytes(2, 'big') + vector + bytes(4)
    else:
        body = bytes([0, 1, 2]) + header.to_bytes(2, 'big') + bytes([0, 2, 36]) + bytes(4)
    frame = bytes(12) + kind.to_bytes(2, 'big') + body
    return frame + bytes(max(0, 60 - len(frame)))


def leave_all_checks(synthetic: Callable[[list[str]], str], sys_hz: int, cpu_hz: int,
                     tx_record: Callable[..., list[str]]) -> list[Check]:
    """Every check of the transmit opportunity and the LeaveAll's; tx_record is selftest.py's, the ring writes and
    commit of one TX record."""
    ms, ratio, srp = sys_hz // 1000, sys_hz // cpu_hz, scenario.CH['srp']

    def graded(sends: tuple, timers: tuple, ordinary: tuple = ()) -> tuple[list[dict], dict]:
        """A held group's log on interface 0 with a TICK every centisecond from 900 ms to 1,500 ms: its MRPDUs
        (ms, EtherType, LeaveAll), each committed at its ms after its build, in a pass of its own; its timers' entries
        (ms, callback) just after their ms's TICK; and passes with no build at the ms in ordinary. Its timer rows
        and its join intervals and run-outs (join_grade.held)."""
        lines, word = ['MARK 1000 save.change'], 0
        for at in range(900, 1_501, 10):
            lines += [f'EVW {at * ms} {n} {w:08x}' for n, w in enumerate((mrpdu_grade.TICK, 1, 0, 0))]
        for at, kind, la in sends:
            frame = mrpdu(kind, la)
            lines += tx_record(srp, 0, frame, word, at * ms)
            word += 2 + (len(frame) + 3) // 4
        lines += [f'ENTRY {at * ms - 2000} build_mrpdu' for at, _, _ in sends]
        lines += [f'PASS {at} {at * ms - 3000} {(at * ms - 3000) // ratio} {5000 // ratio} instr=10'
                  for at in sorted([at for at, _, _ in sends] + list(ordinary))]
        lines += [f'ENTRY {at * ms + 100} {name}' for at, name in timers]
        log = grade.parse(synthetic(lines), sys_hz, cpu_hz)
        group = scenario.Group('leaveall', save=dict(loaded=True, origin='save.change'))
        return mrpdu_grade.rows(grade.Grader(log), group), join_grade.held(log)

    def row(rows: list[dict], kind: str) -> float | None:
        """A timer kind's row on interface 0, in ms."""
        return next((r['ms'] for r in rows if r['probe'].endswith(f'.mrpdu.{kind}.if0')), None)

    la, join = 'on_la_timer', 'on_join_timer'
    out = []
    # MSRP's commit at 1,000 ms arms its join timer, run out by the 19th TICK after its build, at 1,180 ms
    first_rows, first = graded(((1_000, MSRP, False), (1_181, MSRP, True)), ((1_050, la), (1_180, join)))
    out.append(("a LeaveAll whose participant's join timer still runs is timed from that timer's run-out, its "
                "transmit opportunity: 1 ms after the 1,180 ms TICK, though 131 ms after the run-out, and sent there",
                mrpdu_grade.JOIN_CS == 19 and row(first_rows, 'leaveall') == 1.0 and
                first['leave_all']['runs']['sent'] == 1 and not first['leave_all']['failing'] and
                first['runs']['late'] == 0 and not first['failing'], str((first_rows, first))))
    idle_rows, idle = graded(((1_000, MSRP, False), (1_301, MSRP, True)), ((1_300, la),))
    out.append(("a LeaveAll whose participant's join timer has run out is timed from the run-out's own TICK and sent "
                "at once", row(idle_rows, 'leaveall') == 1.0 and idle['leave_all']['runs']['sent'] == 1,
                str((idle_rows, idle))))
    _, skipped = graded(((1_000, MSRP, False), (1_181, MSRP, False), (1_371, MSRP, True)),
                        ((1_050, la), (1_180, join), (1_370, join)))
    _, late = graded(((1_000, MSRP, False), (1_240, MSRP, True)), ((1_050, la), (1_180, join)))
    named = run.stated_misses([dict(group='s', passes=dict(joins=skipped)), dict(group='l', passes=dict(joins=late))])
    out.append(("a LeaveAll its participant sends after an MRPDU without it, a transmit opportunity skipped, is named; "
                "one past THE TRANSMIT's bound after its first opportunity is named late",
                skipped['leave_all']['runs']['skipped'] == 1 and late['leave_all']['runs']['late'] == 1 and
                "s: the LeaveAll timer's run-out at 1050.001 ms (if0 MSRP): its first transmit opportunity at "
                "1180.000 ms sent an MRPDU without the LeaveAll at 1181.000 ms, and the LeaveAll went at 1371.000 ms "
                "(LeaveAll past its first transmit opportunity)" in named and
                "l: the LeaveAll timer's run-out at 1050.001 ms (if0 MSRP): its LeaveAll at 1240.000 ms, 60.000 ms "
                "after its first transmit opportunity at 1180.000 ms, past THE TRANSMIT's 49 ms (LeaveAll late)"
                in named, str(named)))
    _, apart = graded(((1_000, MSRP, False), (1_100, MVRP, False), (1_181, MSRP, True)), ((1_050, la), (1_180, join)))
    out.append(("the LeaveAll is its own participant's: another application's MRPDU before it skips nothing",
                apart['leave_all']['runs']['sent'] == 1 and not apart['leave_all']['failing'], str(apart)))
    _, absent = graded(((1_000, MSRP, False),), ((1_050, la),), ordinary=(1_300,))
    _, pending = graded(((1_000, MSRP, False),), ((1_050, la),), ordinary=(1_200,))
    gone = [n for n in run.stated_misses([dict(group='a', passes=dict(joins=absent)),
                                          dict(group='u', passes=dict(joins=pending))]) if 'LeaveAll' in n]
    out.append(("no LeaveAll after a run-out is absent and named where the log runs on past every participant's "
                "opportunity and the bound, and unresolved, not named, where it ends first",
                absent['leave_all']['runs']['absent'] == 1 and pending['leave_all']['runs']['unresolved'] == 1 and
                len(gone) == 1 and gone[0].startswith("a: the LeaveAll timer's run-out at 1050.001 ms, no LeaveAll")
                and gone[0].endswith('(LeaveAll absent)'), str(gone)))
    reads = [mrpdu_grade.leave_all(mrpdu(k, f, listener)) for k, f, listener in (
        (MSRP, True, False), (MSRP, False, False), (MVRP, True, False), (MVRP, False, False), (MSRP, True, True))]
    out.append(("an MRPDU's LeaveAll is read from its VectorHeaders, MSRP's past its AttributeListLength and a "
                "Listener vector's FourPackedEvents", reads == [True, False, True, False, True], str(reads)))
    args = argparse.Namespace(cpu_regions='cover', mutation='none', record_budget_findings=True,
                              record_share_findings=True)
    skip = [n for n in named if n.endswith('(LeaveAll past its first transmit opportunity)')]
    out.append(('a skipped LeaveAll fails a run whatever findings it records',
                len(skip) == 1 and run.verdict(args, [scenario.Group('s')], [], [], [], skip) == 1, str(skip)))
    return out
