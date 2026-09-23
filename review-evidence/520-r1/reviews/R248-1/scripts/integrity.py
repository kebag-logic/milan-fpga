#!/usr/bin/env python3
"""Byte-level integrity receipt for a review clone.

Proves, without trusting the index's stat cache: HEAD and tree ids, that every
index record equals the HEAD tree record (path, mode, blob id, stage 0), that
every tracked regular file's on-disk bytes hash to its recorded blob id with
the recorded executable bit, symlinks match their recorded target, the index
flags carry no assume-unchanged/skip-worktree bit, no untracked non-ignored
files exist, and each required submodule gitlink equals its checkout HEAD with
a clean checkout.

usage: integrity.py REPO EXPECTED_HEAD EXPECTED_TREE [SUBMODULE...]
Exit 0 only when every check passes; prints one line per check.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ENV = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1", LC_ALL="C")


def git(repo: Path, *args: str, binary: bool = False) -> str | bytes:
    out = subprocess.run(["git", "-C", str(repo), *args], check=True,
                         capture_output=True, env=ENV).stdout
    return out if binary else out.decode()


def main(argv: list[str]) -> int:
    repo, want_head, want_tree, *subs = argv
    repo = Path(repo)
    problems: list[str] = []
    head = git(repo, "rev-parse", "HEAD").strip()
    tree = git(repo, "rev-parse", "HEAD^{tree}").strip()
    print(f"head={head}")
    print(f"tree={tree}")
    if head != want_head:
        problems.append(f"HEAD {head} != {want_head}")
    if tree != want_tree:
        problems.append(f"tree {tree} != {want_tree}")
    tree_recs = {}
    for rec in git(repo, "ls-tree", "-r", "-z", "--full-tree", "HEAD", binary=True).split(b"\0"):
        if not rec:
            continue
        meta, path = rec.split(b"\t", 1)
        mode, _typ, oid = meta.decode().split()
        tree_recs[path.decode()] = (mode, oid)
    index_recs = {}
    for rec in git(repo, "ls-files", "-s", "-z", binary=True).split(b"\0"):
        if not rec:
            continue
        meta, path = rec.split(b"\t", 1)
        mode, oid, stage = meta.decode().split()
        p = path.decode()
        if stage != "0":
            problems.append(f"index stage {stage} at {p}")
        if p in index_recs:
            problems.append(f"duplicate index record {p}")
        index_recs[p] = (mode, oid)
    if index_recs != tree_recs:
        extra = set(index_recs) ^ set(tree_recs)
        diff = [p for p in set(index_recs) & set(tree_recs) if index_recs[p] != tree_recs[p]]
        problems.append(f"index != HEAD tree: {sorted(extra)[:5]} {sorted(diff)[:5]}")
    print(f"index_records={len(index_recs)} tree_records={len(tree_recs)}")
    flags = git(repo, "ls-files", "-v", "-z", binary=True).split(b"\0")
    hidden = [f.decode() for f in flags if f and f[:1] not in (b"H",)]
    if hidden:
        problems.append(f"index flag not H (assume-unchanged/skip-worktree/other): {hidden[:5]}")
    checked = 0
    for p, (mode, oid) in sorted(index_recs.items()):
        full = repo / p
        if mode == "160000":
            continue
        if mode == "120000":
            if not full.is_symlink():
                problems.append(f"symlink missing {p}")
                continue
            target = os.readlink(full).encode()
            got = subprocess.run(["git", "hash-object", "--stdin"], input=target,
                                 capture_output=True, check=True, env=ENV).stdout.decode().strip()
        else:
            if full.is_symlink() or not full.is_file():
                problems.append(f"not a regular file {p}")
                continue
            got = subprocess.run(["git", "hash-object", "--no-filters", str(full)],
                                 capture_output=True, check=True, env=ENV).stdout.decode().strip()
            exe = bool(full.stat().st_mode & 0o100)
            if exe != (mode == "100755"):
                problems.append(f"mode mismatch {p}: recorded {mode}, exec bit {exe}")
        if got != oid:
            problems.append(f"bytes differ {p}: {got} != {oid}")
        checked += 1
    print(f"worktree_files_hashed={checked}")
    untracked = git(repo, "ls-files", "--others", "--exclude-standard").split()
    if untracked:
        problems.append(f"untracked files: {untracked[:10]}")
    print(f"untracked_nonignored={len(untracked)}")
    for sub in subs:
        rec = index_recs.get(sub)
        if not rec or rec[0] != "160000":
            problems.append(f"no gitlink for {sub}")
            continue
        sub_head = git(repo / sub, "rev-parse", "HEAD").strip()
        dirty = git(repo / sub, "status", "--porcelain", "--untracked-files=all").strip()
        print(f"submodule {sub} gitlink={rec[1]} checkout={sub_head} dirty={'yes' if dirty else 'no'}")
        if sub_head != rec[1]:
            problems.append(f"{sub} checkout {sub_head} != gitlink {rec[1]}")
        if dirty:
            problems.append(f"{sub} dirty: {dirty.splitlines()[:5]}")
    for problem in problems:
        print(f"INTEGRITY FAIL: {problem}")
    print(f"integrity: {'OK' if not problems else 'FAIL'}")
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
