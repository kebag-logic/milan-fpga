#!/usr/bin/env python3
"""Check every row of a packet's receipts/INDEX.md (| `path` | bytes | `sha256` |) against the files under ROOT."""
import hashlib, os, re, sys
root = sys.argv[1]
rows = re.findall(r"^\| `([^`]+)` \| ([\d,]+) \| `([0-9a-f]{64})` \|$", open(os.path.join(root, "receipts/INDEX.md")).read(), re.M)
bad = 0
listed = set()
for path, size, digest in rows:
    listed.add(path)
    p = os.path.join(root, path)
    if not os.path.isfile(p):
        print("MISSING", path); bad += 1; continue
    data = open(p, "rb").read()
    if len(data) != int(size.replace(",", "")) or hashlib.sha256(data).hexdigest() != digest:
        print("MISMATCH", path); bad += 1
present = set()
for d, _, fs in os.walk(root):
    for f in fs:
        present.add(os.path.relpath(os.path.join(d, f), root))
unlisted = sorted(present - listed - {"receipts/INDEX.md"})
for u in unlisted:
    print("UNLISTED", u)
print(f"rows {len(rows)}, bad {bad}, unlisted {len(unlisted)}")
sys.exit(1 if bad else 0)
