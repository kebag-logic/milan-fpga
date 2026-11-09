#!/usr/bin/env python3
"""index.py <dir>: write INDEX.md in <dir> and in every directory below it, generated from the files present:
name, bytes and sha256 (16 hex), and the subdirectories."""
import hashlib, sys
from pathlib import Path
def index(d: Path) -> None:
    subs = sorted(p for p in d.iterdir() if p.is_dir())
    files = sorted(p for p in d.iterdir() if p.is_file() and p.name != "INDEX.md")
    lines = [f"# Index of `{d.name}`", "", "Generated from the files present (sha256 truncated to 16 hex).", ""]
    if subs:
        lines += ["Directories: " + ", ".join(f"[`{s.name}/`]({s.name}/INDEX.md)" for s in subs), ""]
    if files:
        lines += ["| File | Bytes | sha256 |", "|---|---|---|"]
        lines += [f"| `{f.name}` | {f.stat().st_size} | `{hashlib.sha256(f.read_bytes()).hexdigest()[:16]}` |" for f in files]
    (d / "INDEX.md").write_text("\n".join(lines) + "\n")
    for s in subs:
        index(s)
index(Path(sys.argv[1]))
