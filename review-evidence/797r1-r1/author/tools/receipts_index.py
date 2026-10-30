#!/usr/bin/env python3
"""Write receipts/INDEX.md from the files present under receipts/: path, bytes, sha256, first line."""
import hashlib
import sys
from pathlib import Path

root = Path(sys.argv[1])
rows = ["# Receipts index", "", "Generated from the files present; regenerate after adding a receipt.", "",
        "| File | Bytes | sha256 | First line |", "|---|---|---|---|"]
for path in sorted(p for p in root.rglob("*") if p.is_file() and p.name != "INDEX.md"):
    data = path.read_bytes()
    first = data.split(b"\n", 1)[0].decode("utf-8", "replace").replace("|", "\\|")[:90]
    rows.append(f"| `{path.relative_to(root).as_posix()}` | {len(data)} | `{hashlib.sha256(data).hexdigest()[:16]}` | {first} |")
(root / "INDEX.md").write_text("\n".join(rows) + "\n")
print(f"indexed {len(rows) - 6} receipts")
