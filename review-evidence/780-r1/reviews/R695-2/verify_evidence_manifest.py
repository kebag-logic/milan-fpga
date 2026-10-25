#!/usr/bin/env python3
"""Verify a published evidence packet's MANIFEST.json against the blobs at a
commit in a bare repository.
Usage: verify_evidence_manifest.py BARE_REPO COMMIT PREFIX
Every manifest entry's published_sha256 must equal the sha256 of the blob at
COMMIT:PREFIX/<file>, and every blob under PREFIX (other than the manifest)
must be listed."""
import hashlib
import json
import subprocess
import sys

repo, commit, prefix = sys.argv[1:4]


def git(*a):
    return subprocess.run(["git", "-C", repo, *a], check=True,
                          capture_output=True).stdout


manifest = json.loads(git("show", f"{commit}:{prefix}/MANIFEST.json"))
listed = {e["file"]: e for e in manifest}
tree = git("ls-tree", "-r", "--name-only", commit, "--", prefix).decode().split("\n")
blobs = {p[len(prefix) + 1:] for p in tree if p and p != f"{prefix}/MANIFEST.json"}
bad = 0
for f, e in sorted(listed.items()):
    if f not in blobs:
        print(f"MISSING {f}")
        bad += 1
        continue
    got = hashlib.sha256(git("show", f"{commit}:{prefix}/{f}")).hexdigest()
    if got != e["published_sha256"]:
        print(f"MISMATCH {f}")
        bad += 1
unlisted = sorted(blobs - set(listed))
for f in unlisted:
    print(f"UNLISTED {f}")
redacted = sum(1 for e in manifest if e.get("path_redacted"))
print(f"entries={len(listed)} blobs={len(blobs)} mismatched_or_missing={bad} "
      f"unlisted={len(unlisted)} path_redacted={redacted}")
sys.exit(1 if bad or unlisted else 0)
