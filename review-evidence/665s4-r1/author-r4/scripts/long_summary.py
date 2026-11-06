#!/usr/bin/env python3
"""Join the long gate set's two runner logs into one table: the seven gates the host reset of 2026-11-05 13:10
left finished (receipts/gates-long/runner.log) and the four that re-ran from the start at the same head
(receipts/gates-long-rest/runner.log). It refuses a gate missing, a gate in both, or two heads.
Usage: long_summary.py PACKET_DIR"""
import re
import sys
from pathlib import Path

LONG = ('builder_require_rv32 ctrl_nvm ctrl_firmware fw_coverage_selftest fw_coverage nvm_cosim nvm_cosim_lint '
        'publication_census firmware_boundary firmware_boundary_verilator ctrl_memory').split()
LINE = re.compile(r'^(\w+) rc=(-?\d+) \(([\d.]+) s\) tree (\w+)$')

receipts = Path(sys.argv[1]) / 'receipts'
rows, heads = {}, set()
for part in ('gates-long', 'gates-long-rest'):
    heads.add((receipts / part / 'HEAD.txt').read_text().strip())
    for line in (receipts / part / 'runner.log').read_text().splitlines():
        found = LINE.match(line)
        if not found:
            continue
        if found[1] in rows:
            raise SystemExit(f'{found[1]} finished in both parts')
        rows[found[1]] = (part, int(found[2]), float(found[3]), found[4])
missing = [name for name in LONG if name not in rows]
if missing or len(heads) != 1:
    raise SystemExit(f'missing {missing}, heads {sorted(heads)}')
bad = [name for name, (_, rc, _, tree) in rows.items() if rc != 0 or tree != 'clean']
lines = [f'head {heads.pop()}', '', '| Gate | Part | rc | s | Tree after |', '|---|---|---:|---:|---|']
lines += [f'| {name} | {rows[name][0]} | {rows[name][1]} | {rows[name][2]} | {rows[name][3]} |' for name in LONG]
lines += ['', f'{len(bad)} of {len(LONG)} gates nonzero or left the tree dirty']
(receipts / 'gates-long-summary.md').write_text('\n'.join(lines) + '\n')
print(lines[-1])
raise SystemExit(1 if bad else 0)
