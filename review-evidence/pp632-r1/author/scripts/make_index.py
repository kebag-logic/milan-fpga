#!/usr/bin/env python3
"""Write receipts/INDEX.md from the files present: path, size, sha256, and the
first line of each text file. usage: make_index.py <receipts dir>"""
import hashlib
import sys
from pathlib import Path

root = Path(sys.argv[1])
rows = []
for path in sorted(p for p in root.rglob("*") if p.is_file() and p.name != "INDEX.md"):
    data = path.read_bytes()
    first = ""
    try:
        first = data.decode().strip().splitlines()[0][:90] if data.strip() else "(empty)"
    except UnicodeDecodeError:
        first = "(binary)"
    first = first.replace("|", "/")
    rows.append(f"| `{path.relative_to(root)}` | {len(data)} | `{hashlib.sha256(data).hexdigest()[:16]}` | {first} |")
out = ["# Receipts index", "", "Generated from the files present by `scripts/make_index.py`.", "",
       f"{len(rows)} files.", "", "| File | Bytes | sha256 (16) | First line |", "|---|---:|---|---|", *rows, ""]
(root / "INDEX.md").write_text("\n".join(out))
print(f"{len(rows)} files indexed")
