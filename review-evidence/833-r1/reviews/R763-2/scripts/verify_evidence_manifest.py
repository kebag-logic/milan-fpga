#!/usr/bin/env python3
"""usage: verify_evidence_manifest.py <review-evidence/833-r1 dir>

Check every MANIFEST.json entry's published_sha256 against the file bytes and
report files present but not listed."""
import hashlib, json, os, sys
root = sys.argv[1]
entries = json.load(open(os.path.join(root, "MANIFEST.json")))
listed = {e["file"] for e in entries}
bad = [e["file"] for e in entries
       if not os.path.isfile(os.path.join(root, e["file"]))
       or hashlib.sha256(open(os.path.join(root, e["file"]), "rb").read()).hexdigest() != e["published_sha256"]]
present = {os.path.relpath(os.path.join(d, f), root) for d, _, fs in os.walk(root) for f in fs}
print(f"entries {len(entries)} mismatched {len(bad)} unlisted {len(present - listed - {'MANIFEST.json'})} "
      f"round-2 entries {sum(e['file'].startswith('author-r2/') for e in entries)}")
for f in bad:
    print("MISMATCH", f)
sys.exit(1 if bad else 0)
