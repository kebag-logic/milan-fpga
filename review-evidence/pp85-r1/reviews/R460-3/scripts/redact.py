#!/usr/bin/env python3
"""Replace host paths in every text receipt under DIR, in place.

usage: redact.py DIR PREFIX=LABEL [PREFIX=LABEL ...]
Longer prefixes are replaced first, so a nested path keeps its most specific label.
"""
import sys
from pathlib import Path

root = Path(sys.argv[1])
subs = sorted((arg.split("=", 1) for arg in sys.argv[2:]), key=lambda s: -len(s[0]))
changed = 0
for f in sorted(root.rglob("*")):
    if not f.is_file():
        continue
    try:
        text = f.read_text()
    except UnicodeDecodeError:
        continue
    new = text
    for prefix, label in subs:
        new = new.replace(prefix, label)
    if new != text:
        f.write_text(new)
        changed += 1
print(f"redacted {changed} files")
