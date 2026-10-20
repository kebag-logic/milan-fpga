#!/usr/bin/env python3
"""Verify the published author receipts without opening review reports."""
import hashlib
import json
import pathlib
import subprocess
import sys
commit = "55c754698d494aaa17cf76f96229f9822c123c3a"
root = "review-evidence/761-r1/"
packet = pathlib.Path(sys.argv[1])
def blob(path):
    return subprocess.check_output(["git", "--no-replace-objects", "show", f"{commit}:{root}{path}"])
manifest = json.loads(blob("MANIFEST.json"))
count = 0
for entry in manifest:
    name = entry["file"]
    if not name.startswith("author-r4/receipts/"):
        continue
    data = blob(name)
    assert hashlib.sha256(data).hexdigest() == entry["published_sha256"], name
    count += 1
    relative = name.removeprefix("author-r4/receipts/")
    if relative.startswith("r4-"):
        dest = packet / "scratch" / "evidence" / relative
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
print(f"Evidence commit: {commit}")
print(f"Published author-r4 receipt hashes verified: {count}; mismatches: 0")
print("Hash equality establishes published-byte integrity, not a digital signature or execution provenance.")
