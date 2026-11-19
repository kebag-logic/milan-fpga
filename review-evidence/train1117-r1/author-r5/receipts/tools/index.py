"""index.py <round-dir>: INDEX.md listing every file present under <round-dir> (but INDEX.md): path, bytes and a
sha256 prefix; refuses a file over 200 KB, INDEX.md itself included (the first-line column dropped at 2,400 files
to keep it within)."""
import hashlib, sys
from pathlib import Path
root = Path(sys.argv[1]); rows = []; big = []
for f in sorted(p for p in root.rglob("*") if p.is_file() and p.name != "INDEX.md"):
    data = f.read_bytes(); rel = f.relative_to(root)
    if len(data) > 200 * 1024:
        big.append(str(rel))
    rows.append(f"| `{rel}` | {len(data)} | `{hashlib.sha256(data).hexdigest()[:10]}` |")
out = ["# INDEX (generated from the files present, after sanitizing)", "",
       f"{len(rows)} files.", "", "| File | Bytes | sha256 (10) |", "|---|---:|---|", *rows, ""]
text = "\n".join(out)
(root / "INDEX.md").write_text(text)
if len(text.encode()) > 200 * 1024:
    big.append(f"INDEX.md ({len(text.encode())} B)")
print(f"{len(rows)} files indexed, INDEX.md {len(text.encode())} B; over 200 KB: {big or 'none'}")
sys.exit(1 if big else 0)
