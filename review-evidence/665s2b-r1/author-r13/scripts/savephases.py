#!/usr/bin/env python3
"""One whole save with no other load, from its log: each phase's steps and their cost, and the time from the
change to durable.

usage: savephases.py CHECKOUT MARK LOG...
MARK is the mark the change follows (save.change for the harness's `save` group, z.set_name.if0 for R711-2's
z-save). The phases come from the log's FLASHOP lines (0xd8 erase, 0x02 page program): before the erase, the
debounce, capture and seal; then the erase, its wait and the blank check; between the first and the last page,
the program phase; after the last, the verify. A step is a work pass with the flash port's or the store's cycles
over 500, its cost read off its modules; or, where the store stepped in a pass that took no input and wrote nothing
to the mailbox, a run of such passes whose longest is over HEAVY cycles, which the log gives as that longest only,
the run ending where the next work pass starts. Durable is the verify's last read-back, the 128-byte step that
moves the authority (nvm_store.c, nvm_commit_done): the save is durable once the verify has read the whole
container, and the time is the start of the work pass after the step that completed it. CPU cycles at 100 MHz; ms
from the change's mark.
"""
import sys

root, mark, logs = sys.argv[1], sys.argv[2], sys.argv[3:]
sys.path.insert(0, root + '/tb/verilator/ctrl_service_budget')
sys.path.insert(0, root + '/sw/mailbox')
import grade  # noqa: E402

STORE = ('nvm_flash_litespi', 'nvm_store')
HEAVY = 60_000
for path in logs:
    text = open(path, errors='replace').read()
    log = grade.parse(text, 100_000_000, 100_000_000)
    marks = {n: c for c, n in log.marks}
    t0 = marks[mark]
    ms = lambda c: (c - t0) / 1e5
    erase = next((c for c, op in log.flash if op == grade.FLASH_ERASE and c > t0), None)
    pages = [c for c, op in log.flash if op == grade.FLASH_PROGRAM and erase is not None and c > erase]
    work = [p for p in log.passes if p.start_sys > t0 and sum(p.modules.get(m, 0) for m in STORE) > 500]
    silent = [p for p in log.passes if p.start_sys > t0 and p.idle_before > HEAVY]
    size = next((int(w.split('=')[1]) for ln in text.splitlines() if ln.startswith('FLASH ') for w in ln.split()
                 if w.startswith('bytes=')), 0)
    if not (erase and pages):
        print(f'{path}: no whole save')
        continue

    def phase(c: int) -> str:
        if c < erase - 20_000:
            return 'debounce, capture, seal'
        if c < pages[0] - 20_000:
            return 'erase, its wait, blank check'
        if c < pages[-1] + 1_000_000:
            return 'program, program wait'
        return 'verify'
    print(f'{path.rsplit("/", 1)[-1]}: erase at {ms(erase):+.1f} ms; {len(pages)} pages, the first at '
          f'{ms(pages[0]):+.1f} ms, the last at {ms(pages[-1]):+.1f} ms; {size} bytes programmed')
    for name in ('debounce, capture, seal', 'erase, its wait, blank check', 'program, program wait', 'verify'):
        own = [p for p in work if phase(p.start_sys) == name]
        quiet = [p for p in silent if phase(p.start_sys) == name]
        line = f'  {name}:'
        if own:
            flash = sorted(p.modules.get('nvm_flash_litespi', 0) for p in own)
            line += (f' {len(own)} steps in work passes, flash port {flash[0]} to {flash[-1]} cycles a step, the longest '
                     f'pass {max(p.cycles for p in own)};')
        if quiet:
            line += (f' {len(quiet)} runs with a step in a pass that wrote nothing to the mailbox, the longest '
                     f'{max(p.idle_before for p in quiet)} cycles;')
        print(line)
    need = -(-size // 128)  # the verify's 128-byte steps over the container (NVM_READ_BYTES)
    reads = sorted([p for p in work if p.start_sys > pages[-1] and p.count('load_flash')] +
                   [p for p in silent if p.start_sys > pages[-1] + 1_000_000], key=lambda p: p.start_sys)
    if len(reads) >= need > 0:
        print(f'  durable by {ms(reads[need - 1].start_sys):+.1f} ms after the change: the {need}th verify read-back, '
              f'before the work pass that starts then; {len(reads)} read-backs seen after the last page')
    else:
        print(f'  not durable within the log: {len(reads)} of the {need} verify read-backs of {size} bytes')
