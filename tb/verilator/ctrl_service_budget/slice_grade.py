# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""THE TIERS' slices against their stated length (#894; #665's round 23 ruling, item 1: tier-2 work runs only in slices
of at most a stated length, and a gate fails any slice over it). The length is ctrl_loop.h's CTRL_LOOP_SLICE_US, and
each slice is measured from where the loop starts it:

- SRP's records in an ordinary pass (THE DRAIN's channel), from the pass's start to the end of its last record's
  handler, srp_mbx's receive (a SPAN line);
- a pass given whole to THE TRANSMIT's build, from its start to its end, THE RETRY's round after the build in the same
  slice (the build is the ENTRY of build_mrpdu inside the pass);
- every other round of THE RETRY, ctrl_loop.c's round_of (a SPAN line), from its own start: an aged step's, whose slice
  starts after the step, and an ordinary pass's own.

The testbench's pass boundary and a span's entry come before the loop's clock read, so a slice measures no shorter than
the loop's own. A pass that writes nothing to the mailbox prints no PASS line: its build sent no frame and its round
committed none, and the round's SPAN line is graded alone.
"""
from __future__ import annotations

import re
from bisect import bisect_left

import grade
import mrpdu_grade
import round_grade
import scenario

#: The stated slice length and the spans that end or make a slice.
SLICE = 'CTRL_LOOP_SLICE_US'
RECORD = 'srp_mbx:receive'
ROUND = round_grade.ROUND
BUILD = mrpdu_grade.BUILD


def stated_us(interfaces: int) -> int:
    """The slice length ctrl_loop.h states at that many interfaces, in microseconds."""
    text = (scenario.ROOT / 'sw/firmware/ctrl/loop/ctrl_loop.h').read_text()
    pick = re.search(rf'^#define {SLICE} \(MBX_N_IF == 1u \? (\d+)u : (\d+)u\)$', text, re.M)
    return int(pick.group(1 if interfaces == 1 else 2))


def claimed(inside: list[tuple[int, int, int, str]]) -> set[int]:
    """The rounds a pass given whole to a build holds in its own slice, by their CPU starts."""
    return {cpu for cpu, _, _, label in inside if label == ROUND}


def origin(p: grade.Pass, records: list[tuple[int, int]]) -> int:
    """Where SRP's slice starts, in CPU cycles: its pass's start, which ctrl_loop.c counts the slice's end from."""
    return p.start_cpu


def slices(log: grade.Log) -> list[dict]:
    """Every tier-2 slice the log shows: its kind, its start in bus cycles and its length in CPU cycles."""
    spans = sorted((int(rest[1]), int(rest[2]), int(rest[0]), rest[4]) for kind, *rest in log.traced
                   if kind == 'SPAN' and rest[4] in (RECORD, ROUND))
    starts = [s[0] for s in spans]
    builds = sorted(cycle for cycle, name in log.entries if name == BUILD)
    out, held_rounds = [], set()
    for p in log.passes:
        end_sys = p.start_sys + p.cycles * log.sys_hz // log.cpu_hz
        inside = spans[bisect_left(starts, p.start_cpu):bisect_left(starts, p.start_cpu + p.cycles)]
        if bisect_left(builds, end_sys) > bisect_left(builds, p.start_sys):
            out.append(dict(kind='build', start_sys=p.start_sys, cycles=p.cycles))
            held_rounds |= claimed(inside)
            continue
        records = [(cpu, cpu + cycles) for cpu, cycles, _, label in inside if label == RECORD]
        if records:
            out.append(dict(kind='srp', start_sys=p.start_sys,
                            cycles=max(end for _, end in records) - origin(p, records)))
    out += [dict(kind='round', start_sys=sys, cycles=cycles) for cpu, cycles, sys, label in spans
            if label == ROUND and cpu not in held_rounds]
    return sorted(out, key=lambda s: s['start_sys'])


def held(log: grade.Log, interfaces: int) -> dict:
    """Each kind's longest slice, the point's stated length in CPU cycles, and each slice over it."""
    limit = stated_us(interfaces) * log.cpu_hz // 1_000_000
    every = slices(log)
    longest = {kind: max((s['cycles'] for s in every if s['kind'] == kind), default=0)
               for kind in ('srp', 'build', 'round')}
    return dict(slices=len(every), longest=longest, limit=limit, over=[s for s in every if s['cycles'] > limit])
