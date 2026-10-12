#!/usr/bin/env python3
"""Replace home and toolchain paths in receipts with neutral placeholders, in
place, plus any PATH=PLACEHOLDER pairs given in SANITIZE_MAP (separated by
semicolons). Usage: SANITIZE_MAP="/path/a=<clone>" sanitize.py <file>..."""
import os
import re, sys
SUBS = [
    (re.compile(r"/home/[^/\s]+/\.local/share/containers/storage/overlay/[0-9a-f]+/diff/usr/share/verilator"), "<verilator-root>"),
    (re.compile(r"/home/[^/\s]+/\.local/share/containers/storage/overlay/[0-9a-f]+/diff/usr/bin/verilator"), "<verilator-bin>"),
    (re.compile(r"/home/[^/\s]+"), "$HOME"),
    (re.compile(r"/tmp/claude-[^\s]*"), "<tmp>"),
]
for pair in filter(None, os.environ.get("SANITIZE_MAP", "").split(";")):
    old, new = pair.split("=", 1)
    SUBS.insert(0, (re.compile(re.escape(old)), new))
for f in sys.argv[1:]:
    t = open(f, encoding="utf-8", errors="surrogateescape").read()
    n = t
    for rx, rep in SUBS:
        n = rx.sub(rep, n)
    if n != t:
        open(f, "w", encoding="utf-8", errors="surrogateescape").write(n)
        print("sanitized", f)
