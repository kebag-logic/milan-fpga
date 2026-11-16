#!/usr/bin/env python3
"""la_join.py HARNESS_DIR RESULTS_DIR GROUP...: for each LeaveAll run-out (on_la_timer) of each group, its outcome and
first frame's delay (mrpdu_grade.resolve), how long before it the last MRPDU build ran (the previous transmission),
when the next join timer ran out after it (on_join_timer), and the CPU cycles the passes in between took. An
experiment's read-out; it grades nothing."""
import sys
from bisect import bisect_left, bisect_right
from pathlib import Path

harness, results = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(harness))
import grade  # noqa: E402
import mrpdu_grade  # noqa: E402

MS = 100_000
for group in sys.argv[3:]:
    text = (results / f'{group}.log').read_text(errors='replace')
    log = grade.parse(text[:text.rfind('\n') + 1], 100_000_000, 100_000_000)
    builds = sorted(c for c, n in log.entries if n == 'build_mrpdu')
    joins = sorted(c for c, n in log.entries if n == 'on_join_timer')
    starts = sorted(p.start_sys for p in log.passes)
    passes = sorted(log.passes, key=lambda p: p.start_sys)
    for entry in sorted(c for c, n in log.entries if n == 'on_la_timer'):
        outcome, frames = mrpdu_grade.resolve(log, entry)
        first = frames[0][0] if frames else entry
        k = bisect_left(builds, entry)
        prev = builds[k - 1] if k else None
        j = bisect_right(joins, entry)
        nxt = joins[j] if j < len(joins) else None
        busy = sum(p.cycles for p in passes[bisect_left(starts, entry):bisect_left(starts, first)])
        span = max(first - entry, 1)
        print(f'{group} leaveall {entry / MS:10.3f} ms {outcome:9s} frame +{(first - entry) / MS:7.3f} ms; '
              f'previous build {"-" if prev is None else f"{(entry - prev) / MS:7.3f} ms before"}; '
              f'next join timer {"-" if nxt is None else f"+{(nxt - entry) / MS:7.3f} ms"}; '
              f'CPU busy {busy / MS:6.2f} ms of the wait ({100 * busy / span:4.1f} %)')
