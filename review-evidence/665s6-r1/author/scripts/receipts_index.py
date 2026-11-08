#!/usr/bin/env python3
"""receipts_index.py <receipts-dir> - write INDEX.md from the files present: path, size, sha256, first line."""
import hashlib
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
rows = []
for p in sorted(root.rglob("*")):
    if not p.is_file() or p.name == "INDEX.md":
        continue
    data = p.read_bytes()
    first = data.split(b"\n", 1)[0][:100].decode("utf-8", "replace").replace("|", "/")
    rows.append(f"| `{p.relative_to(root)}` | {len(data)} | `{hashlib.sha256(data).hexdigest()[:16]}` | {first} |")
(root / "INDEX.md").write_text("# Receipts index (generated from the files present)\n\n"
                               "| File | Bytes | sha256 (16) | First line |\n|---|---:|---|---|\n" + "\n".join(rows) + "\n")
print(f"{len(rows)} receipt(s) indexed")
