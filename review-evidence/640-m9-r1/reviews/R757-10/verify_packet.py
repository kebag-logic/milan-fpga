#!/usr/bin/env python3
"""Check the author-r9 packet: each published file against the publication manifest, and
the author's SHA256SUMS against the manifest's original digests (path redaction changes
published bytes, so a differing file must be flagged path_redacted and match the original)."""
import hashlib, json, pathlib, sys
root = pathlib.Path(sys.argv[1])
manifest = {e["file"]: e for e in json.load(open(root / "MANIFEST.json"))}
bad = checked = redacted = 0
for line in (root / "author-r9/evidence/SHA256SUMS").read_text().splitlines():
    digest, name = line.split(maxsplit=1)
    key = "author-r9/evidence/" + name.lstrip("./")
    entry = manifest.get(key)
    if entry is None:
        print("not in manifest:", key); bad += 1; continue
    published = hashlib.sha256((root / key).read_bytes()).hexdigest()
    checked += 1
    if published != entry["published_sha256"] or digest != entry["original_sha256"]:
        print("MISMATCH", key); bad += 1
    if entry["path_redacted"]:
        redacted += 1
    elif published != digest:
        print("differs without redaction flag", key); bad += 1
print(f"checked {checked}; path-redacted {redacted}; bad {bad}")
sys.exit(1 if bad else 0)
