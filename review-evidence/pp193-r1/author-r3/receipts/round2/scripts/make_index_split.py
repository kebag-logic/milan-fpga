#!/usr/bin/env python3
"""Write the output directory's indexes from the files present (path, bytes,
sha256): one INDEX.md per receipts/<round>/ directory, and receipts/INDEX.md for
the files outside them plus each round's INDEX.md. Each index lists files
relative to the output directory; an index does not list itself.

usage: make_index_split.py <output dir>
"""
import hashlib
import sys
from pathlib import Path

root = Path(sys.argv[1])
rec = root / "receipts"
rounds = sorted(p for p in rec.iterdir() if p.is_dir())


def rows(files):
    return [(p.relative_to(root).as_posix(), p.stat().st_size,
             hashlib.sha256(p.read_bytes()).hexdigest()) for p in files]


def write(index, title, entries):
    lines = [f"# {title}", "",
             "Generated from the files present (path relative to the output directory, bytes,"
             " sha256). This file is not listed.", "",
             "| File | Bytes | sha256 |", "|---|---:|---|"]
    lines += [f"| `{r}` | {n} | `{h}` |" for r, n, h in entries]
    index.write_text("\n".join(lines) + "\n")
    return len(entries)


for d in rounds:
    idx = d / "INDEX.md"
    files = sorted(p for p in d.rglob("*") if p.is_file() and p != idx)
    print(d.name, write(idx, f"Index of receipts/{d.name}", rows(files)), "files")
top = rec / "INDEX.md"
outside = sorted(p for p in root.rglob("*") if p.is_file() and p != top
                 and not any(p.is_relative_to(d) for d in rounds))
outside += [d / "INDEX.md" for d in rounds]
print("top", write(top, "Index of the output directory (round indexes below)", rows(outside)), "files")
