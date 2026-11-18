#!/usr/bin/env python3
"""blocks.py FILE RESOLUTIONS.py: replace FILE's diff3 conflict blocks, in order, by the texts the list R in
RESOLUTIONS.py gives (each a str, or one of 'ours', 'theirs', 'ours+theirs', 'theirs+ours'). Refuses unless the
counts match and no marker survives."""
import runpy
import sys
from pathlib import Path

path = Path(sys.argv[1])
R = runpy.run_path(sys.argv[2])['R']
lines = path.read_text().splitlines(True)
out, i, n = [], 0, 0
while i < len(lines):
    if not lines[i].startswith('<<<<<<< '):
        out.append(lines[i]); i += 1; continue
    o, b, t, part = [], [], [], 'o'
    i += 1
    while not lines[i].startswith('>>>>>>> '):
        l = lines[i]
        if l.startswith('||||||| '):
            part = 'b'
        elif l.rstrip('\n') == '=======':
            part = 't'
        else:
            {'o': o, 'b': b, 't': t}[part].append(l)
        i += 1
    i += 1
    r = R[n]; n += 1
    text = {'ours': ''.join(o), 'theirs': ''.join(t), 'ours+theirs': ''.join(o + t),
            'theirs+ours': ''.join(t + o)}.get(r, r)
    out.append(text)
assert n == len(R), f'{n} blocks, {len(R)} resolutions'
s = ''.join(out)
assert not any(l.startswith(('<<<<<<< ', '>>>>>>> ', '||||||| ')) or l == '=======' for l in s.splitlines())
path.write_text(s)
print(f'{path}: {n} blocks resolved')
