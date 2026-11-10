#!/usr/bin/env python3
"""index.py <receipts dir> - receipts/INDEX.md, generated from the files present: each file, its size, and its first line."""
import sys
from pathlib import Path
root = Path(sys.argv[1])
rows = ["# Receipts index", "", "Generated from the files present (tools/index.py); each receipt's first line names its head.", "",
        "| File | Bytes | First line |", "|---|---|---|"]
for p in sorted(x for x in root.rglob("*") if x.is_file() and x.name != "INDEX.md"):
    first = p.read_text(errors="replace").splitlines()[0][:110].replace("|", "/") if p.stat().st_size else ""
    rows.append(f"| `{p.relative_to(root)}` | {p.stat().st_size} | {first} |")
(root / "INDEX.md").write_text("\n".join(rows) + "\n")
print(len(rows) - 6, "files indexed")
