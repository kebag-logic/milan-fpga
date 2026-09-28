#!/usr/bin/env python3
"""Reviewer check: every tracked path in <repo> equals the exact head tree.

Usage: verify_head_bytes.py <repo> <expected-head> <expected-tree>
Compares HEAD, HEAD's tree, the index entries and the on-disk bytes/modes of
every regular file and symlink against `git ls-tree -r HEAD`; gitlinks are
compared as index records only.  Exits non-zero on any difference.
"""
import os
import stat
import subprocess
import sys

repo, want_head, want_tree = sys.argv[1:4]
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")


def git(*args: str, data: bytes | None = None) -> bytes:
    return subprocess.run(["git", "-C", repo, *args], input=data, env=env,
                          check=True, capture_output=True).stdout


head = git("rev-parse", "HEAD").decode().strip()
tree = git("rev-parse", "HEAD^{tree}").decode().strip()
bad = []
if head != want_head:
    bad.append(f"HEAD {head}")
if tree != want_tree:
    bad.append(f"tree {tree}")
listed = {}
for rec in git("ls-tree", "-r", "-z", "HEAD").split(b"\0"):
    if rec:
        meta, path = rec.split(b"\t", 1)
        mode, _kind, sha = meta.decode().split()
        listed[path.decode()] = (mode, sha)
index = {}
for rec in git("ls-files", "-s", "-z").split(b"\0"):
    if rec:
        meta, path = rec.split(b"\t", 1)
        mode, sha, stage = meta.decode().split()
        index.setdefault(path.decode(), []).append((mode, sha, stage))
if set(index) != set(listed):
    bad.append("index path set differs from tree")
files = []
for path, (mode, sha) in listed.items():
    if index.get(path) != [(mode, sha, "0")]:
        bad.append(f"index record {path}")
    if mode == "160000":
        continue
    full = os.path.join(repo, path)
    st = os.lstat(full)
    if mode == "120000":
        if not stat.S_ISLNK(st.st_mode):
            bad.append(f"not a symlink {path}")
            continue
        blob = os.readlink(full).encode()
        got = git("hash-object", "--stdin", data=blob).decode().strip()
    else:
        if not stat.S_ISREG(st.st_mode):
            bad.append(f"not a file {path}")
            continue
        exe = bool(st.st_mode & 0o100)
        if exe != (mode == "100755"):
            bad.append(f"mode {path}")
        files.append((path, sha))
        continue
    if got != sha:
        bad.append(f"bytes {path}")
paths = "\n".join(p for p, _ in files).encode()
hashes = git("hash-object", "--no-filters", "--stdin-paths", data=paths).decode().split()
for (path, sha), got in zip(files, hashes):
    if got != sha:
        bad.append(f"bytes {path}")
gitlinks = sorted(p for p, (m, _) in listed.items() if m == "160000")
print(f"head={head} tree={tree} paths={len(listed)} files={len(files)} gitlinks="
      + ",".join(f"{p}@{listed[p][1]}" for p in gitlinks))
for item in bad[:50]:
    print("MISMATCH", item)
print("RESULT", "PASS" if not bad else f"FAIL ({len(bad)})")
sys.exit(1 if bad else 0)
