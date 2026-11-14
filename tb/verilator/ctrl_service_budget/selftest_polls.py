# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The self-test's checks of the polls by source (poll_grade.py; #665): every pass's base,
its polls less the heavy items inside them, and every heavy item held to its stated cost at its point, an ACMP or AECP
call that committed no frame the base's, and a base or an item over its cost failing the run whatever findings it
records; and a control held to this image's own unplanted measurement (a reference control) caught only past
its margin."""
from __future__ import annotations

import argparse
import contextlib
import io
import tempfile
from collections.abc import Callable
from pathlib import Path
from unittest.mock import patch

import build
import grade
import join_grade
import mrpdu_grade
import long_notice
import poll_grade
import poll_items
import run
import scenario

Check = tuple[str, bool, str]
#: The labels the testbench prints for each span, read here apart from poll_grade.ITEMS: a pass's first and last
#: firmware poll, then each item's function.
FIRST, LAST = 'adp_mbx:on_poll', 'ctrl_app_srp:deliver'
LABELS = {'withdraw': 'srp_mbx:reset_interface', 'rebuild': 'srp_mbx:open_interface', 'walk': 'mrp_attr_visit',
          'reclaim': 'mrp_reclaim', 'retained': 'srp_mbx:apply_receive', 'mrpdu': 'srp_mbx:build_mrpdu',
          'acmp': 'acmp_mbx:on_poll', 'aecp': 'aecp:transmit'}
#: The items whose call did their work only where it committed a frame of their module's channel.
SENDING = {'acmp': 'acmp', 'aecp': 'aecp'}


def traced_label(name: str | tuple[str, str]) -> str:
    """The label the testbench prints for a SPAN_SYMBOLS entry."""
    return name if isinstance(name, str) else f'{name[0]}:{name[1]}'


def polls_checks(synthetic: Callable[[list[str]], str], sys_hz: int, cpu_hz: int,
                 tx_record: Callable[..., list[str]]) -> list[Check]:
    """A pass's base and each item at its stated cost fit it and a cycle over does not, by point; tx_record is
    selftest.py's, the ring writes and commit of one TX record."""
    ratio = sys_hz // cpu_hz

    def limit(kind: str, interfaces: int = 2) -> int:
        """A stated cost in CPU cycles."""
        return poll_grade.stated_us(interfaces)[kind] * cpu_hz // 1_000_000

    def held(base: int, items: tuple = (), outside: tuple = (), unsent: tuple = (), interfaces: int = 2,
             sent: bytes = b'') -> dict:
        """One pass's polls whose time outside its items is base CPU cycles, ACMP or AECP calls that committed no
        frame among it: the items inside (kind, cycles, nested in the one before), and items after the polls,
        graded; an AECP item commits `sent` where one is given."""
        start = 10_000
        span = lambda at, cycles, label: f'SPAN {ratio * at} {at} {cycles} 00002000 {label}'
        lines, end, outer = [span(start, 50, FIRST)], start + 50, None
        for kind, cycles, nested in items:
            at = outer + 5 if nested else end + 10
            lines.append(span(at, cycles, LABELS[kind]))
            if kind == 'aecp' and sent:
                lines += tx_record(scenario.CH['aecp'], 0, sent, 0, ratio * (at + cycles // 2))
            elif kind in SENDING:
                lines.append(f'TXC {ratio * (at + cycles // 2)} {scenario.CH[SENDING[kind]]} 0')
            if not nested:
                outer, end = at, at + cycles
        for kind, cycles in unsent:
            lines.append(span(end + 10, cycles, LABELS[kind]))
            end += 10 + cycles
        spent = sum(c for _, c, nested in items if not nested)
        slack = base - (end - start - spent) - 40
        assert slack >= 0, (base, end - start - spent)
        end += slack + 40
        lines.append(span(end - 40, 40, LAST))
        lines += [span(end + 500, cycles, LABELS[kind]) for kind, cycles in outside]
        lines.insert(0, f'PASS 1 {ratio * (start - 10)} {start - 10} {end - start + 520 + 10 * ratio} instr=10 '
                        f'store_mbx=1 W {ratio * start}:1:0')
        return grade.grade(synthetic(lines), scenario.Group('g'), sys_hz, cpu_hz, interfaces)['passes']['polls']

    kinds = [k for k in LABELS]
    one, two = poll_grade.stated_us(1), poll_grade.stated_us(2)
    out = [("each point's polls costs are stated, every item's, a long notice's, a declined ACMP offer's and the "
            "base's, the 8x8/2if base dearer than the 1x1/1if's",
            sorted(one) == sorted(two) == sorted(['base', *kinds, poll_grade.LONG, poll_grade.DECLINED]) and
            all(one.values()) and
            all(two.values()) and two['base'] > one['base'], str((one, two))),
           ("the testbench traces a pass's first and last firmware poll, every heavy item and ACMP's offers",
            {FIRST, LAST, *LABELS.values(), 'acmp_rx', 'acmp_mbx:on_frame'} <=
            {traced_label(n) for n in build.SPAN_SYMBOLS} and
            {k: v[0] for k, v in poll_grade.ITEMS.items()} == LABELS, '')]
    every = tuple((k, limit(k) // 4, False) for k in kinds)
    at, over = held(limit('base'), every), held(limit('base') + 1, every)
    out.append(("a pass's base at its stated cost fits it and one a cycle over does not, every item inside it "
                'subtracted', at['over'] == [] and at['passes'] == 1 and
                [(o['kind'], o['cycles']) for o in over['over']] == [('base', limit('base') + 1)], str((at, over))))
    fits, misses = [], []
    for k in kinds:
        a, b = held(limit('base'), ((k, limit(k), False),)), held(limit('base'), ((k, limit(k) + 1, False),))
        fits.append(a['over'] == [] and a['heaviest'][k] == limit(k))
        misses.append([(o['kind'], o['cycles']) for o in b['over']] == [(k, limit(k) + 1)])
    out.append(('each heavy item at its stated cost fits it and one a cycle over does not', all(fits) and all(misses),
                str((fits, misses))))
    for k in SENDING:
        quiet = held(limit('base') + 1, unsent=((k, 101),))
        out.append((f"an {k.upper()} call that committed no {k.upper()} frame is the base's",
                    [(o['kind'], o['cycles']) for o in quiet['over']] == [('base', limit('base') + 1)], str(quiet)))
    far = held(limit('base'), outside=(('rebuild', limit('rebuild') + 1),))
    out.append(('an item outside the polls is neither subtracted from the base nor held as a polls item',
                far['over'] == [] and far['heaviest']['rebuild'] == 0, str(far)))
    record, dearer = (held(limit('base'), outside=(('retained', limit('retained') + d),)) for d in (0, 1))
    out.append(("an SRP record's own apply, outside the polls, is held to its retry's stated cost: at it fits, a "
                'cycle over does not, and neither is a polls item',
                record['over'] == [] and record['heaviest'][poll_grade.RECORD] == limit('retained') and
                record['heaviest']['retained'] == 0 and
                [(o['kind'], o['cycles']) for o in dearer['over']] == [(poll_grade.RECORD, limit('retained') + 1)],
                str((record, dearer))))
    named_record = run.stated_misses([dict(group='r', passes=dict(polls=dearer))])
    out.append(("an SRP record's apply over its stated cost is named, with the cost it passed",
                named_record == [f"r: an SRP record's apply of {limit('retained') + 1:,} CPU cycles, over its stated "
                                 f"{limit('retained'):,}"], str(named_record)))
    nested = held(limit('base'), (('retained', limit('retained'), False), ('walk', limit('retained') // 2, True)))
    out.append(('an item inside another is counted once, as the outer one',
                nested['over'] == [] and nested['heaviest']['walk'] == 0, str(nested)))
    single = held(limit('base', 1) + 1, interfaces=1)
    out.append(("a pass at one interface is held to that point's costs",
                [o['cycles'] for o in single['over']] == [limit('base', 1) + 1], str(single)))
    return out + named_checks(held, limit) + long_checks(held, limit) + offer_checks(synthetic, sys_hz, cpu_hz) + \
        join_checks(synthetic, sys_hz, cpu_hz, tx_record) + reference_checks()


def named_checks(held: Callable[..., dict], limit: Callable[..., int]) -> list[Check]:
    """A base or an item over its stated cost is named and fails the run; held and limit are polls_checks'."""
    base_over = held(limit('base') + 1)
    item_over = held(limit('base'), (('withdraw', limit('withdraw') + 1, False),))
    named = run.stated_misses([dict(group='g', passes=dict(polls=base_over)),
                               dict(group='h', passes=dict(polls=item_over))])
    args = argparse.Namespace(cpu_regions='cover', mutation='none', record_budget_findings=True,
                              record_share_findings=True)
    return [("a pass's base or an item over its stated cost is named, with the cost it passed",
             named == [f"g: a pass's polls base of {limit('base') + 1:,} CPU cycles, over its stated "
                       f"{limit('base'):,}", f"h: a withdraw item of {limit('withdraw') + 1:,} CPU cycles, over "
                       f"its stated {limit('withdraw'):,}"], str(named)),
            ("a pass's base over its stated cost fails a run whatever findings it records",
             run.verdict(args, [scenario.Group('g')], [], [], [], named[:1]) == 1, '')]


def long_checks(held: Callable[..., dict], limit: Callable[..., int]) -> list[Check]:
    """A notice longer than AECP_FAN_BYTES is a poll item of its own at its own stated cost, and the largest legal
    notice's group that measured none is refused (#894: long_notice.py)."""
    fan = poll_grade.fan_bytes()

    def frame(n: int, unsolicited: bool = True) -> bytes:
        """An AEM_RESPONSE of n bytes, unsolicited (the u bit, IEEE 1722.1-2021 7.5.2) or not."""
        head = bytearray(n)
        head[15], head[36] = 1, 0x80 if unsolicited else 0
        return bytes(head)
    big, k = frame(long_notice.LONG_NOTICE_BYTES), poll_grade.LONG
    at, over = (held(limit('base'), (('aecp', limit(k) + d, False),), sent=big) for d in (0, 1))
    out = [('a notice longer than AECP_FAN_BYTES is a long notice\'s item at its own stated cost: at it fits, a cycle '
            'over does not, and neither is the aecp item\'s',
            limit(k) > limit('aecp') and at['over'] == [] and at['heaviest'][k] == limit(k) and
            at['heaviest']['aecp'] == 0 and [c for _, c in at['long']] == [limit(k)] and
            [(o['kind'], o['cycles']) for o in over['over']] == [(k, limit(k) + 1)], str((at, over)))]
    short = [held(limit('base'), (('aecp', limit('aecp'), False),), sent=s)
             for s in (frame(fan), frame(fan + 1, unsolicited=False))]
    out.append(('a notice of AECP_FAN_BYTES, or a longer solicited response, is the aecp item\'s',
                all(q['heaviest']['aecp'] == limit('aecp') and q['heaviest'][k] == 0 and q['long'] == []
                    for q in short), str(short)))
    named = run.stated_misses([dict(group='n', passes=dict(polls=over))])
    out.append(('a long notice\'s item over its stated cost is named, with the cost it passed',
                named == [f'n: a {k} item of {limit(k) + 1:,} CPU cycles, over its stated {limit(k):,}'], str(named)))
    group = long_notice.NAME
    refused = long_notice.missing([dict(group=group, passes=dict(polls=dict(long=[]))),
                                   dict(group='aecp-fanout', passes=dict(polls=dict(long=[]))),
                                   dict(group=group, passes=dict(polls=at))])
    out.append(('the largest legal notice\'s group that measured no long notice is refused, and only that group',
                refused == [f'{group}: no AECP poll item committed a notice longer than AECP_FAN_BYTES, so the largest '
                            'legal notice was not measured'], str(refused)))
    return out


def offer_checks(synthetic: Callable[[list[str]], str], sys_hz: int, cpu_hz: int) -> list[Check]:
    """ACMP's item is its send, the offers THE KEPT COMMAND's redelivery nests in it subtracted from it and from the
    base; an offer is declined exactly when the next is the kept record's re-offer, held to its own cost; the kept
    record's accepted re-offer is held to the ACMP record's; the declines are at most two a send and one (#908)."""
    ratio, acmp = sys_hz // cpu_hz, scenario.CH['acmp']
    limit = lambda kind: poll_grade.stated_us(1)[kind] * cpu_hz // 1_000_000
    kept_limit = poll_grade.record_us(1) * cpu_hz // 1_000_000
    span = lambda at, cycles, label: f'SPAN {ratio * at} {at} {cycles} 00002000 {label}'

    def graded(item: int, nested: tuple = (), before: tuple = (), after: tuple = ()) -> dict:
        """One pass's polls at one interface, base 1,000 cycles, its ACMP item `item` CPU cycles committing a frame,
        the offers nested in it, and handler offers before the polls and offers after them: each (cycles, the kept
        record's re-offer?)."""
        lines, at = [], 1_000
        for cycles, kept in before:
            lines.append(span(at, cycles, poll_items.OFFER if kept else poll_items.HANDLER))
            at += cycles + 10
        start = 10_000
        lines += [span(start, 50, FIRST), span(start + 60, item, LABELS['acmp']),
                  f'TXC {ratio * (start + 65)} {acmp} 0']
        inner = start + 70
        for cycles, kept in nested:
            lines.append(span(inner, cycles, poll_items.OFFER if kept else poll_items.HANDLER))
            inner += cycles + 1
        end = start + 60 + item + 1_000 - 50 - 10 - 40
        lines.append(span(end, 40, LAST))
        at = end + 500
        for cycles, kept in after:
            lines.append(span(at, cycles, poll_items.OFFER if kept else poll_items.HANDLER))
            at += cycles + 10
        lines.insert(0, f'PASS 1 {ratio * (start - 10)} {start - 10} {end - start + 520 + 10 * ratio} instr=10 '
                        f'store_mbx=1 W {ratio * start}:1:0')
        return grade.grade(synthetic(lines), scenario.Group('g'), sys_hz, cpu_hz, 1)['passes']['polls']

    item, kept, rec = limit('acmp') + 4_000, (3_000, True), (2_000, False)
    split = graded(item, (kept, rec))
    out = [('an ACMP item is its send: the kept record\'s re-offer and the records the redelivery hands to their '
            'handler are subtracted from it and from the base',
            split['heaviest']['acmp'] == item - 5_000 and split['heaviest']['base'] == 1_000 and
            not [o for o in split['over'] if o['kind'] in ('acmp', 'base')], str(split))]
    told = graded(limit('acmp') + 5_000, (kept, rec), before=((limit(poll_grade.DECLINED), False),), after=(rec,))
    out.append(('an offer the kept record\'s re-offer follows is declined and held to its own cost, and the kept '
                'record\'s re-offer the next record follows is accepted and held to the ACMP record\'s',
                told['heaviest'][poll_grade.DECLINED] == limit(poll_grade.DECLINED) and
                told['heaviest'][poll_grade.KEPT] == 3_000 and told['over'] == [], str(told)))
    dear = graded(limit('acmp') + kept_limit + 2_001, ((kept_limit + 1, True), rec),
                  before=((limit(poll_grade.DECLINED) + 1, False),))
    named = run.stated_misses([dict(group='o', passes=dict(polls=dear))])
    out.append(('a declined ACMP offer over its stated cost, and a kept command\'s accepted offer over the ACMP '
                'record\'s, are named, with the cost each passed',
                named == [f"o: a declined ACMP offer of {limit(poll_grade.DECLINED) + 1:,} CPU cycles, over its "
                          f"stated {limit(poll_grade.DECLINED):,}",
                          f"o: a kept ACMP command's accepted offer of {kept_limit + 1:,} CPU cycles, over its stated "
                          f"{kept_limit:,}"], str(named)))
    tight = graded(limit('acmp'), before=((100, False), (100, True)), after=((100, True), (100, True), (100, True)))
    bound = run.stated_misses([dict(group='d', passes=dict(polls=tight))])
    out.append(('declined ACMP offers over two a sent owed frame and one are refused, named with the sends',
                bound == ['d: 4 declined ACMP offers, over their bound of two a sent owed frame and one (1 sent)'],
                str(bound)))
    return out


def join_checks(synthetic: Callable[[list[str]], str], sys_hz: int, cpu_hz: int,
                tx_record: Callable[..., list[str]]) -> list[Check]:
    """A join interval is two consecutive MRPDUs of one participant, an interface and an MRP application, with a join
    timer's run-out between them and neither the periodic nor the LeaveAll timer's; each outside Table 4.3's 180.0 to
    240.0 ms narrowed by T_egress at each end, 181.0 to 239.0 ms commit to commit, is named and fails the run (#894's
    contingent ruling of 2026-11-13, item 4; its egress ruling, item 1)."""
    srp, ms, ratio = scenario.CH['srp'], sys_hz // 1000, sys_hz // cpu_hz

    def joins(sends: tuple, timers: tuple = (), idle: tuple = (), ordinary: tuple = (), owed: tuple = ()) -> dict:
        """The join intervals of a log whose MRPDUs are (ms, interface, EtherType), each committed in a pass of its own
        after its build, whose timers are (ms, callback), whose builds at the ms in idle sent nothing, which has passes
        with no build at the ms in ordinary, and whose sends at the ms in owed are their poll's, a pass after their
        build, the ring having refused the frame (A3)."""
        lines, word = [], 0
        for at, interface, kind in sends:
            frame = bytes(12) + kind.to_bytes(2, 'big') + bytes(46)
            lines += tx_record(srp, interface, frame, word, at * ms)
            word += 2 + (len(frame) + 3) // 4
        builds = sorted([at - 1 if at in owed else at for at, _, _ in sends] + list(idle))
        lines += [f'ENTRY {at * ms - 2000} build_mrpdu' for at in builds]
        lines += [f'PASS {at} {at * ms - 3000} {(at * ms - 3000) // ratio} {5000 // ratio} instr=10'
                  for at in sorted(builds + list(owed) + list(ordinary))]   # a pass a ms, idle or not
        lines += [f'ENTRY {at * ms} {name}' for at, name in timers]
        return join_grade.held(grade.parse(synthetic(lines), sys_hz, cpu_hz))

    msrp, mvrp = 0x22EA, 0x88F5
    edge = joins(((1_000, 0, msrp), (1_181, 0, msrp), (1_420, 0, msrp)), ((1_171, 'on_join_timer'),
                                                                        (1_400, 'on_join_timer')))
    out = [('a join interval is two MRPDUs of one participant, the second one a join timer released: 181 and 239 ms, '
            "Table 4.3's 180 and 240 less T_egress, hold", (join_grade.LEAST_MS, join_grade.MOST_MS) == (181.0, 239.0)
            and edge['count'] == 2 and edge['shortest'] == 181.0 and edge['longest'] == 239.0 and edge['over'] == [],
            str(edge))]
    short = joins(((1_000, 0, msrp), (1_180, 0, msrp)), ((1_170, 'on_join_timer'),))
    long = joins(((1_000, 0, mvrp), (1_240, 0, mvrp)), ((1_230, 'on_join_timer'),))
    named = run.stated_misses([dict(group='j', passes=dict(joins=short)), dict(group='k', passes=dict(joins=long))])
    out.append(('a join interval under 181.0 ms or over 239.0 ms is named with its participant',
                named == ['j: a join interval of 180.000 ms (if0 MSRP), outside 181.0 to 239.0 ms',
                          'k: a join interval of 240.000 ms (if0 MVRP), outside 181.0 to 239.0 ms'], str(named)))
    apart = joins(((1_000, 0, msrp), (1_050, 0, mvrp), (1_100, 1, msrp), (1_190, 0, msrp)),
                  ((1_180, 'on_join_timer'),))
    other = joins(((1_000, 0, msrp), (1_090, 0, msrp)), ((1_050, 'on_join_timer'), (1_060, 'on_pt_timer')))
    none = joins(((1_000, 0, msrp), (1_090, 0, msrp)))
    out.append(("a participant's join intervals are its own, and two MRPDUs with a periodic or LeaveAll timer, or no "
                'join timer, between them are none', apart['count'] == 1 and apart['shortest'] == 190.0 and
                other['count'] == 0 and none['count'] == 0, str((apart, other, none))))
    idle = joins(((1_000, 0, msrp), (1_700, 0, msrp)), ((1_190, 'on_join_timer'),), idle=(1_191,))
    out.append(('a join timer that runs out with nothing to send, its build sending no frame, releases nothing and is '
                'empty, and the MRPDU a later request sends ends no join interval',
                idle['count'] == 0 and idle['runs']['empty'] == 1 and not idle['failing'], str(idle)))
    out += horizon_checks(joins, msrp)
    args = argparse.Namespace(cpu_regions='cover', mutation='none', record_budget_findings=True,
                              record_share_findings=True)
    out.append(('a join interval outside its range fails a run whatever findings it records',
                run.verdict(args, [scenario.Group('j')], [], [], [], named[:1]) == 1, ''))
    return out


def horizon_checks(joins: Callable[..., dict], msrp: int) -> list[Check]:
    """A run-out's builds are sought wherever they come (mrpdu_grade.resolve; #894's egress ruling of 2026-11-13,
    item 4): a build past THE TRANSMIT's bound is late, on either side of the 100 ms its search once stopped at, and its
    interval is graded; no build after it is absent in a log that runs on past the bound and unresolved in one that
    ends first, counted and never taken for one that owes nothing; and a frame its build left owed is still its
    build's."""
    def at(end: int) -> dict:
        """One participant's MRPDUs at 1,000 ms and `end`, a join timer's run-out at 1,190 ms between them."""
        return joins(((1_000, 0, msrp), (end, 0, msrp)), ((1_190, 'on_join_timer'),))
    cases = {end: at(end) for end in (1_191, 1_239, 1_241, 1_289, 1_291, 1_500)}
    late = {end: (r['count'], [o['ms'] for o in r['over']], [(o['outcome'], o['after_ms']) for o in r['failing']])
            for end, r in cases.items()}
    out = [("a run-out's build past THE TRANSMIT's bound is late and named, and its interval is graded, on either "
            "side of the 100 ms the search once stopped at: 241, 289, 291 and 500 ms fail, 191 and 239 hold",
            mrpdu_grade.LATE_MS == 49 and late == {
                1_191: (1, [], []), 1_239: (1, [], []), 1_241: (1, [241.0], [('late', 51.0)]),
                1_289: (1, [289.0], [('late', 99.0)]), 1_291: (1, [291.0], [('late', 101.0)]),
                1_500: (1, [500.0], [('late', 310.0)])}, str(late))]
    absent = joins(((1_000, 0, msrp),), ((1_190, 'on_join_timer'),), ordinary=(1_300,))
    pending = joins(((1_000, 0, msrp),), ((1_190, 'on_join_timer'),), ordinary=(1_230,))
    named = run.stated_misses([dict(group='a', passes=dict(joins=absent)), dict(group='u', passes=dict(joins=pending))])
    out.append(('no build after a run-out is absent and named where the log runs on past THE TRANSMIT\'s bound, and '
                'unresolved, counted and not named, where it ends first; neither is taken for a run-out that owes '
                'nothing', absent['runs']['absent'] == 1 and pending['runs']['unresolved'] == 1 and
                not pending['failing'] and absent['runs']['empty'] == pending['runs']['empty'] == 0 and len(named) == 1
                and named[0].startswith("a: the join timer's run-out at 1190.000 ms, no build after it though the log "
                                        'runs on 110.0') and named[0].endswith(' ms (absent)'),
                str((absent, pending, named))))
    owed = joins(((1_000, 0, msrp), (1_200, 0, msrp)), ((1_190, 'on_join_timer'),), owed=(1_200,))
    out.append(("a frame its build left owed, which the poll sends a pass later, is that build's: the run-out "
                'released it and ends a join interval', owed['count'] == 1 and owed['runs']['released'] == 1 and
                owed['shortest'] == 200.0, str(owed)))
    return out


def reference_checks() -> list[Check]:
    """A reference control (build.REFERENCE_CONTROLS, #665) is caught only where its group's planted heaviest
    instance of its kind is more than the stated margin dearer than this image's unplanted one, measured on this
    point's unplanted build in the same run, with no refusal in either run."""
    name = 'srp-compared-by-memcmp'
    kind, group = build.REFERENCE_CONTROLS.get(name), build.MUTATIONS[name][3]
    args = argparse.Namespace(mutation=name)

    def grades(cycles: int | None) -> list[dict]:
        """One run's grade of the control's group with that heaviest instance, none for None."""
        return [] if cycles is None else [dict(group=group, passes=dict(polls=dict(heaviest={kind: cycles})))]

    def verdict(planted: int | None, unplanted: int | None = 20_000, refused: tuple = (),
                unrefused: tuple = ()) -> int:
        """The control's exit status on those two runs, its CONTROL line kept off the self-test's output."""
        with contextlib.redirect_stdout(io.StringIO()):
            return run.reference_verdict(args, grades(planted), list(refused), (grades(unplanted), list(unrefused)))
    edge = 21_000
    out = [("the SRP record cut's control is held to this image's unplanted SRP record, not to a stated cost, with "
            'a margin of 5 %', kind == poll_grade.RECORD and name not in build.POLL_CONTROLS and
            poll_items.REFERENCE_MARGIN_PERCENT == 5, str((kind, sorted(build.POLL_CONTROLS))))]
    if kind is None:
        return out
    margins = tuple(verdict(c) for c in (edge + 1, edge, 20_000, 19_000))
    out.append(('a reference control is caught by a planted record more than its margin dearer than the unplanted '
                'one, and escapes at the margin, at the same cost and cheaper', margins == (0, 1, 1, 1), str(margins)))
    refusals = (verdict(edge + 1, refused=('r',)), verdict(edge + 1, unrefused=('r',)), verdict(edge + 1, None),
                verdict(None))
    out.append(('a reference control escapes with a refusal in either run, or without its group in either',
                refusals == (1, 1, 1, 1), str(refusals)))
    out.append(reference_run_check(name))
    return out


def reference_run_check(name: str) -> Check:
    """run.reference_run builds this point's unplanted image at the control's variant and core in <build-dir>/reference
    and runs the control's group alone there."""
    calls: list = []
    planted = argparse.Namespace(mutation=name, variant=build.MUTATIONS[name][4], point='8x8', cpu_regions='cover',
                                 fetch_l1='split', xip=False, reuse_build=False, regrade=False)
    groups = [scenario.Group(build.MUTATIONS[name][3]), scenario.Group('other')]
    spec = dict(flash_image='-')
    with tempfile.TemporaryDirectory() as tmp, \
            patch.object(build, 'build', lambda where, shape, n_if, **kw: calls.append(
                ('build', where, shape, n_if, kw)) or spec), \
            patch.object(run, 'all_groups', lambda point, s: groups), \
            patch.object(scenario, 'point', lambda label, s: label), \
            patch.object(run, 'run_group', lambda where, out, g, flash: calls.append(('run', where, g.name)) or out), \
            patch.object(run, 'graded', lambda gs, logs, s, out: ([dict(group=g.name) for g in gs], ['x'], [])):
        planted_dir = Path(tmp) / 'b'
        results, refusals = run.reference_run(planted, planted_dir, 'endstation_ax7101_8x8', 2)
    want = [('build', planted_dir / 'reference', 'endstation_ax7101_8x8', 2,
             dict(mutation='none', variant=planted.variant, core=build.Core('cover', 'split', False))),
            ('run', planted_dir / 'reference', build.MUTATIONS[name][3])]
    return ("a reference control's other run is its group alone on this point's unplanted image, at its variant and "
            'core, in the build directory\'s reference', calls == want and results == [dict(group=groups[0].name)]
            and refusals == ['x'], str(calls))
