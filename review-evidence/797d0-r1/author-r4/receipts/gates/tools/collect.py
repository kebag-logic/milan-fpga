#!/usr/bin/env python3
"""Copy gate logs into receipts with host paths normalised; a log over 200 KB leaves a .sha256.txt record instead.

usage: collect.py <logs dir> <receipt dir>
Sizes and hashes in a record are of the log as it was written, before normalising.
"""
import hashlib, sys
from pathlib import Path
src, dst = Path(sys.argv[1]), Path(sys.argv[2])
dst.mkdir(parents=True, exist_ok=True)
SUBS = (("$VALIDATION_STORAGE/797-a706d", "<scratch>"), ("$LANES/797-d0-audit", "<lane>"),
        ("$MANAGEMENT/2026-09-23/797-a706d", "<out>"), ("$WORKSPACE_HOME", "~"), ("$VALIDATION_STORAGE", "<data>"))
LIMIT = 200_000
large = 0
for path in sorted(src.iterdir()):
    raw = path.read_bytes()
    text = raw.decode("utf-8", "replace")
    for old, new in SUBS:
        text = text.replace(old, new)
    if len(text.encode()) > LIMIT:
        lines = text.splitlines()
        (dst / (path.name + ".sha256.txt")).write_text(
            f"sha256 {hashlib.sha256(raw).hexdigest()}\nbytes {len(raw)}\nfirst: {lines[0]}\nlast: {lines[-1]}\n")
        large += 1
    else:
        (dst / path.name).write_text(text)
print(f"{src.name}: {len(list(src.iterdir()))} files, {large} over the limit")
