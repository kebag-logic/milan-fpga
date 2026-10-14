#!/usr/bin/env python3
"""Prove a checkout is byte-for-byte its head: every tracked blob, mode, index entry and gitlink.

Usage: verify_checkout.py <checkout> <expected-head> <expected-tree> <output-json>
Hashes the bytes on disk with `git hash-object` (so assume-unchanged or
skip-worktree flags cannot hide an edit) and compares them with HEAD's tree.
"""
import json
import os
import stat
import subprocess
import sys
from pathlib import Path


def git(root, *args, data=None):
    return subprocess.run(["git", "-C", str(root), *args], input=data, check=True,
                          capture_output=True, env={**os.environ, "GIT_NO_REPLACE_OBJECTS": "1"}).stdout


root, head, tree, out = Path(sys.argv[1]), sys.argv[2], sys.argv[3], Path(sys.argv[4])
problems = []
if git(root, "rev-parse", "HEAD").decode().strip() != head:
    problems.append("HEAD differs")
if git(root, "rev-parse", "HEAD^{tree}").decode().strip() != tree:
    problems.append("head tree differs")
if git(root, "write-tree").decode().strip() != tree:
    problems.append("index tree differs from head tree")
entries = []
for line in git(root, "ls-tree", "-r", "-z", "--full-tree", "HEAD").split(b"\0"):
    if not line:
        continue
    meta, path = line.split(b"\t", 1)
    mode, kind, oid = meta.decode().split()
    entries.append((mode, kind, oid, path.decode()))
files = [e for e in entries if e[1] == "blob"]
regular = [e for e in files if e[0] in ("100644", "100755")]
hashed = git(root, "hash-object", "--no-filters", "--stdin-paths",
             data="".join(e[3] + "\n" for e in regular).encode()).decode().split()
for (mode, _, oid, path), actual in zip(regular, hashed):
    full = root / path
    if full.is_symlink() or not full.is_file():
        problems.append(path + ": not a regular file")
    elif actual != oid:
        problems.append(path + ": bytes differ")
    elif bool(os.stat(full).st_mode & stat.S_IXUSR) != (mode == "100755"):
        problems.append(path + ": mode differs")
for mode, _, oid, path in files:
    if mode == "120000":
        if not (root / path).is_symlink() or git(root, "hash-object", "--stdin", data=os.readlink(root / path).encode()).decode().strip() != oid:
            problems.append(path + ": symlink differs")
gitlinks = {}
for mode, kind, oid, path in entries:
    if kind == "commit":
        sub = root / path
        populated = (sub / ".git").exists()
        actual = git(sub, "rev-parse", "HEAD").decode().strip() if populated else None
        gitlinks[path] = {"pin": oid, "checked_out": actual}
        if populated and actual != oid:
            problems.append(path + ": gitlink checkout differs")
status = git(root, "status", "--porcelain=v1", "--ignored", "--untracked-files=all").decode().splitlines()
flags = git(root, "ls-files", "-v").decode().splitlines()
hidden = [l for l in flags if l[:1] not in ("H",)]
result = {"checkout": "<review clone>", "head": head, "tree": tree, "tracked_blobs": len(files),
          "regular_files_hashed": len(regular), "gitlinks": gitlinks,
          "status_entries_including_ignored": status, "non_H_index_flags": hidden[:20],
          "problems": problems, "clean": not problems and not status and not hidden}
out.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({k: result[k] for k in ("tracked_blobs", "problems", "clean")}))
