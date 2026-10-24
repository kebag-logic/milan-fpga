"""Copy receipt files into the output directory with host paths replaced by placeholders.

usage: python3 -I redact_copy.py <dest-dir> <src>[=<name>] ...
Placeholders: <tmp>, <scratch>, <tools>, <lanes>, <home>. Refuses a file over 200 KB (record sha256 and size instead).
"""
from pathlib import Path
import sys

SUBS = [('$VALIDATION_STORAGE/773-a664', '<tmp>'), ('$VALIDATION_STORAGE/scratch/773-a664', '<scratch>'),
        ('$VALIDATION_TOOLS', '<tools>'), ('$LANES', '<lanes>'), ('$WORKSPACE_HOME', '<home>')]
dest = Path(sys.argv[1])
dest.mkdir(parents=True, exist_ok=True)
for arg in sys.argv[2:]:
    src, _, name = arg.partition('=')
    src = Path(src)
    text = src.read_text(errors='replace')
    for a, b in SUBS:
        text = text.replace(a, b)
    assert len(text.encode()) <= 200_000, f'{src} is over 200 KB'
    (dest / (name or src.name)).write_text(text)
    print(f'{src.name} -> {dest.name}/{name or src.name}')
