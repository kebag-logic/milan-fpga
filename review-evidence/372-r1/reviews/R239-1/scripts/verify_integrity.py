#!/usr/bin/env python3
"""Verify a checkout is byte-identical to a commit: every tracked blob's worktree bytes,
file kind/mode, the index against HEAD's tree, and each required submodule gitlink.

Usage: verify_integrity.py <repo> <expected-head> <expected-tree> [submodule ...]
Uses plumbing only (ls-tree, ls-files -s, hash-object, rev-parse), GIT_NO_REPLACE_OBJECTS=1.
"""
import os
import stat
import subprocess
import sys

env = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], check=True, capture_output=True, env=env).stdout


def main():
    repo, head, tree = sys.argv[1:4]
    subs = sys.argv[4:]
    problems = []
    actual_head = git(repo, "rev-parse", "HEAD").decode().strip()
    actual_tree = git(repo, "rev-parse", "HEAD^{tree}").decode().strip()
    if actual_head != head:
        problems.append(f"HEAD {actual_head} != {head}")
    if actual_tree != tree:
        problems.append(f"tree {actual_tree} != {tree}")
    entries = {}
    for rec in git(repo, "ls-tree", "-r", "-z", "--full-tree", head).split(b"\0"):
        if not rec:
            continue
        meta, path = rec.split(b"\t", 1)
        mode, kind, oid = meta.decode().split()
        entries[path.decode()] = (mode, kind, oid)
    index = {}
    for rec in git(repo, "ls-files", "-s", "-z").split(b"\0"):
        if not rec:
            continue
        meta, path = rec.split(b"\t", 1)
        mode, oid, stage = meta.decode().split()
        index.setdefault(path.decode(), []).append((mode, oid, stage))
    if set(index) != set(entries):
        problems.append(f"index paths differ from HEAD tree: +{sorted(set(index)-set(entries))[:5]} "
                        f"-{sorted(set(entries)-set(index))[:5]}")
    blobs = gitlinks = 0
    for path, (mode, kind, oid) in entries.items():
        recs = index.get(path, [])
        if recs != [(mode, oid, "0")]:
            problems.append(f"index record for {path}: {recs} != {(mode, oid, '0')}")
        full = os.path.join(repo, path)
        if kind == "commit":
            gitlinks += 1
            continue
        blobs += 1
        try:
            st = os.lstat(full)
        except FileNotFoundError:
            problems.append(f"missing {path}")
            continue
        if mode == "120000":
            if not stat.S_ISLNK(st.st_mode):
                problems.append(f"{path} should be a symlink")
                continue
            data = os.readlink(full).encode()
            got = subprocess.run(["git", "hash-object", "--stdin"], input=data, capture_output=True,
                                 check=True, env=env).stdout.decode().strip()
        else:
            if not stat.S_ISREG(st.st_mode):
                problems.append(f"{path} is not a regular file")
                continue
            want_exec = mode == "100755"
            if bool(st.st_mode & stat.S_IXUSR) != want_exec:
                problems.append(f"{path} exec bit mismatch for mode {mode}")
            got = git(repo, "hash-object", "--no-filters", path).decode().strip()
        if got != oid:
            problems.append(f"{path} bytes {got} != {oid}")
    for sub in subs:
        want = entries.get(sub)
        if not want or want[1] != "commit":
            problems.append(f"{sub} is not a gitlink at {head}")
            continue
        got = git(os.path.join(repo, sub), "rev-parse", "HEAD").decode().strip()
        dirty = git(os.path.join(repo, sub), "status", "--porcelain", "--untracked-files=no").decode().strip()
        if got != want[2]:
            problems.append(f"submodule {sub} at {got} != pin {want[2]}")
        if dirty:
            problems.append(f"submodule {sub} has tracked changes")
    status = git(repo, "status", "--porcelain", "--untracked-files=all", "--ignored=no").decode().strip()
    if status:
        problems.append("status not clean: " + status.splitlines()[0])
    print(f"head={actual_head} tree={actual_tree} blobs_verified={blobs} gitlinks={gitlinks} "
          f"submodules_checked={len(subs)} problems={len(problems)}")
    for p in problems[:40]:
        print("PROBLEM", p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
