"""index.py <round-dir>: INDEX.md listing every file present under <round-dir> (but INDEX.md), grouped by directory
(a heading per directory, then each file's name, bytes and sha256 prefix), so a path's directory is written once;
refuses a file over 200 KB, INDEX.md itself included."""
import hashlib, sys
from pathlib import Path
root = Path(sys.argv[1]); big = []; count = 0
out = ["# INDEX (generated from the files present, after sanitizing)", ""]
groups = {}
for f in sorted(p for p in root.rglob("*") if p.is_file() and p.name != "INDEX.md"):
    data = f.read_bytes(); rel = f.relative_to(root)
    if len(data) > 200 * 1024:
        big.append(str(rel))
    groups.setdefault(str(rel.parent), []).append(f"| `{rel.name}` | {len(data)} | `{hashlib.sha256(data).hexdigest()[:10]}` |")
    count += 1
out += [f"{count} files in {len(groups)} directories.", ""]
for d, rows in groups.items():
    out += [f"## `{d}/`" if d != "." else "## `./`", "", "| File | Bytes | sha256 (10) |", "|---|---:|---|", *rows, ""]
text = "\n".join(out)
(root / "INDEX.md").write_text(text)
if len(text.encode()) > 200 * 1024:
    big.append(f"INDEX.md ({len(text.encode())} B)")
print(f"{count} files indexed, INDEX.md {len(text.encode())} B; over 200 KB: {big or 'none'}")
sys.exit(1 if big else 0)
