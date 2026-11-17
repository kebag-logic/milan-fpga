# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The self-test's checks of THE TRANSMIT's transmit opportunity and of the LeaveAll's (mrpdu_grade.py; #665's ruling
of 2026-11-16, Q1, and PR #934). An MRPDU a timer owes is timed from its participant's transmit opportunity: the
TICK that runs the participant's join timer out where that timer still runs at the run-out, the run-out's own TICK
where it does not (IEEE 802.1Q-2018 10.7.4.1). A LeaveAll timer's run-out is its owner's, the participant the
testbench recorded at the expiry, never the participant whose LeaveAll happens to come first. The owner's LeaveAll goes
out at the owner's first transmit opportunity after the run-out, within THE TRANSMIT's bound of it. An owner whose
first MRPDU after the run-out does not carry it has skipped one, which is named and fails the run, as a late, an
absent or an unowned LeaveAll does. The controls hold for both applications and both interfaces, with two
participants' timers overlapping."""
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


Graded = Callable[..., tuple[list[dict], dict]]
LA, JOIN = 'on_la_timer', 'on_join_timer'


def harness(synthetic: Callable[[list[str]], str], sys_hz: int, cpu_hz: int,
            tx_record: Callable[..., list[str]]) -> Graded:
    """The synthetic logs' grader; tx_record is selftest.py's, the ring writes and commit of one TX record."""
    ms, ratio, srp = sys_hz // 1000, sys_hz // cpu_hz, scenario.CH['srp']

    def graded(sends: tuple, timers: tuple, ordinary: tuple = (), empty: tuple = ()) -> tuple[list[dict], dict]:
        """A held group's log with a TICK every centisecond from 900 ms to 1,500 ms: its MRPDUs (ms, EtherType,
        LeaveAll, interface), each committed at its ms after its build, in a pass of its own; its timers' entries
        (ms, callback, owner) just after their ms's TICK, the owner as the testbench records it at the expiry (a
        participant, `unresolved`, or None for no record); passes with no build at the ms in ordinary; and builds
        that send nothing, each in a pass of its own, at the ms in empty. Its timer rows and its join intervals and
        run-outs (join_grade.held)."""
        lines, word = ['MARK 1000 save.change'], 0
        for at in range(900, 1_501, 10):
            lines += [f'EVW {at * ms} {n} {w:08x}' for n, w in enumerate((mrpdu_grade.TICK, 1, 0, 0))]
        for at, kind, leave, interface in sends:
            frame = mrpdu(kind, leave)
            lines += tx_record(srp, interface, frame, word, at * ms)
            word += 2 + (len(frame) + 3) // 4
        lines += [f'ENTRY {at * ms - 2000} build_mrpdu' for at in sorted([s[0] for s in sends] + list(empty))]
        lines += [f'PASS {at} {at * ms - 3000} {(at * ms - 3000) // ratio} {5000 // ratio} instr=10'
                  for at in sorted({at for at, _, _, _ in sends} | set(ordinary) | set(empty))]
        lines += [f'ENTRY {at * ms + 100} {name}' + (f' {who}' if who else '') for at, name, who in timers]
        log = grade.parse(synthetic(lines), sys_hz, cpu_hz)
        group = scenario.Group('leaveall', save=dict(loaded=True, origin='save.change'))
        return mrpdu_grade.rows(grade.Grader(log), group), join_grade.held(log)
    return graded


def row(rows: list[dict], kind: str, interface: int = 0) -> float | None:
    """A timer kind's row on an interface, in ms."""
    return next((r['ms'] for r in rows if r['probe'].endswith(f'.mrpdu.{kind}.if{interface}')), None)


def by(held: dict) -> dict[str, int]:
    """A log's LeaveAlls by outcome, the outcomes that occur."""
    return {o: n for o, n in held['leave_all']['runs'].items() if n}


def named(**joins: dict) -> list[str]:
    """The LeaveAll findings of logs, each its group's."""
    return [m for m in run.stated_misses([dict(group=g, passes=dict(joins=j)) for g, j in joins.items()])
            if 'LeaveAll' in m]


def leave_all_checks(synthetic: Callable[[list[str]], str], sys_hz: int, cpu_hz: int,
                     tx_record: Callable[..., list[str]]) -> list[Check]:
    """Every check of the transmit opportunity and the LeaveAll's; tx_record is selftest.py's, the ring writes and
    commit of one TX record."""
    graded = harness(synthetic, sys_hz, cpu_hz, tx_record)
    single, one = single_checks(graded)
    return single + overlap_checks(graded) + record_checks(graded, one) + anchor_checks(graded)


def single_checks(graded: Graded) -> tuple[list[Check], list[str]]:
    """One participant's LeaveAll: timed from its opportunity, sent, skipped, late, absent or unresolved, and the
    MRPDU parser; with the skipped and late findings named."""
    la, join = LA, JOIN
    out = []
    # MSRP's commit at 1,000 ms arms its join timer, run out by the 19th TICK after its build, at 1,180 ms
    first_rows, first = graded(((1_000, MSRP, False, 0), (1_181, MSRP, True, 0)),
                               ((1_050, la, 'if0 MSRP'), (1_180, join, 'if0 MSRP')))
    out.append(("a LeaveAll whose owner's join timer still runs is timed from that timer's run-out, its transmit "
                "opportunity: 1 ms after the 1,180 ms TICK, though 131 ms after the run-out, and sent there",
                mrpdu_grade.JOIN_CS == 19 and row(first_rows, 'leaveall') == 1.0 and by(first) == {'sent': 1}
                and first['runs']['late'] == 0 and not first['failing'], str((first_rows, first))))
    idle_rows, idle = graded(((1_000, MSRP, False, 0), (1_301, MSRP, True, 0)), ((1_300, la, 'if0 MSRP'),))
    out.append(("a LeaveAll whose owner's join timer has run out is timed from the run-out's own TICK and sent at once",
                row(idle_rows, 'leaveall') == 1.0 and by(idle) == {'sent': 1}, str((idle_rows, idle))))
    _, skipped = graded(((1_000, MSRP, False, 0), (1_181, MSRP, False, 0), (1_371, MSRP, True, 0)),
                        ((1_050, la, 'if0 MSRP'), (1_180, join, 'if0 MSRP'), (1_370, join, 'if0 MSRP')))
    _, late = graded(((1_000, MSRP, False, 0), (1_240, MSRP, True, 0)),
                     ((1_050, la, 'if0 MSRP'), (1_180, join, 'if0 MSRP')))
    one = named(s=skipped, l=late)
    out.append(("a LeaveAll its owner sends after an MRPDU without it, a transmit opportunity skipped, is named; one "
                "past THE TRANSMIT's bound after its first opportunity is named late", by(skipped) == {'skipped': 1} and
                by(late) == {'late': 1} and one == [
                    "s: the LeaveAll timer's run-out at 1050.001 ms (if0 MSRP): its first transmit opportunity at "
                    "1180.000 ms sent an MRPDU without the LeaveAll at 1181.000 ms, and the LeaveAll went at "
                    "1371.000 ms, 191.000 ms after it (LeaveAll past its first transmit opportunity)",
                    "l: the LeaveAll timer's run-out at 1050.001 ms (if0 MSRP): its LeaveAll at 1240.000 ms, 60.000 ms "
                    "after its first transmit opportunity at 1180.000 ms, past THE TRANSMIT's 49 ms (LeaveAll late)"],
                str(one)))
    _, apart = graded(((1_000, MSRP, False, 0), (1_100, MVRP, False, 0), (1_181, MSRP, True, 0)),
                      ((1_050, la, 'if0 MSRP'), (1_180, join, 'if0 MSRP')))
    out.append(("the LeaveAll is its owner's: another application's MRPDU before it skips nothing",
                by(apart) == {'sent': 1}, str(apart)))
    _, absent = graded(((1_000, MSRP, False, 0),), ((1_050, la, 'if0 MSRP'),), ordinary=(1_300,))
    _, pending = graded(((1_000, MSRP, False, 0),), ((1_050, la, 'if0 MSRP'),), ordinary=(1_200,))
    gone = named(a=absent, u=pending)
    out.append(("no MRPDU of its owner after a run-out is absent and named where the log runs on past the owner's "
                "opportunity and the bound, and unresolved, not named, where it ends first",
                by(absent) == {'absent': 1} and by(pending) == {'unresolved': 1} and len(gone) == 1 and
                gone[0].startswith("a: the LeaveAll timer's run-out at 1050.001 ms (if0 MSRP)") and
                gone[0].endswith('(LeaveAll absent)'), str(gone)))
    reads = [mrpdu_grade.leave_all(mrpdu(k, f, listener)) for k, f, listener in (
        (MSRP, True, False), (MSRP, False, False), (MVRP, True, False), (MVRP, False, False), (MSRP, True, True))]
    out.append(("an MRPDU's LeaveAll is read from its VectorHeaders, MSRP's past its AttributeListLength and a "
                "Listener vector's FourPackedEvents", reads == [True, False, True, False, True], str(reads)))
    return out, one


def overlap_checks(graded: Graded) -> list[Check]:
    """Two participants' timers overlapping (PR #934), both applications and both interfaces."""
    la, join = LA, JOIN
    out = []
    # PR #934's overlap: MSRP's and MVRP's timers overlap, and MVRP's LeaveAll comes first after MSRP's expiry
    _, swap = graded(((1_000, MSRP, False, 0), (1_040, MVRP, False, 0), (1_181, MSRP, False, 0),
                      (1_221, MVRP, True, 0), (1_371, MSRP, True, 0)),
                     ((1_050, la, 'if0 MSRP'), (1_180, join, 'if0 MSRP'), (1_190, la, 'if0 MVRP'),
                      (1_220, join, 'if0 MVRP'), (1_370, join, 'if0 MSRP')))
    out.append(("two participants' timers overlapping: the MSRP owner's LeaveAll, which MVRP's at 1,221 ms precedes, "
                "skipped MSRP's first opportunity at 1,180 ms and is named there, 191 ms late; MVRP's is sent",
                by(swap) == {'sent': 1, 'skipped': 1} and named(o=swap) == [
                    "o: the LeaveAll timer's run-out at 1050.001 ms (if0 MSRP): its first transmit opportunity at "
                    "1180.000 ms sent an MRPDU without the LeaveAll at 1181.000 ms, and the LeaveAll went at "
                    "1371.000 ms, 191.000 ms after it (LeaveAll past its first transmit opportunity)"], str(swap)))
    _, clean = graded(((1_000, MSRP, False, 0), (1_040, MVRP, False, 0), (1_181, MSRP, True, 0),
                       (1_221, MVRP, True, 0)),
                      ((1_050, la, 'if0 MSRP'), (1_180, join, 'if0 MSRP'), (1_190, la, 'if0 MVRP'),
                       (1_220, join, 'if0 MVRP')))
    _, reordered = graded(((900, MVRP, False, 0), (1_000, MSRP, False, 0), (1_101, MVRP, True, 0),
                           (1_181, MSRP, True, 0)),
                          ((1_050, la, 'if0 MSRP'), (1_100, la, 'if0 MVRP'), (1_180, join, 'if0 MSRP')))
    out.append(("overlapping timers whose owners each send their LeaveAll at their own first opportunity pass, the "
                "LeaveAlls in the expiries' order or in the reverse one (MVRP's at once, MSRP's at its join timer's "
                "run-out)", by(clean) == {'sent': 2} and by(reordered) == {'sent': 2} and not clean['failing'] and
                not reordered['failing'], str((clean, reordered))))
    _, other_if = graded(((1_000, MVRP, False, 1), (1_181, MVRP, False, 1), (1_371, MVRP, True, 1)),
                         ((1_050, la, 'if1 MVRP'), (1_180, join, 'if1 MVRP'), (1_370, join, 'if1 MVRP')))
    _, late_if = graded(((1_000, MSRP, False, 1), (1_240, MSRP, True, 1)),
                        ((1_050, la, 'if1 MSRP'), (1_180, join, 'if1 MSRP')))
    _, gone_mvrp = graded(((1_000, MVRP, False, 0),), ((1_050, la, 'if0 MVRP'),), ordinary=(1_300,))
    four = named(a=other_if, b=late_if, c=gone_mvrp)
    out.append(("skipped, late and absent LeaveAlls are named for either application on either interface: MVRP's "
                "skipped on interface 1, MSRP's late on interface 1, MVRP's absent on interface 0",
                by(other_if) == {'skipped': 1} and by(late_if) == {'late': 1} and by(gone_mvrp) == {'absent': 1}
                and len(four) == 3 and four[0].startswith("a: the LeaveAll timer's run-out at 1050.001 ms (if1 MVRP)")
                and four[1].startswith("b: the LeaveAll timer's run-out at 1050.001 ms (if1 MSRP)")
                and four[2].startswith("c: the LeaveAll timer's run-out at 1050.001 ms (if0 MVRP): no MRPDU of its "
                                       "owner") and four[2].endswith('(LeaveAll absent)'), str(four)))
    _, apart_if = graded(((1_000, MSRP, False, 0), (1_000, MSRP, False, 1), (1_181, MSRP, True, 1),
                          (1_183, MSRP, False, 0), (1_373, MSRP, True, 0)),
                         ((1_050, la, 'if0 MSRP'), (1_180, join, 'if0 MSRP'), (1_370, join, 'if0 MSRP')))
    out.append(("the owner is its interface's too: interface 1's MSRP LeaveAll does not answer interface 0's MSRP "
                "run-out, whose own skipped its first opportunity", by(apart_if) == {'skipped': 1} and
                [f['who'] for f in apart_if['leave_all']['failing']] == ['if0 MSRP'], str(apart_if)))
    return out


def record_checks(graded: Graded, one: list[str]) -> list[Check]:
    """A run-out whose owner the testbench recorded unresolved or did not record, and the run each finding fails."""
    la, join = LA, JOIN
    out = []
    _, unresolved = graded(((1_000, MSRP, False, 0), (1_181, MSRP, True, 0)),
                           ((1_050, la, 'unresolved 0001a2b4'), (1_180, join, 'if0 MSRP')))
    _, unrecorded = graded(((1_000, MSRP, False, 0), (1_181, MSRP, True, 0)), ((1_050, la, None),))
    lost = named(r=unresolved, n=unrecorded)
    out.append(("a LeaveAll timer's run-out with its owner recorded unresolved, or with no owner recorded, is unowned "
                "and named, never bound to the LeaveAll that comes first", by(unresolved) == {'unowned': 1} and
                by(unrecorded) == {'unowned': 1} and lost == [
                    "r: the LeaveAll timer's run-out at 1050.001 ms, its owner recorded unresolved at the expiry "
                    "(LeaveAll owner unresolved)",
                    "n: the LeaveAll timer's run-out at 1050.001 ms, no owner recorded at the expiry (LeaveAll owner "
                    "unresolved)"], str(lost)))
    args = argparse.Namespace(cpu_regions='cover', mutation='none', record_budget_findings=True,
                              record_share_findings=True)
    skip = [n for n in one if n.endswith('(LeaveAll past its first transmit opportunity)')]
    unowned = lost[:1]
    out.append(('a skipped or unowned LeaveAll fails a run whatever findings it records',
                len(skip) == 1 and len(unowned) == 1 and
                run.verdict(args, [scenario.Group('s')], [], [], [], skip) == 1 and
                run.verdict(args, [scenario.Group('r')], [], [], [], unowned) == 1, str((skip, unowned))))
    return out


def anchor_checks(graded: Graded) -> list[Check]:
    """A LeaveAll timer's run-out inside another participant's join interval (PR #934), and where a build that sends
    nothing counts its lateness from (mrpdu_grade.anchor): its timer's owner's first transmit opportunity, from the
    posted TICKs."""
    la, join, pt = LA, JOIN, 'on_pt_timer'
    # MVRP's LeaveAll timer runs out after MSRP's skipped opportunity, inside MSRP's join interval, and goes first
    _, inside = graded(((1_000, MSRP, False, 0), (1_010, MVRP, False, 0), (1_181, MSRP, False, 0),
                        (1_191, MVRP, True, 0), (1_371, MSRP, True, 0)),
                       ((1_050, la, 'if0 MSRP'), (1_180, join, 'if0 MSRP'), (1_185, la, 'if0 MVRP'),
                        (1_190, join, 'if0 MVRP'), (1_370, join, 'if0 MSRP')))
    out = [("a LeaveAll timer's run-out inside another participant's join interval, after its skipped opportunity, "
            "whose LeaveAll goes first: MSRP's is named skipped at its 1,180 ms opportunity, MVRP's is sent",
            by(inside) == {'sent': 1, 'skipped': 1} and named(b=inside) == [
                "b: the LeaveAll timer's run-out at 1050.001 ms (if0 MSRP): its first transmit opportunity at "
                "1180.000 ms sent an MRPDU without the LeaveAll at 1181.000 ms, and the LeaveAll went at 1371.000 ms, "
                "191.000 ms after it (LeaveAll past its first transmit opportunity)"], str(inside))]
    # the periodic timer's run-out at 1,300 ms; MSRP's join timer ran out at 1,180 ms, and a commit at 1,250 ms arms one
    # to the 1,430 ms TICK; each build at 1,360 or 1,460 ms sends nothing
    cases = dict(
        alone=graded(((1_000, MSRP, False, 0),), ((1_300, pt, 'if0 MSRP'),), (1_400,), (1_360,)),
        callback=graded(((1_000, MSRP, False, 0),), ((1_300, pt, 'if0 MSRP'), (1_330, join, 'if0 MVRP')), (1_400,),
                        (1_360,)),
        own=graded(((1_000, MSRP, False, 0), (1_250, MSRP, False, 0)), ((1_300, pt, 'if0 MSRP'),), (), (1_460,)),
        other=graded(((1_000, MSRP, False, 0), (1_250, MVRP, False, 0)), ((1_300, pt, 'if0 MSRP'),), (), (1_460,)),
        unowned=graded(((1_000, MSRP, False, 0), (1_040, MVRP, False, 0)),
                       ((1_300, pt, None), (1_330, join, 'if0 MVRP')), (1_400,), (1_360,)),
        latest=graded(((1_000, MSRP, False, 0), (1_250, MVRP, False, 0)), ((1_300, pt, None),), (), (1_460,)))
    late = {k: ([(f['kind'], f['from_ms'], f['after_ms']) for f in h['failing']], h['runs']['empty'])
            for k, (_, h) in cases.items()}
    said = named_late(cases['callback'][1])
    out.append(("a build that sends nothing is late past THE TRANSMIT's bound after its timer's owner's first transmit "
                "opportunity, from the posted TICKs: not after another participant's join callback (late at 59.979 ms, "
                "a callback at 1,330 ms or not) nor its running join timer; the owner's own running one holds it; and "
                "with no owner recorded, the latest of the participants'", late == {
                    'alone': ([('periodic', 1300.001, 59.979)], 0),
                    'callback': ([('periodic', 1300.001, 59.979)], 1), 'own': ([], 1),
                    'other': ([('periodic', 1300.001, 159.979)], 0),
                    'unowned': ([('periodic', 1300.001, 59.979)], 1), 'latest': ([], 1)} and said == [
                    "c: the periodic timer's run-out at 1300.001 ms, its first frame or build 59.979 ms after its "
                    "participant's transmit opportunity at 1300.001 ms, past THE TRANSMIT's 49 ms (late)"],
                str((late, said))))
    return out


def named_late(held: dict) -> list[str]:
    """A log's late or absent builds as a run names them."""
    return [m for m in run.stated_misses([dict(group='c', passes=dict(joins=held))])
            if m.endswith(('(late)', '(absent)'))]
