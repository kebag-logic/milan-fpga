# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The self-test's checks of the retried notice's row (#665, notice_window.py): it is timed from the port's answer to
its last recipient's commit, a row later than its 20 ms fails the run whatever its options record, build.py's age-less
plant is caught only when every group's row is late, and every group holds its load across the answer.

selftest.py passes its synthetic-log helpers in, so this module imports nothing of it.
"""
from __future__ import annotations

import argparse
import contextlib
import io
from collections.abc import Callable

import build
import notice_window
import run
import scenario

Check = tuple[str, bool, str]
AECP = scenario.CH['aecp']
CTL1 = scenario.CTL1
#: The answer's entry and the first recipient's commit, in bus cycles; the last recipient's commit is the case's own.
ANSWER, FIRST = 101_000, 801_000


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
    results = lambda r: [dict(group='notice-retried-0', probes=[r])]
    verdicts = tuple(run.verdict(args, [g], [], [], [], run.notice_misses(results(r))) for r in (within, late))
    out.append(('a retried notice later than its bound fails the run whatever the options record, and one within '
                'it passes', verdicts == (0, 1), str(verdicts)))
    control = argparse.Namespace(cpu_regions='cover', mutation='retry-ageless', record_budget_findings=True,
                                 record_share_findings=True)
    names = notice_window.names()
    caught = tuple(quietly(lambda n=n: run.verdict(control, [g], [], [], [], [f'{name}: late' for name in n]))
                   for n in (names, names[1:]))
    out.append(("the age-less plant is caught only when every group's retried notice is later than its bound",
                caught == (0, 1), str(caught)))
    out.append(("the age-less plant runs every group of the answering-later arm, and that arm's run takes them alone",
                build.MUTATIONS['retry-ageless'][3:] == (','.join(names), 'answering-later')
                and [x.name for x in run.all_groups(points[0], dict(variant='answering-later'))] == names, ''))
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
