#!/usr/bin/env python3
"""Check the published evidence tree's MANIFEST.json against the files present.

Usage: python3 -I verify_manifest.py <evidence-root> <prefix>

Every MANIFEST entry whose path starts with <prefix> is hashed and compared with
its published_sha256; files under <prefix> that the manifest does not list are
reported too. Prints one line per mismatch and a summary; exit 1 on any mismatch.
"""
import hashlib
import json
import sys
from pathlib import Path

root, prefix = Path(sys.argv[1]), sys.argv[2]
entries = [e for e in json.loads((root / "MANIFEST.json").read_text()) if e["file"].startswith(prefix)]
bad = 0
listed = set()
for e in entries:
    listed.add(e["file"])
    p = root / e["file"]
    if not p.is_file():
        print(f"MISSING {e['file']}")
        bad += 1
        continue
    got = hashlib.sha256(p.read_bytes()).hexdigest()
    if got != e["published_sha256"]:
        print(f"MISMATCH {e['file']} {got} != {e['published_sha256']}")
        bad += 1
present = {str(p.relative_to(root)) for p in (root / prefix).rglob("*") if p.is_file()}
unlisted = sorted(present - listed)
for u in unlisted:
    print(f"UNLISTED {u}")
redacted = sum(1 for e in entries if e.get("path_redacted"))
print(f"{prefix}: {len(entries)} listed, {len(entries) - bad} match, {bad} bad, "
      f"{len(unlisted)} unlisted, {redacted} path-redacted")
sys.exit(1 if bad else 0)
