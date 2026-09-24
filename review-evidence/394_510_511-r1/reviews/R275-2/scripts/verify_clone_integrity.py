#!/usr/bin/env python3
"""Prove a checkout still holds the exact reviewed head, byte for byte.

Checks: HEAD and tree ids; index == HEAD tree (mode, object id, stage 0, path);
no assume-unchanged / skip-worktree flags; every tracked regular file and
symlink hashes (git hash-object --no-filters) to its index blob; mode bits of
regular files agree with 100644/100755; no untracked or ignored paths; and the
required submodules are gitlinks at stage 0 whose checkouts sit exactly at
the gitlink commit with a clean status.
Usage: verify_clone_integrity.py <checkout> <expected-head> <expected-tree> <submodule>...
"""
import os
import stat
import subprocess
import sys

repo, want_head, want_tree, *subs = sys.argv[1:]
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")


def git(*args, cwd=repo):
    return subprocess.run(["git", *args], cwd=cwd, env=env, check=True,
                          capture_output=True).stdout


fail = []
head = git("rev-parse", "HEAD").decode().strip()
tree = git("rev-parse", "HEAD^{tree}").decode().strip()
print(f"HEAD {head} tree {tree}")
if head != want_head:
    fail.append(f"HEAD {head} != {want_head}")
if tree != want_tree:
    fail.append(f"tree {tree} != {want_tree}")

tree_ent = {}
for rec in git("ls-tree", "-r", "-z", "--full-tree", "HEAD").split(b"\0"):
    if rec:
        meta, path = rec.split(b"\t", 1)
        mode, _typ, oid = meta.split()
        tree_ent[path] = (mode, oid)
idx_ent = {}
for rec in git("ls-files", "-s", "-z").split(b"\0"):
    if rec:
        meta, path = rec.split(b"\t", 1)
        mode, oid, stage = meta.split()
        if stage != b"0":
            fail.append(f"unmerged stage {stage} at {path!r}")
        idx_ent[path] = (mode, oid)
if idx_ent != tree_ent:
    diff = set(idx_ent.items()) ^ set(tree_ent.items())
    fail.append(f"index != HEAD tree ({len(diff)} differing entries)")
print(f"index entries {len(idx_ent)} == tree entries {len(tree_ent)}: {idx_ent == tree_ent}")

nonH =[l for l in git("ls-files", "-v", "-z").split(b"\0") if l and l[:2] != b"H "]
if nonH:
    fail.append(f"{len(nonH)} index entries carry non-H flags, e.g. {nonH[:3]}")
print(f"non-H ls-files -v flags: {len(nonH)}")

checked = 0
for path, (mode, oid) in sorted(idx_ent.items()):
    p = os.path.join(repo.encode(), path)
    if mode == b"160000":
        continue
    try:
        st = os.lstat(p)
    except FileNotFoundError:
        fail.append(f"missing {path!r}")
        continue
    if mode == b"120000":
        if not stat.S_ISLNK(st.st_mode):
            fail.append(f"not a symlink {path!r}")
            continue
        got = subprocess.run(["git", "hash-object", "--stdin"], input=os.readlink(p),
                             env=env, capture_output=True, check=True).stdout.strip()
    else:
        if not stat.S_ISREG(st.st_mode):
            fail.append(f"not a regular file {path!r}")
            continue
        exe = bool(st.st_mode & 0o100)
        if exe != (mode == b"100755"):
            fail.append(f"mode bit mismatch {path!r} index {mode.decode()} exec={exe}")
        got = git("hash-object", "--no-filters", "--", path.decode("utf-8", "surrogateescape")).strip()
    if got != oid:
        fail.append(f"bytes differ {path!r}")
    checked += 1
print(f"tracked non-gitlink paths hashed: {checked}")

extra = git("status", "--porcelain=v1", "--ignored", "--untracked-files=all",
            "--ignore-submodules=none", "-z").split(b"\0")
extra = [e for e in extra if e]
if extra:
    fail.append(f"status not empty: {extra[:5]}")
print(f"status entries (incl. ignored/untracked/submodule): {len(extra)}")

for sub in subs:
    ent = idx_ent.get(sub.encode())
    if not ent or ent[0] != b"160000":
        fail.append(f"{sub}: not a stage-0 gitlink")
        continue
    pin = ent[1].decode()
    sp = os.path.join(repo, sub)
    shead = git("rev-parse", "HEAD", cwd=sp).decode().strip()
    top = git("rev-parse", "--show-toplevel", cwd=sp).decode().strip()
    sst = git("status", "--porcelain=v1", "--ignored", "--untracked-files=all", cwd=sp)
    ok = shead == pin and os.path.realpath(top) == os.path.realpath(sp) and not sst.strip()
    print(f"submodule {sub}: gitlink {pin} checkout {shead} toplevel-ok "
          f"{os.path.realpath(top) == os.path.realpath(sp)} clean {not sst.strip()}")
    if not ok:
        fail.append(f"{sub}: checkout/status mismatch")

print("RESULT", "PASS" if not fail else "FAIL")
for f in fail:
    print("  FAIL", f)
sys.exit(0 if not fail else 1)
