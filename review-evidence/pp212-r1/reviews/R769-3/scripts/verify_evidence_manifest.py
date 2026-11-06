#!/usr/bin/env python3
"""Check published files under the given prefixes against the evidence MANIFEST.json.
usage: verify_evidence_manifest.py <pp212-r1 dir> <prefix>..."""
import hashlib, json, os, sys
root, prefixes = sys.argv[1], sys.argv[2:]
man = json.load(open(os.path.join(root, "MANIFEST.json")))
listed = {e["file"]: e for e in man if any(e["file"].startswith(p) for p in prefixes)}
bad = missing = 0
for f, e in sorted(listed.items()):
    p = os.path.join(root, f)
    if not os.path.isfile(p):
        missing += 1; print("MISSING", f); continue
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
    if h != e["published_sha256"]:
        bad += 1; print("MISMATCH", f)
on_disk = set()
for p in prefixes:
    for dp, _, fs in os.walk(os.path.join(root, p)):
        for n in fs:
            on_disk.add(os.path.relpath(os.path.join(dp, n), root))
extra = sorted(on_disk - set(listed))
for f in extra: print("UNLISTED", f)
redacted = sum(1 for e in listed.values() if e.get("path_redacted") or e["original_sha256"] != e["published_sha256"])
print(f"listed {len(listed)}, on disk {len(on_disk)}, mismatched {bad}, missing {missing}, unlisted {len(extra)}, redacted-or-rewritten {redacted}")
sys.exit(1 if bad or missing or extra else 0)
