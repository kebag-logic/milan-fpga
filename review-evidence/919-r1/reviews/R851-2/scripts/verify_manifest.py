#!/usr/bin/env python3
"""Check every author-r3/author-r4 file of the evidence archive against its MANIFEST.json published_sha256,
and list redacted entries (original != published)."""
import hashlib, json, sys
from pathlib import Path
man, base = Path(sys.argv[1]), Path(sys.argv[2])
rows = [r for r in json.loads(man.read_text()) if r["file"].startswith(("author-r3/", "author-r4/"))]
bad = []; red = []
for r in rows:
    p = base / r["file"]
    if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest() != r["published_sha256"]:
        bad.append(r["file"])
    if r["path_redacted"] or r["original_sha256"] != r["published_sha256"]:
        red.append(r["file"])
files = {str(p.relative_to(base)) for d in ("author-r3", "author-r4") for p in (base / d).rglob("*") if p.is_file()}
print(f"manifest rows r3+r4 {len(rows)}, published-hash mismatches {len(bad)} {bad[:5]}")
print(f"files on disk not in manifest {sorted(files - {r['file'] for r in rows})[:5]}")
print(f"redacted entries {len(red)}: {red}")
