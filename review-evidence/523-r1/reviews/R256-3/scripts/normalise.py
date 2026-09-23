#!/usr/bin/env python3
"""Replace literal host paths in published receipts with neutral placeholders.

Usage: normalise.py RECEIPT_DIR NAME=PATH [NAME=PATH ...]
Each PATH is replaced by $NAME, longest first; then the scoped tool's
container image root and the caller's home directory are replaced too.
Originals are kept, unpublished, by the caller.
"""
import re, sys
from pathlib import Path

pairs = sorted((arg.split("=", 1) for arg in sys.argv[2:]), key=lambda kv: -len(kv[1]))
home = re.escape(str(Path.home()))
rules = [(re.compile(home + r"/\.local/share/containers/storage/overlay/[0-9a-f]+/diff"), "$VERILATOR_IMAGE_ROOT")]
rules += [(re.compile(re.escape(path)), "$" + name) for name, path in pairs]
rules += [(re.compile(home), "$HOME")]
for path in sorted(Path(sys.argv[1]).rglob("*")):
    if path.is_file():
        text = path.read_text(errors="surrogateescape")
        new = text
        for rule, repl in rules:
            new = rule.sub(lambda m, r=repl: r, new)
        if new != text:
            path.write_text(new, errors="surrogateescape")
            print("normalised", path)
