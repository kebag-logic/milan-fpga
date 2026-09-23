#!/usr/bin/env python3
"""Verify a review clone is byte-exact at the reviewed head.

usage: restore_verify.py <clone> <head-sha> <tree-sha>
Checks HEAD and tree ids, index == HEAD tree (mode, oid, stage 0), every
tracked regular file's working bytes and executable bit against its blob,
gitlink pins (and initialized submodule HEADs), and an empty
`git status --porcelain --ignored`. Exit 0 on success.
"""
import os
import subprocess
import sys


def git(repo, *a):
    return subprocess.run(["git", "-C", repo, *a], capture_output=True, check=True).stdout


def main():
    repo, head, tree = sys.argv[1:4]
    bad = []
    if git(repo, "rev-parse", "HEAD").decode().strip() != head:
        bad.append("HEAD differs")
    if git(repo, "rev-parse", "HEAD^{tree}").decode().strip() != tree:
        bad.append("tree differs")
    lt = {}
    for line in git(repo, "ls-tree", "-r", "-z", "HEAD").split(b"\0"):
        if line:
            meta, path = line.split(b"\t", 1)
            mode, typ, oid = meta.decode().split()
            lt[path] = (mode, typ, oid)
    idx = {}
    for line in git(repo, "ls-files", "-s", "-z").split(b"\0"):
        if line:
            meta, path = line.split(b"\t", 1)
            mode, oid, stage = meta.decode().split()
            idx[path] = (mode, oid, stage)
    if set(lt) != set(idx):
        bad.append("index path set differs from HEAD tree")
    for p, (mode, _t, oid) in lt.items():
        m2, o2, st = idx.get(p, (None, None, None))
        if (m2, o2, st) != (mode, oid, "0"):
            bad.append(f"index entry differs: {p!r}")
    files = gitlinks = 0
    for p, (mode, typ, oid) in lt.items():
        fp = os.path.join(repo.encode(), p)
        if typ == "commit":
            gitlinks += 1
            sub = fp.decode()
            if os.path.exists(os.path.join(sub, ".git")):
                h = git(sub, "rev-parse", "HEAD").decode().strip()
                if h != oid:
                    bad.append(f"submodule {p!r} at {h} not {oid}")
            continue
        files += 1
        if mode == "120000":
            if os.readlink(fp).encode() != git(repo, "cat-file", "blob", oid):
                bad.append(f"symlink differs: {p!r}")
            continue
        got = subprocess.run(["git", "-C", repo, "hash-object", "--no-filters", "--", p.decode()],
                             capture_output=True, check=True).stdout.decode().strip()
        if got != oid:
            bad.append(f"bytes differ: {p!r}")
        exe = os.access(fp, os.X_OK)
        if exe != (mode == "100755"):
            bad.append(f"mode differs: {p!r}")
    st = git(repo, "status", "--porcelain=v1", "--ignored", "--untracked-files=all").decode()
    print(f"HEAD {head}; tree {tree}; tracked non-gitlink entries {files}; gitlinks {gitlinks}")
    print(f"status --porcelain --ignored lines: {len(st.splitlines())}")
    for b in bad:
        print("BAD", b)
    print("RESULT:", "PASS" if not bad and not st.strip() else "FAIL")
    return 0 if not bad and not st.strip() else 1


if __name__ == "__main__":
    sys.exit(main())
