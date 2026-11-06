# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""THE TRANSMIT's row (#665; ctrl_loop.h; FR_NFR.md 3.4.1): under every channel at its refill rate, each MRPDU a join,
periodic or LeaveAll timer made owed, timed from the deadline, the centisecond whose TICK ran the timer out, to the TX
commit of the frame that answers it.

A timer that runs out with nothing to send owes nothing, and lwSRP reports no such thing: a build after it that sends
no frame shows it. So a timer's row ends at the frames of the builds that follow it, the first and, where the other
interface owes one too, the one after: at most one ordinary pass stands between two (ctrl_loop.c, whole_runs).
"""
from __future__ import annotations

import grade
import scenario

#: The lwSRP callbacks that end a timer (mrp_mad.c), and the row's name for each.
TIMERS = {'on_join_timer': 'join', 'on_pt_timer': 'periodic', 'on_la_timer': 'leaveall'}
#: The function each MRPDU's build enters (srp_mbx.c).
BUILD = 'build_mrpdu'
#: MBX_EV_TYPE_TICK (mbx_contract.h): a TICK event's type, the low byte of its first word.
TICK = 4
PATH = 'mrpdu'
#: How far a row looks for its builds: past any bound, so a build that is late is a row over it, never no row.
LOOK_MS = 100


def ticks(log: grade.Log) -> list[int]:
    """Each centisecond's TICK, by the cycle its record was posted."""
    return [cycle for cycle, words in log.records if words[0] & 0xFF == TICK]


def commits(grader: grade.Grader, entry: int) -> list[tuple[int, int]]:
    """The (cycle, interface) of the frames of the builds after a timer's entry, as the module docstring says."""
    log = grader.log
    srp = scenario.CH['srp']
    limit = entry + int(LOOK_MS * log.sys_hz / 1000)
    builds = [c for c, name in log.entries if name == BUILD and entry < c < limit]
    passes = [p for p in log.passes
              if p.start_sys + p.cycles * log.sys_hz // log.cpu_hz > entry and p.start_sys < limit]
    out: list[tuple[int, int]] = []
    ordinary = 0
    for p in passes:
        end = p.start_sys + p.cycles * log.sys_hz // log.cpu_hz
        if not any(p.start_sys <= c < end for c in builds):
            ordinary += 1 if out else 0
            if ordinary > 1:
                break
            continue
        sent = [(c, i) for c, ch, i, _ in log.tx if ch == srp and p.start_sys <= c < end]
        if not sent and not out:
            return []
        out += sent
        ordinary = 0
        if len({i for _, i in out}) == 2:
            break
    return out


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
