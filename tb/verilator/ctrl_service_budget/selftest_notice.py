# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The self-test's checks of the retried notice's row (#665, notice_window.py): it is timed from the port's answer to
its last recipient's commit, a row later than its 20 ms fails the run whatever its options record, build.py's age-less
plant is caught only when every group's row is late, its aged build's plant only when every group's timer-driven MRPDU
is over its bound, and every group holds its load across the answer; of the queue's rows, and of THE TRANSMIT's.

selftest.py passes its synthetic-log helpers in, so this module imports nothing of it.
"""
from __future__ import annotations

import argparse
import contextlib
import io
from collections.abc import Callable

import build
import grade
import mrpdu_grade
import notice_window
import run
import scenario

Check = tuple[str, bool, str]
AECP = scenario.CH['aecp']
CTL1 = scenario.CTL1
#: The answer's entry and the first recipient's commit, in bus cycles; the last recipient's commit is the case's own.
ANSWER, FIRST = 101_000, 801_000
#: The cycle of the synthetic TICK, and the clocks the synthetic logs are read at.
TICK_AT, SYS_HZ, CPU_HZ = 5_000, 100_000_000, 100_000_000


def row(synthetic: Callable, one: Callable, tx_sequence: Callable, aem_response: Callable, last: int) -> dict:
    """A retried notice's probe over its port's answer and its two recipients' commits, the last at last."""
    notice = lambda ctl, seq: aem_response(ctl, seq, command=0x000F, unsolicited=True, descriptor=(5, 0))
    probe = scenario.Probe('n.stream_info.if0', "a retried notice, from its port's answer (THE RETRY)", 'notify',
                           'entry:retry_port_answers', [f'notify:{AECP}:000f:5:0'], recipients=((CTL1, 0), (CTL1, 1)),
                           until='notice.end', path=notice_window.PATH)
    lines = ['MARK 1000 n.stream_info.if0', f'ENTRY {ANSWER} retry_port_answers',
             *tx_sequence(AECP, [(0, notice(CTL1, 1), FIRST), (1, notice(CTL1, 2), last)]),
             f'MARK {last + 1000} notice.end']
    return one(synthetic(lines), probe)


def quietly(action: Callable[[], int]) -> int:
    """A verdict without its CONTROL line."""
    with contextlib.redirect_stdout(io.StringIO()):
        return action()


def timer_rows(synthetic: Callable, tx_sequence: Callable, commit: int, built: bool = True) -> list[dict]:
    """A held group's timer rows: a TICK posted at TICK_AT, its join timer's end, a pass with its build and a commit."""
    srp = scenario.CH['srp']
    frame = bytes(60)
    sent = tx_sequence(srp, [(0, frame, commit)]) if built else []
    lines = ['MARK 1000 load', f'EVW {TICK_AT} 0 {mrpdu_grade.TICK:08x}', f'EVW {TICK_AT} 1 00000001',
             f'EVW {TICK_AT} 2 00000000', f'EVW {TICK_AT} 3 00000000', f'ENTRY {TICK_AT + 100} on_join_timer',
             f'ENTRY {commit - 2000} build_mrpdu',
             f'PASS 1 {commit - 3000} {commit - 3000} 5000 instr=10 store_mbx=1 W {commit - 1000}:1:0', *sent]
    log = grade.parse(synthetic(lines), SYS_HZ, CPU_HZ)
    group = scenario.Group('notice-retried-0', save=dict(loaded=True, origin='load'))
    return mrpdu_grade.rows(grade.Grader(log), group)


def timer_checks(synthetic: Callable, tx_sequence: Callable) -> list[Check]:
    """THE TRANSMIT's row: from the TICK that ran the timer out to the commit, against T_svc, and none for no frame."""
    within = timer_rows(synthetic, tx_sequence, TICK_AT + 1_900_000)
    late = timer_rows(synthetic, tx_sequence, TICK_AT + 2_100_000)
    none = timer_rows(synthetic, tx_sequence, TICK_AT + 1_900_000, built=False)
    return [("a timer's MRPDU is timed from its TICK to its commit, 19 ms within its 20 ms",
             len(within) == 1 and within[0]['ms'] == 19.0 and within[0]['within_budget'] is True, str(within)),
            ('one at 21 ms is over its bound', len(late) == 1 and late[0]['within_budget'] is False, str(late)),
            ('a timer that ends with nothing to send, whose build sends no frame, has no row', none == [], str(none))]


def queue_checks() -> list[Check]:
    """The queued notices' bounds: read from the headers, each point's own, the first of a queue held to its own."""
    got = notice_window.queued_ms(1), notice_window.queued_ms(2)
    first = notice_window.queued_first_ms(1), notice_window.queued_first_ms(2)
    rows = lambda first, last, bound: [dict(group='g', probes=[
        dict(status='measured', path=[notice_window.QUEUED, 0], ms=first, budget_ms=bound, within_budget=True),
        dict(status='measured', path=[notice_window.QUEUED, 0], ms=last, budget_ms=bound,
             within_budget=last <= bound)])]
    verdicts = tuple(len(run.notice_misses(rows(a, b, notice_window.queued_ms(n)), n)) for a, b, n in
                     ((21.5, 57.0, 2), (22.5, 57.0, 2), (21.5, 63.0, 2), (19.5, 21.0, 1), (20.5, 21.0, 1)))
    return [("a queued notice's bound is the constants', 22 ms at one interface and 62 ms at two", got == (22, 62),
             str(got)),
            ("a queue's first notice's bound is the constants', T_svc at one interface and 22 ms at two",
             first == (20, 22), str(first)),
            ("a queue's first notice is held to its point's own bound and every other to the queue's bound",
             verdicts == (0, 1, 1, 0, 1), str(verdicts))]


def notice_checks(synthetic: Callable, one: Callable, tx_sequence: Callable, aem_response: Callable,
                  points: list[scenario.Point]) -> list[Check]:
    """Every check of the retried notice's row."""
    within = row(synthetic, one, tx_sequence, aem_response, ANSWER + 1_500_000)
    late = row(synthetic, one, tx_sequence, aem_response, ANSWER + 2_200_000)
    out = [("a retried notice is timed from its port's answer, the entry, to its last recipient's commit",
            within.get('ms') == 15.0 and within.get('within_budget') is True, str(within)),
           ('a retried notice 22 ms after its answer misses its 20 ms bound, though within its 24 ms ceiling',
            late.get('within_budget') is False and late.get('within_ceiling') is True, str(late))]
    args = argparse.Namespace(cpu_regions='cover', mutation='none', record_budget_findings=True,
                              record_share_findings=True)
    g = scenario.Group('notice-retried-0')
    timed = dict(path=['mrpdu', 0], status='measured')
    results = lambda r: [dict(group='notice-retried-0', probes=[r, timed])]
    verdicts = tuple(run.verdict(args, [g], [], [], [], run.notice_misses(results(r), 2)) for r in (within, late))
    out.append(('a retried notice later than its bound fails the run whatever the options record, and one within '
                'it passes', verdicts == (0, 1), str(verdicts)))
    untimed = run.notice_misses([dict(group='notice-retried-0', probes=[within])], 2)
    out.append(('a group that holds its load across the timers with no MRPDU they owed fails the run',
                len(untimed) == 1 and 'no timer-driven MRPDU' in untimed[0], str(untimed)))
    control = argparse.Namespace(cpu_regions='cover', mutation='retry-ageless', record_budget_findings=True,
                                 record_share_findings=True)
    names = notice_window.names()
    caught = tuple(quietly(lambda n=n: run.verdict(control, [g], [], [], [], [f'{name}: late' for name in n]))
                   for n in (names, names[1:]))
    never = [f'{name}.stream_info.if0: no end: no notification to [x]' for name in names]
    caught += tuple(quietly(lambda r=r: run.verdict(control, [g], r, [], [], [])) for r in
                    (never, never[1:], [*never, 'notice-retried-0.held.srp.if0: refused']))
    out.append(("the age-less plant is caught only when every group's retried notice is later than its bound or never "
                "committed in its window, with no other refusal", caught == (0, 1, 0, 1, 1), str(caught)))
    out.append(("the age-less plant runs every group of the answering-later arm, and that arm's run takes them alone",
                build.MUTATIONS['retry-ageless'][3:] == (','.join(names), 'answering-later')
                and [x.name for x in run.all_groups(points[0], dict(variant='answering-later'))] == names, ''))
    srp = argparse.Namespace(cpu_regions='cover', mutation='transmit-aged', record_budget_findings=True,
                             record_share_findings=True)
    held = lambda n, row='mrpdu.join': [f'{name}.{row}.if1: 21.000 ms over its budget 20 ms' for name in n]
    built = tuple(quietly(lambda m=m: run.verdict(srp, [g], [], m, [], []))
                  for m in (held(names), held(names[1:]), held(names, 'held.srp')))
    out.append(("the aged build's plant is caught only when every group's timer-driven MRPDU is over its bound, not "
                "by another row", built == (0, 1, 1), str(built)))
    out.append(("the aged build's plant runs every group of the answering-later arm",
                build.MUTATIONS['transmit-aged'][3:] == (','.join(names), 'answering-later'), ''))
    out += timer_checks(synthetic, tx_sequence)
    out += queue_checks()
    wrong = []
    for p in points:
        for group in notice_window.groups(p):
            steps = group.steps
            load, flood, end = (steps.index(s) for s in ('mark notice.load', 'flood gm 1', 'flood gm 0'))
            bind = next(n for n, s in enumerate(steps) if s.startswith('wait ms ') and
                        int(s.split()[2]) >= notice_window.BIND_MS)
            held_ms = notice_window.ANSWER_MS + notice_window.RUN_MS - notice_window.LOAD_MS
            if not (bind < load < flood < end and notice_window.LOAD_MS < notice_window.ANSWER_MS <
                    notice_window.LOAD_MS + held_ms and group.save.get('origin') == 'notice.load'):
                wrong.append(group.name)
    out.append(('every retried notice group binds before its load, floods and holds every channel across the '
                "port's answer, and grades its held records from the load's mark", not wrong, str(wrong)))
    return out
