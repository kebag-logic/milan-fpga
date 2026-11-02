#!/usr/bin/env python3
"""This round's tables and figures for SPLIT_CONTROL_MEMORY.md section 13, from the legs' results (rows13.py's
rules): the rows over a save's 24 windows and over the four backlog windows, the per-pass share of each set, and the
figures the prose names. Writes OUT.md (the tables) and OUT.json (the figures).

usage: fig13.py CHECKOUT BUILDS OUT
"""
import json
import sys
from pathlib import Path

checkout, builds, out = sys.argv[1:4]
sys.argv = [sys.argv[0], checkout, builds, '/dev/null']
sys.path.insert(0, str(Path(__file__).parent))
import rows13  # noqa: E402

B = Path(builds)
COLS = [('1x1/1if', 'N-A1,N-B1'), ('1x1/1if, with both drafts', 'D-A1,D-B1'), ('8x8/2if', 'N-A8,N-B8'),
        ('8x8/2if, with both drafts', 'D-A8,D-B8')]
columns = [(label, [rows13.load(B / n) for n in legs.split(',')]) for label, legs in COLS]
names = {label: legs.split(',') for label, legs in COLS}


def share_rows() -> list[str]:
    head = ['| Groups | ' + ' | '.join(c[0] for c in columns) + ' |', '|---|' + '---:|' * len(columns)]
    return head + [f'| {label} | ' + ' | '.join(' / '.join(rows13.share_cell(r, which) for r in legs)
                                                 for _, legs in columns) + ' |'
                   for which, label in (('backlog', 'The four backlog windows'), ('save', "A save's 24 windows"),
                                        ('all', 'Every group the leg ran'))]


figures = {}
for which in ('backlog', 'save', 'all'):
    for label, legs in columns:
        for leg, res in zip(names[label], legs):
            over, passes, longest, groups = rows13.shares(res, which)
            w = rows13.worst(res, which)
            figures[f'{which}:{leg}'] = dict(
                over=over, passes=passes, longest=round(longest, 3), groups=groups,
                srp_last=w.get('SRP record, last', ((0, 0),))[0][1],
                aecp_last=w.get('AECP record, last', ((0, 0),))[0][1],
                misses=sorted(r for r, e in w.items() if not e[1]))
text = ['## A save\'s windows', ''] + [ln for ln in rows13.table(columns, 'save', '')[2:] if ln]
text += ['', '## The four backlog windows', ''] + [ln for ln in rows13.table(columns, 'backlog', '')[2:] if ln]
text += ['', '## The share', ''] + share_rows()
Path(out + '.md').write_text('\n'.join(text) + '\n')
Path(out + '.json').write_text(json.dumps(figures, indent=1) + '\n')
print('\n'.join(text))
for k, v in figures.items():
    print(k, v)
