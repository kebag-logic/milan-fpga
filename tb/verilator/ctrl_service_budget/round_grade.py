# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The costs THE RETRY's round is admitted at (#665; aecp_mbx.h, AECP_NOTICE_US and AECP_ROUND_COLD_US; aecp.h,
AECP_ATTEMPT_US). A round spends what its slice has left at these stated costs (aecp.c, scan; aecp_mbx.c, retry), and
the rows by every source charge its notices at them (rows_tiers.py, THE TIERS in ctrl_loop.h, #894), so a round
dearer than its stated cost would overspend its pass with no row to show it. Each is an upper bound: every round the
loop calls (ctrl_loop.c's round_of, a SPAN line) is held here to AECP_ROUND_COLD_US + n x AECP_NOTICE_US + k x
AECP_ATTEMPT_US, n the notices it built, each a success of the event scan (aecp.c's finish, a CALL line inside the
round), and k its refused attempts, its aecp_command calls (CALL lines) less n. Each cost is read at the image's shape
(THE SHAPES, shape_costs.py): AECP_ROUND_COLD_US and AECP_ATTEMPT_US are the shape's own, never the interface count's
(#894's ruling issuecomment-6878014227, item 1), and AECP_NOTICE_US is the interface count's, as aecp_mbx.h derives it.
"""
from __future__ import annotations

from bisect import bisect_left

import grade
import scenario
import shape_costs

#: The round's span and the calls inside it that count its notices and attempts.
ROUND = 'ctrl_loop:round_of'
ATTEMPT = 'aecp_command'
BUILT = 'aecp:finish'


def stated_us(given: int | shape_costs.Shape) -> dict[str, int]:
    """The round's stated costs in microseconds at an image's shape, or at that many interfaces at the shipping
    shape's streams (shape_costs.shape): once, a notice and a refused attempt, each as aecp_mbx.h and aecp.h derive it
    there, through the costs ctrl_loop.h lists for the shape (shape_costs.at) and its interface count."""
    ctrl = scenario.ROOT / 'sw/firmware/ctrl/aecp'
    text = (ctrl / 'aecp_mbx.h').read_text() + (ctrl / 'aecp.h').read_text()
    values = {**shape_costs.at(given, scenario.ROOT), 'MBX_N_IF': shape_costs.interfaces(given)}
    value = lambda name: shape_costs.evaluated(text, name, values)
    return dict(cold=value('AECP_ROUND_COLD_US'), notice=value('AECP_NOTICE_US'), attempt=value('AECP_ATTEMPT_US'))


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


def held(log: grade.Log, given: int | shape_costs.Shape) -> dict:
    """Each round against its stated cost in CPU cycles at the image's shape (or interface count, stated_us): the
    rounds, the heaviest by notices built, and those over."""
    us = stated_us(given)
    every = rounds(log)
    heaviest: dict[int, int] = {}
    over = []
    for r in every:
        limit = (us['cold'] + r['notices'] * us['notice'] + r['refused'] * us['attempt']) * log.cpu_hz // 1_000_000
        heaviest[r['notices']] = max(heaviest.get(r['notices'], 0), r['cycles'])
        if r['cycles'] > limit or r['refused'] < 0:
            over.append(dict(r, limit=limit))
    return dict(rounds=len(every), heaviest={str(n): c for n, c in sorted(heaviest.items())}, stated=us, over=over)
