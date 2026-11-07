# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The budget grader self-test's checks of the composed maximum (#665), which selftest.py runs.

Synthetic backlog windows check run.composed_maximum: the longest pass of every backlog window, its
lower bound while a window left its load unreleased, the backlog rows a run did not include, and the
record results.json carries and the table renders. opening_checks holds each backlog window to a
drained event ring when it opens, the precondition of its defined load, and the refusal to the
records held. Each check is (name, held, detail), as selftest.py's.
"""
from __future__ import annotations

from types import SimpleNamespace

import build as builder
import grade
import run
import scenario


def maximum_checks() -> list[tuple[str, bool, str]]:
    """The composed maximum over synthetic backlog windows: its lower bound, the backlog rows a run
    did not include, and the record results.json carries and the table renders."""
    window = lambda group, cycles, done: dict(group=group, probes=[], timeouts=[], passes=dict(composed=dict(
        cycles=cycles, ms=cycles / 50_000, passes=3, window_ms=100.0, events_held=0, serviced=done,
        unreleased={} if done
        else {'srp': 32})))
    record = lambda top, group, unreleased, best, not_run=(): dict(
        cycles=top, ms=top / 50_000, group=group, windows=4 - len(not_run), rows=4, not_run=list(not_run),
        partial=bool(not_run), lower_bound=bool(unreleased), unreleased=list(unreleased),
        released=dict(cycles=best[0], ms=best[0] / 50_000, group=best[1]) if best else None)
    out = []
    # Every backlog window, the longest of them with SRP unreleased, so a lower bound; the released
    # windows' longest stands beside it, and the fixture's short window is no backlog row. Then
    # every window released, so no lower bound.
    full = [window('fixture', 9_000_000, True), window('backlog', 700_000, True),
            window('backlog-adp', 1_500_000, False), window('backlog-adp-refill', 1_200_000, False),
            window('backlog-owed', 600_000, True)]
    released = [window('backlog', 700_000, True), window('backlog-adp', 650_000, True),
                window('backlog-adp-refill', 680_000, True), window('backlog-owed', 600_000, True)]
    at_least = record(1_500_000, 'backlog-adp', ['backlog-adp', 'backlog-adp-refill'], (700_000, 'backlog'))
    got = [run.composed_maximum(full), run.composed_maximum(released)]
    out.append(('the composed maximum is the longest pass of every backlog window, a lower bound while one '
                'left its load unreleased', got == [at_least, record(700_000, 'backlog', [], (700_000, 'backlog'))],
                str(got)))
    # The longest window released its load and a shorter one did not: still a lower bound.
    shorter = [window('backlog', 1_800_000, True), window('backlog-adp', 1_500_000, False),
               window('backlog-adp-refill', 1_200_000, True), window('backlog-owed', 600_000, True)]
    got = run.composed_maximum(shorter)
    out.append(('the composed maximum is a lower bound while a window shorter than the longest left its load '
                'unreleased', got == record(1_800_000, 'backlog', ['backlog-adp'], (1_800_000, 'backlog')),
                str(got)))
    # The answering-ports arm's three backlog rows, without the refill row, and one row alone: each run
    # names the rows it did not include.
    three = [window('backlog', 740_260, True), window('backlog-adp', 645_058, True),
             window('backlog-owed', 582_392, True)]
    partial = record(740_260, 'backlog', [], (740_260, 'backlog'), ['backlog-adp-refill'])
    got = [run.composed_maximum(three), run.composed_maximum(three[:1])]
    want = [partial, record(740_260, 'backlog', [], (740_260, 'backlog'),
                            ['backlog-adp', 'backlog-adp-refill', 'backlog-owed'])]
    out.append(('a run without every backlog row names the rows not run, and its composed maximum is partial',
                got == want, str(got)))
    # results.json's record is the one the table renders: a lower bound over every window, a partial
    # figure, and both at once (an unreleased window run alone).
    both = record(1_500_000, 'backlog-adp', ['backlog-adp'], None, ['backlog', 'backlog-adp-refill', 'backlog-owed'])
    cases = ((full, at_least, 'Composed maximum over the 4 backlog windows: at least 1,500,000 CPU cycles '
              '(30.000 ms), backlog-adp, a lower bound (load unreleased in backlog-adp, backlog-adp-refill).',
              '700,000 (14.000 ms), backlog.'),
             (three, partial, 'Composed maximum over 3 of 4 backlog windows, a partial figure (backlog-adp-refill '
              'not run): 740,260 CPU cycles (14.805 ms), backlog.', '740,260 (14.805 ms), backlog.'),
             (full[2:3], both, 'Composed maximum over 1 of 4 backlog windows, a partial figure (backlog, '
              'backlog-adp-refill, backlog-owed not run): at least 1,500,000 CPU cycles (30.000 ms), backlog-adp, '
              'a lower bound (load unreleased in backlog-adp).', 'none.'))
    wrong = []
    for results, top, line, best in cases:
        saved = run.summary('1x1', '0' * 64, results, [], [])['composed_maximum']
        lines = [text for text in run.table(results, '1x1').splitlines()
                 if text.startswith(('Composed maximum', 'Over the windows'))]
        if saved != top or lines != [line, f'Over the windows that released their whole load only: {best}']:
            wrong.append(f'results.json {saved}; table {lines}')
    out.append(("results.json's composed maximum is the record the table renders, with its lower-bound and "
                'partial labels', not wrong, '; '.join(wrong)))
    return out


def stimulus_checks(points: list[scenario.Point]) -> list[tuple[str, bool, str]]:
    """Each AECP group offers one frame a refill period of the channel's token bucket (scenario.paced), and a build's
    flash window is its arm's (build.flash_window_refusals)."""
    aecp = scenario.CH['aecp']
    wait = f'wait cycles {scenario.CONTRACT.channels[aecp].refill_ms * scenario.MS}'
    fast = []
    for p in points:
        group = scenario.paced(scenario.Group('aecp', steps=['frame 0 00', 'wait quiet 3', 'frame 0 01']), aecp)
        steps = group.steps
        fast += [f'{p.interfaces}: {steps[n]}' for n in range(len(steps))
                 if steps[n].startswith('frame ') and (n == 0 or steps[n - 1] != wait)]
    out = [('each frame of an AECP group waits a refill period of its token bucket', not fast, str(fast))]
    regions = lambda mode: {'addresses': {'flash': 7}, 'memory_regions': [[0, 1, 'rxc', 'p'], [7, 1, mode, 'p']]}
    cases = [(False, 'r', True), (False, 'rxc', False), (False, 'rc', False), (True, 'rxc', True), (True, 'r', False)]
    wrong = [(xip, mode) for xip, mode, fits in cases
             if (not builder.flash_window_refusals({**regions(mode), 'xip': xip})) != fits]
    out.append(("a build's flash window is uncached and not executable, but in the hybrid-XIP arm", not wrong,
                str(wrong)))
    return out


def opening_checks(points: list[scenario.Point]) -> list[tuple[str, bool, str]]:
    """Each backlog window opens on a drained event ring (scenario.OPEN_WINDOW), the event records
    it holds are counted through the ring index's wrap, and a window short of its load says so."""
    want = ('wait events 0 within 40000000', 'gap 1', 'mark composed')
    openings = {}
    for p in points:
        for g in scenario.backlog_groups(p):
            steps = g.script().splitlines()
            at = steps.index('mark composed')
            openings[f'{g.name}@{p.interfaces}'] = tuple(steps[at - 2:at + 1])
    wrong = {k: v for k, v in openings.items() if v != want}
    out = [('every backlog window waits for the event ring to drain, then opens', bool(openings) and not wrong,
            str(wrong))]
    words = scenario.CONTRACT.ev_words
    tail = scenario.EVT_TAIL_WORD
    wrap = 0x10000 // words + 3
    cases = [(5, [], 5), (5, [(1, tail, 2 * words)], 3), (5, [(1, tail, 2 * words), (20, tail, 5 * words)], 3),
             (wrap + 1, [(1, tail, 0xFFFF & -words), (2, tail, 3 * words)], 1)]
    counted = [grade.Grader(SimpleNamespace(records=[(10, [])] * n, writes=writes)).events_held(15)
               for n, writes, _ in cases]
    out.append(('the event records held are those posted before the mark less the released, through the wrap',
                counted == [held for *_, held in cases], str(counted)))
    group = scenario.Group('backlog-adp')
    aged = scenario.Group('backlog-adp@verify-aged2-0')
    full = {**grade.defined_load('backlog-adp'), 'LINK': 0}
    over = {**full, 'GM': full['GM'] + 1}

    def verdict(group: scenario.Group, load: dict[str, int]) -> bool:
        """Whether check_load takes that population for that group."""
        try:
            grade.check_load(group, load, [])
        except grade.Refusal:
            return False
        return True

    flood = (verdict(aged, full), verdict(aged, over), verdict(aged, {**over, 'GM': full['GM'] + 2}),
             verdict(aged, {**full, 'GM': full['GM'] - 1}), verdict(scenario.Group('backlog-adp'), over))
    out.append(("an aged window may hold the flood's last change past its row's, one and no more, and no fewer; a window "
                "under no flood holds its row's exactly", flood == (True, True, False, False, False), str(flood)))
    got = {**grade.defined_load('backlog-adp'), 'GM': 12, 'LINK': 0}
    try:
        grade.check_load(group, got, [], 5)
        words_said = 'accepted'
    except grade.Refusal as error:
        words_said = str(error)
    out.append(('a window short of its grandmaster changes is refused, naming the event records held when it opened',
                "'GM': 12" in words_said and '5 event records held when it opened' in words_said, words_said))
    return out
