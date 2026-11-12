# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The rows by every source (#665: decision D's tier bounds, which bind each point's flip, #890): R4, R5 and R6 as
response-time bounds from each source's stated cost and arrival bound, at 1x1/1if and 8x8/2if, and the queued notices
at the bounds the loop search holds; flip_grade.py holds them.

A row's bound is the smallest W (ms) at which the record's own work, plus every source's arrival bound in a window of
length W, each at its stated cost, fits in W: the every-source count, never a measurement (#665: no row is held by
measurement alone). Each arrival bound is a contract rate (sw/mailbox/mailbox.yaml, read from the tree) or a protocol
timer, its clause named below. Each stated cost is the load gate's at this tree's TSN stack pin (load_grade.STATED_US
with the polls' and the headers', load_grade.stated), the polls' items poll_grade.py's, and a LINK event's ROW_COSTS'.
What can precede the row's record is THE DRAIN as ctrl_loop.h states it: SRP's records first, a pass that took more
than CTRL_LOOP_RX_PER_PASS of them taking no other channel's, while the pass has spent less than CTRL_LOOP_DRAIN_US.

The rows, each with its tier's bound (#665: tier 1 20 ms, SRP 90 ms, the last queued notice 125 ms, at every shape):
  R4      the AECP channel's last record of its burst, beside the composed burst, with every notice queued: tier 1
  R5      SRP's last record of its burst, with a link change on every interface inside the window: SRP
  R6      SRP's last record of the composed burst (every channel's burst at once), with every notice queued: SRP
  first   the first queued notice, AECP_QUEUED_FIRST_MS (aecp_mbx.h, which the loop search holds the loop to): tier 1
  last    every notice queued behind it, AECP_QUEUED_MS (aecp_mbx.h, derived from the loop's constants and held by the
          loop search, ctrl_retry_search.py): the last queued notice's

Sources, and their arrival bound in a window of W ms:
  records    channel c: its burst + floor(W / refill_c) (mailbox.yaml `rate`, the fabric's limiter, per channel). A
             record behind the row's in its own ring does not precede it.
  ticks      floor(W / tick_ms) + 1 TICK records (mailbox.yaml tick_ms), each a centisecond to its consumers at the
             larger of their stated cost and CTRL_LOOP_TICK_US.
  timers     coalesced, one record a slot until taken, so at most one an ordinary pass, and no more than the slot's
             protocol timers fire in W: ADP's advertise timer (Milan v1.2 5.6.3.5.9, Table 5.50), its delay re-armed by
             an ADP record (5.6.3.5.3) and each bound sink's discovery aging (5.6.4.5; IEEE 1722.1-2021 6.2.2.5);
             ACMP's TMR_NO_RESP a sink (Milan v1.2 5.5.2.3, Table 5.26); MAAP's probe and announce (IEEE 1722-2016
             B.3.4.1, B.3.4.2, Table B.8); AECP's registrations' probes (Milan v1.2 5.4.5.3), each descriptor's
             counters (5.4.5.2, Table 5.22), the lock (5.4.2.2) and a START.
  gm         coalesced (mailbox.yaml): at most one an interface an ordinary pass, and no more than its sources in
             W: an Announce and a peer delay exchange each at its interval and an announce receipt timeout (IEEE
             802.1AS-2011 10.7.2.2, 11.5.2.2 and 10.7.3.2; load_grade.GM_INTERVALS_MS).
  links      R5 only: one change an interface (the row's definition); its withdrawal and rebuild are items.
  passes     every ordinary pass, at the polls' base and the pass's events' fixed part.
  items      the polls' heavy items, each by its own source: the walk at most one an interface a pass and no more than
             a centisecond's or a build's; the reclaim two an interface a pass and no more than SRP's records and the
             builds; a retained record one a pass and no more than SRP's records; an owed MRPDU two a build; ACMP's
             and AECP's owed frames one a pass and no more than their sources; R5's withdrawal and rebuild one an
             interface.
  rounds     THE RETRY: one a pace past the last (aecp_mbx.h), yielding rounds first, then firm ones, each at
             AECP_ROUND_COLD_US and AECP_NOTICE_US a notice, at most the point's queue of notices.
  builds     THE TRANSMIT: one a JoinTime a participant (IEEE 802.1Q-2018 10.7.4.1, Table 10-7; Milan v1.2 Table 4.3):
             every interface's build of both MRPDUs or twice as many of one, whichever costs more.
  steps      THE STEP: floor(W / (10 (CTRL_LOOP_STEP_AGE + 1))) + 1 aged steps at CTRL_LOOP_STEP_PASS_US.
"""
from __future__ import annotations

import ast
import math
import operator
import re
from pathlib import Path
from typing import NamedTuple

import load_grade
import poll_grade

#: Each row's bound in ms: tier 1, SRP's (half of MRP's JoinTime as the firmware applies it) and the last queued
#: notice's, at every shape (#665, decision D).
BOUNDS = {'R4': 20, 'R5': 90, 'R6': 90, 'first': 20, 'last': 125}
#: The rows the method solves; the queued notices are the tree's derived bounds.
SOLVED = ('R4', 'R5', 'R6')
#: Each point's counts: its interfaces, sinks an interface (all counted on each), the descriptors with counters and
#: the notices a reset can leave pending (load_grade.POINTS; aecp.h, AECP_NOTICES_MOST).
POINTS = ('1x1/1if', '8x8/2if')
#: A LINK event's stated cost in us (the most measured over every instance plus 5 %, rounded up to 5 us): the load has
#: no LINK term, a LINK change having no arrival rate, so its tables do not state it.
ROW_COSTS = {'1x1/1if': {'event.LINK': 150}, '8x8/2if': {'event.LINK': 300}}
#: The sources the docstring names, each a part of every solved row's window (links R5's alone), and the terms of
#: demand() that make each up.
SOURCES = {'records': ('aecp', 'srp', 'others'), 'ticks': ('ticks',), 'timers': ('timers',), 'gm': ('gm',),
           'links': ('links',), 'passes': ('passes',),
           'items': ('item.walk', 'item.reclaim', 'item.retained', 'item.mrpdu', 'item.acmp', 'item.aecp',
                     'item.withdraw', 'item.rebuild'),
           'rounds': ('rounds',), 'builds': ('builds',), 'steps': ('steps',)}
#: The other channels a row's window carries beside SRP's.
OTHERS = ('aecp', 'acmp', 'adp', 'maap')
#: The constants the method reads from the loop's and AECP's headers.
NAMES = ('CTRL_LOOP_DRAIN_US', 'CTRL_LOOP_RX_PER_PASS', 'CTRL_LOOP_STEP_AGE', 'CTRL_LOOP_STEP_PASS_US',
         'CTRL_LOOP_BUILD_PASS_US', 'CTRL_LOOP_BUILD_ONE_PASS_US', 'CTRL_LOOP_SHARE_US', 'CTRL_LOOP_SHARE_MARGIN_US',
         'CTRL_LOOP_TICK_US', 'AECP_NOTICE_US', 'AECP_ROUND_COLD_US', 'AECP_ROUND_PACE_MS', 'AECP_ROUND_YIELD_PACE_MS',
         'AECP_ROUND_YIELD_NOTICES', 'AECP_ROUND_YIELDS', 'AECP_ROUND_FIRM_NOTICES', 'AECP_NOTICES_MOST',
         'AECP_QUEUED_FIRST_MS', 'AECP_QUEUED_MS')


def header(root: Path, n_if: int, texts: dict[str, str] | None = None) -> dict[str, int]:
    """The loop's and AECP's constants at that many interfaces, each expression evaluated (or a planted header's)."""
    text = ''.join((texts or {}).get(p) or (root / p).read_text() for p in load_grade.ROW_HEADERS)
    macros = {m[1]: m[2].split('//')[0].strip() for m in re.finditer(r'^#define (\w+) (.+)$', text, re.M)}
    macros['MBX_N_IF'] = str(n_if)

    def value(name: str) -> int:
        """A constant's integer value: its body with each name it reads replaced by that name's value."""
        body = re.sub(r'(\d+)u\b', r'\1', macros[name])
        body = re.sub(r'[A-Z][A-Z0-9_]+', lambda m: str(value(m[0])), body)
        pick = re.fullmatch(r'\((.+) == (\d+) \? (\d+) : (\d+)\)', body)
        if pick:
            return int(pick[3] if arithmetic(pick[1]) == int(pick[2]) else pick[4])
        return arithmetic(body)
    return {n: value(n) for n in NAMES}


#: The operators a header's integer expression may use, as C evaluates them on unsigned operands.
OPERATORS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.floordiv}


def arithmetic(text: str) -> int:
    """An integer expression of the headers' (constants, + - * /, parentheses), evaluated as C's unsigned arithmetic
    would for these positive operands; any other form is refused."""
    def walk(node: ast.AST) -> int:
        """The node's value."""
        if isinstance(node, ast.Constant) and isinstance(node.value, int):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in OPERATORS:
            return OPERATORS[type(node.op)](walk(node.left), walk(node.right))
        raise ValueError(f'{text!r} is not an integer expression of the headers\' form')
    return walk(ast.parse(text, mode='eval').body)


def costs(root: Path, point: str, table: dict | None = None) -> dict[str, float]:
    """A point's stated costs: the load gate's at the pin (or a planted table), the polls' items and ROW_COSTS'."""
    c = load_grade.stated(root, point, table or load_grade.STATED_US)
    polls = poll_grade.stated_us(load_grade.POINTS[point]['n_if'])
    for k in ('withdraw', 'rebuild', 'aecp'):
        c[f'item.{k}'] = polls[k]
    c['item.retained'] = max(c['item.retained'], c['record.srp'])
    return {**c, **ROW_COSTS[point]}


def contract(root: Path) -> tuple[dict[str, tuple[int, int]], int]:
    """Each receive channel's (burst, refill_ms) and the TICK period, from the mailbox contract."""
    y = load_grade.parsed((root / 'sw/mailbox/mailbox.yaml').read_text())
    return {c['name']: (c['rate']['burst'], c['rate']['refill_ms']) for c in y['channels']}, y['tick_ms']


def rounds_us(h: dict, w_ms: float) -> tuple[float, int]:
    """THE RETRY's rounds a window holds beside records: the yielding ones, then firm ones, at their stated costs."""
    room = h['CTRL_LOOP_SHARE_US'] - h['CTRL_LOOP_SHARE_MARGIN_US'] - h['AECP_ROUND_COLD_US']
    per = max(1, min(h['AECP_ROUND_FIRM_NOTICES'], room // h['AECP_NOTICE_US']))
    left, t, us, n = h['AECP_NOTICES_MOST'], 0.0, 0.0, 0
    for _ in range(h['AECP_ROUND_YIELDS']):
        if t > w_ms or left <= 0:
            break
        built = min(left, h['AECP_ROUND_YIELD_NOTICES'])
        us += h['AECP_ROUND_COLD_US'] + built * h['AECP_NOTICE_US']
        left, t, n = left - built, t + h['AECP_ROUND_YIELD_PACE_MS'], n + 1
    while t <= w_ms and left > 0:
        built = min(left, per)
        us += h['AECP_ROUND_COLD_US'] + built * h['AECP_NOTICE_US']
        left, t, n = left - built, t + h['AECP_ROUND_PACE_MS'], n + 1
    return us, n


def timer_us(s: dict, c: dict, w_ms: float, passes: int, rate: dict) -> float:
    """The timer slots' events in W, each slot at most one an ordinary pass and no more than its timers fire."""
    sinks = s['sinks_per_if']
    adp = min(passes, 2 + math.floor(w_ms / rate['adp'][1]) + sinks)
    acmp = min(passes, sinks)
    maap = min(passes, 1)
    aecp = min(passes, s['registrations'] * s['n_if'] + s['counter_descriptors'] + 2)
    return s['n_if'] * (adp * c['event.ADP'] + acmp * c['event.ACMP'] + maap * c['event.MAAP']) + aecp * c['event.AECP']


def builds(h: dict, s: dict) -> tuple[float, int]:
    """THE TRANSMIT's builds in any window under a JoinTime: their cost and their count."""
    both, one = s['n_if'] * h['CTRL_LOOP_BUILD_PASS_US'], 2 * s['n_if'] * h['CTRL_LOOP_BUILD_ONE_PASS_US']
    return (both, s['n_if']) if both >= one else (one, 2 * s['n_if'])


class Inputs(NamedTuple):
    """A point's inputs to the method: its header constants, stated costs, counts, channel rates and TICK period."""

    h: dict
    c: dict
    s: dict
    rate: dict
    tick_ms: int


def demand(row: str, inputs: Inputs, w_ms: float) -> dict[str, float]:
    """Each source's work in microseconds in a window of w_ms before the row's record is taken."""
    h, c, s, rate, tick_ms = inputs
    out = {}
    n_if, cap = s['n_if'], h['CTRL_LOOP_RX_PER_PASS']
    def arrive(ch: str) -> int:
        """The channel's records in the window: its burst and a record a refill."""
        return rate[ch][0] + math.floor(w_ms / rate[ch][1])
    ticks = math.floor(w_ms / tick_ms) + 1
    out['ticks'] = ticks * (c['event.TICK'] + max(c['centisecond'], h['CTRL_LOOP_TICK_US']))
    link, burst = row == 'R5', rate['srp'][0]
    if row == 'R4':
        out['aecp'] = rate['aecp'][0] * c['record.aecp']
        # AECP takes its cap a pass, THE DRAIN's channel first: SRP's backlog, refilled while it drains, all ahead
        aecp_passes = math.ceil(rate['aecp'][0] / cap) + ticks
        draining = max(0.0, w_ms - out['aecp'] / 1000)
        out['srp'] = (burst + math.floor(draining / rate['srp'][1])) * c['record.srp']
    else:
        out['srp'] = burst * c['record.srp']
    cost_b, count_b = builds(h, s)
    passes, timers, events = 1, 0.0, 0.0
    held = (n_if + 1) if link else 0
    for _ in range(60):
        timers = timer_us(s, c, w_ms, passes, rate)
        events = out['ticks'] + timers
        drained = math.ceil((out['srp'] + events) / h['CTRL_LOOP_DRAIN_US'])
        n = (aecp_passes + 1 + drained) if row == 'R4' else (1 + drained + held)
        if n == passes:
            break
        passes = n
    out['timers'] = timers
    if row == 'R4':
        out['others'] = sum(min(arrive(o), passes * cap) * c[f'record.{o}'] for o in OTHERS if o != 'aecp')
    else:
        light = math.floor(events / max(1, h['CTRL_LOOP_DRAIN_US'] - cap * c['record.srp'])) + held
        out['others'] = sum(min(arrive(o), light * cap) * c[f'record.{o}'] for o in OTHERS)
    gm = sum(math.floor(w_ms / ms) + 1 for ms in load_grade.GM_INTERVALS_MS)
    out['gm'] = n_if * min(passes, gm) * c['event.GM']
    out['builds'] = cost_b
    out['steps'] = (math.floor(w_ms / (10 * (h['CTRL_LOOP_STEP_AGE'] + 1))) + 1) * h['CTRL_LOOP_STEP_PASS_US']
    srp_in = arrive('srp')
    out['item.walk'] = min(passes * n_if, n_if * (ticks + count_b)) * c['item.walk']
    out['item.reclaim'] = min(2 * n_if * passes, 2 * (srp_in + count_b)) * c['item.reclaim']
    out['item.retained'] = min(passes, srp_in) * c['item.retained']
    out['item.mrpdu'] = min(passes, 2 * count_b) * c['item.mrpdu']
    out['item.acmp'] = min(passes, arrive('acmp') + arrive('adp') + n_if * s['sinks_per_if']) * c['item.acmp']
    out['item.aecp'] = min(passes, arrive('aecp') + n_if * s['registrations']) * c['item.aecp']
    if link:
        out['item.withdraw'] = n_if * c['item.withdraw']
        out['item.rebuild'] = n_if * c['item.rebuild']
        out['links'] = n_if * c['event.LINK']
    out['passes'] = passes * (c['events_none'] + c['base'])
    out['rounds'] = rounds_us(h, w_ms)[0]
    return out


def solve(row: str, inputs: Inputs, dropped: str | None = None) -> tuple[float | None, dict[str, float]]:
    """The smallest W in ms, in steps of 0.01, at which every source's work fits; None if none under 2,000 ms. A term
    `dropped` is left out (the controls': each source must lengthen W)."""
    w, d = 0.01, {}
    while w < 2000:
        d = {k: v for k, v in demand(row, inputs, w).items() if k != dropped}
        total = sum(d.values()) / 1000
        if total <= w:
            return w, d
        w = max(w + 0.01, math.ceil(total * 100) / 100)
    return None, d


def point_inputs(root: Path, point: str, table: dict | None = None, texts: dict | None = None) -> Inputs:
    """A point's header constants, stated costs, counts and contract."""
    s = dict(load_grade.POINTS[point])
    h = header(root, s['n_if'], texts)
    s['notices'] = h['AECP_NOTICES_MOST']
    rate, tick_ms = contract(root)
    return Inputs(h, costs(root, point, table), s, rate, tick_ms)


def rows(root: Path, point: str, table: dict | None = None, texts: dict | None = None,
         dropped: str | None = None, inputs: Inputs | None = None) -> dict[str, tuple[float | None, dict[str, float]]]:
    """Each row's W in ms with its terms in ms, the queued notices' the tree's derived bounds; `inputs`, a point's
    point_inputs() already read."""
    inputs = inputs or point_inputs(root, point, table, texts)
    h = inputs.h
    out = {}
    for row in SOLVED:
        w, d = solve(row, inputs, dropped)
        out[row] = (w, {k: v / 1000 for k, v in d.items()})
    out['first'] = (float(h['AECP_QUEUED_FIRST_MS']), {'AECP_QUEUED_FIRST_MS': float(h['AECP_QUEUED_FIRST_MS'])})
    out['last'] = (float(h['AECP_QUEUED_MS']), {'AECP_QUEUED_MS': float(h['AECP_QUEUED_MS'])})
    return out


def documented() -> set[str]:
    """The sources the module's docstring names, each a line of its source list."""
    part = __doc__.split('Sources, and their arrival bound')[1]
    return set(re.findall(r'^  ([a-z]+) {2,}', part, re.M))


def unsourced(root: Path, points: tuple[str, ...] = POINTS) -> list[str]:
    """Each source the docstring names that a solved row's window does not count, and each term no source names."""
    out = [f'the source {name} names no term of the method' for name in sorted(documented() - set(SOURCES))]
    out += [f'the method counts a source the docstring does not name: {name}' for name in sorted(set(SOURCES) -
                                                                                              documented())]
    for point in points:
        for row in SOLVED:
            terms = rows(root, point)[row][1]
            for name, keys in SOURCES.items():
                if (name != 'links' or row == 'R5') and not any(terms.get(k, 0.0) > 0 for k in keys):
                    out.append(f'{point} {row}: the source {name} is not counted')
            out += [f'{point} {row}: the term {k} has no source' for k in terms
                    if not any(k in keys for keys in SOURCES.values()) and k not in ('AECP_QUEUED_FIRST_MS',
                                                                                    'AECP_QUEUED_MS')]
    return out


def findings(root: Path, points: tuple[str, ...] = POINTS, table: dict | None = None, bounds: dict | None = None,
             texts: dict | None = None) -> list[str]:
    """Each row over its tier's bound at each point, with its largest term."""
    out = []
    for point in points:
        for row, (w, terms) in rows(root, point, table, texts).items():
            top = max(terms, key=terms.get)
            b = (bounds or BOUNDS)[row]
            if w is None or w > b:
                shown = 'no W under 2,000 ms' if w is None else f'{w:.2f} ms'
                out.append(f'{point} {row}: by every source {shown}, over its bound {b} ms; the largest term {top} '
                           f'{terms[top]:.2f} ms')
    return out


def report(root: Path, points: tuple[str, ...] = POINTS) -> list[str]:
    """Each row at each point: its W, its bound, its residual and its three largest terms."""
    lines = ['| Point | Row | By every source, ms | Bound, ms | Residual, ms | Largest terms, ms |',
             '|---|---|---:|---:|---:|---|']
    for point in points:
        for row, (w, terms) in rows(root, point).items():
            top = ', '.join(f'{k} {v:.2f}' for k, v in sorted(terms.items(), key=lambda t: -t[1])[:3])
            shown, residual = ('none under 2,000', '') if w is None else (f'{w:.2f}', f'{w - BOUNDS[row]:+.2f}')
            lines.append(f'| {point} | {row} | {shown} | {BOUNDS[row]} | {residual} | {top} |')
    return lines
