#!/usr/bin/env python3
"""Copy gate logs into the receipts, one directory per source, with host path prefixes redacted.

usage: collect.py <dest dir> <label> <file or dir>...
A file of at most 200 KB is copied with the prefixes in REDACT replaced by their placeholders (nothing else
changes). A larger one is not copied: its name, size and the sha256 of the ORIGINAL go into <dest>/LARGE-LOGS.txt
under its label and relative name, and its last 120 lines go beside it as <name>.tail (cut to 64 KB, redacted).
"""
import hashlib, sys
from pathlib import Path

LIMIT = 200 * 1024
REDACT = [(b"$MANAGEMENT", b"<management>"), (b"$WORKSPACE_HOME", b"<home>"),
          (b"$LANES", b"<lanes>"), (b"$VALIDATION_STORAGE", b"<scratch>"), (b"$VALIDATION_STORAGE", b"<data>"),
          (b"/srv/act-slots", b"<slots>")]


def redact(data: bytes) -> bytes:
    for a, b in REDACT:
        data = data.replace(a, b)
    return data


dest, label = Path(sys.argv[1]), sys.argv[2]
dest.mkdir(parents=True, exist_ok=True)
large = []
for arg in sys.argv[3:]:
    src = Path(arg)
    files = sorted(p for p in src.rglob("*") if p.is_file()) if src.is_dir() else [src]
    base = src if src.is_dir() else src.parent
    for f in files:
        rel = f.relative_to(base)
        out = dest / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        data = f.read_bytes()
        if len(data) <= LIMIT:
            out.write_bytes(redact(data))
            continue
        large.append(f"{label}/{rel}\t{len(data)} bytes\tsha256 {hashlib.sha256(data).hexdigest()}")
        tail = b"\n".join(data.splitlines()[-120:])[-64 * 1024:]
        out.with_name(out.name + ".tail").write_bytes(redact(tail) + b"\n")
if large:
    with open(dest / "LARGE-LOGS.txt", "a") as fh:
        fh.write("\n".join(large) + "\n")
print(f"{label}: {len(large)} large file(s) recorded by hash")
