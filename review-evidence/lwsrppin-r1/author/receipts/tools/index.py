"""index.py RECEIPTS: append a file table (bytes, sha256 prefix) to INDEX.md's head text."""
import hashlib, sys
from pathlib import Path
r = Path(sys.argv[1]); head = (r / "INDEX.head.md").read_text()
rows = ["| File | Bytes | sha256 (16) |", "|---|---:|---|"]
for f in sorted(p for p in r.rglob("*") if p.is_file() and p.name not in ("INDEX.md", "INDEX.head.md")):
    rows.append(f"| `{f.relative_to(r)}` | {f.stat().st_size:,} | `{hashlib.sha256(f.read_bytes()).hexdigest()[:16]}` |")
(r / "INDEX.md").write_text(head + "\n## Files\n\n" + "\n".join(rows) + "\n")
