#!/usr/bin/env python3
"""Check every row of an evidence packet's receipts/INDEX.md (path | bytes | sha256 prefix) against the files.

Usage: python3 -I verify_index.py <packet-dir containing receipts/INDEX.md>
Prints one line per row and a summary; exit 1 on any mismatch, missing file, or unlisted file.
"""
import hashlib
import pathlib
import re
import sys

root = pathlib.Path(sys.argv[1]) / "receipts"
rows = re.findall(r"^\| `([^`]+)` \| ([\d,]+) \| `([0-9a-f]{16})` \|", (root / "INDEX.md").read_text(), re.M)
bad = 0
listed = set()
for rel, size, pref in rows:
    listed.add(rel)
    p = root / rel
    if not p.is_file():
        print(f"MISSING {rel}")
        bad += 1
        continue
    data = p.read_bytes()
    ok = len(data) == int(size.replace(",", "")) and hashlib.sha256(data).hexdigest().startswith(pref)
    print(("OK " if ok else "MISMATCH ") + rel)
    bad += not ok
unlisted = sorted(str(f.relative_to(root)) for f in root.rglob("*") if f.is_file() and f.name != "INDEX.md"
                  and str(f.relative_to(root)) not in listed)
for u in unlisted:
    print(f"UNLISTED {u}")
print(f"rows={len(rows)} bad={bad} unlisted={len(unlisted)}")
sys.exit(1 if bad or unlisted else 0)
