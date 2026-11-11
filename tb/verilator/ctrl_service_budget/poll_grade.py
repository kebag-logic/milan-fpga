# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The polls by source (#665): a light base every ordinary pass runs, and the heavy work,
each item its own function, which does its work only once its source has posted it, each at a stated cost.

A pass's polls run from the first firmware poll's entry, ADP's, to the last one's return, SRP's delivery (the
composition's order: ADP, ACMP, MAAP, AECP and its delivery, SRP and its delivery; a test fixture's poll comes after
them all). That section less the items inside it is the pass's base, which every ordinary pass is charged. Each item:

  withdraw   SRP's withdrawal of an interface whose link went down (srp_mbx.c, reset_interface), entered in the poll
             that sees the link level change; its source is a link change, one an interface
  rebuild    SRP's new participants for an interface whose link came back (open_interface), one interface a poll; a
             link change, one an interface
  walk       SRP's walk of a registrar whose attributes changed since the last (snapshot: lwSRP's mrp_attr_visit,
             entered only while the interface is stale); its sources are an attribute's state change, which an SRP
             record, a centisecond of lwSRP's timers and a declaration of THE TRANSMIT's make
  reclaim    lwSRP's reclaim of an interface's freed attributes (mrp_reclaim, entered only once a record or a build
             left one to free); its source is an SRP record or a build
  retained   SRP's retry of a record its participant refused for storage (apply_receive, one waits at a time); its
             source is an SRP record
  mrpdu      an MRPDU a build left owed (build_mrpdu, A3 of ctrl_loop.h, one a poll); its source is THE TRANSMIT's build
  acmp       ACMP's owed frame (acmp_mbx.c's poll, which sends one when ACMP owes one: A3); its sources are ACMP's
             responses and commands, from a record, an ADP record or a TMR_NO_RESP. A call that committed no ACMP frame
             sent nothing and is the base's
  aecp       AECP's owed response, a completed command's notification or a probe (aecp.c's transmit, which sends only
             what the core owes); its sources are AECP's records, its applies and its registrations' monitors. A call
             that committed no AECP frame sent nothing and is the base's

An item nested in another (a walk inside a retained record's apply) is that one's, counted once. Calls outside the polls
(a record's own apply, a build's MRPDU, a round's notices, the LINK event's withdrawal) are their own source's, not the
polls'. A record's own apply, SRP's (apply_receive outside the polls, the record's handler's: RECORD), is the work its
retained retry repeats, so it is held to the same stated cost (#665): an SRP record
dearer than its retry's stated cost fails the gate as the retry would.

Each cost is the most measured over every group at its point plus 5 %, rounded up to 5 us (100 CPU cycles a
microsecond on the split CPU), or where no group stages an item the cost of the measured work that holds it (STATED_US):
a stated cost is an upper bound, and a gate fails when any measured instance exceeds it
(#665). Each item's arrival bound, from its source's protocol timer or
contract rate, is the response-time method's (docs/design/SPLIT_CONTROL_MEMORY.md section 13).
"""
from __future__ import annotations

from bisect import bisect_left

import grade
import poll_items
import scenario

#: A pass's first and last firmware poll, and each item's traced function and its sending channel (poll_items).
FIRST, LAST, ITEMS = poll_items.FIRST, poll_items.LAST, poll_items.ITEMS
#: The stated costs in microseconds at 1x1/1if and 8x8/2if: each the most measured over every group of arm A and the
#: answering-every-port arm at its point plus 5 %, rounded up to 5 us. No group stages a retained record or an MRPDU
#: its ring refused, so those two have no measured line: a retained record's retry is the apply an SRP record's handler
#: makes, stated at the SRP record's cost (250 and 365 us), and an owed MRPDU is a part of a build of one, stated at
#: that pass's cost (CTRL_LOOP_BUILD_ONE_PASS_US, 405 and 1,215 us). The SRP record's and AECP's item (a notice to the
#: registered controllers) are measured on the image whose notice is built once and addressed per recipient and whose
#: SRP comparisons are same()'s (#665: the notice and SRP record cuts), over every group of both arms.
STATED_US = {1: dict(base=155, withdraw=90, rebuild=290, walk=20, reclaim=25, retained=250, mrpdu=405, acmp=65,
                    aecp=210),
             2: dict(base=280, withdraw=245, rebuild=630, walk=60, reclaim=35, retained=365, mrpdu=1215, acmp=185,
                    aecp=270)}


#: An SRP record's own apply (srp_mbx:apply_receive outside the polls), held to the retained item's stated cost.
RECORD = 'record'


def stated_us(interfaces: int) -> dict[str, int]:
    """The base's and each item's stated cost in microseconds at that many interfaces."""
    return dict(STATED_US[interfaces])


def spans(log: grade.Log) -> dict[str, list[tuple[int, int, int]]]:
    """Each traced label's spans, sorted: (CPU cycle it started, CPU cycles, bus cycle it started)."""
    out: dict[str, list[tuple[int, int, int]]] = {}
    for kind, *rest in log.traced:
        if kind == 'SPAN' and len(rest) >= 5:
            out.setdefault(rest[4], []).append((int(rest[1]), int(rest[2]), int(rest[0])))
    for v in out.values():
        v.sort()
    return out


def sections(traced: dict[str, list[tuple[int, int, int]]]) -> list[tuple[int, int, int]]:
    """Each pass's polls: (CPU cycle the first poll entered, the cycle the last returned, the bus cycle it began),
    the last poll the first one after it, before the next pass's first."""
    firsts, lasts = traced.get(FIRST, []), traced.get(LAST, [])
    out = []
    starts = [s for s, _, _ in lasts]
    for k, (start, _, start_sys) in enumerate(firsts):
        nxt = firsts[k + 1][0] if k + 1 < len(firsts) else 1 << 62
        j = bisect_left(starts, start)
        if j < len(lasts) and lasts[j][0] < nxt:
            out.append((start, lasts[j][0] + lasts[j][1], start_sys))
    return out


def committed(log: grade.Log) -> dict[int, list[int]]:
    """Each channel's TX commits, the bus cycles sorted."""
    out: dict[int, list[int]] = {}
    for cycle, ch, _ in log.commits:
        out.setdefault(ch, []).append(cycle)
    for v in out.values():
        v.sort()
    return out


def instances(log: grade.Log, traced: dict, commits: dict[int, list[int]], start: int,
              end: int) -> list[tuple[str, int]]:
    """The items inside a pass's polls that did their work, outermost first, each (kind, CPU cycles)."""
    found = []
    for kind, (label, channel) in ITEMS.items():
        rows = traced.get(label, [])
        for s, cycles, s_sys in rows[bisect_left(rows, (start, -1, -1)):]:
            if s >= end:
                break
            if channel is not None:
                marks = commits.get(scenario.CH[channel], [])
                end_sys = s_sys + cycles * log.sys_hz // log.cpu_hz
                if bisect_left(marks, end_sys) == bisect_left(marks, s_sys):
                    continue
            found.append((s, s + cycles, kind))
    return outermost(found)


def outermost(found: list[tuple[int, int, str]]) -> list[tuple[str, int]]:
    """The items no other contains, each (kind, CPU cycles): one nested in another is that one's."""
    outer, reach = [], -1
    for s, e, kind in sorted(found, key=lambda r: (r[0], -r[1])):
        if s >= reach:
            outer.append((kind, e - s))
            reach = e
    return outer


def held(log: grade.Log, interfaces: int) -> dict:
    """Each pass's base and each item against its stated cost in CPU cycles: the passes, the heaviest of each, and
    every one over its cost."""
    limits = {kind: us * log.cpu_hz // 1_000_000 for kind, us in stated_us(interfaces).items()}
    limits[RECORD] = limits['retained']
    traced, commits = spans(log), committed(log)
    heaviest = dict.fromkeys(limits, 0)
    over = []
    every = sections(traced)
    for start, end, start_sys in every:
        items = instances(log, traced, commits, start, end)
        base = end - start - sum(cycles for _, cycles in items)
        for kind, cycles in [('base', base), *items]:
            heaviest[kind] = max(heaviest[kind], cycles)
            if cycles > limits[kind]:
                over.append(dict(kind=kind, start_sys=start_sys, cycles=cycles))
    # each SRP record's own apply: an apply_receive call in no pass's polls
    polls = [(start, end) for start, end, _ in every]
    for s, cycles, s_sys in traced.get(ITEMS['retained'][0], []):
        k = bisect_left(polls, (s + 1, -1)) - 1
        if k >= 0 and polls[k][0] <= s < polls[k][1]:
            continue
        heaviest[RECORD] = max(heaviest[RECORD], cycles)
        if cycles > limits[RECORD]:
            over.append(dict(kind=RECORD, start_sys=s_sys, cycles=cycles))
    return dict(passes=len(every), heaviest=heaviest, limits=limits, over=over)
