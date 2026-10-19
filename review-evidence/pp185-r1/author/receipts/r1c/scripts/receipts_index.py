"""Write receipts/INDEX.md from the files present under receipts/: every file with its
size and sha256, grouped by directory. Files over 200 KB are not copied in; they are
listed from OVER-200KB.sha256 (sha256, size, path) and marked as such."""
import hashlib
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
rows = {}
for p in sorted(root.rglob("*")):
    if not p.is_file() or p.name == "INDEX.md":
        continue
    rel = p.relative_to(root)
    digest = hashlib.sha256(p.read_bytes()).hexdigest()
    rows.setdefault(str(rel.parent), []).append((rel.name, p.stat().st_size, digest))

over = []
listing = root / "OVER-200KB.sha256"
if listing.exists():
    for line in listing.read_text().splitlines():
        if line.strip():
            digest, size, path = line.split(None, 2)
            over.append((path, int(size), digest))

out = ["# Receipts index", "",
       "Generated from the files present under `receipts/` (size in bytes, sha256).",
       f"{sum(len(v) for v in rows.values())} files.", ""]
for d in sorted(rows):
    out += [f"## {d}/" if d != "." else "## ./", "", "| File | Bytes | sha256 |", "|---|---|---|"]
    out += [f"| `{n}` | {s} | `{h}` |" for n, s, h in rows[d]]
    out.append("")
if over:
    out += ["## Over 200 KB (not copied; recorded in OVER-200KB.sha256)", "",
            "| File | Bytes | sha256 |", "|---|---|---|"]
    out += [f"| `{p}` | {s} | `{h}` |" for p, s, h in over]
    out.append("")
(root / "INDEX.md").write_text("\n".join(out))
print(f"INDEX.md: {sum(len(v) for v in rows.values())} files, {len(over)} over 200 KB")
