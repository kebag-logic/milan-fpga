#!/usr/bin/env python3
"""Check every row of a packet INDEX.md (| [name](path) | bytes | `sha256` |) against the files beside it,
and list files present but not indexed. Usage: verify_index.py <packet-dir>"""
import hashlib, re, sys
from pathlib import Path
root = Path(sys.argv[1])
rows = re.findall(r"^\| \[[^\]]+\]\(([^)]+)\) \| (\d+) \| `([0-9a-f]{64})` \|", (root / "INDEX.md").read_text(), re.M)
bad = 0
for rel, n, h in rows:
    p = root / rel
    if not p.is_file():
        print("MISSING", rel); bad += 1; continue
    b = p.read_bytes()
    if len(b) != int(n) or hashlib.sha256(b).hexdigest() != h:
        print("MISMATCH", rel, len(b), n); bad += 1
indexed = {r[0] for r in rows}
extra = sorted(str(p.relative_to(root)) for p in root.rglob("*") if p.is_file() and str(p.relative_to(root)) not in indexed and p.name != "INDEX.md")
print(f"rows={len(rows)} bad={bad} unindexed={len(extra)}")
for e in extra: print("UNINDEXED", e)
sys.exit(1 if bad else 0)
