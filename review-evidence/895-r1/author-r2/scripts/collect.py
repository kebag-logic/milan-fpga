#!/usr/bin/env python3
"""Copy a run's text outputs into the receipts (lane 895 round 2): each file up to 200 KB with host paths replaced,
each larger one recorded by size and sha256 in large.txt. usage: collect.py SRC DEST [GLOB...]"""
import hashlib, sys
from pathlib import Path
src, dest = Path(sys.argv[1]), Path(sys.argv[2])
globs = sys.argv[3:] or ['**/*']
SUBS = [('/data-2/milan/tmp/895-a775', '<scratch>'), ('$LANES/895-talker', '<clone>'),
        ('$LANES/895r2sweep-shard', '<sweep-clone>'), ('$MANAGEMENT', '<mgmt>'),
        ('$WORKSPACE_HOME', '<home>'), ('$VALIDATION_TOOLS', '<tools>'), ('$VALIDATION_STORAGE/scratch', '<tools>')]
large = []
for g in globs:
    for f in sorted(src.glob(g)):
        if not f.is_file():
            continue
        rel = f.relative_to(src)
        data = f.read_bytes()
        if len(data) > 200_000:
            large.append(f'{len(data)} {hashlib.sha256(data).hexdigest()} {rel}')
            continue
        text = data.decode('utf-8', 'replace')
        for a, b in SUBS:
            text = text.replace(a, b)
        out = dest / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text)
if large:
    with (dest / 'large.txt').open('a') as fh:
        fh.write('\n'.join(large) + '\n')
print(f'{src} -> {dest}: {len(large)} large')
