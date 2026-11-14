#!/usr/bin/env python3
"""Verify the published evidence archive for PR #913 round 2 (#911).

usage: verify_evidence.py <extracted review-evidence/911-r1 directory>

Checks every MANIFEST.json entry's published sha256 and that no file is
unlisted, then every row of author-r2/receipts/INDEX.md (bytes and the
16-hex sha256 prefix). Prints counts; exit 0 when nothing mismatches.
"""
import hashlib
import json
import os
import sys
from pathlib import Path

root = Path(sys.argv[1])
manifest = json.loads((root / "MANIFEST.json").read_text())
bad, listed = [], set()
for entry in manifest:
    listed.add(entry["file"])
    path = root / entry["file"]
    if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != entry["published_sha256"]:
        bad.append(entry["file"])
present = {str(p.relative_to(root)) for p in root.rglob("*") if p.is_file()} - {"MANIFEST.json"}
print(f"MANIFEST.json: {len(manifest)} entries, {len(manifest) - len(bad)} match, "
      f"mismatched {bad or 'none'}, unlisted {sorted(present - listed) or 'none'}")
receipts = root / "author-r2/receipts"
rows = [ln.split("|")[1:4] for ln in (receipts / "INDEX.md").read_text().splitlines()
        if ln.startswith("| ") and not ln.startswith("| file")]
index_bad = []
for name, size, prefix in ((a.strip(), b.strip(), c.strip()) for a, b, c in rows):
    data = (receipts / name).read_bytes()
    if str(len(data)) != size or hashlib.sha256(data).hexdigest()[:16] != prefix:
        index_bad.append(name)
print(f"author-r2 INDEX.md: {len(rows)} rows, {len(rows) - len(index_bad)} match, "
      f"mismatched {index_bad or 'none'}")
sys.exit(1 if bad or index_bad or present - listed else 0)
