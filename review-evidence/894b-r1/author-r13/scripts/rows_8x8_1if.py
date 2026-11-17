#!/usr/bin/env python3
"""8x8/1if's rows by every source as the tree derives them, with no input supplied from outside it: rows_tiers.rows at
rows_tiers.point_inputs(root, '8x8/1if') (since a840c14d: 8x8/1if's own polls, notices and builds, its records' and
events' costs 8x8/2if's by load_grade.NEAREST), the long-window load and the load with every AECP command the largest
legal one, and what flip_grade.tx_held says of THE TRANSMIT's figure there. Read only; prints the table.
usage: python3 -I rows_8x8_1if.py TREE (the largest-command load as R844-4's published_rows_recipe.py takes it)"""
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_budget'))
import flip_grade  # noqa: E402
import rows_tiers  # noqa: E402

POINT = '8x8/1if'
head = subprocess.run(['git', '-C', str(root), 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
inputs = rows_tiers.point_inputs(root, POINT)
print(f'# {POINT} rows by every source, derived in the tree at {head}')
print(f'stated: CTRL_LOOP_TX_MS {inputs.tx_stated} ms; notices {inputs.s["notices"]}')
print('| Row | W, ms |\n|---|---:|')
for row, (value, _terms) in rows_tiers.rows(root, POINT, rows_tiers.BUILT, inputs).items():
    print(f'| {row} | {value:.2f} |')
print(f'tx_held findings: {flip_grade.tx_held(root, (POINT,)) or "none"}')
import load_grade  # noqa: E402

near = load_grade.NEAREST.get(POINT, POINT)
print(f'long-window load at the pin: {sum(load_grade.load(root, POINT, load_grade.STATED_US).values()):.3f}')
largest = {**load_grade.STATED_US, near: {**load_grade.STATED_US[near], 'record.aecp': rows_tiers.LONG_RECORD_US[POINT],
                                          'item.aecp.notice': rows_tiers.LONG_NOTICE_US[POINT]}}
print(f'with every AECP command the largest legal one: {sum(load_grade.load(root, POINT, largest).values()):.3f} '
      f'(record.aecp {rows_tiers.LONG_RECORD_US[POINT]} us, its notice {rows_tiers.LONG_NOTICE_US[POINT]} us)')
