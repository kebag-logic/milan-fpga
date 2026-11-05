#!/usr/bin/env python3
"""Copy gate logs into the receipts, verbatim, one directory per source.

usage: collect.py <dest dir> <label> <file or dir>...
A file of at most 200 KB is copied as it is. A larger one is not: its name, size
and sha256 go into <dest>/LARGE-LOGS.txt under its label and scratch-relative
name, and its last 120 lines go beside it as <name>.tail (cut to 64 KB).
"""
import hashlib, shutil, sys
from pathlib import Path

LIMIT = 200 * 1024
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
        size = f.stat().st_size
        if size <= LIMIT:
            shutil.copyfile(f, out)
            continue
        data = f.read_bytes()
        large.append(f"{label}/{rel}\t{size} bytes\tsha256 {hashlib.sha256(data).hexdigest()}")
        tail = b"\n".join(data.splitlines()[-120:])[-64 * 1024:]
        out.with_name(out.name + ".tail").write_bytes(tail + b"\n")
if large:
    with open(dest / "LARGE-LOGS.txt", "a") as fh:
        fh.write("\n".join(large) + "\n")
print(f"{label}: {len(large)} large file(s) recorded by hash")
