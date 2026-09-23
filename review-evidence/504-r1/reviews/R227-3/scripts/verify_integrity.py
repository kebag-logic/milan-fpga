#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Verify a review clone is byte-identical to its exact head.

Usage: verify_integrity.py <clone> <expected-head> <expected-tree>

Checks, without trusting index flags: HEAD and tree ids; no assume-unchanged or
skip-worktree index flags; every index entry is stage 0; every tracked regular
file and symlink hashes to its index blob and carries its index mode; the
working tree has no untracked or modified paths; and every gitlink matches
HEAD's tree, with each initialised submodule checked out at that commit and
clean. Prints one line per check and exits non-zero on any mismatch.
"""
import os
import stat
import subprocess
import sys


def git(clone, *args, raw=False):
    out = subprocess.run(["git", "-C", clone, *args], check=True,
                         capture_output=True, env={**os.environ,
                                                   "GIT_NO_REPLACE_OBJECTS": "1"})
    return out.stdout if raw else out.stdout.decode()


def main():
    clone, head, tree = sys.argv[1:4]
    failures = []
    got_head = git(clone, "rev-parse", "HEAD").strip()
    got_tree = git(clone, "rev-parse", "HEAD^{tree}").strip()
    print(f"HEAD {got_head} tree {got_tree}")
    if got_head != head or got_tree != tree:
        failures.append("head/tree mismatch")
    flags = [line for line in git(clone, "ls-files", "-v").splitlines()
             if line[:1] != "H" and line[:1] != "S" or line[:1] in "hS"]
    hidden = [line for line in git(clone, "ls-files", "-v").splitlines()
              if line[:1] in ("h", "S", "s")]
    print(f"index flags hiding changes: {len(hidden)}")
    if hidden:
        failures.append(f"hidden index flags: {hidden[:5]}")
    entries = git(clone, "ls-files", "-s", "-z", raw=True).split(b"\0")
    checked = gitlinks = 0
    head_tree = {}
    for rec in git(clone, "ls-tree", "-r", "-z", "HEAD", raw=True).split(b"\0"):
        if rec:
            meta, path = rec.split(b"\t", 1)
            mode, _kind, sha = meta.decode().split()
            head_tree[path] = (mode, sha)
    for rec in entries:
        if not rec:
            continue
        meta, path = rec.split(b"\t", 1)
        mode, sha, stage = meta.decode().split()
        if stage != "0":
            failures.append(f"unmerged {path!r}")
            continue
        if head_tree.get(path) != (mode, sha):
            failures.append(f"index differs from HEAD at {path!r}")
        full = os.path.join(clone.encode(), path)
        if mode == "160000":
            gitlinks += 1
            sub = full.decode()
            if os.path.isdir(os.path.join(sub, ".git")) or \
                    os.path.isfile(os.path.join(sub, ".git")):
                sub_head = git(sub, "rev-parse", "HEAD").strip()
                dirty = git(sub, "status", "--porcelain").strip()
                print(f"gitlink {path.decode()} pin {sha} checkout {sub_head} "
                      f"dirty={bool(dirty)}")
                if sub_head != sha or dirty:
                    failures.append(f"submodule {path!r} off pin or dirty")
            else:
                print(f"gitlink {path.decode()} pin {sha} (not initialised)")
            continue
        st = os.lstat(full)
        if mode == "120000":
            ok = stat.S_ISLNK(st.st_mode)
            data = os.readlink(full)
        else:
            ok = stat.S_ISREG(st.st_mode) and \
                (("100755" if st.st_mode & 0o111 else "100644") == mode)
            with open(full, "rb") as handle:
                data = handle.read()
        blob = subprocess.run(["git", "hash-object", "--no-filters",
                               "--stdin"], input=data, check=True,
                              capture_output=True).stdout.decode().strip()
        if not ok or blob != sha:
            failures.append(f"bytes/mode differ at {path!r}")
        checked += 1
    status = git(clone, "status", "--porcelain", "--ignored=no",
                 "--untracked-files=all").strip()
    print(f"tracked blobs verified: {checked}; gitlinks: {gitlinks}")
    print(f"status porcelain: {status or '(clean)'}")
    if status:
        failures.append("working tree not clean")
    for failure in failures:
        print("FAIL: " + failure)
    print("INTEGRITY " + ("PASS" if not failures else "FAIL"))
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
