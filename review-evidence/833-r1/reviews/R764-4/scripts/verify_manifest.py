#!/usr/bin/env python3
"""Check every published_sha256 in an evidence MANIFEST.json against the files beside it."""
import hashlib, json, sys
from pathlib import Path
root = Path(sys.argv[1]); prefix = sys.argv[2] if len(sys.argv) > 2 else ""
entries = json.loads((root / "MANIFEST.json").read_text())
bad = missing = ok = 0
for e in entries:
    if not e["file"].startswith(prefix):
        continue
    p = root / e["file"]
    if not p.is_file():
        missing += 1; print("MISSING", e["file"]); continue
    if hashlib.sha256(p.read_bytes()).hexdigest() != e["published_sha256"]:
        bad += 1; print("BAD", e["file"])
    else:
        ok += 1
listed = {e["file"] for e in entries}
extra = [str(p.relative_to(root)) for p in root.rglob("*") if p.is_file() and p.name != "MANIFEST.json"
         and str(p.relative_to(root)).startswith(prefix) and str(p.relative_to(root)) not in listed]
print(f"prefix={prefix!r} ok={ok} bad={bad} missing={missing} unlisted={len(extra)}")
for x in extra[:10]: print("UNLISTED", x)
sys.exit(1 if bad or missing else 0)
