#!/usr/bin/env python3
"""Recompute an author receipts INDEX.md (truncated sha256 + bytes) and count workflow step rc files."""
import hashlib, re, sys
from pathlib import Path
root = Path(sys.argv[1])
rows = re.findall(r"^\| `([^`]+)` \| ([\d,]+) \| `([0-9a-f]{16})` \|", (root / "INDEX.md").read_text(), re.M)
bad = 0
for name, size, sha in rows:
    p = root / name
    if not p.is_file():
        print("MISSING", name); bad += 1; continue
    b = p.read_bytes()
    if len(b) != int(size.replace(",", "")) or hashlib.sha256(b).hexdigest()[:16] != sha:
        print("MISMATCH", name); bad += 1
listed = {r[0] for r in rows}
extra = [str(p.relative_to(root)) for p in root.rglob("*") if p.is_file() and p.name != "INDEX.md" and str(p.relative_to(root)) not in listed]
rcs = sorted(root.glob("workflows/logs/*.rc"))
nonzero = [p.name for p in rcs if p.read_text().strip() != "0"]
print(f"index rows {len(rows)}, bad {bad}, unlisted files {len(extra)} {extra[:5]}")
print(f"workflow rc files {len(rcs)}, nonzero {nonzero}")
heads = set()
for p in root.glob("workflows/logs/*.log"):
    m = re.match(r"# head ([0-9a-f]{40})", p.read_text(errors="replace"))
    if m: heads.add(m.group(1))
print("workflow log heads", heads)
