#!/usr/bin/env python3
"""Verify every published_sha256 in an evidence MANIFEST.json and list
files on disk that the manifest does not name. Usage: verify_manifest.py DIR [PREFIX]"""
import hashlib, json, sys
from pathlib import Path
root = Path(sys.argv[1]); prefix = sys.argv[2] if len(sys.argv) > 2 else ""
m = json.loads((root / "MANIFEST.json").read_text())
named = {e["file"] for e in m}
ok = bad = missing = 0
for e in m:
    if not e["file"].startswith(prefix):
        continue
    p = root / e["file"]
    if not p.is_file():
        missing += 1; print("MISSING", e["file"]); continue
    h = hashlib.sha256(p.read_bytes()).hexdigest()
    if h == e["published_sha256"]: ok += 1
    else: bad += 1; print("MISMATCH", e["file"])
extra = [str(p.relative_to(root)) for p in root.rglob("*") if p.is_file()
         and str(p.relative_to(root)) != "MANIFEST.json"
         and str(p.relative_to(root)).startswith(prefix)
         and str(p.relative_to(root)) not in named]
for x in extra: print("UNLISTED", x)
print(f"prefix={prefix!r} ok={ok} mismatch={bad} missing={missing} unlisted={len(extra)}")
sys.exit(1 if bad or missing or extra else 0)
