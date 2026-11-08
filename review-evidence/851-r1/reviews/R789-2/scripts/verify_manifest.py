#!/usr/bin/env python3
"""Check every author-r2 entry of an evidence MANIFEST.json against the extracted files."""
import hashlib, json, os, sys
root = sys.argv[1]; prefix = sys.argv[2] if len(sys.argv) > 2 else "author-r2/"
m = json.load(open(os.path.join(root, "MANIFEST.json")))
listed = {e["file"]: e for e in m if e["file"].startswith(prefix)}
bad = missing = 0
for f, e in sorted(listed.items()):
    p = os.path.join(root, f)
    if not os.path.isfile(p):
        missing += 1; print("MISSING", f); continue
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
    if h != e["published_sha256"]:
        bad += 1; print("MISMATCH", f)
on_disk = set()
for d, _, fs in os.walk(os.path.join(root, prefix)):
    for x in fs:
        on_disk.add(os.path.relpath(os.path.join(d, x), root))
unlisted = sorted(on_disk - set(listed))
for u in unlisted: print("UNLISTED", u)
red = sum(1 for e in listed.values() if e.get("path_redacted"))
print(f"entries={len(listed)} on_disk={len(on_disk)} mismatch={bad} missing={missing} unlisted={len(unlisted)} redacted={red}")
sys.exit(1 if bad or missing else 0)
