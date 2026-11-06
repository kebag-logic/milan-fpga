#!/usr/bin/env python3
"""Write receipts/INDEX.md from the files present: path, size and sha256 of each, one row per file."""
import hashlib, sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
rows = []
for p in sorted(root.rglob("*")):
    if p.is_file() and p.name != "INDEX.md":
        data = p.read_bytes()
        rows.append(f"| `{p.relative_to(root)}` | {len(data)} | `{hashlib.sha256(data).hexdigest()[:16]}` |")
text = ["# Receipts index", "", f"{len(rows)} files, generated from the files present.", "",
        "| File | Bytes | sha256 (first 16) |", "|---|---:|---|", *rows, ""]
(root / "INDEX.md").write_text("\n".join(text))
print(f"{len(rows)} files indexed")
