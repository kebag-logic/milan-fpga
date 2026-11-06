# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The costs THE RETRY's search rests on (#665; ctrl_loop.h, CTRL_LOOP_STEP_PASS_US, CTRL_LOOP_BUILD_PASS_US and
CTRL_LOOP_BUILD_ONE_PASS_US; sw/firmware/ctrl/test/ctrl_retry_search.py). A pass given whole to a build or an aged step
leaves the round after it what that work leaves of THE SHARE, and the search counts the notices such a pass carries
from these costs, so a dearer pass would carry fewer notices than the bound says, with no pass over the share to show
it. A pass whose round found nothing to do is its work alone, and each is held to its stated cost here.
"""
from __future__ import annotations

import re
from bisect import bisect_left

import grade
import mrpdu_grade
import scenario

#: The kinds of pass held to a cost, and the ctrl_loop.h constant that states each.
COSTS = {'step': 'CTRL_LOOP_STEP_PASS_US', 'build': 'CTRL_LOOP_BUILD_PASS_US',
         'build-one': 'CTRL_LOOP_BUILD_ONE_PASS_US'}


#: The modules of THE RETRY's round, and the most a round that finds nothing to do takes of them, in CPU cycles: at
#: most about 500 measured, against 7,000 for one refused attempt.
ROUND_MODULES = ('aecp', 'ctrl_app_aecp', 'ctrl_aecp')
ROUND_IDLE_CYCLES = 1000


def stated_us(interfaces: int) -> dict[str, int]:
    """Each kind's stated cost in microseconds at that many interfaces (ctrl_loop.h)."""
    text = (scenario.ROOT / 'sw/firmware/ctrl/loop/ctrl_loop.h').read_text()
    pattern = r'#define {} \(MBX_N_IF == 1u \? (\d+)u : (\d+)u\)'
    return {kind: int(re.search(pattern.format(name), text).group(1 if interfaces == 1 else 2))
            for kind, name in COSTS.items()}


def within(marks: list[int], start: int, end: int) -> int:
    """How many of the sorted marks fall in [start, end)."""
    return bisect_left(marks, end) - bisect_left(marks, start)


def round_idle(modules: dict[str, int]) -> bool:
    """Whether a pass's AECP modules took no more than a round that finds nothing to do."""
    return sum(cycles for name, cycles in modules.items() if name.startswith(ROUND_MODULES)) <= ROUND_IDLE_CYCLES


def held(log: grade.Log, interfaces: int) -> dict:
    """Each kind's heaviest pass whose round did nothing, its stated cost in CPU cycles, and each pass over that cost.
    A pass that writes nothing to the mailbox carries no modules, and can carry no round that tried a port."""
    builds = sorted(cycle for cycle, name in log.entries if name == mrpdu_grade.BUILD)
    limits = {kind: us * log.cpu_hz // 1_000_000 for kind, us in stated_us(interfaces).items()}
    aged = {start for _, start, _, _, was in log.stepped if was}
    span = [(p.start_sys, p.cycles, 'step' if p.start_sys in aged else None) for p in log.passes
            if round_idle(p.modules)]
    written = {p.start_sys for p in log.passes}
    span += [(start, cycles, 'step') for _, start, cycles, _, was in log.stepped if was and start not in written]
    heaviest = dict.fromkeys(COSTS, 0)
    over = []
    for start, cycles, kind in span:
        made = within(builds, start, start + cycles * log.sys_hz // log.cpu_hz)
        if kind is None and made:
            kind = 'build' if made > 1 else 'build-one'
        if kind is None:
            continue
        heaviest[kind] = max(heaviest[kind], cycles)
        if cycles > limits[kind]:
            over.append(dict(kind=kind, start_sys=start, cycles=cycles))
    return dict(heaviest=heaviest, limits=limits, over=over)
