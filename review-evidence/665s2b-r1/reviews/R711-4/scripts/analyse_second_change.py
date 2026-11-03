#!/usr/bin/env python3
"""Probe P2's analysis (review R711-4): each save the log shows, read off its flash operations as
save_grade.first_save reads the first (its erase, its pages before the next erase, the read-backs after its last
page until they cover the image), timed from the change marks (save.change, save2.change) against
save_window.bound_ms for the image the group declares.

usage: python3 -I analyse_second_change.py <tree> <results dir> <group>
"""
import dataclasses
import json
import sys
from pathlib import Path

tree, results, name = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
sys.path.insert(0, str(tree / 'tb/verilator/ctrl_service_budget'))
import grade  # noqa: E402
import save_grade  # noqa: E402
import save_window  # noqa: E402

SYS_HZ = CPU_HZ = 100_000_000
log = grade.parse((results / f'{name}.log').read_text(), SYS_HZ, CPU_HZ)
result = json.loads((results / f'{name}.json').read_text())
image = result['save']['image']
bound = save_window.bound_ms(image, save_window.CHANGED)
marks = {m: c for c, m in log.marks}
erases = [c for c, op, _, _ in log.flash_ops if op == grade.FLASH_ERASE]
print(f'group {name}: image {image} B, stated worst case {bound} ms ({save_window.steps(image, 2)} steps)')
print(f'marks: ' + ', '.join(f'{k} {v / 1e5:.3f} ms' for k, v in marks.items()))
print(f'erases at: ' + ', '.join(f'{c / 1e5:.3f} ms' for c in erases))
print(f'floods: {log.floods}')
saves = []
for n, e in enumerate(erases):
    view = dataclasses.replace(log, flash_ops=[x for x in log.flash_ops if x[0] >= e],
                               reads=[x for x in log.reads if x[0] >= e], polls=[x for x in log.polls if x >= e])
    s = save_grade.first_save(view)
    saves.append(s)
    print(f'save {n + 1}: erase {s.erase / 1e5:.3f} ms, slot {s.base:#x}, {len(s.pages)} pages, {s.image} B, '
          f'durable {s.durable / 1e5 if s.durable else None} ms')
# The first change is written by the first save. The second comes SECOND_MS after the first, once the first save's
# capture has ended (its first-dirty window, then its capture's steps, at most CTRL_LOOP_STEP_AGE + 1 ticks apart:
# at 1x1 within 1,000 + 10 + 4 x 30 ms of the first change), so it opens a window of its own and is written by the
# next save, the second the log shows (nvm_store.c: nvm_mark, nvm_idle).
for n, label in ((0, 'save.change'), (1, 'save2.change')):
    change = marks.get(label)
    if change is None or n >= len(saves) or not saves[n].durable:
        print(f'{label}: its save is not durable in the run')
        continue
    ms = (saves[n].durable - change) / 1e5
    print(f'{label}: durable in save {n + 1} (erase {saves[n].erase / 1e5:.3f} ms), {ms:.3f} ms after the change, '
          f'against the stated worst case {bound} ms: {"within" if ms <= bound else "OVER by %.3f ms" % (ms - bound)}')
print(f"harness's own save_time (first save from save.change): {result['save']}")
