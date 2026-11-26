#!/usr/bin/env python3
"""R941-1: the split-target commit case's erase after its `committing` mark, from a finished run's log.

Usage: commit_window.py <clone> <commit.log> <sys_hz>. Prints the erases, the wait in ms and the head's own
target_grade.windowed verdict ([] = within its window bounds).
"""
import sys
from pathlib import Path

clone, log, sys_hz = Path(sys.argv[1]).resolve(), Path(sys.argv[2]), int(sys.argv[3])
for sub in ('tb/verilator/nvm_split_target', 'tb/verilator/ctrl_service_budget'):
    sys.path.insert(0, str(clone / sub))
import target_grade as tg  # noqa: E402
import grade as budget  # noqa: E402

text = log.read_text(errors='replace')
obs = tg.observe(text, sys_hz, sys_hz)
marks = [(c, n) for c, n in obs.log.marks if n == 'committing']
erases = [c for c, op, *_ in obs.log.flash_ops if op == budget.FLASH_ERASE]
print('committing mark cycles:', [c for c, _ in marks])
print('erase cycles:', erases)
if marks and erases:
    print(f'first erase {(erases[0] - marks[0][0]) * 1000.0 / sys_hz:.1f} ms after the committing mark')
print('window bounds (ms):', tg.window_bounds())
print('windowed findings:', tg.windowed(obs))
