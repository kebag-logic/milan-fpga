#!/usr/bin/env python3
"""Replace host-specific absolute paths in a receipts directory with neutral placeholders, in place.

Usage: redact.py <receipts dir> <path>=<placeholder> [...]
e.g.   redact.py receipts "$PACKET=<packet>" "$CLONE=<clone>" "$HOME=\$HOME"
"""
import sys
from pathlib import Path

subs = [a.split('=', 1) for a in sys.argv[2:]]
for p in sorted(Path(sys.argv[1]).rglob('*')):
    if not p.is_file():
        continue
    t = p.read_text(errors='surrogateescape')
    n = t
    for a, b in subs:
        n = n.replace(a, b)
    if n != t:
        p.write_text(n, errors='surrogateescape')
        print('redacted', p.name)
