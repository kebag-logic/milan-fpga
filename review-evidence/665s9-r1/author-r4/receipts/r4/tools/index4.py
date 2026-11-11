#!/usr/bin/env python3
"""index4.py <receipts/r4 dir>: INDEX.md generated from the files present: each file, its size, and its first line."""
import sys
from pathlib import Path
root = Path(sys.argv[1])
rows = ["# Round 4 receipts index", "", "Generated from the files present (tools/index4.py); each receipt's first line "
        "names its head or tree where it has one.", "", "| File | Bytes | First line |", "|---|---|---|"]
for p in sorted(x for x in root.rglob("*") if x.is_file() and x.name != "INDEX.md"):
    lines = p.read_text(errors="replace").splitlines() if p.stat().st_size else [""]
    first = (lines[0] if lines else "")[:110].replace("|", "/")
    rows.append(f"| `{p.relative_to(root)}` | {p.stat().st_size} | {first} |")
(root / "INDEX.md").write_text("\n".join(rows) + "\n")
print(len(rows) - 6, "files indexed")
