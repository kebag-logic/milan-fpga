#!/usr/bin/env python3
"""R222-3: verify the public evidence archive manifest at a given commit.

Hashes blobs only (no content interpretation) for every manifest entry, checks
every tracked file under the archive root is listed, and reports entries that
declare a content omission. Usage:
  06_evidence_manifest.py <bare-repo> <commit> <archive-root> <out>
"""
import hashlib
import json
import subprocess
import sys

repo, commit, root, out = sys.argv[1:5]


def git(*args: str) -> bytes:
    return subprocess.run(["git", "-C", repo, *args], check=True,
                          capture_output=True).stdout


manifest = json.loads(git("show", f"{commit}:{root}/MANIFEST.json"))
tracked = set(git("ls-tree", "-r", "--name-only", commit, f"{root}/")
              .decode().splitlines())
tracked.discard(f"{root}/MANIFEST.json")
lines = [f"commit {commit} root {root}",
         f"manifest entries: {len(manifest)}",
         f"tracked files (excluding MANIFEST.json): {len(tracked)}"]
bad = 0
listed = set()
omissions = []
for e in manifest:
    path = f"{root}/{e['file']}"
    listed.add(path)
    if path not in tracked:
        bad += 1
        lines.append(f"MISSING-IN-TREE {e['file']}")
        continue
    h = hashlib.sha256(git("show", f"{commit}:{path}")).hexdigest()
    if h != e["published_sha256"]:
        bad += 1
        lines.append(f"HASH-MISMATCH {e['file']}")
    if "content_omission" in e:
        omissions.append(f"{e['file']}: content_omission={e['content_omission']!r}")
unlisted = sorted(tracked - listed)
lines.append(f"unlisted tracked files: {len(unlisted)}")
lines += [f"  UNLISTED {u}" for u in unlisted]
lines.append(f"entries verified: {len(manifest)} mismatches/missing: {bad}")
lines.append(f"path_redacted entries: {sum(1 for e in manifest if e.get('path_redacted'))}")
lines.append(f"content_omission entries: {len(omissions)}")
lines += [f"  {o}" for o in omissions]
text = "\n".join(lines) + "\n"
open(out, "w").write(text)
print(text)
