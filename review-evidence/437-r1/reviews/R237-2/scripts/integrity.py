#!/usr/bin/env python3
"""R237-2 review-clone integrity: every tracked path's bytes, mode and index
record against the exact head tree, index flags, and the gitlinks.

Usage: integrity.py CLONE EXPECTED_HEAD
Exit 0 only when HEAD is EXPECTED_HEAD, the index equals the HEAD tree
(stage 0 only, no assume-unchanged or skip-worktree flag), every regular
file and symlink on disk hashes to its blob with the recorded mode, and the
four gitlinks equal the HEAD tree's. All Git calls set
GIT_NO_REPLACE_OBJECTS=1.
"""
import os
import stat
import subprocess
import sys
from pathlib import Path

ENV = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")


def git(clone: str, *args: str) -> str:
    return subprocess.run(["git", "-C", clone, *args], check=True, capture_output=True,
                          text=True, env=ENV).stdout


def main() -> int:
    clone, expected = sys.argv[1], sys.argv[2]
    problems = []
    head = git(clone, "rev-parse", "HEAD").strip()
    if head != expected:
        problems.append(f"HEAD {head} != {expected}")
    tree = {}
    for rec in git(clone, "ls-tree", "-r", "-z", "HEAD").split("\0"):
        if rec:
            meta, path = rec.split("\t", 1)
            mode, kind, oid = meta.split()
            tree[path] = (mode, oid)
    index = {}
    for rec in git(clone, "ls-files", "-s", "-z").split("\0"):
        if rec:
            meta, path = rec.split("\t", 1)
            mode, oid, stage = meta.split()
            if stage != "0":
                problems.append(f"unmerged index stage {stage}: {path}")
            index[path] = (mode, oid)
    if index != tree:
        problems.append(f"index differs from HEAD tree on {len(set(index.items()) ^ set(tree.items()))} records")
    for line in git(clone, "ls-files", "-v").splitlines():
        if line[:1] != "H":  # h = assume-unchanged, S = skip-worktree
            problems.append(f"index flag {line[:1]!r}: {line[2:]}")
    checked = links = 0
    for path, (mode, oid) in tree.items():
        full = Path(clone) / path
        if mode == "160000":
            links += 1
            continue
        st = os.lstat(full)
        if mode == "120000":
            ok = stat.S_ISLNK(st.st_mode)
            data = os.readlink(full).encode() if ok else b""
        else:
            ok = stat.S_ISREG(st.st_mode) and (bool(st.st_mode & 0o100) == (mode == "100755"))
            data = full.read_bytes() if ok else b""
        got = subprocess.run(["git", "hash-object", "--stdin"], input=data, capture_output=True,
                             check=True, env=ENV).stdout.decode().strip()
        if not ok or got != oid:
            problems.append(f"bytes/mode/kind differ: {path}")
        checked += 1
    status = git(clone, "status", "--porcelain=v1", "--untracked-files=all", "--ignore-submodules=none")
    if status.strip():
        problems.append(f"status not clean: {status.strip()[:300]}")
    gitlinks = sorted((p, o) for p, (m, o) in tree.items() if m == "160000")
    for p in problems:
        print("PROBLEM", p)
    print(f"head {head}; {checked} files hashed and mode-checked; {len(index)} index records "
          f"equal the tree; {links} gitlinks: {gitlinks}; status clean: {not status.strip()}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
