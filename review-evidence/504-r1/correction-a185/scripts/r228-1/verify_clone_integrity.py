#!/usr/bin/env python3
"""Prove a checkout is exactly its HEAD: index == commit, bytes/modes == index,
no hidden index flags, required submodules at their gitlinks and clean.

Usage: verify_clone_integrity.py <checkout> <expected-head> [<submodule>...]
Exit 0 only when every check passes.
"""

import hashlib
import os
import stat
import subprocess
import sys
from pathlib import Path

root, expected = Path(sys.argv[1]).resolve(), sys.argv[2]
required = sys.argv[3:]
env = {**os.environ, "GIT_NO_REPLACE_OBJECTS": "1"}


def git(*args, cwd=root):
    return subprocess.run(["git", *args], cwd=cwd, env=env, check=True,
                          capture_output=True, text=True).stdout


def blob_id(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


problems = []
head = git("rev-parse", "HEAD").strip()
if head != expected:
    problems.append(f"HEAD {head} != {expected}")
tree = git("rev-parse", "HEAD^{tree}").strip()
committed = {}
for line in git("ls-tree", "-r", "-z", "HEAD").split("\0"):
    if line:
        meta, path = line.split("\t", 1)
        mode, _kind, sha = meta.split()
        committed[path] = (mode, sha)
index = {}
for line in git("ls-files", "-s", "-z").split("\0"):
    if line:
        meta, path = line.split("\t", 1)
        mode, sha, stage = meta.split()
        if stage != "0":
            problems.append(f"unmerged index stage {stage}: {path}")
        index[path] = (mode, sha)
if index != committed:
    problems.append(f"index differs from HEAD: {len(set(index.items()) ^ set(committed.items()))} entries")
flags = [l for l in git("ls-files", "-v").splitlines() if not l.startswith("H ")]
if flags:
    problems.append(f"{len(flags)} index entries carry assume-unchanged/skip-worktree flags")
checked = {"file": 0, "symlink": 0, "gitlink": 0}
for path, (mode, sha) in committed.items():
    disk = root / path
    if mode == "160000":
        checked["gitlink"] += 1
        if (disk / ".git").exists():
            actual = git("rev-parse", "HEAD", cwd=disk).strip()
            if actual != sha:
                problems.append(f"submodule {path} at {actual} != gitlink {sha}")
            if git("status", "--porcelain", cwd=disk).strip():
                problems.append(f"submodule {path} worktree not clean")
        elif path in required:
            problems.append(f"required submodule {path} not initialized")
        continue
    st = os.lstat(disk)
    if mode == "120000":
        checked["symlink"] += 1
        if not stat.S_ISLNK(st.st_mode) or blob_id(os.readlink(disk).encode()) != sha:
            problems.append(f"symlink mismatch {path}")
        continue
    checked["file"] += 1
    if not stat.S_ISREG(st.st_mode):
        problems.append(f"not a regular file {path}")
        continue
    if blob_id(disk.read_bytes()) != sha:
        problems.append(f"bytes differ {path}")
    exe = bool(st.st_mode & stat.S_IXUSR)
    if exe != (mode == "100755"):
        problems.append(f"mode differs {path}: {oct(st.st_mode)} vs {mode}")
status = git("status", "--porcelain", "--ignored=no").strip()
if status:
    problems.append("worktree status not empty: " + status.replace("\n", "; ")[:300])
for sub in required:
    if sub not in committed or committed[sub][0] != "160000":
        problems.append(f"required gitlink missing: {sub}")
print(f"head={head} tree={tree} checked={checked} required={required}")
for sub in required:
    print(f"gitlink {sub} = {committed.get(sub, ('?', '?'))[1]}")
print("INTEGRITY " + ("PASS" if not problems else "FAIL"))
for p in problems:
    print("  " + p)
sys.exit(1 if problems else 0)
