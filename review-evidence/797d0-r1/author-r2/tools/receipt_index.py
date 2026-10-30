"""Write receipts/INDEX.md: every file under the output directory with its size and sha256.

Usage: python3 -I tools/receipt_index.py <output dir>
"""
import hashlib
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
index = root / "receipts" / "INDEX.md"
rows = []
for path in sorted(p for p in root.rglob("*") if p.is_file() and p != index):
    rel = path.relative_to(root).as_posix()
    rows.append(f"| `{rel}` | {path.stat().st_size} | `{hashlib.sha256(path.read_bytes()).hexdigest()}` |")
text = ["# Receipt index", "",
        "Generated from the files present by `python3 -I tools/receipt_index.py <output dir>`.",
        "Host paths inside logs are normalised: `<lane>` is the lane checkout, `<scratch>` the lane's scratch",
        "directory, `<out>` this directory and `~` the home directory. Logs over 200 KB are replaced by a",
        "`.sha256.txt` record (sha256, size, first and last lines) and kept outside this directory.", "",
        f"{len(rows)} files.", "", "| File | Bytes | sha256 |", "|---|---:|---|"] + rows
index.write_text("\n".join(text) + "\n")
print(f"{index.relative_to(root)}: {len(rows)} files")
