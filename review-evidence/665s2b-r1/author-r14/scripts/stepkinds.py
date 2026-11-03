#!/usr/bin/env python3
"""Each kind of the store's step in a leg's group log, from the passes that carry a step (STEPPASS lines and work
passes with step=1) and the flash steps closed inside them (FLASHOP, FLASHPOLL, FLASHRD): the longest pass and the
longest step's own CPU cycles (the store's and its flash port's) of each kind, and every step-carrying pass's longest.

usage: stepkinds.py CHECKOUT LOG SYS_HZ [CHANGE_MARK]
Kinds: erase issue, busy poll, blank-check read-back (reads before the save's first page), page program issue,
verify read-back (reads after the last page), and a step with no flash command: before the erase the capture and the
seal (after the change's first-dirty window), otherwise an idle step.
"""
import sys
from pathlib import Path

checkout, log_path, sys_hz = Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3])
sys.path.insert(0, str(checkout / 'tb/verilator/ctrl_service_budget'))
import grade  # noqa: E402
import save_grade  # noqa: E402

log = grade.parse(log_path.read_text(), sys_hz, sys_hz)
passes = [(s, c, st) for s, c, st in log.step_passes]
passes += [(p.start_sys, p.cycles, p.count('store')) for p in log.passes if p.fields.get('step')]
passes.sort()
save = save_grade.first_save(log)
change = next((c for c, n in log.marks if n == 'save.change'), None)
first_page = save.pages[0][0] if save and save.pages else 1 << 62
last_page = save.pages[-1][0] if save and save.pages else 1 << 62
events = [(c, 'erase issue') for c, op, *_ in log.flash_ops if op == grade.FLASH_ERASE]
events += [(c, 'page program issue') for c, op, *_ in log.flash_ops if op == grade.FLASH_PROGRAM]
events += [(c, 'busy poll') for c in log.polls]
events += [(first, 'blank-check read-back' if first < first_page else 'verify read-back')
           for first, _, _, _ in save_grade.merged_reads(log)]
events.sort()
kinds: dict[str, list] = {}
k = 0
for start, cycles, store in passes:
    end = start + cycles * log.sys_hz // log.cpu_hz
    while k < len(events) and events[k][0] < start:
        k += 1
    inside = [kind for c, kind in events[k:k + 4] if start <= c <= end]
    if inside:
        kind = inside[0]
    elif change is not None and save is not None and change < start < save.erase:
        kind = 'capture or seal, or idle in the first-dirty window'
    else:
        kind = 'idle'
    kinds.setdefault(kind, []).append((cycles, store, start))
print(f'{log_path.name}: {len(passes)} passes carry a step')
for kind, rows in kinds.items():
    top, own = max(rows), max(rows, key=lambda r: r[1])
    print(f'  {kind}: {len(rows)} steps, the longest pass {top[0]} cycles (at {top[2]}), the longest step {own[1]} '
          f'cycles (at {own[2]})')
if passes:
    top = max(passes, key=lambda r: r[1])
    print(f'  every step-carrying pass: the longest {top[1]} cycles ({top[1] / (log.cpu_hz / 1000):.3f} ms) at {top[0]}')
