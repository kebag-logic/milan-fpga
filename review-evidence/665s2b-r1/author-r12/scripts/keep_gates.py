#!/usr/bin/env python3
"""Copy a directory of gate logs into receipts, scrubbing host paths. A file over 200 KB is not copied: its sha256, size and
tail go there instead. usage: keep_gates.py SRC OUT"""
import hashlib
import re
import sys
from pathlib import Path

LIMIT = 200 * 1024
SCRUB = ((re.compile(r'$VALIDATION_STORAGE/665s2b-a683o'), '<scratch>'), (re.compile(r'$LANES/'), '<lanes>/'),
         (re.compile(r'$VALIDATION_TOOLS'), '<tools>'), (re.compile(r'$VALIDATION_STORAGE/scratch'), '<scratch2>'),
         (re.compile(r'$WORKSPACE_HOME'), '<home>'))
src, out = Path(sys.argv[1]), Path(sys.argv[2])
large = []
for f in sorted(p for p in src.rglob('*') if p.is_file()):
    rel = f.relative_to(src)
    data = f.read_bytes()
    text = data.decode('utf-8', 'replace')
    for pattern, repl in SCRUB:
        text = pattern.sub(repl, text)
    dest = out / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    if len(data) > LIMIT:
        large.append(f'{hashlib.sha256(data).hexdigest()}  {len(data)}  {rel}')
        (dest.parent / (dest.name + '.tail')).write_text('\n'.join(text.splitlines()[-200:])[-150000:] + '\n')
    else:
        dest.write_text(text)
(out / 'LARGE-LOGS.txt').write_text('\n'.join(large) + '\n')
print(len(large), 'large')
