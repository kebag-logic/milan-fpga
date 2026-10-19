#!/usr/bin/env python3
"""Check an evidence receipts INDEX.md (| `path` | bytes | sha256-16 |) against
the files present beside it. Usage: verify_index.py RECEIPTS_DIR"""
import hashlib, re, sys
from pathlib import Path
root = Path(sys.argv[1])
rows = {}
for line in (root / "INDEX.md").read_text().splitlines():
    m = re.match(r"\| `([^`]+)` \| (\d+) \| `([0-9a-f]{16})` \|", line)
    if m:
        rows[m.group(1)] = (int(m.group(2)), m.group(3))
present = {str(p.relative_to(root)) for p in root.rglob("*") if p.is_file()} - {"INDEX.md"}
bad = 0
for rel, (size, h) in sorted(rows.items()):
    p = root / rel
    if not p.is_file():
        print("MISSING", rel); bad += 1; continue
    b = p.read_bytes()
    if len(b) != size or hashlib.sha256(b).hexdigest()[:16] != h:
        print("MISMATCH", rel, len(b), size); bad += 1
for rel in sorted(present - set(rows)):
    print("UNLISTED", rel); bad += 1
declared = re.search(r"^(\d+) files\.", (root / "INDEX.md").read_text(), re.M)
print(f"rows={len(rows)} present={len(present)} declared={declared.group(1) if declared else None} bad={bad}")
sys.exit(1 if bad else 0)
