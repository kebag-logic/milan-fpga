"""backlog-owed at 8x8/1if on two images, from their traces (read only): when the composed window opens and the egress
hold releases (MARK composed, MARK room), the release's place in its millisecond (the trace's MS lines), the rows the
egress decides, and every pass and transmit completion from the release to 215,000 cycles after it, each relative to
the release in us. usage: python3 -I aecp_last_phase.py NAME=LEG_DIR NAME=LEG_DIR (each with results/backlog-owed.*)"""
import json
import re
import sys
from pathlib import Path

for arg in sys.argv[1:]:
    name, leg = arg.split('=', 1)
    res = Path(leg) / 'results'
    marks, ms, lines = {}, [], []
    for line in (res / 'backlog-owed.log').read_text().splitlines():
        w = line.split()
        if w and w[0] == 'MARK' and w[2] in ('composed', 'room'):
            marks[w[2]] = int(w[1])
        elif w and w[0] == 'MS':
            ms.append(int(w[1]))
        lines.append(line)
    room, composed = marks['room'], marks['composed']
    edge = max(t for t in ms if t <= room)
    print(f'== {name}: composed window at {composed:,}, release at {room:,} ({room - composed:,} cycles after it), '
          f'{(room - edge) / 100:.1f} us past a millisecond')
    rows = {p['probe']: p['ms'] for p in json.loads((res / 'backlog-owed.json').read_text())['probes']
            if 'owed' in p['probe'] and ('last' in p['probe'] or p['probe'].startswith('backlog.owed'))}
    print('rows, ms: ' + ', '.join(f'{k} {v:.5f}' for k, v in rows.items()))
    for line in lines:
        w = line.split()
        if not w:
            continue
        if w[0] == 'PASS' and room <= int(w[2]) <= room + 215_000:
            m = re.search(r'mods=(\S+)', line)
            mods = dict(x.split(':') for x in m[1].rstrip(',').split(',')) if m else {}
            top = sorted(((int(v), k) for k, v in mods.items()), reverse=True)[:4]
            print(f'  pass at +{(int(w[2]) - room) / 100:7.1f} us, {int(w[4]):,} cycles: '
                  + ', '.join(f'{k} {v:,}' for v, k in top))
        elif w[0] == 'TXC' and room <= int(w[1]) <= room + 215_000:
            print(f'  transmit complete at +{(int(w[1]) - room) / 100:7.1f} us, channel {w[2]}')
