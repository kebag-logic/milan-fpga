#!/usr/bin/env python3
"""Verify a review clone is exactly at its head after probes.

Usage: verify_restore.py <repo> <expected-head> <expected-tree> <gitlink>=<sha> ...

Checks: HEAD and HEAD^{tree}; index tree == HEAD tree; every tracked regular
file's working bytes hash to its index blob and its mode matches; no
assume-unchanged / skip-worktree flags; no untracked or ignored paths; each
named gitlink is recorded at the expected sha, and an initialised submodule
checkout sits at that sha with a clean, leftover-free worktree.
"""
import os
import stat
import subprocess
import sys


def git(repo, *a, text=True):
    return subprocess.run(["git", "-C", repo, *a], check=True,
                          capture_output=True, text=text).stdout


def main():
    repo, head, tree = sys.argv[1:4]
    links = dict(x.split("=", 1) for x in sys.argv[4:])
    ok = True

    def chk(cond, msg):
        nonlocal ok
        print(("OK   " if cond else "FAIL ") + msg)
        ok &= bool(cond)

    chk(git(repo, "rev-parse", "HEAD").strip() == head, f"HEAD == {head}")
    chk(git(repo, "rev-parse", "HEAD^{tree}").strip() == tree, f"HEAD^{{tree}} == {tree}")
    chk(git(repo, "write-tree").strip() == tree, "index tree == HEAD tree")
    flags = [l for l in git(repo, "ls-files", "-v").splitlines()
             if l[:1] != "H" and l[:1] != "S" or l[:1].islower()]
    chk(not [l for l in git(repo, "ls-files", "-v").splitlines() if l[:1].islower() or l[:1] == "S"],
        "no assume-unchanged / skip-worktree flags")
    entries = git(repo, "ls-files", "-s", "-z").split("\0")
    n = bad = 0
    for e in entries:
        if not e:
            continue
        meta, path = e.split("\t", 1)
        mode, blob, _ = meta.split()
        if mode == "160000":
            continue
        n += 1
        full = os.path.join(repo, path)
        try:
            st = os.lstat(full)
        except FileNotFoundError:
            print(f"  missing {path}"); bad += 1; continue
        if mode == "120000":
            h = git(repo, "hash-object", "--stdin", text=False) if False else None
            target = os.readlink(full).encode()
            h = subprocess.run(["git", "-C", repo, "hash-object", "--stdin"],
                               input=target, capture_output=True, check=True).stdout.decode().strip()
            if h != blob:
                print(f"  symlink differs {path}"); bad += 1
            continue
        want_x = mode == "100755"
        is_x = bool(st.st_mode & stat.S_IXUSR)
        if want_x != is_x:
            print(f"  mode differs {path}"); bad += 1
        h = subprocess.run(["git", "-C", repo, "hash-object", "--no-filters", path],
                           capture_output=True, check=True, text=True).stdout.strip()
        if h != blob:
            print(f"  bytes differ {path}"); bad += 1
    chk(bad == 0, f"{n} tracked files byte- and mode-exact ({bad} mismatches)")
    left = git(repo, "status", "--porcelain", "--ignored", "--untracked-files=all")
    chk(left.strip() == "", "no modified, untracked or ignored paths in the parent")
    for p, sha in links.items():
        rec = git(repo, "ls-tree", "HEAD", p).split()
        chk(len(rec) >= 3 and rec[1] == "commit" and rec[2] == sha, f"gitlink {p} recorded at {sha}")
        sub = os.path.join(repo, p)
        if os.path.exists(os.path.join(sub, ".git")):
            chk(git(sub, "rev-parse", "HEAD").strip() == sha, f"  {p} checkout at {sha}")
            chk(git(sub, "status", "--porcelain", "--ignored", "--untracked-files=all").strip() == "",
                f"  {p} worktree clean, no leftovers")
        else:
            print(f"INFO {p} not initialised in this clone")
    print("RESULT", "RESTORED" if ok else "NOT RESTORED")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
