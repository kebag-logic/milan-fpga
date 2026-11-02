#!/usr/bin/env python3
"""How long a save's step waits for a pass that takes it, in a save's windows, from logs of the measurement-only
clone (receipts/measure/R-*/read-backs.patch), which prints every pass that ran the flash port.

usage: stepwait.py CHECKOUT LOG...
A step is a pass with the flash port over 1,000 CPU cycles (the loop's clock read is about 200 a pass); a tick is
an event record of type 4 (TICK), one every 10 ms. A step is owed from the first tick after the step before it,
so its wait is its pass's start less that tick. Reported over the steps whose wait overlaps the window, owed
before its close (composed_end) and taken after its opening (composed), with the longest pass that carried one;
ms at 100 MHz.
"""
import sys

root, logs = sys.argv[1], sys.argv[2:]
sys.path.insert(0, root + '/tb/verilator/ctrl_service_budget')
sys.path.insert(0, root + '/sw/mailbox')
import grade  # noqa: E402

TICK = 4
worst = (0, '')
for path in logs:
    log = grade.parse(open(path, errors='replace').read(), 100_000_000, 100_000_000)
    marks = dict((n, c) for c, n in log.marks)
    start, end = marks['composed'], marks['composed_end']
    ticks = sorted(c for c, words in log.records if words[0] & 0xff == TICK)
    steps = [p for p in log.passes if p.modules.get('nvm_flash_litespi', 0) > 1_000]
    waits, prev = [], 0
    for p in steps:
        owed = next((t for t in ticks if prev < t <= p.start_sys), None)
        prev = p.start_sys
        if owed is not None and owed <= end and p.start_sys >= start:
            waits.append((p.start_sys - owed, p.cycles, owed))
    name = path.rsplit('/', 1)[-1].removesuffix('.log')
    if not waits:
        print(f'{name}: no step waited inside the window')
        continue
    w = max(waits)
    print(f'{name}: {len(waits)} steps waited inside the window ({(end - start) / 1e5:.2f} ms), the longest wait '
          f'{w[0] / 1e5:.2f} ms (owed at {(w[2] - start) / 1e5:+.2f} ms), the longest pass carrying one '
          f'{max(c for _, c, _ in waits)} cycles')
    worst = max(worst, (w[0], name))
print(f'longest wait over every window: {worst[0] / 1e5:.2f} ms, {worst[1]}')
