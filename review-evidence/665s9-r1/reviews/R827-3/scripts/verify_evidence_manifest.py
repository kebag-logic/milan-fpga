"""Verify a published review-evidence tree against its MANIFEST.json, from git objects.

Usage: python3 -I verify_evidence_manifest.py <repo> <commit> <evidence-dir-in-tree>
Every manifest entry's published file must exist at the commit with the listed
published_sha256, and every file in the tree except MANIFEST.json must be listed.
Prints the counts and every mismatch; exit 0 when there is none, 1 otherwise.
"""
import hashlib
import json
import subprocess
import sys

repo, commit, root = sys.argv[1], sys.argv[2], sys.argv[3].rstrip("/")


def git(*args: str, data: bytes | None = None) -> bytes:
    return subprocess.run(["git", "-C", repo, *args], input=data, capture_output=True, check=True).stdout


manifest = json.loads(git("show", f"{commit}:{root}/MANIFEST.json"))
listed = {e["file"]: e["published_sha256"] for e in manifest}
names = [n for n in git("ls-tree", "-r", "--name-only", commit, root).decode().splitlines()
         if n != f"{root}/MANIFEST.json"]
batch = git("cat-file", "--batch", data="".join(f"{commit}:{n}\n" for n in names).encode())
actual, pos = {}, 0
for name in names:
    header_end = batch.index(b"\n", pos)
    size = int(batch[pos:header_end].split()[2])
    body = batch[header_end + 1:header_end + 1 + size]
    pos = header_end + 1 + size + 1
    actual[name[len(root) + 1:]] = hashlib.sha256(body).hexdigest()
bad = [f"hash mismatch: {f}" for f in listed if f in actual and actual[f] != listed[f]]
bad += [f"listed, not published: {f}" for f in listed if f not in actual]
bad += [f"published, not listed: {f}" for f in actual if f not in listed]
redacted = sum(1 for e in manifest if e.get("path_redacted"))
print(f"manifest entries {len(listed)}, published files {len(actual)}, path-redacted {redacted}, "
      f"mismatches {len(bad)}")
for line in bad[:50]:
    print(line)
sys.exit(1 if bad else 0)
