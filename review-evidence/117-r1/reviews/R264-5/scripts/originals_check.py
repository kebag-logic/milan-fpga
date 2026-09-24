#!/usr/bin/env python3
"""Which files of an earlier archive commit are byte-identical to the as-recorded originals.

Usage: originals_check.py <bare-repo> <earlier-commit> <pin MANIFEST.json>
Compares each file's SHA-256 at the earlier commit with the pin's
MANIFEST.json original_sha256.
"""
import hashlib
import json
import subprocess
import sys

repo, old, man = sys.argv[1:]
eq = ne = miss = 0
diff = []
for e in json.load(open(man)):
    r = subprocess.run(["git", "-C", repo, "cat-file", "blob", f"{old}:review-evidence/117-r1/{e['file']}"], capture_output=True)
    if r.returncode:
        miss += 1
        continue
    if hashlib.sha256(r.stdout).hexdigest() == e["original_sha256"]:
        eq += 1
    else:
        ne += 1
        diff.append(e["file"])
print(f"files at {old[:8]} equal to MANIFEST.json original_sha256: {eq}; differ: {ne}; absent: {miss}")
for f in diff:
    print("  differs:", f)
