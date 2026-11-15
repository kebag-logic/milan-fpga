#!/usr/bin/env python3
"""Replace host paths in the text receipts under a directory with neutral tokens, in place: the scratch directory,
the lane's checkout, the management tree and the home directory. usage: sanitize.py RECEIPTS_DIR"""
import sys
from pathlib import Path

SUBS = (('/data-2/milan/tmp/894-a773', '$SCRATCH'), ('$LANES/894-tiers', '$LANE'),
        ('$LANES', '$LANES'), ('$VALIDATION_TOOLS', '$TOOLS'), ('$VALIDATION_STORAGE/scratch', '$TOOLS'),
        ('$MANAGEMENT', '$MGMT'), ('$WORKSPACE_HOME', '$HOME'), ('/tmp/', '$TMP/'))
n = 0
for f in Path(sys.argv[1]).rglob('*'):
    if not f.is_file():
        continue
    try:
        text = f.read_text()
    except UnicodeDecodeError:
        continue
    new = text
    for a, b in SUBS:
        new = new.replace(a, b)
    if new != text:
        f.write_text(new)
        n += 1
print(f'{n} files rewritten')
