# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The self-test's checks of the polls by source (poll_grade.py; #665, the round 22 ruling, item 1): every pass's base,
its polls less the heavy items inside them, and every heavy item held to its stated cost at its point, an ACMP or AECP
call that committed no frame the base's, and a base or an item over its cost failing the run whatever findings it
records."""
from __future__ import annotations

import argparse
from collections.abc import Callable

import build
import grade
import poll_grade
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


def polls_checks(synthetic: Callable[[list[str]], str], sys_hz: int, cpu_hz: int) -> list[Check]:
    """A pass's base and each item at its stated cost fit it and a cycle over does not, by point."""
    ratio = sys_hz // cpu_hz

    def limit(kind: str, interfaces: int = 2) -> int:
        """A stated cost in CPU cycles."""
        return poll_grade.stated_us(interfaces)[kind] * cpu_hz // 1_000_000

    def held(base: int, items: tuple = (), outside: tuple = (), unsent: tuple = (), interfaces: int = 2) -> dict:
        """One pass's polls whose time outside its items is base CPU cycles, ACMP or AECP calls that committed no
        frame among it: the items inside (kind, cycles, nested in the one before), and items after the polls,
        graded."""
        start = 10_000
        span = lambda at, cycles, label: f'SPAN {ratio * at} {at} {cycles} 00002000 {label}'
        lines, end, outer = [span(start, 50, FIRST)], start + 50, None
        for kind, cycles, nested in items:
            at = outer + 5 if nested else end + 10
            lines.append(span(at, cycles, LABELS[kind]))
            if kind in SENDING:
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
    out = [("each point's polls costs are stated, every item's and the base's, the 8x8/2if base dearer than the "
            "1x1/1if's", sorted(one) == sorted(two) == sorted(['base', *kinds]) and all(one.values()) and
            all(two.values()) and two['base'] > one['base'], str((one, two))),
           ("the testbench traces a pass's first and last firmware poll and every heavy item",
            {FIRST, LAST, *LABELS.values()} <= {traced_label(n) for n in build.SPAN_SYMBOLS} and
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
    nested = held(limit('base'), (('retained', limit('retained'), False), ('walk', limit('retained') // 2, True)))
    out.append(('an item inside another is counted once, as the outer one',
                nested['over'] == [] and nested['heaviest']['walk'] == 0, str(nested)))
    single = held(limit('base', 1) + 1, interfaces=1)
    out.append(("a pass at one interface is held to that point's costs",
                [o['cycles'] for o in single['over']] == [limit('base', 1) + 1], str(single)))
    base_over = held(limit('base') + 1)
    item_over = held(limit('base'), (('withdraw', limit('withdraw') + 1, False),))
    named = run.stated_misses([dict(group='g', passes=dict(polls=base_over)),
                               dict(group='h', passes=dict(polls=item_over))])
    out.append(("a pass's base or an item over its stated cost is named, with the cost it passed",
                named == [f"g: a pass's polls base of {limit('base') + 1:,} CPU cycles, over its stated "
                          f"{limit('base'):,}", f"h: a withdraw item of {limit('withdraw') + 1:,} CPU cycles, over "
                          f"its stated {limit('withdraw'):,}"], str(named)))
    args = argparse.Namespace(cpu_regions='cover', mutation='none', record_budget_findings=True,
                              record_share_findings=True)
    out.append(("a pass's base over its stated cost fails a run whatever findings it records",
                run.verdict(args, [scenario.Group('g')], [], [], [], named[:1]) == 1, ''))
    return out
