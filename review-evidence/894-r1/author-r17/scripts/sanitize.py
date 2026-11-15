#!/usr/bin/env python3
"""Replace host paths in the text files under a directory with neutral tokens, in place. The substitutions are given
on the command line, longest first, so this file names no host path itself.
usage: sanitize.py DIR FROM=TO [FROM=TO ...]"""
import sys
from pathlib import Path

subs = [a.split('=', 1) for a in sys.argv[2:]]
n = 0
for f in Path(sys.argv[1]).rglob('*'):
    if not f.is_file():
        continue
    try:
        text = f.read_text()
    except UnicodeDecodeError:
        continue
    new = text
    for a, b in subs:
        new = new.replace(a, b)
    if new != text:
        f.write_text(new)
        n += 1
print(f'{n} files rewritten')
