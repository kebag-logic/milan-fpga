#!/usr/bin/env python3
"""Verify downloaded published evidence against its MANIFEST.json.

Usage: verify_evidence.py <evidence-dir> <prefix>

<evidence-dir> holds MANIFEST.json and the downloaded files; <prefix> limits
the check to manifest entries under that subdirectory (e.g. author-r2).
Every listed file must exist with its published_sha256, no file under the
prefix may be unlisted, and redactions are reported.
"""
import hashlib
import json
import os
import sys

root, prefix = sys.argv[1], sys.argv[2]
manifest = json.load(open(os.path.join(root, "MANIFEST.json")))
listed, ok, bad, redacted = set(), 0, [], []
for e in manifest:
    p = e["file"]
    if not p.startswith(prefix + "/"):
        continue
    listed.add(p)
    data = open(os.path.join(root, p), "rb").read()
    if hashlib.sha256(data).hexdigest() == e["published_sha256"]:
        ok += 1
    else:
        bad.append(p)
    if e["original_sha256"] != e["published_sha256"] or e.get("path_redacted"):
        redacted.append(p)
present = {os.path.relpath(os.path.join(d, f), root)
           for d, _, fs in os.walk(os.path.join(root, prefix)) for f in fs}
print(f"manifest entries under {prefix}: {len(listed)}")
print(f"hash ok: {ok}  mismatched: {len(bad)}  redacted: {len(redacted)}")
print(f"unlisted files: {sorted(present - listed)}")
for p in bad:
    print("MISMATCH", p)
sys.exit(1 if bad or present - listed else 0)
