"""Check the published author-r6 receipts against the evidence manifest.

Usage: python3 -I check_author_r6_receipts.py <MANIFEST.json> <dir holding author-r6/>

<MANIFEST.json> is review-evidence/640-m10-r1/MANIFEST.json at evidence commit
b669415749ee1f9e73d23443f714b6ac000e6596; <dir> holds the downloaded
author-r6/ tree. Reports (a) downloaded files whose bytes match the manifest's
published_sha256, and (b) the author's own SHA256SUMS lines whose hash differs
from the manifest's original_sha256.
"""
import hashlib
import json
import os
import sys

manifest_path, root = sys.argv[1], sys.argv[2]
entries = {e["file"]: e for e in json.load(open(manifest_path, encoding="utf-8"))}
r6 = {k: v for k, v in entries.items() if k.startswith("author-r6/")}

ok = bad = absent = 0
for key, ent in sorted(r6.items()):
    path = os.path.join(root, key)
    if not os.path.exists(path):
        absent += 1
        continue
    digest = hashlib.sha256(open(path, "rb").read()).hexdigest()
    if digest == ent["published_sha256"]:
        ok += 1
    else:
        bad += 1
        print("PUBLISHED MISMATCH", key)
print(f"(a) manifest entries {len(r6)}: published bytes match {ok}, mismatch {bad}, not downloaded {absent}")

agree = 0
for line in open(os.path.join(root, "author-r6/evidence/SHA256SUMS"), encoding="utf-8"):
    digest, rel = line.split(None, 1)
    key = "author-r6/" + rel.strip().lstrip("./")
    ent = entries.get(key)
    if ent is None:
        print("(b) NOT IN MANIFEST", key)
    elif ent["original_sha256"] != digest:
        print(f"(b) ORIGINAL DIFFERS {key}: author {digest[:16]} manifest {ent['original_sha256'][:16]}")
    else:
        agree += 1
print(f"(b) author SHA256SUMS lines agreeing with manifest original_sha256: {agree}")
