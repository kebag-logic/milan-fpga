#!/usr/bin/env python3
"""verify_evidence_manifest.py <evidence-dir> [prefix]: hash every file the published MANIFEST.json lists (optionally
only those under <prefix>) against its published_sha256, and list files present but not in the manifest."""
import hashlib, json, pathlib, sys
ev = pathlib.Path(sys.argv[1]); prefix = sys.argv[2] if len(sys.argv) > 2 else ""
m = json.loads((ev / "MANIFEST.json").read_text())
ok = bad = miss = 0; listed = set()
for e in m:
    p = e["file"]
    if not p.startswith(prefix): continue
    listed.add(p); f = ev / p
    if not f.exists(): miss += 1; print("MISSING", p); continue
    if hashlib.sha256(f.read_bytes()).hexdigest() == e["published_sha256"]: ok += 1
    else: bad += 1; print("MISMATCH", p)
extra = [str(f.relative_to(ev)) for f in (ev / prefix).rglob("*") if f.is_file() and str(f.relative_to(ev)) not in listed] if prefix else []
print(f"prefix={prefix!r} ok={ok} mismatch={bad} missing={miss} unlisted={len(extra)}")
for x in extra[:10]: print("UNLISTED", x)
sys.exit(1 if bad or miss else 0)
