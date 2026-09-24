#!/usr/bin/env python3
"""Reviewer receipt (R313-1): prove the review clone holds exact head bytes.

Usage: python3 verify_clone.py <clone> <expected-head> <expected-tree>

Checks HEAD and tree ids; the index equals HEAD's tree (path, mode, blob,
stage 0 only, no assume-unchanged/skip-worktree bits); every tracked regular
file and symlink hashes to its blob with the recorded mode; every gitlink's
checkout is at the recorded commit with a clean worktree (or is an
uninitialised, unrequired entry); and no untracked or ignored file remains.
"""
import os
import stat
import subprocess
import sys

clone, want_head, want_tree = sys.argv[1:4]
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")


def git(*a, cwd=clone):
    return subprocess.run(["git", *a], cwd=cwd, env=env, check=True,
                          capture_output=True, text=True).stdout


bad = []
head = git("rev-parse", "HEAD").strip()
tree = git("rev-parse", "HEAD^{tree}").strip()
if head != want_head or tree != want_tree:
    bad.append(f"head/tree {head} {tree}")
tree_rows = {}
for ln in git("ls-tree", "-r", "--full-tree", "HEAD").splitlines():
    meta, path = ln.split("\t", 1)
    mode, typ, oid = meta.split()
    tree_rows[path] = (mode, oid)
idx = {}
for ln in git("ls-files", "-s").splitlines():
    meta, path = ln.split("\t", 1)
    mode, oid, st = meta.split()
    if st != "0":
        bad.append(f"stage {st}: {path}")
    idx[path] = (mode, oid)
if idx != tree_rows:
    bad.append(f"index != HEAD tree ({len(set(idx) ^ set(tree_rows))} path diffs)")
for ln in git("ls-files", "-v").splitlines():
    if ln[0] not in "H":
        bad.append(f"index flag {ln[:1]}: {ln[2:]}")
checked = 0
gitlinks = []
for path, (mode, oid) in tree_rows.items():
    full = os.path.join(clone, path)
    if mode == "160000":
        gitlinks.append((path, oid))
        continue
    st = os.lstat(full)
    if mode == "120000":
        ok = stat.S_ISLNK(st.st_mode)
    else:
        ok = stat.S_ISREG(st.st_mode) and (
            bool(st.st_mode & 0o111) == (mode == "100755"))
    got = git("hash-object", "--no-filters", "--", path).strip() if ok and mode != "120000" else (
        subprocess.run(["git", "hash-object", "--stdin"], input=os.readlink(full),
                       cwd=clone, env=env, capture_output=True, text=True).stdout.strip()
        if ok else "")
    if not ok or got != oid:
        bad.append(f"bytes/mode differ: {path}")
    checked += 1
for path, oid in gitlinks:
    sub = os.path.join(clone, path)
    if not os.path.exists(os.path.join(sub, ".git")):
        print(f"gitlink {path} {oid}: not initialised (as at review start)")
        continue
    got = git("rev-parse", "HEAD", cwd=sub).strip()
    dirty = git("status", "--porcelain", "--ignored", cwd=sub).strip()
    print(f"gitlink {path} {oid}: checkout {got} {'clean' if not dirty else 'DIRTY'}")
    if got != oid or dirty:
        bad.append(f"gitlink {path}")
extra = git("status", "--porcelain", "--ignored").strip()
if extra:
    bad.append("untracked/ignored:\n" + extra)
print(f"HEAD {head} tree {tree}; {checked} tracked files hashed; "
      f"{len(gitlinks)} gitlinks")
print("CLONE EXACT" if not bad else "CLONE DIFFERS:\n" + "\n".join(bad))
sys.exit(1 if bad else 0)
