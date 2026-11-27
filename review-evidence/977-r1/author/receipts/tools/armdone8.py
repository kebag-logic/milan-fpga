#!/usr/bin/env python3
"""armdone8.py: each arm's groups finished (a DONE in round 7's pool, or for the five rescripted groups of the none and
answering-ports arms in round 8's), of its groups."""
import json
from pathlib import Path
T = Path('<scratch>')
RE = {'adp-link', 'adp-gm', 'adp-discover', 'adp-advertise', 'control'}
for p in ('1x1', '8x8-1if'):
    for b in sorted((T / 'r8/b' / p).iterdir()):
        names = [g['name'] for g in json.loads((b / 'groups.json').read_text())]
        def done(g):
            r = 'r8' if (b.name in ('none', 'answering-ports') and g in RE) else 'r7'
            return (T / r / 'arms' / p / b.name / f's-{g}' / 'DONE').exists()
        n = sum(done(g) for g in names)
        print(f'{p} {b.name}: {n} of {len(names)}{"  COMPLETE" if n == len(names) else ""}')
