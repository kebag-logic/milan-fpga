#!/usr/bin/env python3
"""Hash every published author-r3 file named by the evidence manifest; report mismatches and unlisted files.
usage: verify_manifest.py <evidence root>"""
import hashlib, json, sys
from pathlib import Path
root = Path(sys.argv[1])
rows = json.loads((root/"MANIFEST.json").read_text())
listed = {r["file"]: r for r in rows}
ok = bad = 0
for name, r in listed.items():
    if not name.startswith("author-r3/"): continue
    p = root/name
    if not p.is_file(): bad += 1; print("MISSING", name); continue
    h = hashlib.sha256(p.read_bytes()).hexdigest()
    if h == r["published_sha256"]: ok += 1
    else: bad += 1; print("MISMATCH", name)
extra = [str(p.relative_to(root)) for p in (root/"author-r3").rglob("*") if p.is_file() and str(p.relative_to(root)) not in listed]
red = sum(1 for n, r in listed.items() if n.startswith("author-r3/") and r.get("path_redacted"))
print(f"manifest rows {len(rows)}; author-r3 verified {ok}, bad {bad}, unlisted {len(extra)}, path-redacted {red}")
print("\n".join(extra[:10]))
