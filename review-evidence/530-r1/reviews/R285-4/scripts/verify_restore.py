#!/usr/bin/env python3
"""Verify a review clone is byte-exact at the reviewed head after probes.

Usage: verify_restore.py <repo> <expected-head> <expected-tree>

Checks, all through git plumbing:
  * HEAD and its tree equal the expected ids;
  * every index entry is stage 0 and its mode/blob equal HEAD's tree entry;
  * every tracked regular file / symlink on disk hashes to its blob id and
    carries the recorded executable bit;
  * no index entry carries assume-unchanged or skip-worktree;
  * the working tree has no untracked or ignored files;
  * every gitlink in HEAD equals the submodule checkout's HEAD, and each
    submodule checkout is clean (untracked and ignored included).
Exit 0 when every check holds.
"""
import os
import subprocess
import sys


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], check=True,
                          capture_output=True, env={**os.environ,
                          "GIT_NO_REPLACE_OBJECTS": "1"}).stdout


def main() -> int:
    repo, want_head, want_tree = sys.argv[1:4]
    bad = []
    head = git(repo, "rev-parse", "HEAD").decode().strip()
    tree = git(repo, "rev-parse", "HEAD^{tree}").decode().strip()
    print(f"HEAD {head}\nTREE {tree}")
    if head != want_head or tree != want_tree:
        bad.append("head/tree mismatch")

    tree_entries = {}
    for rec in git(repo, "ls-tree", "-r", "-z", "HEAD").split(b"\0"):
        if not rec:
            continue
        meta, path = rec.split(b"\t", 1)
        mode, _typ, oid = meta.decode().split()
        tree_entries[path.decode()] = (mode, oid)

    index_entries = {}
    for rec in git(repo, "ls-files", "-s", "-z").split(b"\0"):
        if not rec:
            continue
        meta, path = rec.split(b"\t", 1)
        mode, oid, stage = meta.decode().split()
        if stage != "0":
            bad.append(f"unmerged index entry {path.decode()}")
        index_entries[path.decode()] = (mode, oid)
    if index_entries != tree_entries:
        bad.append("index differs from HEAD tree")

    for rec in git(repo, "ls-files", "-v", "-z").split(b"\0"):
        if rec and rec[:1] != b"H":
            bad.append(f"index flag {rec[:1].decode()} on {rec[2:].decode()}")

    files = [(p, m, o) for p, (m, o) in tree_entries.items() if m != "160000"]
    checked = 0
    for path, mode, oid in files:
        full = os.path.join(repo, path)
        if mode == "120000":
            if not os.path.islink(full):
                bad.append(f"not a symlink: {path}")
                continue
            data = os.readlink(full).encode()
        else:
            if os.path.islink(full) or not os.path.isfile(full):
                bad.append(f"missing or not a file: {path}")
                continue
            with open(full, "rb") as fh:
                data = fh.read()
            is_exec = bool(os.stat(full).st_mode & 0o111)
            if is_exec != (mode == "100755"):
                bad.append(f"mode bit differs: {path}")
        got = subprocess.run(["git", "hash-object", "--no-filters", "--stdin"],
                             input=data, check=True,
                             capture_output=True).stdout.decode().strip()
        if got != oid:
            bad.append(f"blob differs: {path}")
        checked += 1
    print(f"tracked files byte-checked: {checked}")

    extra = git(repo, "status", "--porcelain", "--ignored",
                "--ignore-submodules=all").decode().strip()
    if extra:
        bad.append("untracked/ignored/modified entries:\n" + extra)

    for path, (mode, oid) in tree_entries.items():
        if mode != "160000":
            continue
        sub = os.path.join(repo, path)
        if not os.path.exists(os.path.join(sub, ".git")):
            print(f"gitlink {path} {oid} (not initialised)")
            continue
        sub_head = git(sub, "rev-parse", "HEAD").decode().strip()
        dirty = git(sub, "status", "--porcelain", "--ignored").decode().strip()
        print(f"gitlink {path} {oid} checkout {sub_head} "
              f"{'clean' if not dirty else 'DIRTY'}")
        if sub_head != oid:
            bad.append(f"submodule {path} off pin")
        if dirty:
            bad.append(f"submodule {path} dirty:\n{dirty}")

    for b in bad:
        print("FAIL", b)
    print("RESTORE VERIFIED" if not bad else "RESTORE NOT VERIFIED")
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
