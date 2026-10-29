# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The budget grader self-test's checks of the composed maximum (#665), which selftest.py runs.

Synthetic backlog windows check run.composed_maximum: the longest pass of every backlog window, its
lower bound while a window left its load unreleased, the backlog rows a run did not include, and the
record results.json carries and the table renders. Each check is (name, held, detail), as selftest.py's.
"""
from __future__ import annotations

import run


def maximum_checks() -> list[tuple[str, bool, str]]:
    """The composed maximum over synthetic backlog windows: its lower bound, the backlog rows a run
    did not include, and the record results.json carries and the table renders."""
    window = lambda group, cycles, done: dict(group=group, probes=[], timeouts=[], passes=dict(composed=dict(
        cycles=cycles, ms=cycles / 50_000, passes=3, window_ms=100.0, serviced=done, unreleased={} if done
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
