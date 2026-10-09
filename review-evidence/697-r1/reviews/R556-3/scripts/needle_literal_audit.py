#!/usr/bin/env python3
# For each required killer, check that its needle occurs in a string literal of tests/*.cpp
# (an assertion's own streamed message), not only in GoogleTest's default output. argv[1] = tree root.
import json, re, sys
from pathlib import Path
root = Path(sys.argv[1])
literals = [l for p in (root / 'tests').glob('*.cpp') for l in re.findall(r'"((?:\\.|[^"\\])*)"', p.read_text())]
table = json.loads((root / 'tests/mutations.json').read_text())
kills = [(m['name'], k) for m in table for k in m['kills']]
direct = [n for n, k in kills if any(k['needle'] in l for l in literals)]
composed = [(n, k['test'], k['needle']) for n, k in kills if not any(k['needle'] in l for l in literals)]
print(f'kills {len(kills)}; needle inside one test string literal {len(direct)}; composed across streamed values {len(composed)}')
for row in composed:
    print('composed', *row, sep=' | ')
