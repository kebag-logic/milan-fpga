#!/usr/bin/env python3
"""Verify an isolated review clone against its exact head (read-only).

Usage: verify_clone.py <clone> <expected-head> <expected-tree>
Checks HEAD and tree ids, a clean status (ignored files included), index ==
HEAD (mode, blob, path), and every tracked file's raw bytes (git blob hash of
the working-tree bytes) and executable bit against HEAD. Lists gitlinks.
Exit 0 only if everything matches.
"""
import hashlib
import os
import subprocess
import sys

clone, want_head, want_tree = sys.argv[1:4]


def git(*args: str) -> bytes:
    return subprocess.run(["git", "-C", clone, *args], check=True,
                          capture_output=True).stdout


bad = 0
head = git("rev-parse", "HEAD").decode().strip()
tree = git("rev-parse", "HEAD^{tree}").decode().strip()
print(f"HEAD {head} (expected {want_head})")
print(f"tree {tree} (expected {want_tree})")
bad += head != want_head
bad += tree != want_tree
status = git("status", "--porcelain", "--ignored").decode()
print(f"status --porcelain --ignored: {'clean' if not status else status!r}")
bad += bool(status)
index = sorted(l.split(b"\t", 1)[0].split()[0:2] + [l.split(b"\t", 1)[1]]
               for l in git("ls-files", "-s", "-z").split(b"\0") if l)
treel = []
gitlinks = []
for entry in git("ls-tree", "-r", "-z", "HEAD").split(b"\0"):
    if not entry:
        continue
    meta, path = entry.split(b"\t", 1)
    mode, kind, blob = meta.split()
    treel.append([mode, blob, path])
    if mode == b"160000":
        gitlinks.append((path.decode(), blob.decode()))
treel.sort()
same_index = [[m, b, p] for m, b, p in index] == treel
print(f"index (mode, blob, path) == HEAD tree: {same_index}")
bad += not same_index
checked = 0
for mode, blob, path in treel:
    if mode == b"160000":
        continue
    full = os.path.join(clone, path.decode())
    if mode == b"120000":
        data = os.readlink(full).encode()
    else:
        with open(full, "rb") as fh:
            data = fh.read()
    h = hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()
    checked += 1
    if h != blob.decode():
        bad += 1
        print(f"BYTE MISMATCH {path.decode()}")
    if mode in (b"100644", b"100755"):
        is_x = os.access(full, os.X_OK)
        if is_x != (mode == b"100755"):
            bad += 1
            print(f"MODE MISMATCH {path.decode()}")
print(f"tracked files checked: {checked}; gitlinks: {len(gitlinks)} {gitlinks}")
print(f"mismatches: {bad}")
sys.exit(1 if bad else 0)
