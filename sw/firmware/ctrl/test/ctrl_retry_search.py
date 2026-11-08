# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""THE RETRY's bound by construction (#665; aecp_mbx.h, AECP_QUEUED_PASSES): a search of ctrl_loop_service's choices.

Each pass is charged all of THE SHARE. What a pass does is the loop's rule, read from ctrl_loop.c and restated here;
what it may be asked to do is the search: at every pass, whether records wait, whether THE DRAIN's channel holds some,
whether a build or an aged step takes a pass given whole, within the counts a window admits, and when in the spacing
the queue's retry falls due. The latest commit over all of them must fit the constants aecp_mbx.h states.

The counts, at a window of ms milliseconds: THE DRAIN's passes (ctrl_loop.h); a build of both of an interface's MRPDUs
once an interface, or of one of them twice, since a participant sends once a JoinTime and owes one pass for an
Applicant that moves with its join timer idle; and an aged step each CTRL_LOOP_STEP_AGE + 1 centiseconds dispatched,
which lag their ticks by at most what THE TRANSMIT's bound allows them.

A notice whose port refuses is not in the queue, and costs a round AECP_ATTEMPT_US: a round tries each of
AECP_ROUND_PORTS ports once (aecp.c, scan). So each search also runs with every count of refusing ports a queue admits,
its notices out of the queue and its attempts charged to every round ahead of the notices, whether or not they are due,
which no round can exceed. A port's attempt is a window read, which answers for every notice it serves or for none, and
every port serves one (ports), so a queue has a port answering: at most AECP_ROUND_PORTS - 1 refuse. Where two counts
leave a round, a step and a build the same room, the fewer refusals leave the longer queue, so only that one is
searched.

A pass given whole to a build or an aged step may have no room for a notice past its attempts, and is searched carrying
none. The round's own pass must have room for one, or a queue beside refused attempts would never be served.
"""
from __future__ import annotations

import ast
import operator
import re
import sys
from dataclasses import dataclass, replace
from functools import lru_cache
from pathlib import Path
from typing import NamedTuple

CTRL = Path(__file__).resolve().parents[1]


def arithmetic(text: str) -> int:
    """An integer expression of + - * and //, which is all the macros this search reads hold."""
    operators = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.FloorDiv: operator.floordiv}

    def walk(node: ast.expr) -> int:
        """A node's value: a constant, or an operator on two others."""
        if isinstance(node, ast.Constant):
            return int(node.value)
        if isinstance(node, ast.BinOp) and type(node.op) in operators:
            return operators[type(node.op)](walk(node.left), walk(node.right))
        raise ValueError(f'not arithmetic: {text}')

    return walk(ast.parse(text.strip(), mode='eval').body)


def constants(interfaces: int) -> dict[str, int]:
    """The headers' constants at that many interfaces, every macro this search reads evaluated in integers."""
    text = ''.join((CTRL / name).read_text(encoding='utf-8') for name in
                   ('loop/ctrl_loop.h', 'aecp/aecp.h', 'aecp/aecp_mbx.h'))
    macros = {m[1]: m[2] for m in re.finditer(r'^#define (\w+) (.+)$', text, re.M)}
    macros['MBX_N_IF'] = str(interfaces)

    def value(name: str) -> int:
        """A macro's integer value: arithmetic on other macros, or `(X == n ? a : b)`."""
        body = re.sub(r'(\d+)u\b', r'\1', macros[name])
        body = re.sub(r'[A-Z][A-Z0-9_]+', lambda m: str(value(m[0])), body).replace('/', '//')
        conditional = re.fullmatch(r'\((.+) == (\d+) \? (\d+) : (\d+)\)', body)
        if conditional:
            return int(conditional[3] if arithmetic(conditional[1]) == int(conditional[2]) else conditional[4])
        return arithmetic(body)

    names = ('CTRL_LOOP_WHOLE_RUN', 'CTRL_LOOP_TX_MS', 'CTRL_LOOP_SHARE_US', 'CTRL_LOOP_SHARE_MARGIN_US',
             'CTRL_LOOP_STEP_PASS_US', 'CTRL_LOOP_BUILD_PASS_US', 'CTRL_LOOP_BUILD_ONE_PASS_US',
             'CTRL_LOOP_SRP_DRAINS', 'CTRL_LOOP_STEP_AGE', 'CTRL_LOOP_T_SVC_MS', 'AECP_RETRY_MAX_MS',
             'AECP_REGISTRATIONS', 'AECP_NOTICE_US', 'AECP_ROUND_PACE_MS', 'AECP_ROUND_YIELD_PACE_MS',
             'AECP_ROUND_YIELD_NOTICES', 'AECP_ROUND_YIELDS', 'AECP_ROUND_FIRM_NOTICES', 'AECP_QUEUED_PASSES',
             'AECP_QUEUED_MS', 'AECP_QUEUED_CEILING_MS', 'AECP_QUEUED_FIRST_MS', 'AECP_NOTICES_MOST',
             'AECP_ATTEMPT_US', 'AECP_ROUND_PORTS', 'AECP_ROUND_COLD_US')
    out = {name: value(name) for name in names}
    out['refusing'] = len(ports(interfaces)) - 1
    return out


def ports(interfaces: int) -> list[str]:
    """The ports a round tries, one attempt each (aecp.h, AECP_ROUND_PORTS; aecp.c, scan): GET_STREAM_INFO's and
    GET_COUNTERS', which every notice of those commands reads through the first interface's window, and each AVB
    interface's GET_AVB_INFO and GET_AS_PATH, through its own. Each serves a notice of Milan v1.2 Table 5.22 at every
    shape: every shape has a stream, and every AVB interface its GET_AVB_INFO and GET_AS_PATH notices."""
    return ['GET_STREAM_INFO', 'GET_COUNTERS', *(f'{command} {i}' for i in range(interfaces)
                                                 for command in ('GET_AVB_INFO', 'GET_AS_PATH'))]


@dataclass(frozen=True)
class Window:
    """One search: what the passes given whole carry and how many of each the window admits."""
    notices: int
    round_carries: int
    step_carries: int
    build_carries: int
    builds: int
    steps: int
    drains: int
    yields: int
    yield_notices: int
    firm_notices: int
    pace_ms: int
    yield_pace_ms: int
    whole_run: int
    spacing_ms: int
    pass_ms: int


class State(NamedTuple):
    """Where the loop stands as a pass starts, and what the window has left to do to it."""
    t: int
    left: int
    run: int
    whole: int
    backlog: bool
    firm: bool
    spent: int
    events: bool
    pace: int
    held: bool
    drains: int
    builds: int
    steps: int
    due: int


def given(w: Window, s: State) -> list[State]:
    """The passes given whole that may run next: a build, an aged step, or the round alone (ctrl_loop.c)."""
    out = []
    ready = s.held and s.t >= s.pace
    for build in (False, True) if s.builds else (False,):
        for step in (False, True) if s.steps and not build else (False,):
            if not ready and not build and not step:
                continue
            n = s._replace(t=s.t + w.pass_ms, run=0, whole=s.whole + 1, builds=s.builds - build, steps=s.steps - step)
            if ready:
                most = w.build_carries if build else w.step_carries if step else w.round_carries
                yielding = w.yields != 0 and s.backlog and not s.firm
                built = min(s.left, w.yield_notices if yielding else min(most, w.firm_notices) if s.backlog else most)
                spent = s.spent + (1 if s.backlog and built else 0) if s.left > built else 0
                n = n._replace(left=s.left - built, spent=spent, firm=spent + 1 > w.yields, held=s.left > built,
                               pace=s.t + (w.yield_pace_ms if s.backlog and not s.firm else w.pace_ms))
            out.append(n)
    return out


def ordinary(w: Window, s: State) -> list[State]:
    """An ordinary pass: its poll holds a retry due by then, and it may leave records or THE DRAIN's behind."""
    return [s._replace(t=s.t + w.pass_ms, run=s.run + 1, whole=0, backlog=wait or drain, events=drain,
                       held=s.held or s.t >= s.due, drains=s.drains - drain)
            for wait in (False, True) for drain in ((False, True) if s.drains else (False,))]


def latest(w: Window, target: int) -> int:
    """The latest ms the target-th notice of the queue commits, counted from its port's answer."""
    left_after = w.notices - target

    @lru_cache(maxsize=None)
    def go(s: State) -> int:
        """The latest commit from a state: the pass given whole where one may run, else an ordinary one."""
        if s.left <= left_after:
            return s.t
        may = s.run != 0 or (s.whole < w.whole_run and (not s.backlog or s.firm) and not s.events)
        return max(go(n) for n in (given(w, s) if may else []) or ordinary(w, s))

    return max(go(State(w.pass_ms, w.notices, run, whole, backlog, firm, w.yields if firm else 0, events, 0, False,
                        w.drains, w.builds, w.steps, due))
               for due in range(w.spacing_ms + 1) for run in (0, 1) for whole in range(w.whole_run)
               for backlog in (False, True) for firm in ((True,) if w.yields == 0 else (False, True))
               for events in (False, True))


@lru_cache(maxsize=None)
def searched(w: Window) -> tuple[int, int]:
    """The first and the last notice's latest commit in a window, searched once whatever the constants it is checked
    against."""
    return latest(w, 1), latest(w, w.notices)


def windows(c: dict[str, int], interfaces: int) -> list[Window]:
    """The searches of a point: its builds of both MRPDUs and its builds of one, at each count of refusing ports."""
    margin = c['CTRL_LOOP_SHARE_US'] - c['CTRL_LOOP_SHARE_MARGIN_US'] - c['AECP_ROUND_COLD_US']
    centiseconds = (c['AECP_QUEUED_MS'] + c['CTRL_LOOP_TX_MS']) // 10
    steps = 1 + (centiseconds - 1) // (c['CTRL_LOOP_STEP_AGE'] + 1)
    common = dict(notices=c['AECP_NOTICES_MOST'], steps=steps, drains=c['CTRL_LOOP_SRP_DRAINS'],
                  yields=c['AECP_ROUND_YIELDS'], yield_notices=c['AECP_ROUND_YIELD_NOTICES'],
                  firm_notices=c['AECP_ROUND_FIRM_NOTICES'],
                  pace_ms=c['AECP_ROUND_PACE_MS'], yield_pace_ms=c['AECP_ROUND_YIELD_PACE_MS'],
                  whole_run=c['CTRL_LOOP_WHOLE_RUN'], spacing_ms=c['AECP_RETRY_MAX_MS'],
                  pass_ms=c['CTRL_LOOP_SHARE_US'] // 1000)
    out = []
    for build_us, builds in ((c['CTRL_LOOP_BUILD_PASS_US'], interfaces),
                             (c['CTRL_LOOP_BUILD_ONE_PASS_US'], 2 * interfaces)):
        rooms = {}
        for refused in range(c['refusing'] + 1):
            carries = lambda spent_us, k=refused: (margin - spent_us - k * c['AECP_ATTEMPT_US']) // c['AECP_NOTICE_US']
            rooms.setdefault((carries(0), carries(c['CTRL_LOOP_STEP_PASS_US']), carries(build_us)), refused)
        for (whole, step, build), refused in rooms.items():
            window = Window(round_carries=whole, step_carries=step, build_carries=build, builds=builds, **common)
            out.append(replace(window, notices=c['AECP_NOTICES_MOST'] - refused))
    return out


#: What the first notice of a queue may take, in ms, by interfaces: T_svc at 1x1/1if, and 22 ms at 8x8/2if by the
#: maintainer's decision of 2026-11-08 (FR_NFR.md 3.4.1).
FIRST_ALLOWED_MS = {1: 20, 2: 22}


def findings(interfaces: int, planted: dict[str, int] | None = None) -> tuple[list[str], list[str]]:
    """What the search found at a point, and every way it exceeds what aecp_mbx.h states, or a planted restatement."""
    c = {**constants(interfaces), **(planted or {})}
    log, wrong, longest = [], [], 0
    if len(ports(interfaces)) != c['AECP_ROUND_PORTS']:
        wrong.append(f'the port model at {interfaces} interface(s) is not AECP_ROUND_PORTS')
    for w in windows(c, interfaces):
        if w.round_carries == 0:
            # no round would build one, so the queue has no bound to search
            wrong.append(f"the round's own pass at {interfaces} interface(s) has no room for a notice past its "
                         'attempts')
            continue
        first, last = searched(w)
        longest = max(longest, last)
        log.append(f'{interfaces} interface(s): {w.notices} notices, {w.round_carries}/{w.step_carries}/'
                   f'{w.build_carries} a round, step and build, {w.builds} builds, {w.steps} steps: first {first} ms, '
                   f'last {last} ms (stated {c["AECP_QUEUED_FIRST_MS"]} and {c["AECP_QUEUED_MS"]} ms)')
        if first > c['AECP_QUEUED_FIRST_MS']:
            wrong.append(f'the first notice at {interfaces} interface(s): {first} ms over AECP_QUEUED_FIRST_MS')
        if last > c['AECP_QUEUED_MS']:
            wrong.append(f'the last notice at {interfaces} interface(s): {last} ms over AECP_QUEUED_MS')
    if c['AECP_QUEUED_FIRST_MS'] > FIRST_ALLOWED_MS[interfaces]:
        wrong.append(f'AECP_QUEUED_FIRST_MS at {interfaces} interface(s) over the {FIRST_ALLOWED_MS[interfaces]} ms '
                     'it may take')
    if longest < c['AECP_QUEUED_MS']:
        wrong.append(f'AECP_QUEUED_MS at {interfaces} interface(s) is not the search\'s {longest} ms: restate it')
    if c['AECP_QUEUED_MS'] > c['AECP_QUEUED_CEILING_MS']:
        wrong.append(f'AECP_QUEUED_MS over its ceiling at {interfaces} interface(s)')
    return log, wrong


#: The search's planted controls at two interfaces: a constant restated, and the words its finding must carry. The
#: window restored to every port refusing, which the port model does not admit with a queue, puts the first notice at
#: 28 ms; the first notice's bound at T_svc is the one 8x8/2if had before the maintainer's decision of 2026-11-08.
CONTROLS = (({'AECP_QUEUED_MS': 64}, 'is not the search'), ({'AECP_ATTEMPT_US': 300}, 'has no room for a notice'),
            ({'AECP_QUEUED_MS': 60}, 'over AECP_QUEUED_MS'), ({'AECP_QUEUED_CEILING_MS': 60}, 'over its ceiling'),
            ({'refusing': 6}, 'over AECP_QUEUED_FIRST_MS'), ({'AECP_QUEUED_FIRST_MS': 20}, 'over AECP_QUEUED_FIRST_MS'),
            ({'AECP_QUEUED_FIRST_MS': 24}, 'it may take'))


def controls() -> list[str]:
    """Each planted control the search did not catch."""
    return [str(planted) for planted, words in CONTROLS if not any(words in w for w in findings(2, planted)[1])]


def main() -> int:
    """Both points' searches, printed; nonzero where one exceeds what aecp_mbx.h states."""
    wrong = []
    for interfaces in (1, 2):
        log, found = findings(interfaces)
        print('\n'.join(log))
        wrong += found
    print('\n'.join(wrong) or 'THE RETRY search: every queue within its stated bound')
    return 1 if wrong else 0


if __name__ == '__main__':
    sys.exit(main())
