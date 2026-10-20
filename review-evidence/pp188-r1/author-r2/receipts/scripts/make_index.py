#!/usr/bin/env python3
"""Generate <out>/receipts/INDEX.md from the files present under <out>.
usage: make_index.py <output dir>"""
import hashlib
import sys
from pathlib import Path

out = Path(sys.argv[1])
rows = []
for p in sorted(out.rglob("*")):
    if not p.is_file() or p.name == "INDEX.md" and p.parent.name == "receipts":
        continue
    data = p.read_bytes()
    first = ""
    try:
        for line in data.decode("utf-8").splitlines():
            if line.strip():
                first = line.strip().lstrip("#").strip()[:90].replace("|", "\\|")
                break
    except UnicodeDecodeError:
        first = "(binary)"
    rows.append((str(p.relative_to(out)), len(data), hashlib.sha256(data).hexdigest()[:16], first))
lines = ["# Receipt index (generated from the files present)", "",
         f"{len(rows)} files.", "",
         "| File | Bytes | sha256 (first 16) | First line |", "|---|---:|---|---|"]
lines += [f"| `{r}` | {n} | {h} | {f} |" for r, n, h, f in rows]
(out / "receipts").mkdir(exist_ok=True)
(out / "receipts" / "INDEX.md").write_text("\n".join(lines) + "\n")
print(f"indexed {len(rows)} files")
