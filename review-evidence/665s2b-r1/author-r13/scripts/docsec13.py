#!/usr/bin/env python3
"""Fill this round's subsection of docs/design/SPLIT_CONTROL_MEMORY.md from the legs: every table cell from a leg's
results or a log, and the prose's figures from the same data. Prints the filled text and writes figures.json.

usage: docsec13.py CHECKOUT BUILDS RECEIPTS TEMPLATE OUT
"""
import json
import subprocess
import sys
from pathlib import Path

checkout, builds, receipts, template, out = sys.argv[1:6]
B = Path(builds)
HERE = Path(__file__).parent
sys.argv = [sys.argv[0], checkout, builds, '/dev/null']
sys.path.insert(0, str(HERE))
import rows13  # noqa: E402
sys.path.insert(0, str(Path(checkout) / 'tb/verilator/ctrl_service_budget'))
import grade  # noqa: E402

load = lambda name: rows13.load(B / name)
COLS = [('1x1/1if', 'N-A1,N-B1'), ('1x1/1if, with both drafts', 'D-A1,D-B1'), ('8x8/2if', 'N-A8,N-B8'),
        ('8x8/2if, with both drafts', 'D-A8,D-B8')]
columns = [(label, [load(n) for n in legs.split(',')]) for label, legs in COLS]


def table_lines(which: str) -> list[str]:
    lines = rows13.table(columns, which, '')[2:]
    return [ln for ln in lines if ln]


def share_line(which: str) -> str:
    return ' / '.join if False else None


def share_table() -> list[str]:
    head = ['| Groups | ' + ' | '.join(c[0] for c in columns) + ' |', '|---|' + '---:|' * len(columns)]
    rows = []
    for which, label in (('backlog', 'The four backlog windows'), ('save', "A save's 24 windows"),
                         ('all', 'Every group the leg ran')):
        rows.append(f'| {label} | ' + ' | '.join(' / '.join(rows13.share_cell(r, which) for r in legs)
                                                  for _, legs in columns) + ' |')
    return head + rows


def worst(which: str, row: str) -> float:
    return max(rows13.worst(r, which)[row][0][1] for _, legs in columns for r in legs if row in rows13.worst(r, which))


def total_over(which: str) -> tuple[int, int]:
    over = passes = 0
    for _, legs in columns:
        for r in legs:
            o, p, _, _ = rows13.shares(r, which)
            over, passes = over + o, passes + p
    return over, passes


def step_pass(legs: list[str]) -> float:
    """The longest pass that carries a store step in a save's windows, from the logs."""
    longest = 0
    for leg in legs:
        for log in sorted((B / leg / 'results').glob('backlog-adp@*.log')):
            parsed = grade.parse(log.read_text(errors='replace'), 100_000_000, 100_000_000)
            for p in parsed.passes:
                if p.modules.get('nvm_flash_litespi', 0) + p.modules.get('nvm_store', 0) > 20_000:
                    longest = max(longest, p.cycles)
            longest = max([longest] + [m for _, _, m in parsed.idle])
    return longest / 1e5


figures = {}
figures['save_rows'] = '\n'.join(table_lines('save'))
figures['rows'] = '\n'.join(table_lines('backlog'))
figures['share'] = '\n'.join(share_table())
o, p = total_over('save')
figures['save_over'], figures['save_passes'] = o, p
o8, _ = total_over('all')
figures['all_over'] = o8
figures['srp8_save'] = max(worst('save', 'SRP record, last') for _ in [0])
figures['srp8_backlog'] = worst('backlog', 'SRP record, last')
figures['aecp_save'] = worst('save', 'AECP record, last')
figures['step_pass'] = step_pass(['N-A8', 'N-B8', 'D-A8', 'D-B8', 'N-A1', 'N-B1', 'D-A1', 'D-B1'])
text = Path(template).read_text()
Path(out).write_text(json.dumps({k: v for k, v in figures.items() if not isinstance(v, str)}, indent=1) + '\n')
print(json.dumps({k: v for k, v in figures.items() if not isinstance(v, str)}, indent=1))
print(figures['save_rows'])
print(figures['rows'])
print(figures['share'])
