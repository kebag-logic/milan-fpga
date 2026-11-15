"""index.py <round-dir>: INDEX.md listing every file present under <round-dir> (but INDEX.md): path, bytes, sha256
prefix, and its first non-empty line as a description; refuses a file over 200 KB."""
import hashlib, sys
from pathlib import Path
root = Path(sys.argv[1]); rows = []; big = []
for f in sorted(p for p in root.rglob("*") if p.is_file() and p.name != "INDEX.md"):
    data = f.read_bytes(); rel = f.relative_to(root)
    if len(data) > 200 * 1024:
        big.append(str(rel))
    try:
        first = next((ln.strip() for ln in data.decode().splitlines() if ln.strip()), "")
    except UnicodeDecodeError:
        first = "(binary)"
    first = first.replace("|", "/")[:110]
    rows.append(f"| `{rel}` | {len(data)} | `{hashlib.sha256(data).hexdigest()[:16]}` | {first} |")
out = ["# INDEX (generated from the files present, after sanitizing)", "",
       f"{len(rows)} files.", "", "| File | Bytes | sha256 (16) | First line |", "|---|---:|---|---|", *rows, ""]
(root / "INDEX.md").write_text("\n".join(out))
print(f"{len(rows)} files indexed; over 200 KB: {big or 'none'}")
sys.exit(1 if big else 0)
