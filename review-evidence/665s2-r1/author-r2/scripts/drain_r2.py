#!/usr/bin/env python3
"""The composed window of a backlog group's log: the population it committed, the records each
work pass released per channel, and the backlog each probe arrived behind.

Usage: drain_r2.py HARNESS_DIR LOG [LOG ...]
It reads the logs with the harness's own parser (grade.parse) and the contract's ring words.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(sys.argv[1]).resolve()))
import grade  # noqa: E402
import scenario  # noqa: E402

TAILS = {scenario.ch_word(n, 'RX_TAIL'): name for n, name in grade.CHANNEL.items()}
for path in map(Path, sys.argv[2:]):
    log = grade.parse(path.read_text(), 100_000_000, 50_000_000)
    g = grade.Grader(log)
    marks = {name: cycle for cycle, name in log.marks}
    t0, t1 = marks['composed'], marks['composed_end']
    print(f'== {path.parent.name}/{path.name}: composed window {g.ms(t1 - t0):.2f} ms')
    print(f'   committed {grade.population(log, t0, t1)}; refused in window '
          f'{[(tag, size) for c, _, tag, size in log.refused if t0 <= c <= t1]}')
    total: dict[str, int] = {}
    for p in grade.composed_passes(log, t0, t1):
        released: dict[str, int] = {}
        for _, word, _ in p.writes:
            if word in TAILS:
                released[TAILS[word]] = released.get(TAILS[word], 0) + 1
        for k, v in released.items():
            total[k] = total.get(k, 0) + v
        print(f'   pass at {g.ms(p.start_sys - t0):8.2f} ms, {g.cpu_ms(p.cycles):6.2f} ms long, releases {released}')
    print(f'   released by passes starting in the window {total}')
    for name, cycle in sorted(marks.items(), key=lambda kv: kv[1]):
        if name.startswith('backlog.') and t0 <= cycle <= t1:
            probe = next(pr for grp in scenario.backlog_groups(scenario.Point('x', '', 1, 0, 0, 0, 0))
                         for pr in grp.probes if pr.name == name)
            start = g.start(probe, grade.interface_of(name), cycle, t1)
            ring, ahead = g.ahead(probe, start)
            print(f'   {name}: input at {g.ms(start - t0):.3f} ms into the window, {ahead} records ahead in {ring}')
