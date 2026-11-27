# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The costs the rows by every source charge a pass given whole (#665, #894; ctrl_loop.h, CTRL_LOOP_STEP_PASS_US,
CTRL_LOOP_BUILD_PASS_US and CTRL_LOOP_BUILD_ONE_PASS_US; rows_tiers.py). A pass given whole to a build or an aged step
leaves the round after it what that work leaves of its slice, and the rows charge such a pass these costs, so a
dearer pass would leave its slice less than the rows say, with no pass over the share to show it. A pass whose round
found nothing to do is its work alone, and each is held to its stated cost here.

Where a registration's re-declarations stay in the build's own slice (redeclared), each such pass of a registering
group that commits a Listener Message is held to its stated cost by name, and a registering group with none is
refused, so the hold is never vacuous (#977's requirement to measure re-declaring build passes).
"""
from __future__ import annotations

import re
from bisect import bisect_left

import grade
import mrpdu_grade
import scenario
import shape_costs

#: The kinds of pass held to a cost, and the ctrl_loop.h constant that states each.
COSTS = {'step': 'CTRL_LOOP_STEP_PASS_US', 'build': 'CTRL_LOOP_BUILD_PASS_US',
         'build-one': 'CTRL_LOOP_BUILD_ONE_PASS_US'}


#: The modules of THE RETRY's round, and the most a round that finds nothing to do takes of them, in CPU cycles: at
#: most about 500 measured, against 7,000 for one refused attempt.
ROUND_MODULES = ('aecp', 'ctrl_app_aecp', 'ctrl_aecp')
ROUND_IDLE_CYCLES = 1000


def stated_us(interfaces: int | shape_costs.Shape) -> dict[str, int]:
    """Each kind's stated cost in microseconds at a shape, or at that many interfaces at the shipping shape's streams
    (ctrl_loop.h): the builds' as THE SHAPES list them (shape_costs.at; #894's shape ruling, item
    (b)), the step's by the interface count."""
    text = (scenario.ROOT / 'sw/firmware/ctrl/loop/ctrl_loop.h').read_text()
    pattern = r'#define {} \(MBX_N_IF == 1u \? (\d+)u : (\d+)u\)'
    listed = shape_costs.at(interfaces, scenario.ROOT)
    one = shape_costs.interfaces(interfaces) == 1
    return {kind: listed[name] if name in shape_costs.NAMES else
            int(re.search(pattern.format(name), text).group(1 if one else 2)) for kind, name in COSTS.items()}


def within(marks: list[int], start: int, end: int) -> int:
    """How many of the sorted marks fall in [start, end)."""
    return bisect_left(marks, end) - bisect_left(marks, start)


def round_idle(modules: dict[str, int]) -> bool:
    """Whether a pass's AECP modules took no more than a round that finds nothing to do."""
    return sum(cycles for name, cycles in modules.items() if name.startswith(ROUND_MODULES)) <= ROUND_IDLE_CYCLES


def held(log: grade.Log, interfaces: int | shape_costs.Shape) -> dict:
    """Each kind's heaviest pass whose round did nothing, its stated cost in CPU cycles, and each pass over that cost.
    A pass that writes nothing to the mailbox carries no modules, and can carry no round that tried a port."""
    builds = sorted(cycle for cycle, name in log.entries if name == mrpdu_grade.BUILD)
    srp = scenario.CH['srp']
    frames = sorted(cycle for cycle, ch, _ in log.commits if ch == srp)
    limits = {kind: us * log.cpu_hz // 1_000_000 for kind, us in stated_us(interfaces).items()}
    aged = {start for _, start, _, _, was in log.stepped if was}
    span = [(p.start_sys, p.cycles, 'step' if p.start_sys in aged else None) for p in log.passes
            if round_idle(p.modules)]
    written = {p.start_sys for p in log.passes}
    span += [(start, cycles, 'step') for _, start, cycles, _, was in log.stepped if was and start not in written]
    heaviest = dict.fromkeys(COSTS, 0)
    over = []
    for start, cycles, kind in span:
        end = start + cycles * log.sys_hz // log.cpu_hz
        if kind is None and within(builds, start, end):
            kind = 'build' if within(frames, start, end) > 1 else 'build-one'
        if kind is None:
            continue
        heaviest[kind] = max(heaviest[kind], cycles)
        if cycles > limits[kind]:
            over.append(dict(kind=kind, start_sys=start, cycles=cycles))
    return dict(heaviest=heaviest, limits=limits, over=over)


#: A Listener's MSRP AttributeType (IEEE 802.1Q-2018 35.2.2.4, Table 35-1), and the groups whose records re-declare
#: every input's Listener (register_window.py, #977).
LISTENER = 3
REDECLARING = ('srp-register', 'srp-register-burst')
#: The kind a re-declaring build pass over its stated cost is reported as.
REDECLARE = 're-declaring build'


def listener_message(frame: bytes) -> bool:
    """Whether an MSRP frame carries a Listener Message, its Messages walked by their AttributeListLength (IEEE
    802.1Q-2018 35.2.2.4, 10.8.2) to the PDU's EndMark."""
    if len(frame) <= 15 or frame[12:14] != b'\x22\xea':
        return False
    at = 15
    while at + 4 <= len(frame) and frame[at] | frame[at + 1]:
        if frame[at] == LISTENER:
            return True
        at += 4 + int.from_bytes(frame[at + 2:at + 4], 'big')
    return False


def declared_in_build(shape: shape_costs.Shape) -> bool:
    """Whether a shape's registration cost is set and its re-declarations stay in THE TRANSMIT's build slice
    (ctrl_loop.h after THE SHAPES: CTRL_LOOP_SRP_REG_US non-zero, CTRL_LOOP_DECLARE_ALONE 0): 1x1/1if (#977)."""
    text = (scenario.ROOT / shape_costs.HEADER).read_text()
    chain = text[text.index("// THE DRAIN's registration cost"):]
    chain = chain[:chain.index('#endif')]
    pattern = (r'#(?:el)?if CTRL_LOOP_SHAPE\((\d+)u, (\d+)u, (\d+)u\)\n#define CTRL_LOOP_SRP_REG_US (\d+)u\n'
               r'#define CTRL_LOOP_SETTLE_ALONE \d+u\n#define CTRL_LOOP_DECLARE_ALONE (\d+)u')
    return any(shape_costs.Shape(*map(int, head)) == shape and int(reg) != 0 and int(alone) == 0
               for *head, reg, alone in re.findall(pattern, chain))


def redeclared(log: grade.Log, interfaces: int | shape_costs.Shape, group: str) -> dict:
    """A registering group's build passes that commit a Listener Message, at a shape whose re-declarations stay in
    the build's slice (declared_in_build), each against its kind's stated cost, as held() reads both, and each over
    it; refused where the group has none, since the hold would then hold nothing."""
    if group not in REDECLARING or not declared_in_build(shape_costs.shape(interfaces, scenario.ROOT)):
        return dict(passes=[], over=[])
    builds = sorted(cycle for cycle, name in log.entries if name == mrpdu_grade.BUILD)
    srp = scenario.CH['srp']
    frames = sorted(cycle for cycle, ch, _ in log.commits if ch == srp)
    listened = sorted(cycle for cycle, ch, _, frame in log.tx if ch == srp and listener_message(frame))
    limits = {kind: us * log.cpu_hz // 1_000_000 for kind, us in stated_us(interfaces).items()}
    passes, over = [], []
    for p in log.passes:
        end = p.start_sys + p.cycles * log.sys_hz // log.cpu_hz
        if not round_idle(p.modules) or not within(builds, p.start_sys, end) or not within(listened, p.start_sys, end):
            continue
        kind = 'build' if within(frames, p.start_sys, end) > 1 else 'build-one'
        passes.append(dict(kind=kind, start_sys=p.start_sys, cycles=p.cycles, limit=limits[kind]))
        if p.cycles > limits[kind]:
            over.append(dict(kind=REDECLARE, start_sys=p.start_sys, cycles=p.cycles, limit=limits[kind]))
    if not passes:
        raise grade.Refusal(f'{group}: no build pass committed a re-declaration (a Listener Message), where the '
                            'build makes them in its own slice')
    return dict(passes=passes, over=over)
