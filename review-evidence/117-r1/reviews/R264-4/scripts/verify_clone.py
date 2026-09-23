#!/usr/bin/env python3
"""Verify a clone is at exact head bytes: HEAD and tree ids, index equals the
HEAD tree, every tracked regular file and symlink hashes to its index blob
with its index mode, no assume-unchanged/skip-worktree flag, gitlinks at stage
0 with the expected ids, and no untracked or ignored file.
usage: verify_clone.py <clone> <head> <tree> <path=gitlink>..."""
import os
import stat
import subprocess
import sys

clone, head, tree = sys.argv[1:4]
want = dict(a.split("=") for a in sys.argv[4:])


def git(*a, inp=None):
    return subprocess.run(["git", "-C", clone, *a], input=inp, capture_output=True, check=True).stdout


bad = []
if git("rev-parse", "HEAD").decode().strip() != head:
    bad.append("HEAD")
if git("rev-parse", "HEAD^{tree}").decode().strip() != tree:
    bad.append("HEAD tree")
if git("write-tree").decode().strip() != tree:
    bad.append("index tree")
flags = [l for l in git("ls-files", "-v").decode().splitlines() if l[:1] != "H"]
if flags:
    bad.append(f"index flags {len(flags)}")
n = 0
paths, blobs, modes = [], [], []
for rec in git("ls-files", "-s", "-z").split(b"\0"):
    if not rec:
        continue
    meta, path = rec.split(b"\t", 1)
    mode, sha, stage = meta.decode().split()
    path = path.decode()
    if stage != "0":
        bad.append(f"stage {stage} {path}")
    if mode == "160000":
        if want.get(path) != sha:
            bad.append(f"gitlink {path} {sha}")
        continue
    full = os.path.join(clone, path)
    st = os.lstat(full)
    if mode == "120000":
        if not stat.S_ISLNK(st.st_mode):
            bad.append(f"not symlink {path}")
    else:
        exe = bool(st.st_mode & 0o100)
        if not stat.S_ISREG(st.st_mode) or (mode == "100755") != exe:
            bad.append(f"mode {path}")
    paths.append(path)
    blobs.append(sha)
    n += 1
got = git("hash-object", "--no-filters", "--stdin-paths", inp="\n".join(os.path.join(clone, p) for p in paths).encode()).decode().split()
# symlinks: hash the link target text as git does
for i, p in enumerate(paths):
    full = os.path.join(clone, p)
    if os.path.islink(full):
        got[i] = git("hash-object", "--stdin", inp=os.readlink(full).encode()).decode().strip()
mism = [p for p, a, b in zip(paths, blobs, got) if a != b]
bad += [f"bytes {p}" for p in mism]
missing = set(want) - {l.split(b"\t")[1].decode() for l in git("ls-files", "-s", "-z").split(b"\0") if l.startswith(b"160000")}
bad += [f"missing gitlink {m}" for m in missing]
extra = git("status", "--porcelain", "--ignored", "--untracked-files=all").decode().strip()
if extra:
    bad.append("untracked/ignored/modified: " + extra.replace("\n", "; ")[:300])
print(f"tracked non-gitlink entries verified: {n}; gitlinks checked: {len(want)}")
print("RESULT", "PASS" if not bad else "FAIL: " + " | ".join(bad[:20]))
