#!/usr/bin/env python3
"""Replace host-local path prefixes in receipt files with neutral placeholders.

Usage: python3 -I sanitize_receipts.py <receipts dir> <raw copy dir> [NAME=PREFIX ...]
Each file is first copied unchanged into the raw copy dir (never published),
then rewritten in place: every PREFIX given becomes $NAME (longest first),
the home directory becomes $HOME, a container overlay prefix becomes
$VERILATOR_PREFIX and a /tmp entry becomes $TMPDIR/x. Prints the files changed
and the replacement counts.
"""
import os
import re
import shutil
import sys
from pathlib import Path

src = Path(sys.argv[1])
raw = Path(sys.argv[2])
raw.mkdir(parents=True, exist_ok=True)
home = os.path.expanduser("~")
named = sorted((a.split("=", 1) for a in sys.argv[3:]), key=lambda kv: -len(kv[1]))
rules = [(re.compile(re.escape(home) + r"/\.local/share/containers/storage/overlay/[0-9a-f]+/diff"),
          "$VERILATOR_PREFIX")]
rules += [(re.compile(re.escape(prefix)), "$" + name) for name, prefix in named]
rules += [(re.compile(re.escape(home)), "$HOME"), (re.compile(r"/tmp/[A-Za-z0-9._-]+"), "$TMPDIR/x")]
for p in sorted(src.iterdir()):
    if not p.is_file():
        continue
    text = p.read_text(encoding="utf-8", errors="surrogateescape")
    shutil.copy2(p, raw / p.name)
    n = 0
    for rx, rep in rules:
        text, k = rx.subn(rep, text)
        n += k
    if n:
        p.write_text(text, encoding="utf-8", errors="surrogateescape")
        print(f"{p.name}: {n} replacement(s)")
