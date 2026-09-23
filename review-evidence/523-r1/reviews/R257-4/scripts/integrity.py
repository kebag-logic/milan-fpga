#!/usr/bin/env python3
"""Prove a checkout's tracked worktree bytes, modes, index and gitlinks.

Usage: integrity.py <repo> <expected-head>
Every index entry is hashed from disk and compared with its stage-0 blob and
mode; gitlinks compare the submodule checkout HEAD when initialised. The
index must match HEAD's tree, no entry may carry assume-unchanged or
skip-worktree flags, and each initialised submodule must be clean. Prints a
digest of the observations and exits 0 only when all hold.
"""
import hashlib
import os
import stat
import subprocess
import sys


def git(repo, *args, env=None):
    return subprocess.run(["git", "-C", repo, *args], check=True, capture_output=True,
                          env=env).stdout


def blob_id(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def main() -> int:
    repo, expected = sys.argv[1], sys.argv[2]
    env = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")
    problems = []
    head = git(repo, "rev-parse", "HEAD", env=env).decode().strip()
    if head != expected:
        problems.append(f"HEAD {head} != expected {expected}")
    tree = git(repo, "rev-parse", "HEAD^{tree}", env=env).decode().strip()
    index_tree = git(repo, "write-tree", env=env).decode().strip()
    if index_tree != tree:
        problems.append(f"index tree {index_tree} != HEAD tree {tree}")
    flags = git(repo, "ls-files", "-v", "-z", env=env).split(b"\0")
    odd = [f for f in flags if f and f[:2] not in (b"H ",)]
    if odd:
        problems.append(f"{len(odd)} entries with non-H ls-files -v tags: {odd[:5]}")
    entries = git(repo, "ls-files", "-s", "-z", env=env).split(b"\0")
    digest = hashlib.sha256()
    counts = {"regular": 0, "exec": 0, "symlink": 0, "gitlink": 0}
    for raw in entries:
        if not raw:
            continue
        meta, path = raw.split(b"\t", 1)
        mode, oid, stage = meta.decode().split()
        if stage != "0":
            problems.append(f"unmerged stage {stage}: {path!r}")
        full = os.path.join(repo.encode(), path)
        digest.update(raw + b"\0")
        if mode == "160000":
            counts["gitlink"] += 1
            if os.path.isdir(os.path.join(full, b".git")) or os.path.isfile(os.path.join(full, b".git")):
                sub = git(full.decode(), "rev-parse", "HEAD", env=env).decode().strip()
                if sub != oid:
                    problems.append(f"gitlink {path!r} checkout {sub} != {oid}")
                dirty = git(full.decode(), "status", "--porcelain", "--untracked-files=no", env=env)
                if dirty:
                    problems.append(f"submodule {path!r} dirty: {dirty[:200]!r}")
                digest.update(b"sub " + sub.encode() + b"\0")
            else:
                digest.update(b"sub uninitialised\0")
            continue
        try:
            st = os.lstat(full)
        except FileNotFoundError:
            problems.append(f"missing {path!r}")
            continue
        if mode == "120000":
            counts["symlink"] += 1
            if not stat.S_ISLNK(st.st_mode) or blob_id(os.readlink(full)) != oid:
                problems.append(f"symlink mismatch {path!r}")
            continue
        if not stat.S_ISREG(st.st_mode):
            problems.append(f"not a regular file {path!r}")
            continue
        with open(full, "rb") as handle:
            data = handle.read()
        if blob_id(data) != oid:
            problems.append(f"bytes differ {path!r}")
        executable = bool(st.st_mode & stat.S_IXUSR)
        if executable != (mode == "100755"):
            problems.append(f"mode differs {path!r}: index {mode}, disk exec={executable}")
        counts["exec" if mode == "100755" else "regular"] += 1
    untracked = git(repo, "status", "--porcelain", "--untracked-files=all", env=env).decode()
    print(f"head {head}\ntree {tree}\nindex-tree {index_tree}")
    print(f"entries {counts} index-digest {digest.hexdigest()}")
    print("status --porcelain (untracked/modified, ignored excluded):")
    print(untracked if untracked else "  <empty>")
    for p in problems:
        print("PROBLEM:", p)
    print("INTEGRITY:", "PASS" if not problems else "FAIL")
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
