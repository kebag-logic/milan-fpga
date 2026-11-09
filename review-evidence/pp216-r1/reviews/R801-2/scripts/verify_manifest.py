#!/usr/bin/env python3
"""verify_manifest.py EVIDENCE_DIR: check every MANIFEST.json entry's published_sha256 against the
file in EVIDENCE_DIR, and list files present but not in the manifest."""
import hashlib, json, sys
from pathlib import Path
root = Path(sys.argv[1])
m = json.loads((root / "MANIFEST.json").read_text())
listed = set(); bad = []; missing = []
for e in m:
    p = root / e["file"]; listed.add(e["file"])
    if not p.is_file(): missing.append(e["file"]); continue
    if hashlib.sha256(p.read_bytes()).hexdigest() != e["published_sha256"]: bad.append(e["file"])
present = {str(p.relative_to(root)) for p in root.rglob("*") if p.is_file()} - {"MANIFEST.json"}
unlisted = sorted(present - listed)
pre = sys.argv[2] if len(sys.argv) > 2 else ""
sel = [f for f in listed if f.startswith(pre)]
print(f"entries {len(m)}; under '{pre}': {len(sel)}; mismatched {len(bad)}; missing {len(missing)}; unlisted {len(unlisted)}")
for x in bad[:20]: print("MISMATCH", x)
for x in missing[:20]: print("MISSING", x)
for x in unlisted[:20]: print("UNLISTED", x)
redacted = [e["file"] for e in m if e.get("path_redacted") or e["original_sha256"] != e["published_sha256"]]
print(f"redacted or rewritten entries: {len(redacted)}; under '{pre}': {sum(f.startswith(pre) for f in redacted)}")
sys.exit(1 if bad or missing else 0)
