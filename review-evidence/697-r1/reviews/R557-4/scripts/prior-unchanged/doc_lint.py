#!/usr/bin/env python3
# Sentence-length and relative-link lint for changed docs; argv[1] = tree root, rest = files.
import re, sys
from pathlib import Path
root = Path(sys.argv[1])
for name in sys.argv[2:]:
    path = root / name
    text = path.read_text()
    prose = re.sub(r'```.*?```', '', text, flags=re.S)
    prose = '\n'.join(l for l in prose.splitlines() if not l.lstrip().startswith('|') and not l.startswith('#'))
    prose = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', prose)
    for s in re.split(r'(?<=[.!?])\s+|\n\n', prose):
        words = s.split()
        if len(words) > 25:
            print(f'{name}: {len(words)} words: {" ".join(words)[:120]}')
    for target in re.findall(r'\]\(([^)#\s]+)(?:#[^)]*)?\)', text):
        if not re.match(r'https?:', target) and not (path.parent / target).exists():
            print(f'{name}: broken relative link {target}')
print('lint done')
