"""Verify a checkout is byte-exact at a commit: index entries equal the commit's tree (mode and blob),
every tracked regular file's bytes hash to its blob, symlinks point where the blob says, no index entry is
flagged assume-unchanged or skip-worktree, the status is empty, and each named submodule's checked-out head
equals its gitlink.

Usage: python3 -I verify_checkout.py <repo> <commit> <submodule>...
"""
import os
import subprocess
import sys

repo, commit, subs = sys.argv[1], sys.argv[2], sys.argv[3:]
git = lambda *a: subprocess.run(["git", "-C", repo, *a], capture_output=True, text=True, check=True).stdout
head = git("rev-parse", "HEAD").strip()
tree = git("rev-parse", "HEAD^{tree}").strip()
print("head", head, "tree", tree, "match", head == commit)
want = {}
for line in git("ls-tree", "-r", "--full-tree", commit).splitlines():
    meta, path = line.split("\t", 1)
    mode, kind, obj = meta.split()
    want[path] = (mode, obj)
index = {}
for line in git("ls-files", "-s").splitlines():
    meta, path = line.split("\t", 1)
    mode, obj, stage = meta.split()
    index[path] = (mode, obj)
print("index==tree", index == want, len(index))
flags = [l for l in git("ls-files", "-v").splitlines() if l[:1] not in ("H",)]
print("flagged index entries", len(flags), flags[:5])
bad = []
for path, (mode, obj) in want.items():
    full = os.path.join(repo, path)
    if mode == "160000":
        continue
    if mode == "120000":
        target = os.readlink(full)
        blob = subprocess.run(["git", "-C", repo, "cat-file", "blob", obj], capture_output=True).stdout.decode()
        if target != blob:
            bad.append(path)
        continue
    got = subprocess.run(["git", "-C", repo, "hash-object", "--no-filters", full], capture_output=True,
                         text=True).stdout.strip()
    exe = os.access(full, os.X_OK)
    if got != obj or exe != (mode == "100755"):
        bad.append(path)
print("byte/mode mismatches", len(bad), bad[:5])
print("status", repr(git("status", "--porcelain", "--ignore-submodules=none")))
for s in subs:
    link = want[s][1]
    try:
        h = subprocess.run(["git", "-C", os.path.join(repo, s), "rev-parse", "HEAD"], capture_output=True,
                           text=True).stdout.strip()
    except Exception as e:  # noqa: BLE001
        h = str(e)
    print("submodule", s, link, h, "match", link == h)
