#!/usr/bin/env python3
"""Verify the published evidence tree against its publication MANIFEST.json and
the author's round2 MANIFEST.sha256 (original digests).
usage: verify_publication.py <extracted review-evidence/771-r1 dir>"""
import hashlib, json, os, sys
root = sys.argv[1]
man = json.load(open(os.path.join(root, "MANIFEST.json")))
by = {e["file"]: e for e in man}
bad = 0; n = 0; red = 0
for e in man:
    p = os.path.join(root, e["file"])
    if not os.path.exists(p):
        print("MISSING", e["file"]); bad += 1; continue
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
    n += 1
    if h != e["published_sha256"]:
        print("PUBLISHED-MISMATCH", e["file"]); bad += 1
    if not e.get("path_redacted") and e["original_sha256"] != e["published_sha256"]:
        print("UNREDACTED-BUT-DIFFERENT", e["file"]); bad += 1
    red += bool(e.get("path_redacted"))
# cross-check author round2 manifest originals
r2 = os.path.join(root, "author-r2/round2/MANIFEST.sha256")
orig = {}
for line in open(r2):
    d, f = line.rstrip("\n").split(None, 1)
    orig["author-r2/round2/" + f.lstrip("*")] = d
xbad = 0; xn = 0
for f, d in orig.items():
    e = by.get(f)
    if e is None:
        print("NOT-IN-PUBLICATION", f); continue
    xn += 1
    if e["original_sha256"] != d:
        print("ORIGINAL-MISMATCH", f); xbad += 1
print(f"published entries checked {n}, redacted {red}, failures {bad}; round2 originals cross-checked {xn}, mismatches {xbad}")
sys.exit(1 if bad or xbad else 0)
