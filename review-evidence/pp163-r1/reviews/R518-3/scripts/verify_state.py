#!/usr/bin/env python3
"""Verify a checkout is byte-exact at a commit: HEAD, tree, index, every tracked blob and mode, status.

Usage: verify_state.py REPO HEAD TREE OUT.json
Hashes every tracked file's raw bytes as a git blob and compares it with the HEAD tree entry,
checks the executable bit against the mode, lists gitlinks (submodules) with their recorded
commits, and requires an empty `git status --porcelain --ignored=no`. Exit 0 only if all hold.
"""
import hashlib
import json
import os
import subprocess
import sys

repo, head, tree, out = sys.argv[1:5]


def git(*args):
    return subprocess.run(["git", "-C", repo, *args], capture_output=True, check=True).stdout


entries = git("ls-tree", "-r", "-z", "--full-tree", "HEAD").split(b"\0")
bad, gitlinks, count = [], [], 0
for e in filter(None, entries):
    meta, path = e.split(b"\t", 1)
    mode, kind, sha = meta.decode().split()
    p = os.path.join(repo, path.decode())
    if kind == "commit":
        gitlinks.append({"path": path.decode(), "commit": sha})
        continue
    count += 1
    if mode == "120000":
        data = os.readlink(p).encode()
    else:
        with open(p, "rb") as fh:
            data = fh.read()
        if (mode == "100755") != bool(os.stat(p).st_mode & 0o100):
            bad.append({"path": path.decode(), "issue": "mode"})
    blob = hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()
    if blob != sha:
        bad.append({"path": path.decode(), "issue": "bytes"})
result = {
    "head": git("rev-parse", "HEAD").decode().strip(),
    "head_tree": git("rev-parse", "HEAD^{tree}").decode().strip(),
    "index_tree": git("write-tree").decode().strip(),
    "tracked_entries": count,
    "mismatches": bad,
    "gitlinks": gitlinks,
    "status_porcelain": git("status", "--porcelain").decode(),
}
result["ok"] = (result["head"] == head and result["head_tree"] == tree and result["index_tree"] == tree
                and not bad and result["status_porcelain"] == "")
with open(out, "w") as fh:
    json.dump(result, fh, indent=1)
print(json.dumps(result, indent=1))
sys.exit(0 if result["ok"] else 1)
