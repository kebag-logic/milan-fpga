#!/usr/bin/env python3
"""The longest gap between consecutive passes that carry the store's step, in each group log of a leg: over the
composed window where the group has one (composed to composed_end), and over the whole log. The store owes a step
every centisecond, so a gap past two ticks means the step waited; THE STEP's age limit takes it as a pass of its own
once more than two centiseconds have been dispatched since it last ran. So the TICK records posted between two
consecutive step-carrying passes are summed too, each its COUNT of centiseconds: with three or more the later one may
be an aged step, with two or fewer it cannot be.

usage: stepgaps.py CHECKOUT RESULTS_DIR SYS_HZ [GROUP_GLOB]
"""
import sys
from pathlib import Path

checkout, results, sys_hz = Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3])
pattern = sys.argv[4] if len(sys.argv) > 4 else '*.log'
sys.path.insert(0, str(checkout / 'tb/verilator/ctrl_service_budget'))
import grade  # noqa: E402

ms = sys_hz / 1000
worst = (0.0, '')
most = (0, '')
TICK = next(v for v, name in grade.EVENT.items() if name == 'TICK')
for path in sorted(results.glob(pattern)):
    log = grade.parse(path.read_text(), sys_hz, sys_hz)
    starts = sorted([s for s, _, _ in log.step_passes] + [p.start_sys for p in log.passes if p.fields.get('step')])
    marks = {name: cycle for cycle, name in log.marks}
    change = marks.get('save.change', marks.get('settled', 0))
    # each TICK record's centiseconds, its COUNT (mailbox.yaml): the age counts centiseconds, not records
    ticks = sorted((c, words[1] & 0xFFFF) for c, words in log.records if words[0] & 0xFF == TICK)

    def longest(lo: int, hi: int) -> tuple[float, int]:
        """The longest gap between consecutive step-carrying passes over [lo, hi], and the most ticks posted in one."""
        inside = [s for s in starts if lo <= s <= hi]
        before = [s for s in starts if s < lo][-1:]
        seq = before + inside
        gaps = [(b - a) / ms for a, b in zip(seq, seq[1:])]
        counts = [sum(n for t, n in ticks if a < t < b) for a, b in zip(seq, seq[1:])]
        return max(gaps, default=0.0), max(counts, default=0)
    whole = longest(change, 1 << 62)
    window = longest(marks['composed'], marks['composed_end']) if 'composed' in marks else None
    if window is not None and window[0] > worst[0]:
        worst = (window[0], path.stem)
    if window is not None and window[1] > most[0]:
        most = (window[1], path.stem)
    print(f"{path.stem}: {len(starts)} step-carrying passes; after its change or settling the longest gap "
          f"{whole[0]:.2f} ms, at most {whole[1]} centiseconds posted in one"
          + (f"; in its composed window {window[0]:.2f} ms, at most {window[1]}" if window is not None else ''))
print(f'longest gap in any composed window: {worst[0]:.2f} ms ({worst[1]}); most centiseconds posted in one: {most[0]} '
      f'({most[1]})')
