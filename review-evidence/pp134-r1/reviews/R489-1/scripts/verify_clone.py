#!/usr/bin/env python3
"""Verify a checkout is byte-exact at an expected head (review R489-1).

Usage: verify_clone.py <repo> <head> <tree>
Checks HEAD, HEAD^{tree}, the index tree, a clean porcelain status (ignored
and untracked included), every index entry's mode and blob against HEAD,
every working file's raw bytes (git hash-object --no-filters) and executable
bit against its index entry, and lists gitlinks (mode 160000).
"""
import os
import subprocess
import sys


def git(repo, *args, data=None):
    return subprocess.run(["git", "-C", repo, *args], check=True, capture_output=True,
                          input=data).stdout


def main() -> int:
    repo, head, tree = sys.argv[1:4]
    bad = []
    got_head = git(repo, "rev-parse", "HEAD").decode().strip()
    got_tree = git(repo, "rev-parse", "HEAD^{tree}").decode().strip()
    idx_tree = git(repo, "write-tree").decode().strip()
    print(f"HEAD {got_head}\nTREE {got_tree}\nINDEX-TREE {idx_tree}")
    if got_head != head or got_tree != tree or idx_tree != tree:
        bad.append("head/tree/index-tree mismatch")
    status = git(repo, "status", "--porcelain=v1", "--ignored", "--untracked-files=all").decode()
    print(f"status entries (incl. ignored/untracked): {len(status.splitlines())}")
    if status.strip():
        print(status)
        bad.append("status not clean")
    index = {}
    for rec in git(repo, "ls-files", "-s", "-z").split(b"\0"):
        if not rec:
            continue
        meta, path = rec.split(b"\t", 1)
        mode, blob, stage = meta.decode().split()
        index[path] = (mode, blob, stage)
    treemap = {}
    for rec in git(repo, "ls-tree", "-r", "-z", "HEAD").split(b"\0"):
        if not rec:
            continue
        meta, path = rec.split(b"\t", 1)
        mode, _kind, blob = meta.decode().split()
        treemap[path] = (mode, blob)
    if {p: v[:2] for p, v in index.items()} != treemap:
        bad.append("index != HEAD tree")
    links = [p.decode() for p, v in index.items() if v[0] == "160000"]
    for path, (mode, blob, stage) in index.items():
        if stage != "0":
            bad.append(f"unmerged {path!r}")
        if mode == "160000":
            continue
        full = os.path.join(repo.encode(), path)
        if mode == "120000":
            if os.readlink(full).encode() != git(repo, "cat-file", "blob", blob):
                bad.append(f"symlink {path!r}")
            continue
        h = git(repo, "hash-object", "--no-filters", "--", path.decode()).decode().strip()
        if h != blob:
            bad.append(f"blob {path!r}")
        exe = os.access(full, os.X_OK)
        if (mode == "100755") != exe:
            bad.append(f"mode {path!r}")
    print(f"files checked: {len(index)}; gitlinks: {len(links)} {links}")
    print("RESULT:", "OK" if not bad else "MISMATCH " + "; ".join(bad))
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
