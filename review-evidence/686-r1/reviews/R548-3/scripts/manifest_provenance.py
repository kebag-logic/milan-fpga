#!/usr/bin/env python3
"""Compare MANIFEST.json provenance between two archive heads and verify published hashes.
Usage: manifest_provenance.py <old.json> <new.json> <evidence-root>"""
import hashlib, json, sys
from pathlib import Path
old = {e["file"]: e for e in json.load(open(sys.argv[1]))}
new = {e["file"]: e for e in json.load(open(sys.argv[2]))}
root = Path(sys.argv[3])
changed = [f for f in old if f in new and old[f] != new[f]]
removed = [f for f in old if f not in new]
print("old entries", len(old), "new entries", len(new), "added", len(set(new) - set(old)))
print("changed entries:", changed)
print("removed entries:", removed)
bad = 0
for f, e in new.items():
    p = root / f
    if not p.is_file():
        print("MISSING", f); bad += 1; continue
    h = hashlib.sha256(p.read_bytes()).hexdigest()
    if h != e["published_sha256"]:
        print("PUBLISHED-HASH-MISMATCH", f); bad += 1
on_disk = {str(p.relative_to(root)) for p in root.rglob("*") if p.is_file()} - {"MANIFEST.json"}
print("files on disk not in MANIFEST.json:", sorted(on_disk - set(new))[:10], len(on_disk - set(new)))
print("published-hash failures:", bad)
sys.exit(1 if bad or removed else 0)
