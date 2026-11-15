# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""THE TRANSMIT's row (#665; ctrl_loop.h; FR_NFR.md 3.4.1): under every channel at its refill rate, each MRPDU a join,
periodic or LeaveAll timer made owed, timed from the deadline, the centisecond whose TICK ran the timer out, to the TX
commit of the frame that answers it.

A timer that runs out with nothing to send owes nothing, and lwSRP reports no such thing: a build after it that sends
no frame shows it. So a timer's run-out is resolved by the builds that follow it, wherever they come, with no horizon
(#894's egress ruling of 2026-11-13, item 4; resolve): the first after it and, where the other participant or
interface owes one too, the next, at most one ordinary or idle pass standing between two (ctrl_loop.c, whole_runs), each
build's frames those it commits and those it leaves owed, which only the poll sends, before the next build (A3). The
run-out is `released` where they send frames, `empty` where the first sends none, `late` where its first frame, or its
first build where it sends none, comes past THE TRANSMIT's bound after it (LATE_MS), `absent` where no build follows it
in a log that runs on past that bound, and `unresolved` where the log ends first. A late or absent build fails the run
(join_grade.held); an unresolved one is counted and named, never taken for one that owes nothing.
"""
from __future__ import annotations

from bisect import bisect_left, bisect_right
from pathlib import Path

import grade
import scenario
from tier1_rows import tx_budget_ms

#: The lwSRP callbacks that end a timer (mrp_mad.c), and the row's name for each.
TIMERS = {'on_join_timer': 'join', 'on_pt_timer': 'periodic', 'on_la_timer': 'leaveall'}
#: The function each MRPDU's build enters (srp_mbx.c).
BUILD = 'build_mrpdu'
#: MBX_EV_TYPE_TICK (mbx_contract.h): a TICK event's type, the low byte of its first word.
TICK = 4
PATH = 'mrpdu'
#: THE TRANSMIT's bound in ms as ctrl_loop.h derives it (CTRL_LOOP_TX_BOUND_MS, tier1_rows.tx_budget_ms): a run-out's
#: build past it is late, and a log that runs on past it with no build after a run-out has none.
LATE_MS = tx_budget_ms((Path(__file__).resolve().parents[3] / 'sw/firmware/ctrl/loop/ctrl_loop.h').read_text())
#: The outcomes of a timer's run-out (resolve), and those that fail a run.
OUTCOMES = ('released', 'empty', 'late', 'absent', 'unresolved')
FAILING = ('late', 'absent')


def ticks(log: grade.Log) -> list[int]:
    """Each centisecond's TICK, by the cycle its record was posted."""
    return [cycle for cycle, words in log.records if words[0] & 0xFF == TICK]


def commits(grader: grade.Grader, entry: int) -> list[tuple[int, int]]:
    """The (cycle, interface) of the frames of the builds after a timer's entry, as the module docstring says."""
    return released(grader.log, entry)


def released(log: grade.Log, entry: int) -> list[tuple[int, int]]:
    """commits' frames, from the log alone: what the timer that ran out at entry released, late or not (join_grade.py
    too)."""
    outcome, frames = resolve(log, entry)
    return frames if outcome in ('released', 'late') else []


def end_of(log: grade.Log, p: grade.Pass) -> int:
    """A pass's end, in bus cycles."""
    return p.start_sys + p.cycles * log.sys_hz // log.cpu_hz


#: index's last log and what it found there.
_INDEXED: list = [None, None]


def index(log: grade.Log) -> tuple[list[int], list[grade.Pass], list[tuple[int, int]], int]:
    """A log's builds, its passes and its SRP frames, each in time order, and its last cycle: the last millisecond it
    records, or its last pass's end."""
    if _INDEXED[0] is not log:
        srp = scenario.CH['srp']
        passes = sorted(log.passes, key=lambda p: p.start_sys)
        last = max([*log.ms.values(), *(end_of(log, p) for p in passes), 0])
        _INDEXED[:] = [log, (sorted(c for c, name in log.entries if name == BUILD), passes,
                             sorted((c, i) for c, ch, i, _ in log.tx if ch == srp), last)]
    return _INDEXED[1]


def resolve(log: grade.Log, entry: int) -> tuple[str, list[tuple[int, int]]]:
    """The outcome (OUTCOMES) of the timer that ran out at entry, and the (cycle, interface) of the frames its builds
    sent, as the module docstring says."""
    builds, passes, sent, last = index(log)
    starts = [p.start_sys for p in passes]
    late = entry + int(LATE_MS * log.sys_hz / 1000)
    k = bisect_right(builds, entry)
    if k == len(builds):
        return ('absent' if last > late else 'unresolved'), []

    def pass_at(cycle: int) -> int:
        """The index of the pass a build at that cycle ran in."""
        return max(0, bisect_right(starts, cycle) - 1)
    run, at = [builds[k]], pass_at(builds[k])
    for b in builds[k + 1:]:
        # every pass between the two, idle ones too (a pass's index counts them), but those that send what a build
        # left owed
        between = passes[at + 1:pass_at(b)]
        owed = sum(1 for p in between if bisect_left(sent, (p.start_sys, -1)) < bisect_left(sent, (end_of(log, p), -1)))
        if passes[pass_at(b)].index - passes[at].index - 1 - owed > 1:
            break
        run.append(b)
        at = pass_at(b)
    first = passes[pass_at(run[0])].start_sys if passes else run[0]
    stop = builds[k + len(run)] if k + len(run) < len(builds) else 1 << 62
    frames, interfaces, own = [], set(), sent[bisect_left(sent, (first, -1)):bisect_left(sent, (stop, -1))]
    for cycle, interface in own:
        if len(interfaces) == 2 and interface not in interfaces:
            break
        frames.append((cycle, interface))
        interfaces.add(interface)
    head = frames[0][0] if frames else run[0]
    return ('late' if head > late else 'released' if frames else 'empty'), frames


def outcomes(log: grade.Log) -> list[tuple[int, str, str]]:
    """Each timer's run-out of the log: its cycle, its timer's row name (TIMERS) and its outcome."""
    return [(entry, TIMERS[name], resolve(log, entry)[0]) for entry, name in log.entries if name in TIMERS]


def rows(grader: grade.Grader, group: scenario.Group) -> list[dict]:
    """A held group's timer rows: for each timer and interface the longest, each a row of its own."""
    if not group.save or not group.save.get('loaded'):
        return []
    log = grader.log
    origin = next(cycle for cycle, name in log.marks if name == group.save.get('origin', 'save.change'))
    posted = ticks(log)
    worst: dict[tuple[str, int], tuple[int, int]] = {}
    for entry, name in log.entries:
        if name not in TIMERS or entry < origin:
            continue
        deadline = max((c for c in posted if c <= entry), default=None)
        if deadline is None or deadline < origin:
            continue
        for end, interface in commits(grader, entry):
            key = (TIMERS[name], interface)
            if key not in worst or end - deadline > worst[key][1] - worst[key][0]:
                worst[key] = (deadline, end)
    out = []
    for (kind, interface), (deadline, end) in sorted(worst.items()):
        probe = scenario.Probe(f'{group.name}.mrpdu.{kind}.if{interface}',
                               f'an MRPDU its {kind} timer owes, the longest', 'srp', 'tick', [], path=PATH)
        ms = grader.ms(end - deadline)
        out.append(dict(probe=probe.name, row=probe.row, family=probe.family, interface=interface,
                        path=list(probe.path_key()), start_sys=deadline, end_sys=end, wait_ms=0.0, ring='srp', ahead=0,
                        sys_cycles=end - deadline, cpu_cycles=grader.cpu_cycles(end - deadline), ms=round(ms, 5),
                        passes=len(grader.window_passes(deadline, end)), status='measured',
                        **grade.verdicts(ms, probe)))
    return out
