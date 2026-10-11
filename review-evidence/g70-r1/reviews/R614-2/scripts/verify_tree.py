#!/usr/bin/env python3
"""Verify bytes and executable modes against a Git tree, including its index.

Usage: verify_tree.py REPO REF [EXPORTED_TREE]
An export skips index/status checks but compares every tracked byte and mode.
"""
import hashlib
import os
from pathlib import Path
import stat
import subprocess
import sys

repo = Path(sys.argv[1]).resolve()
ref = sys.argv[2]
root = Path(sys.argv[3]).resolve() if len(sys.argv) > 3 else repo
def git(*args):
    return subprocess.check_output(["git", "-C", str(repo), *args])

head = git("rev-parse", ref).decode().strip()
tree = git("rev-parse", ref + "^{tree}").decode().strip()
entries = git("ls-tree", "-rz", ref).split(b"\0")
failures = []
gitlinks = []
count = 0
for entry in filter(None, entries):
    meta, name = entry.split(b"\t", 1)
    mode, kind, oid = meta.decode().split()
    name = os.fsdecode(name)
    path = root / name
    if mode == "160000":
        gitlinks.append((name, oid))
        if root == repo:
            actual = subprocess.check_output(["git", "-C", str(path), "rev-parse", "HEAD"]).decode().strip()
            if actual != oid:
                failures.append(f"gitlink checkout differs: {name}")
        continue
    data = os.fsencode(os.readlink(path)) if mode == "120000" else path.read_bytes()
    actual = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    actual_mode = "120000" if path.is_symlink() else ("100755" if path.stat().st_mode & stat.S_IXUSR else "100644")
    if actual != oid or actual_mode != mode:
        failures.append(f"blob/mode differs: {name}: {actual_mode} {actual}, expected {mode} {oid}")
    count += 1
print(f"commit={head}\ntree={tree}\ntracked_blobs={count}\ngitlinks={gitlinks}")
if root == repo:
    index = git("write-tree").decode().strip()
    status = git("status", "--porcelain=v2", "--untracked-files=all").decode()
    print(f"index_tree={index}\nstatus={status!r}")
    if index != tree or status:
        failures.append("index or worktree is not exact and clean")
print("\n".join(failures) if failures else "PASS: all tracked bytes and modes match; required gitlinks verified")
sys.exit(bool(failures))
