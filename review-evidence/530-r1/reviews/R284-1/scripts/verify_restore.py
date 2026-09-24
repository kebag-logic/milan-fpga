#!/usr/bin/env python3
"""Prove a checkout holds exactly its HEAD: every tracked regular file's bytes
hash to the index blob, its mode matches, the index equals HEAD's tree, no
assume-unchanged/skip-worktree flag hides anything, and each named submodule's
gitlink equals its checked-out HEAD (recursing into the same proof).

Usage: python3 verify_restore.py <repo> [<submodule-path>...]
Exit 0 only if every check holds.
"""
import os
import stat
import subprocess
import sys

ENV = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")


def git(repo, *args, data=None):
    return subprocess.run(["git", "-C", repo, *args], env=ENV, input=data,
                          capture_output=True, check=True).stdout


def prove(repo):
    bad = 0
    head = git(repo, "rev-parse", "HEAD").decode().strip()
    tree = git(repo, "rev-parse", "HEAD^{tree}").decode().strip()
    idx_tree = git(repo, "write-tree").decode().strip()
    if idx_tree != tree:
        print(f"[FAIL] {repo}: index tree {idx_tree} != HEAD tree {tree}")
        bad += 1
    flags = [l for l in git(repo, "ls-files", "-v", "-z").split(b"\0") if l and not l.startswith(b"H ")]
    if flags:
        print(f"[FAIL] {repo}: {len(flags)} index entries carry a hiding flag")
        bad += 1
    n = 0
    for rec in git(repo, "ls-files", "-s", "-z").split(b"\0"):
        if not rec:
            continue
        meta, path = rec.split(b"\t", 1)
        mode, blob, stage = meta.split()
        p = os.path.join(repo, path.decode())
        if stage != b"0":
            print(f"[FAIL] {repo}: unmerged {path!r}")
            bad += 1
            continue
        if mode == b"160000":
            continue
        n += 1
        st = os.lstat(p) if os.path.lexists(p) else None
        if st is None:
            print(f"[FAIL] {repo}: missing {path!r}")
            bad += 1
            continue
        if mode == b"120000":
            ok = stat.S_ISLNK(st.st_mode) and git(repo, "hash-object", "--stdin", data=os.readlink(p).encode()).strip() == blob
        else:
            want_x = mode == b"100755"
            is_x = bool(st.st_mode & stat.S_IXUSR)
            with open(p, "rb") as fh:
                h = git(repo, "hash-object", "--no-filters", "--stdin", data=fh.read()).strip()
            ok = stat.S_ISREG(st.st_mode) and want_x == is_x and h == blob
        if not ok:
            print(f"[FAIL] {repo}: {path!r} differs from its index blob/mode")
            bad += 1
    print(f"{repo}: HEAD {head} tree {tree}; {n} tracked files byte/mode-exact" if not bad else f"{repo}: {bad} failure(s)")
    return bad


def main():
    repo = os.path.abspath(sys.argv[1])
    bad = prove(repo)
    for sub in sys.argv[2:]:
        link = git(repo, "ls-files", "-s", "--", sub).decode().split()
        want = link[1] if link and link[0] == "160000" else None
        got = git(os.path.join(repo, sub), "rev-parse", "HEAD").decode().strip()
        if want != got:
            print(f"[FAIL] gitlink {sub}: index {want} checkout {got}")
            bad += 1
        else:
            print(f"gitlink {sub}: {got} (index == checkout)")
        bad += prove(os.path.join(repo, sub))
    print("RESTORE VERIFIED" if not bad else "RESTORE NOT VERIFIED")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
