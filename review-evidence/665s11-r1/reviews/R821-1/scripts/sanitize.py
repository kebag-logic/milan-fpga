#!/usr/bin/env python3
"""sanitize.py DIR CHECKOUT [TOOLS_DIR ...]: replace this host's absolute paths in every receipt under DIR with
neutral placeholders, in place, so a published receipt names no home directory or host layout. The packet is
this script's parent directory; CHECKOUT is the reviewed clone; each TOOLS_DIR becomes <tools>."""
import os
import sys
from pathlib import Path

packet = str(Path(__file__).resolve().parents[1])
home = os.path.expanduser('~')
RULES = [(packet, '<packet>'), (str(Path(sys.argv[2]).resolve()), '<checkout>')]
RULES += [(str(Path(t).resolve()), '<tools>') for t in sys.argv[3:]]
RULES += [(home, '$HOME')]
for path in sorted(Path(sys.argv[1]).rglob('*')):
    if not path.is_file():
        continue
    text = path.read_bytes().decode('utf-8', errors='replace')
    new = text
    for old, rep in RULES:
        new = new.replace(old, rep)
    if new != text:
        path.write_text(new)
        print(f'sanitized {path.name}')
