#!/usr/bin/env python3
"""Check every author-r4 entry of the evidence packet's MANIFEST.json against the published bytes.

usage: verify_manifest.py <git-dir-with-evidence-commit> <commit> [prefix]
Reads blobs with `git cat-file`; never executes packet content.
"""
import hashlib
import json
import subprocess
import sys

repo, commit = sys.argv[1], sys.argv[2]
prefix = sys.argv[3] if len(sys.argv) > 3 else "author-r4/"
root = "review-evidence/665s11-r1/"


def blob(path: str) -> bytes:
    return subprocess.run(["git", "-C", repo, "cat-file", "blob", f"{commit}:{root}{path}"],
                          check=True, capture_output=True).stdout


manifest = json.loads(blob("MANIFEST.json"))
listed = {e["file"]: e for e in manifest if e["file"].startswith(prefix)}
tree = subprocess.run(["git", "-C", repo, "ls-tree", "-r", "--name-only", commit, root + prefix],
                      check=True, capture_output=True, text=True).stdout.split()
present = {p[len(root):] for p in tree}
bad = 0
for f, e in sorted(listed.items()):
    if f not in present:
        print(f"MISSING {f}")
        bad += 1
        continue
    h = hashlib.sha256(blob(f)).hexdigest()
    if h != e["published_sha256"]:
        print(f"MISMATCH {f}")
        bad += 1
for f in sorted(present - set(listed)):
    print(f"UNLISTED {f}")
    bad += 1
print(f"entries {len(listed)} present {len(present)} bad {bad}")
sys.exit(1 if bad else 0)
