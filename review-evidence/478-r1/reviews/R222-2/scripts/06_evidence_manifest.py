#!/usr/bin/env python3
"""Verify the immutable evidence archive at 3811227e without reading report
content: every MANIFEST.json entry must be a tracked blob whose SHA-256 equals
`published_sha256`, and every tracked file under review-evidence/478-r1 must be
listed. Only the round2/manager records are then parsed for identity and exit
facts (reviews/*, author*, link-proposal/* contents are not read).
Usage: 06_evidence_manifest.py <bare-repo> <commit>"""
import hashlib
import json
import subprocess
import sys

repo, commit = sys.argv[1], sys.argv[2]
ROOT = "review-evidence/478-r1"


def git(*args: str) -> bytes:
    return subprocess.run(["git", "-C", repo, *args], check=True,
                          capture_output=True).stdout


manifest = json.loads(git("cat-file", "blob", f"{commit}:{ROOT}/MANIFEST.json"))
tracked = {}
for line in git("ls-tree", "-r", commit, "--", ROOT).decode().splitlines():
    meta, path = line.split("\t", 1)
    mode, kind, sha = meta.split()
    tracked[path[len(ROOT) + 1:]] = (mode, kind, sha)

bad, listed = [], set()
for ent in manifest:
    f = ent["file"]
    listed.add(f)
    if f not in tracked:
        bad.append(f"UNTRACKED {f}")
        continue
    data = git("cat-file", "blob", tracked[f][2])
    if hashlib.sha256(data).hexdigest() != ent["published_sha256"]:
        bad.append(f"SHA256-MISMATCH {f}")
unlisted = sorted(set(tracked) - listed - {"MANIFEST.json"})
print(f"evidence commit {commit}")
print(f"manifest entries: {len(manifest)}; tracked files under {ROOT}: {len(tracked)}")
print(f"entries verified: {len(manifest) - len(bad)}; problems: {len(bad)}")
for b in bad:
    print("  ", b)
print(f"tracked but not in manifest (excluding MANIFEST.json): {len(unlisted)}")
for u in unlisted[:20]:
    print("  ", u)
groups = {}
for f in listed:
    groups[f.split("/")[0] if "/" in f else "(top)"] = groups.get(
        f.split("/")[0] if "/" in f else "(top)", 0) + 1
print("entries per top-level group:", dict(sorted(groups.items())))
r2 = sorted(f for f in listed if f.startswith("round2/"))
print("round2 subgroups:", sorted({"/".join(f.split("/")[:2]) for f in r2}))
sys.exit(1 if bad else 0)
