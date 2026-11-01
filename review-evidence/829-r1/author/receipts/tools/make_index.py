#!/usr/bin/env python3
"""Write receipts/INDEX.md from the files actually present: path, bytes, sha256."""
import hashlib
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
index = root / "INDEX.md"
rows = []
for path in sorted(p for p in root.rglob("*") if p.is_file() and p != index):
    rows.append((path.relative_to(root), path.stat().st_size,
                 hashlib.sha256(path.read_bytes()).hexdigest()))
lines = ["# Receipts index", "", f"Generated from the {len(rows)} files present.", "",
         "| File | Bytes | sha256 |", "|---|---:|---|"]
lines += [f"| `{rel}` | {size} | `{digest}` |" for rel, size, digest in rows]
index.write_text("\n".join(lines) + "\n")
print(f"{len(rows)} files, largest {max(r[1] for r in rows)} bytes")
