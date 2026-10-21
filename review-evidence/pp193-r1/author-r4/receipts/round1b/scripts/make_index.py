#!/usr/bin/env python3
"""Write INDEX.md of an output directory from the files present: path, bytes, sha256."""
import hashlib, sys
from pathlib import Path

root = Path(sys.argv[1])
index = root / "receipts" / "INDEX.md"
rows = []
for p in sorted(root.rglob("*")):
    if p.is_file() and p != index:
        rows.append((p.relative_to(root).as_posix(), p.stat().st_size,
                     hashlib.sha256(p.read_bytes()).hexdigest()))
lines = ["# Index of the output directory", "",
         "Generated from the files present (path, bytes, sha256). This file is not listed.", "",
         "| File | Bytes | sha256 |", "|---|---:|---|"]
lines += [f"| `{r}` | {n} | `{h}` |" for r, n, h in rows]
index.write_text("\n".join(lines) + "\n")
print(f"{len(rows)} files indexed")
