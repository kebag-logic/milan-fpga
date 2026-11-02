#!/usr/bin/env python3
"""Each save window's passes from its observation log: the longest pass of the group and of its window, and every
pass that carries a store step from the window's opening to 40 ms after its close.

usage: savewin.py <checkout> <log>...
A step is a work pass with the flash port's or the store's cycles over 20,000, or a run of passes that wrote nothing
to the mailbox whose longest is over HEAVY cycles: the store's step in a pass that took no input writes nothing to
the mailbox, so the log gives that pass only as its run's longest, and the run ends where the next work pass starts.
A log still being written is read to its last whole line.
"""
import sys

root, logs = sys.argv[1], sys.argv[2:]
sys.path.insert(0, root + '/tb/verilator/ctrl_service_budget')
sys.path.insert(0, root + '/sw/mailbox')
import grade  # noqa: E402

STEP = ('nvm_flash_litespi', 'nvm_store')
#: An idle run's longest over this carries a store step: a pass with nothing to do is at most 43,000 cycles at 8x8.
HEAVY = 60_000
for path in logs:
    text = open(path, errors='replace').read()
    text = text[:text.rfind('\n') + 1]
    if text.count('\n') and not text.rstrip().rsplit('\n', 1)[-1].startswith('RESULT'):
        text = text.rstrip().rsplit('\n', 1)[0] + '\n'
    log = grade.parse(text, 100_000_000, 100_000_000)
    marks = {n: c for c, n in log.marks}
    name = path.rsplit('/', 1)[-1].removesuffix('.log')
    if 'composed' not in marks:
        print(f'{name}: no window yet ({len(log.passes)} work passes)')
        continue
    start, end = marks['composed'], marks.get('composed_end', 1 << 62)
    inside = [p for p in log.passes if start <= p.start_sys <= end]
    near = [p for p in log.passes if start <= p.start_sys <= end + 4_000_000]
    top = max(log.passes, key=lambda p: p.cycles)
    wtop = max(inside, key=lambda p: p.cycles) if inside else None
    idle = max((m for _, _, m in log.idle), default=0)
    print(f'{name}: passes {len(log.passes)}, longest work pass {top.cycles} at {(top.start_sys - start) / 1e5:+.2f} ms, '
          f'window longest {wtop.cycles if wtop else 0}, longest pass with no mailbox write {idle}, over the share '
          f'{sum(1 for p in log.passes if p.cycles > 200_000) + sum(1 for _, _, m in log.idle if m > 200_000)}, '
          f'window {(end - start) / 1e5:.2f} ms')
    # the store's steps around the window: a work pass with its cycles, or the run before a work pass whose longest
    # carries one (the run ends at that work pass's start); the longest gap between two is how long a step waited
    around = [p for p in log.passes if start - 3_000_000 <= p.start_sys <= end + 4_000_000]
    steps = [p.start_sys for p in around if sum(p.modules.get(m, 0) for m in STEP) > 20_000 or p.idle_before > HEAVY]
    gaps = [b - a for a, b in zip(steps, steps[1:])]
    print(f'    store steps from 30 ms before the window to 40 ms after it: {len(steps)}, the longest gap between two '
          f'{max(gaps, default=0) / 1e5:.2f} ms')
    for p in near:
        flash = sum(p.modules.get(m, 0) for m in STEP)
        if flash > 20_000:
            print(f'    step in a work pass {p.cycles} at {(p.start_sys - start) / 1e5:+.2f} ms: store {flash}, other '
                  f'{p.cycles - flash}')
        if p.idle_before > HEAVY:
            print(f'    step in a pass with no mailbox write, its run\'s longest {p.idle_before}, before the work pass at '
                  f'{(p.start_sys - start) / 1e5:+.2f} ms')
