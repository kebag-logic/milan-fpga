#!/usr/bin/env python3
"""The gate table from a gate run's logs: each gate's command (its log's first line), rc and the
tree's state after it, in the runner's order (summary.md). Usage: gate_table.py GATES_DIR"""
import re
import sys
from pathlib import Path

gates = Path(sys.argv[1])
rows = [line.split(' | ') for line in (gates / 'summary.md').read_text().splitlines()
        if line.startswith('| ') and not line.startswith('| Gate')]
print('| Gate (log `receipts/gates/<gate>.log`) | Command | rc | Tree after |')
print('|---|---|---:|---|')
for name, rc, _seconds, tree in ((r[0][2:], r[1], r[2], r[3][:-2]) for r in rows):
    log = gates / f'{name}.log'
    first = (log.read_text(errors='replace') if log.is_file() else
             (gates / f'{name}.log.digest.txt').read_text()).splitlines()[0]
    m = re.match(r'\$ \(cd (\S+)\) (.*)', first)
    cmd = (m.group(2) if m and m.group(1) == '.' else f'cd {m.group(1)} && {m.group(2)}') if m else '(see digest)'
    cmd = re.sub(r'/\S*/tmp/', '<scratch>/tmp/', cmd)
    cmd = re.sub(r'(PYTHON=)?/\S*/bin/python3?\b', lambda m: 'PYTHON=python3' if m.group(1) else 'python3', cmd)
    print(f'| `{name}` | `{cmd}` | {rc} | {tree} |')
