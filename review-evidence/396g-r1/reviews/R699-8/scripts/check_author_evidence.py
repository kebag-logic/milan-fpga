#!/usr/bin/env python3
"""Check every author-r8 file of the public evidence tree against its MANIFEST.json digest.

usage: check_author_evidence.py <MANIFEST.json> <review-evidence/396g-r1 directory> <prefix>
Prints one line per mismatch or missing file, any file under <prefix> the manifest does not list,
and a summary; exit 0 only when every listed file matches and none is unlisted.
"""
import hashlib
import json
import pathlib
import sys

manifest, root, prefix = json.load(open(sys.argv[1])), pathlib.Path(sys.argv[2]), sys.argv[3]
entries = [e for e in manifest if e["file"].startswith(prefix)]
bad = 0
for e in entries:
    p = root / e["file"]
    digest = hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else "MISSING"
    if digest != e["published_sha256"]:
        bad += 1
        print("MISMATCH", e["file"], digest)
listed = {e["file"] for e in entries}
unlisted = sorted(str(p.relative_to(root)) for p in (root / prefix).rglob("*")
                  if p.is_file() and str(p.relative_to(root)) not in listed)
for u in unlisted:
    print("UNLISTED", u)
print(f"{prefix}: {len(entries)} listed, {len(entries) - bad} match, {bad} mismatch, {len(unlisted)} unlisted")
sys.exit(0 if not bad and not unlisted else 1)
