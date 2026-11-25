#!/usr/bin/env python3
"""usage: evidence_manifest_check.py DIR  -- DIR is review-evidence/cicd3-r1 extracted from commit 726d9d25.
Recomputes every listed file's sha256 against MANIFEST.json's published_sha256 and lists unlisted files."""
import hashlib, json, os, sys, collections
root = sys.argv[1]
m = json.load(open(os.path.join(root, "MANIFEST.json")))
bad, missing, per = [], [], collections.Counter()
for e in m:
    p = os.path.join(root, e["file"])
    if not os.path.exists(p):
        missing.append(e["file"]); continue
    if hashlib.sha256(open(p, "rb").read()).hexdigest() != e["published_sha256"]:
        bad.append(e["file"])
    per[e["file"].split("/")[0]] += 1
have = {os.path.relpath(os.path.join(r, f), root) for r, _, fs in os.walk(root) for f in fs} - {"MANIFEST.json"}
print(f"entries {len(m)}; digest mismatches {bad}; missing {missing}; unlisted {sorted(have - {e['file'] for e in m})}")
print("per directory:", dict(sorted(per.items())))
