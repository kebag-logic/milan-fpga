#!/usr/bin/env python3
"""manifest_check.py ROOT: check every MANIFEST.json row's published_sha256
against the file under ROOT, and list files under ROOT the manifest omits."""
import hashlib, json, sys
from pathlib import Path
root = Path(sys.argv[1])
rows = json.load(open(root / "MANIFEST.json"))
bad = missing = 0
listed = set()
red = 0
for r in rows:
    f = root / r["file"]; listed.add(r["file"])
    red += bool(r.get("path_redacted"))
    if not f.is_file():
        print("ABSENT", r["file"]); missing += 1; continue
    h = hashlib.sha256(f.read_bytes()).hexdigest()
    if h != r["published_sha256"]:
        print("HASH", r["file"]); bad += 1
on_disk = {p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()}
extra = sorted(on_disk - listed - {"MANIFEST.json"})
for e in extra: print("UNLISTED", e)
print(f"{len(rows)} manifest rows, {missing} absent, {bad} hash mismatches, "
      f"{len(extra)} unlisted files, {red} path_redacted, {len(on_disk)} files on disk")
sys.exit(1 if (bad or missing) else 0)
