# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The costs THE RETRY's round is admitted at (#665; aecp_mbx.h, AECP_NOTICE_US and AECP_ROUND_COLD_US; aecp.h,
AECP_ATTEMPT_US). A round spends what its pass has left at these stated costs (aecp.c, scan; aecp_mbx.c, retry), and
THE RETRY's search counts the notices a pass carries from them (sw/firmware/ctrl/test/ctrl_retry_search.py), so a round
dearer than its stated cost would overspend its pass with no row to show it. Each is an upper bound: every round the
loop calls (ctrl_loop.c's round_of, a SPAN line) is held here to AECP_ROUND_COLD_US + n x AECP_NOTICE_US + k x
AECP_ATTEMPT_US, n the notices it built, each a success of the event scan (aecp.c's finish, a CALL line inside the
round), and k its refused attempts, its aecp_command calls (CALL lines) less n.
"""
from __future__ import annotations

import re
from bisect import bisect_left

import grade
import scenario

#: The round's span and the calls inside it that count its notices and attempts.
ROUND = 'ctrl_loop:round_of'
ATTEMPT = 'aecp_command'
BUILT = 'aecp:finish'


def stated_us(interfaces: int) -> dict[str, int]:
    """The round's stated costs in microseconds at that many interfaces: once, a notice and a refused attempt."""
    ctrl = scenario.ROOT / 'sw/firmware/ctrl/aecp'
    mailbox, core = (ctrl / 'aecp_mbx.h').read_text(), (ctrl / 'aecp.h').read_text()
    pick = lambda name: int(re.search(rf'#define {name} \(MBX_N_IF == 1u \? (\d+)u : (\d+)u\)', mailbox)
                            .group(1 if interfaces == 1 else 2))
    attempt = int(re.search(r'#define AECP_ATTEMPT_US (\d+)u', core).group(1))
    return dict(cold=pick('AECP_ROUND_COLD_US'), notice=pick('AECP_NOTICE_US'), attempt=attempt)


def inside(cycles: list[int], start: int, end: int) -> int:
    """How many of the sorted CPU cycles fall in [start, end): the calls a round made."""
    return bisect_left(cycles, end) - bisect_left(cycles, start)


def rounds(log: grade.Log) -> list[dict]:
    """Every round the log traced: its start, CPU cycles, the notices it built and its refused attempts."""
    calls = {name: sorted(int(rest[1]) for kind, *rest in log.traced if kind == 'CALL' and rest[2] == name)
             for name in (ATTEMPT, BUILT)}
    within = lambda name, start, end: inside(calls[name], start, end)
    out = []
    for kind, *rest in log.traced:
        if kind != 'SPAN' or rest[4] != ROUND:
            continue
        start, cycles = int(rest[1]), int(rest[2])
        built = within(BUILT, start, start + cycles)
        out.append(dict(start_sys=int(rest[0]), cycles=cycles, notices=built,
                        refused=within(ATTEMPT, start, start + cycles) - built))
    return out


def held(log: grade.Log, interfaces: int) -> dict:
    """Each round against its stated cost in CPU cycles: the rounds, the heaviest by notices built, and those over."""
    us = stated_us(interfaces)
    every = rounds(log)
    heaviest: dict[int, int] = {}
    over = []
    for r in every:
        limit = (us['cold'] + r['notices'] * us['notice'] + r['refused'] * us['attempt']) * log.cpu_hz // 1_000_000
        heaviest[r['notices']] = max(heaviest.get(r['notices'], 0), r['cycles'])
        if r['cycles'] > limit or r['refused'] < 0:
            over.append(dict(r, limit=limit))
    return dict(rounds=len(every), heaviest={str(n): c for n, c in sorted(heaviest.items())}, stated=us, over=over)
