# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The self-test's checks of THE RETRY's round costs (round_grade.py; #665, a stated cost is an upper bound): every
round held to AECP_ROUND_COLD_US + n x AECP_NOTICE_US + k x AECP_ATTEMPT_US at its point, n and k read off the calls
inside it, and a round over that failing the run whatever findings it records."""
from __future__ import annotations

import argparse
import re
from collections.abc import Callable

import build
import grade
import round_grade
import run
import scenario

Check = tuple[str, bool, str]
#: What the testbench prints for the round's span and the calls in it (build.py's SPAN and CALL tables).
ROUND, ATTEMPT, BUILT = 'ctrl_loop:round_of', 'aecp_command', 'aecp:finish'


def header_us(interfaces: int) -> dict[str, int]:
    """The round's costs as the headers state them, read here apart from round_grade.stated_us."""
    text = ''.join((scenario.ROOT / 'sw/firmware/ctrl/aecp' / name).read_text() for name in ('aecp.h', 'aecp_mbx.h'))
    macro = lambda name: re.search(rf'^#define {name} (.+)$', text, re.M).group(1)
    pick = lambda name: int(re.findall(r'(\d+)u', macro(name))[1 if interfaces == 1 else 2])
    return dict(cold=pick('AECP_ROUND_COLD_US'), notice=pick('AECP_NOTICE_US'),
                attempt=int(macro('AECP_ATTEMPT_US').rstrip('u')))


def round_checks(synthetic: Callable[[list[str]], str], sys_hz: int, cpu_hz: int) -> list[Check]:
    """A round at its stated cost fits it and one a cycle over does not, by notices built and attempts refused."""
    us = header_us(2)
    limit = lambda n, k: (us['cold'] + n * us['notice'] + k * us['attempt']) * cpu_hz // 1_000_000

    def held(cycles: int, built: int, refused: int, outside: int = 0, interfaces: int = 2) -> dict:
        """The grade of one round of those CPU cycles, its notices and refused attempts, and calls outside it."""
        start = 5000
        lines = [f'PASS 1 {2 * start - 100} {start - 50} {cycles + 100} instr=10 store_mbx=1 W {2 * start}:1:0',
                 f'SPAN {2 * start} {start} {cycles} 00001000 {ROUND}']
        calls = [BUILT] * built + [ATTEMPT] * (built + refused)
        lines += [f'CALL {2 * (start + 1 + n)} {start + 1 + n} {name}' for n, name in enumerate(calls)]
        lines += [f'CALL {2 * (start + cycles + 1 + n)} {start + cycles + 1 + n} {ATTEMPT}'
                  for n in range(outside)]
        lines += [f'CALL {2 * (start - 2 - n)} {start - 2 - n} {BUILT}' for n in range(outside)]
        return grade.grade(synthetic(lines), scenario.Group('g'), sys_hz, cpu_hz, interfaces)['passes']['rounds']

    got = round_grade.stated_us(1), round_grade.stated_us(2)
    out = [("each point's round costs are its headers' own, a notice to 16 recipients cheaper than one to 32",
            got == (header_us(1), us) and got[0]['notice'] < us['notice'], str(got)),
           ('the testbench traces the round and the calls that count its notices and attempts',
            ('ctrl_loop', 'round_of') in build.SPAN_SYMBOLS and {'aecp_command', ('aecp', 'finish')} <=
            set(build.CALL_SYMBOLS), '')]
    fits, misses = [], []
    for n, k in ((0, 0), (1, 0), (4, 0), (2, 3), (0, 6)):
        at, over = held(limit(n, k), n, k), held(limit(n, k) + 1, n, k)
        fits.append(at['over'] == [] and at['rounds'] == 1)
        misses.append([(o['notices'], o['refused']) for o in over['over']] == [(n, k)])
    out.append(('a round at its stated cost, by notices built and attempts refused, fits it and one a cycle over it '
                'does not', all(fits) and all(misses), str((fits, misses))))
    out.append(('calls outside a round count none of its notices or attempts',
                held(limit(0, 0), 0, 0, outside=3)['over'] == [] and held(limit(0, 0) + 1, 0, 0, outside=3)['over'],
                ''))
    one = held(limit(1, 0), 1, 0, interfaces=1)
    out.append(("a round at one interface is held to that point's costs",
                [o['cycles'] for o in one['over']] == [limit(1, 0)], str(one)))
    named = run.stated_misses([dict(group='g', passes=dict(rounds=held(limit(2, 3) + 1, 2, 3)))])
    out.append(('a round over its stated cost is named, with its notices, its refused attempts and the cost it passed',
                named == [f'g: a round of 2 notice(s) and 3 refused attempt(s), {limit(2, 3) + 1:,} CPU cycles, '
                          f'over its stated {limit(2, 3):,}'], str(named)))
    args = argparse.Namespace(cpu_regions='cover', mutation='none', record_budget_findings=True,
                              record_share_findings=True)
    out.append(('a round over its stated cost fails a run whatever findings it records',
                run.verdict(args, [scenario.Group('g')], [], [], [], named) == 1, ''))
    return out
