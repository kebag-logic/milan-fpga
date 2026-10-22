#!/usr/bin/env python3
"""Write receipts/INDEX.md from the files present: path, size, sha256, and the
first line of each text file. With --collapse, a subdirectory that holds its own
INDEX.md is listed as that one index (with the count and bytes of the files it
covers) instead of file by file, so the top-level index stays small.
usage: make_index.py <receipts dir> [--collapse]"""
import hashlib
import sys
from pathlib import Path

root = Path(sys.argv[1])
collapse = "--collapse" in sys.argv[2:]
indexed = sorted(d for d in root.iterdir() if d.is_dir() and (d / "INDEX.md").is_file()) if collapse else []


def first_line(data: bytes) -> str:
    try:
        text = data.decode().strip()
    except UnicodeDecodeError:
        return "(binary)"
    return (text.splitlines()[0][:90] if text else "(empty)").replace("|", "/")


rows = []
for path in sorted(p for p in root.rglob("*") if p.is_file() and p.name != "INDEX.md"):
    if any(d in path.parents for d in indexed):
        continue
    data = path.read_bytes()
    rows.append(f"| `{path.relative_to(root)}` | {len(data)} | `{hashlib.sha256(data).hexdigest()[:16]}` | {first_line(data)} |")
subs = []
for d in indexed:
    files = [p for p in d.rglob("*") if p.is_file() and p.name != "INDEX.md"]
    idx = (d / "INDEX.md").read_bytes()
    subs.append(f"| `{d.name}/INDEX.md` | {len(files)} | {sum(p.stat().st_size for p in files)} | "
                f"`{hashlib.sha256(idx).hexdigest()[:16]}` |")
out = ["# Receipts index", "", "Generated from the files present by `scripts/make_index.py`.", ""]
if subs:
    out += ["Directories with their own index (each lists its files, sizes and hashes):", "",
            "| Index | Files | Bytes | sha256 (16) of the index |", "|---|---:|---:|---|", *subs, ""]
out += [f"{len(rows)} files listed here.", "", "| File | Bytes | sha256 (16) | First line |", "|---|---:|---|---|",
        *rows, ""]
(root / "INDEX.md").write_text("\n".join(out))
print(f"{len(rows)} files indexed, {len(subs)} sub-indices")
