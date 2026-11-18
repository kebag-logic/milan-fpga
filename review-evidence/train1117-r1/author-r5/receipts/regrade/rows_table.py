#!/usr/bin/env python3
"""rows_table.py TREE: each point's rows from flip_grade.py --check --point (figure, owner bound, margin), its load
against its ceiling, and its findings, as Markdown; plus THE TRANSMIT's held figure where flip_grade reports it."""
import re
import subprocess
import sys
from pathlib import Path

tree = Path(sys.argv[1])
for point in ('1x1/1if', '8x8/1if', '8x8/2if'):
    out = subprocess.run([sys.executable, '-B', 'tb/verilator/ctrl_service_budget/flip_grade.py', '--check', '--point',
                          point], cwd=tree, capture_output=True, text=True).stdout
    rows, load, held, over = [], None, [], []
    for line in out.splitlines():
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells) >= 5 and cells[0] == point and re.fullmatch(r'[-+]?[\d.]+', cells[2] or 'x') and \
                re.fullmatch(r'[\d.]+', cells[3] or 'x') and re.fullmatch(r'[-+][\d.]+', cells[4] or 'x'):
            rows.append(cells[1:6])
        elif len(cells) >= 4 and cells[0] == point and re.fullmatch(r'0\.\d+', cells[1]) and load is None:
            load = cells[1:4]
        elif line.startswith('HELD'):
            held.append(line)
        elif line.startswith('OVER'):
            over.append(line)
    print(f'### {point}\n')
    if load:
        print(f'Load {load[0]} against its ceiling {load[1]} ({load[2]}).\n')
    print('| Row | Figure, ms | Bound, ms | Margin, ms |\n|---|---:|---:|---:|')
    for r in rows:
        print(f'| {r[0]} | {r[1]} | {r[2]} | {r[3]} |')
    print()
    for h in held:
        print(f'- {h}')
    print(f'- findings: {len(over) + sum(1 for h in held if "OVER" in h)} OVER line(s)' + (':' if over else ''))
    for o in over:
        print(f'  - {o[:220]}')
    print()
