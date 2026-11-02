#!/usr/bin/env python3
"""One save with no other load, from a log of the measurement-only clone (receipts/measure/R-*/read-backs.patch),
which prints every journal read (FLASHRD cycle from to) and every pass that ran the flash port as a PASS line.

usage: readback.py CHECKOUT LOG...
Each step's cost is the flash port's and the store's cycles in its pass, a step being a pass with the flash port
over 1,000 cycles (the loop's clock read is about 200 a pass). Phases from the FLASHOP lines: erase, its wait and
the blank check before the first page; the program and its waits up to the last page; the verify after it.
Durable is the end of the pass that made the save's last journal read, the verify's last read-back, which moves the
authority (nvm_store.c); ms from the change's mark (save.change), CPU cycles at 100 MHz.
"""
import bisect
import sys

root, logs = sys.argv[1], sys.argv[2:]
sys.path.insert(0, root + '/tb/verilator/ctrl_service_budget')
sys.path.insert(0, root + '/sw/mailbox')
import grade  # noqa: E402

STEP = 1_000
for path in logs:
    text = open(path, errors='replace').read()
    reads = [tuple(int(v) for v in ln.split()[1:4]) for ln in text.splitlines() if ln.startswith('FLASHRD ')]
    log = grade.parse(text, 100_000_000, 100_000_000)
    del text
    t0 = dict((n, c) for c, n in log.marks)['save.change']
    ms = lambda c: (c - t0) / 1e5
    erase = next(c for c, op in log.flash if op == grade.FLASH_ERASE and c > t0)
    pages = [c for c, op in log.flash if op == grade.FLASH_PROGRAM and c > erase]
    starts = [p.start_sys for p in log.passes]
    by_pass = {}
    for c, lo, hi in reads:
        if c > t0:
            k = bisect.bisect_right(starts, c) - 1
            by_pass.setdefault(k, []).append((c, lo, hi))
    print(f'{path.rsplit("/", 1)[-1]}: erase at {ms(erase):+.1f} ms, {len(pages)} pages from {ms(pages[0]):+.1f} to '
          f'{ms(pages[-1]):+.1f} ms, {len(log.passes)} passes printed')
    phases = {}
    for k, p in enumerate(log.passes):
        port = p.modules.get('nvm_flash_litespi', 0)
        if p.start_sys <= t0 or port <= STEP:
            continue
        own = port + p.modules.get('nvm_store', 0)
        got = by_pass.get(k, [])
        programs = [c for c in pages + [erase] if p.start_sys <= c < p.start_sys + p.cycles + 10]
        kind = ('read-back' if got else 'program issue' if any(c in pages for c in programs)
                else 'erase issue' if erase in programs else 'busy poll')
        end = p.start_sys + p.cycles + 10
        phase = ('erase, its wait, blank check' if end < pages[0] else
                 'program, its waits' if p.start_sys <= pages[-1] + 10 else 'verify')
        entry = phases.setdefault((phase, kind), [0, 0, 0, 0, 0])
        entry[0] += 1
        entry[1] = max(entry[1], own)
        entry[2] = max(entry[2], p.cycles)
        entry[3] += sum(hi - lo for _, lo, hi in got)
        entry[4] = max(entry[4], sum(hi - lo for _, lo, hi in got))
    for (phase, kind), (n, own, whole, total, most) in phases.items():
        extra = f', {total} bytes read, at most {most} a step' if total else ''
        print(f'  {phase}, {kind}: {n} steps, the flash port and the store at most {own} cycles a step, its pass at '
              f'most {whole}{extra}')
    after = sorted(k for k in by_pass if log.passes[k].start_sys > pages[-1])
    if after:
        last = log.passes[after[-1]]
        nxt = log.passes[after[-1] + 1].start_sys if after[-1] + 1 < len(log.passes) else last.start_sys + last.cycles
        span = sum(hi - lo for k in after for _, lo, hi in by_pass[k])
        print(f'  durable at {ms(nxt):+.1f} ms after the change: the last of {len(after)} verify read-backs, '
              f'{span} bytes, ends with the pass at {ms(last.start_sys):+.1f} ms')
    print(f'  {sum(1 for c, _, _ in reads if c > t0)} journal reads after the change, the last at '
          f'{ms(max(c for c, _, _ in reads)):+.1f} ms')
    print(f'  FLASH line: {next((ln for ln in open(path) if ln.startswith("FLASH ")), "").strip()}')
