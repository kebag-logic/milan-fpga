"""gates/extra-table.md: the assignment's named gates beyond the workflows, from their own logs and rc files.

usage: extra_table.py <gates scratch>
Each row's head comes from the log's first line; a gate whose log names another head, or whose rc is not 0, is BAD.
"""
import sys
from pathlib import Path
G = Path(sys.argv[1]); L = G / 'extra' / 'logs'; head = (G / 'HEAD').read_text().strip()
IDS = ['diff-check', 'tally-mutants', 'nvm-self-test', 'test-builder', 'budget-self-test', 'budget-1x1', 'budget-8x8',
       'wire-8x8-none', 'wire-8x8-composed']
rows = ['| Gate | Command | rc | Log |', '|---|---|---:|---|']
bad = 0
for i in IDS:
    log, rc = L / f'{i}.log', L / f'{i}.rc'
    if not rc.exists():
        rows.append(f'| {i} | | MISSING | |'); bad += 1; continue
    first = log.read_text(errors='replace').splitlines()[0]
    cmd = first.split(': ', 1)[1].replace(str(G), '<gates>') if ': ' in first else ''
    r = rc.read_text().strip(); ok = r == '0' and head in first; bad += not ok
    rows.append(f'| {i} | `{cmd}` | {r if ok else "BAD " + r} | `extra/logs/{i}.log` |')
trees = sorted(L.glob('tree-after*.txt'))
rows.append('')
rows.append('Tree after: ' + '; '.join(f'{t.name} {"clean" if not t.read_text().strip() else "DIRTY"}' for t in trees))
rows.append(f'\n{len(IDS)} gates, {bad} bad')
(G / 'extra-table.md').write_text('\n'.join(rows) + '\n')
print('\n'.join(rows))
sys.exit(1 if bad else 0)
