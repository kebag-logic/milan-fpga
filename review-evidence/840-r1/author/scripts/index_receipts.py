#!/usr/bin/env python3
"""Redact host paths in every receipt under <out>/receipts, then write
<out>/receipts/INDEX.md from the files present (path, size, sha256).
Usage: index_receipts.py <out-dir>"""
import hashlib
import socket
import sys
from pathlib import Path

out = Path(sys.argv[1])
receipts = out / "receipts"
RULES = (("$VALIDATION_STORAGE/840-a732", "<scratch>"),
         ("$LANES/840-identity-link", "<lane>"),
         ("$LANES", "<lanes>"),
         ("$VALIDATION_TOOLS", "<tools>"),
         ("$VALIDATION_STORAGE/scratch", "<scratch2>"),
         ("$VALIDATION_STORAGE", "<tmp>"),
         ("$MANAGEMENT", "<management>"),
         ("$WORKSPACE_HOME", "<home>"),
         (socket.gethostname(), "<host>"))
rows = []
for path in sorted(p for p in receipts.rglob("*") if p.is_file() and p.name != "INDEX.md"):
    data = path.read_bytes()
    try:
        text = data.decode()
    except UnicodeDecodeError:
        text = None
    if text is not None:
        new = text
        for old, mark in RULES:
            new = new.replace(old, mark)
        if new != text:
            path.write_text(new)
            data = new.encode()
    if len(data) > 200 * 1024:
        raise SystemExit(f"{path}: {len(data)} bytes, over the 200 KB receipt limit")
    rows.append((path.relative_to(receipts).as_posix(), len(data), hashlib.sha256(data).hexdigest()))
lines = ["# Receipt index", "", "Generated from the files present by scripts/index_receipts.py.", "",
         "| File | Bytes | sha256 |", "|---|---:|---|"]
lines += [f"| `{name}` | {size} | `{digest}` |" for name, size, digest in rows]
(receipts / "INDEX.md").write_text("\n".join(lines) + "\n")
print(f"{len(rows)} receipts indexed")
