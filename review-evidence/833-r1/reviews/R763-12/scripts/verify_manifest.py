#!/usr/bin/env python3
"""Check every MANIFEST.json entry under a prefix against the downloaded file bytes.

usage: verify_manifest.py <MANIFEST.json> <evidence root> <prefix>
"""
import hashlib, json, sys
from pathlib import Path
manifest, root, prefix = sys.argv[1:4]
entries = [e for e in json.load(open(manifest)) if e["file"].startswith(prefix)]
bad = redacted = 0
for e in entries:
    p = Path(root) / e["file"]
    h = hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else "ABSENT"
    if h != e["published_sha256"]:
        bad += 1; print("MISMATCH", e["file"])
    if e.get("path_redacted") or e["original_sha256"] != e["published_sha256"]:
        redacted += 1
on_disk = {str(p.relative_to(root)) for p in (Path(root) / prefix).rglob("*") if p.is_file()}
unlisted = sorted(on_disk - {e["file"] for e in entries})
print(f"{prefix}: {len(entries)} entries, {bad} mismatched, {redacted} redacted, unlisted on disk: {unlisted}")
sys.exit(1 if bad or unlisted else 0)
