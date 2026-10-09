#!/usr/bin/env python3
"""Replace host-specific absolute path prefixes in receipt files with placeholders.

Usage: sanitize_paths.py <file>...   (rewrites in place; longest prefix first)
Placeholders: $PACKET (this review packet), $CLONE (the reviewed clone),
$TOOLS (the reviewer host's tool directory), $VERILATOR_ROOT_DIR (where the
pinned Verilator wrapper's installation lives), $SV2V13_DIR (the directory
holding sv2v 0.0.13), $USER_HOME. Only path text changes; no result does.
"""
import re
import sys

RULES = [
    (re.compile(r"/home/[^/\s]+/\.local/share/containers/storage/overlay/[0-9a-f]+/diff/usr/share/verilator"),
     "$VERILATOR_ROOT_DIR"),
    (re.compile(r"/home/[^/\s]+/\.local/bin"), "$SV2V13_DIR"),
    (re.compile(r"$REVIEWS/641-r566-2-packet"), "$PACKET"),
    (re.compile(r"$REVIEWS/r566-2-641"), "$CLONE"),
    (re.compile(r"$VALIDATION_TOOLS"), "$TOOLS"),
    (re.compile(r"/home/(?!runner/)[^/\s]+"), "$USER_HOME"),
]
for name in sys.argv[1:]:
    with open(name, encoding="utf-8", errors="surrogateescape") as handle:
        text = handle.read()
    for pattern, repl in RULES:
        text = pattern.sub(repl, text)
    with open(name, "w", encoding="utf-8", errors="surrogateescape") as handle:
        handle.write(text)
