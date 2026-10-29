#!/usr/bin/env python3
"""Write INDEX.md in <root> and in every directory under it, from the files present.

usage: index.py <root>
"""
import hashlib
import sys
from pathlib import Path


def main() -> int:
    root = Path(sys.argv[1])
    for d in sorted([root] + [p for p in root.rglob("*") if p.is_dir()]):
        files = sorted(p for p in d.rglob("*") if p.is_file() and p.name != "INDEX.md")
        rows = []
        for f in files:
            data = f.read_bytes()
            rows.append(f"| `{f.relative_to(d)}` | {len(data)} | `{hashlib.sha256(data).hexdigest()[:16]}` |")
        title = "." if d == root else str(d.relative_to(root))
        (d / "INDEX.md").write_text(
            f"# Index of `{title}`\n\nGenerated from the files present (sha256 truncated to 16 hex).\n\n"
            "| File | Bytes | sha256 |\n|---|---|---|\n" + "\n".join(rows) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
