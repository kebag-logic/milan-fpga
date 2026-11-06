#!/usr/bin/env python3
"""Check the published round 8 evidence against its MANIFEST.json published_sha256 entries."""
import hashlib, json, pathlib, sys
root = pathlib.Path(sys.argv[1])
entries = json.load(open(root / "MANIFEST.json"))
print("manifest entries", len(entries), "keys", sorted(entries[0]))
listed, good, bad, missing = set(), 0, [], []
for entry in entries:
    name = entry["file"]
    if not name.startswith("author-r8/"):
        continue
    listed.add(name)
    path = root / name
    if not path.exists():
        missing.append(name)
    elif hashlib.sha256(path.read_bytes()).hexdigest() == entry["published_sha256"]:
        good += 1
    else:
        bad.append(name)
disk = {str(p.relative_to(root)) for p in (root / "author-r8").rglob("*") if p.is_file()}
print(f"author-r8 listed {len(listed)} ok {good} bad {len(bad)} missing {len(missing)} unlisted {len(disk - listed)}")
print("bad sample", bad[:5], "unlisted sample", sorted(disk - listed)[:5])
