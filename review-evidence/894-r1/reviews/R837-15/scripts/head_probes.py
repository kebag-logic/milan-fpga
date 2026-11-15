#!/usr/bin/env python3
"""Read-only probes at a milan-fpga checkout (argv[1], the repository root; submodules initialised).

1. rows_grade.py without its module docstring has the same AST, positions included, at 26898c05 and HEAD.
2. tx_statements at each point at HEAD, then with CTRL_LOOP_TX_MS planted in memory (no file is written) under
   and over its row at each interface count.
Usage: python3 -B head_probes.py <repo-root>   (prints one line a result)"""
import ast
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()


def tree(rev):
    src = subprocess.run(['git', '-C', str(root), 'show', f'{rev}:tb/verilator/ctrl_service_budget/rows_grade.py'],
                         capture_output=True, text=True, check=True).stdout
    t = ast.parse(src)
    if t.body and isinstance(t.body[0], ast.Expr) and isinstance(t.body[0].value, ast.Constant):
        t.body = t.body[1:]
    return ast.dump(t, include_attributes=True), src.count('\n')


a, na = tree('26898c05')
b, nb = tree('HEAD')
print(f'rows_grade.py AST without docstring identical 26898c05..HEAD: {a == b}; lines {na} {nb}')

sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_budget'))
import rows_tiers  # noqa: E402

loop = 'sw/firmware/ctrl/loop/ctrl_loop.h'
header = (root / loop).read_text()
fig = '#define CTRL_LOOP_TX_MS (MBX_N_IF == 1u ? 34u : 99u)'
print(f'head figure present once: {header.count(fig) == 1}')
print(f'tx_statements at HEAD: {rows_tiers.tx_statements(root)}')
for leg in ('34u : 98u', '33u : 99u', '34u : 99u', '35u : 100u'):
    texts = {loop: header.replace(fig, fig.replace('34u : 99u', leg))}
    print(leg, {p: rows_tiers.tx_statements(root, (p,), texts) for p in rows_tiers.POINTS})
