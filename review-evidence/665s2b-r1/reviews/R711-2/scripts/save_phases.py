#!/usr/bin/env python3
"""One whole save with no other load: the time from the change to the last read-back, and each step's cost.

usage: save_phases.py <checkout> <z-save.log>"""
import sys
root, path = sys.argv[1:3]
sys.path.insert(0, root + '/tb/verilator/ctrl_service_budget'); sys.path.insert(0, root + '/sw/mailbox')
import grade
text = open(path, errors='replace').read()
text = text[:text.rfind('\n') + 1]
if not text.rstrip().rsplit('\n', 1)[-1].startswith('RESULT'):
    text = text.rstrip().rsplit('\n', 1)[0] + '\n'
log = grade.parse(text, 100_000_000, 100_000_000)
marks = dict((n, c) for c, n in log.marks)
t0 = marks['z.set_name.if0']
rows = [(p.start_sys, p.cycles, p.modules.get('nvm_flash_litespi', 0), p.modules.get('nvm_store', 0)) for p in log.passes
        if p.start_sys > t0 and (p.modules.get('nvm_flash_litespi', 0) > 500 or p.modules.get('nvm_store', 0) > 500)]
print('steps', len(rows), 'first', (rows[0][0] - t0) / 1e5, 'ms, last', (rows[-1][0] - t0) / 1e5, 'ms after the change')
last = None; start = None; n = 0
for r in rows + [(0, 0, -1, -1)]:
    key = round(r[2], -3), round(r[3], -3)
    if key != last:
        if last is not None:
            print(f'  {n:4d} steps from +{(start - t0) / 1e5:8.1f} ms: flash port ~{last[0]:7.0f}, store ~{last[1]:6.0f} cycles, pass max {mx}')
        last, start, n, mx = key, r[0], 0, 0
    n += 1; mx = max(mx, r[1])
for l in text.splitlines():
    if l.startswith('FLASH '): print(l)
