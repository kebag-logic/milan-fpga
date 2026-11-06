#!/usr/bin/env python3
"""Round 16 item 2's table (#665, ctrl_loop.h, THE SHARE): each pass class's heaviest measured pass, CPU cycles and
its margin under the 200,000-cycle share, per column of legs (a column's legs' results directories pooled), with
the group that holds it. Classes as passclass.py reads them off the logs.

usage: classtable.py BUILDS OUT.md "LABEL=LEG[,LEG...]" ...   (a LEG is BUILDS/LEG/results, or LEG@SUBDIR)
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
builds, out, *cols = sys.argv[1:]
ORDER = (('records', 'takes a record: its events, its records, two a channel (one in a pass that dispatches a '
                     'centisecond), and the polls'),
         ('events', 'takes events and no record: the polls, and at most one event beside THE TRANSMIT\'s build'),
         ('none', 'takes nothing and writes to the mailbox: the polls\' owed output, THE TRANSMIT\'s build, '
                  'THE RETRY\'s round, THE STEP before its deadline'),
         ('whole-step', 'given whole to an aged step: the step and THE RETRY\'s round'),
         ('whole', 'given whole to an aged retry: one round'),
         ('whole-transmit', 'given whole to an aged build: one build and one round'),
         ('idle', 'writes nothing to the mailbox: the polls with nothing owed, or THE STEP before its deadline (a run\'s '
                  'longest)'),
         ('build', 'of the above, one that carries THE TRANSMIT\'s build or the poll\'s owed SRP frame'),
         ('step', 'of the above, one that carries the store\'s step'))
table = {}
for col in cols:
    label, legs = col.split('=', 1)
    dirs = []
    for leg in legs.split(','):
        name, _, sub = leg.partition('@')
        dirs.append(str(Path(builds) / name / (sub or 'results')))
    res = subprocess.run([sys.executable, str(HERE / 'passclass.py'), *dirs, '--json'], capture_output=True,
                         text=True, check=True)
    table[label] = json.loads(res.stdout)
lines = ['| Class | What it holds | ' + ' | '.join(table) + ' |', '|---|---|' + '---:|' * len(table)]
for cls, what in ORDER:
    cells = []
    for label, data in table.items():
        b = data['best'].get(cls)
        cells.append('-' if b is None else f"{b['cycles']:,} ({200_000 - b['cycles']:,} under; {b['group']})")
    lines.append(f'| {cls} | {what} | ' + ' | '.join(cells) + ' |')
Path(out).write_text('\n'.join(lines) + '\n')
print('\n'.join(lines))
