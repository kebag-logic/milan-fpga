#!/usr/bin/env python3
"""Redact host-specific absolute paths in text receipts, in place.
Usage: redact_receipts.py <receipts-dir>
Replaces the pinned simulator's container root, the user's home and the
review slot root with neutral placeholders; prints each file it changed."""
import pathlib, re, sys
RULES = [
    (re.compile(r"/home/[^/\s]+/\.local/share/containers/storage/overlay/[0-9a-f]+/diff"), "<pinned-sim-root>"),
    (re.compile(r"$VALIDATION_TOOLS/pinned-verilator-5\.050"), "<pinned-sim-wrapper-dir>"),
    (re.compile(r"$REVIEWS/854-r804-3-packet"), "<packet>"),
    (re.compile(r"$REVIEWS/r804-3-854"), "<clone>"),
    (re.compile(r"/home/[^/\s]+"), "<home>"),
]
for path in sorted(pathlib.Path(sys.argv[1]).rglob("*")):
    if not path.is_file():
        continue
    text = path.read_text(errors="replace")
    new = text
    for pattern, repl in RULES:
        new = pattern.sub(repl, new)
    if new != text:
        path.write_text(new)
        print("redacted", path.name)
