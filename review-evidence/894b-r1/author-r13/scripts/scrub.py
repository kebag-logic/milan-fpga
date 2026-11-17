#!/usr/bin/env python3
"""Copy a text file into the packet with host paths replaced by round 10's receipt placeholders ($SCRATCH, $HOME,
/<data-2>, /<data>); a file over 190 KB is excerpted (its first and last 600 lines, the cut named in the file).
usage: scrub.py SRC DST"""
import sys
from pathlib import Path

SUBS = (('/data-2/milan/tmp/894b-a781', '$SCRATCH'), ('$WORKSPACE_HOME', '$HOME'), ('/data-2/milan', '/<data-2>'),
        ('$VALIDATION_STORAGE', '/<data>'), ('hackerman-kl', '<account>'), ('/tmp/', '/<tmp>/'))
src, dst = Path(sys.argv[1]), Path(sys.argv[2])
text = src.read_text(errors='replace')
for a, b in SUBS:
    text = text.replace(a, b)
if len(text.encode()) > 190 * 1024:
    lines = text.splitlines()
    text = '\n'.join([*lines[:600], f'[... {len(lines) - 1200} lines cut: the file is {len(lines)} lines; '
                      'the first and last 600 kept ...]', *lines[-600:]]) + '\n'
dst.parent.mkdir(parents=True, exist_ok=True)
dst.write_text(text)
print(f'{dst}: {len(text.encode()):,} B')
