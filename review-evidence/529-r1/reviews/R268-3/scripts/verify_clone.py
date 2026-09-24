#!/usr/bin/env python3
"""Verify a review clone is exactly its HEAD: HEAD/tree ids, index records
equal to the HEAD tree records, every tracked blob's worktree bytes and mode
(hashed as git blobs, symlinks by target), no untracked/ignored/modified
residue, and each gitlink's submodule at its pinned commit with a clean
worktree (an uninitialized submodule is reported as such).
usage: verify_clone.py CLONE EXPECT_HEAD EXPECT_TREE"""
import hashlib, os, stat, subprocess, sys
c, eh, et = sys.argv[1:4]
def g(*a, cwd=c):
    return subprocess.run(["git", *a], cwd=cwd, capture_output=True, text=True, check=True).stdout
bad = 0
head, tree = g("rev-parse", "HEAD").strip(), g("rev-parse", "HEAD^{tree}").strip()
print("HEAD", head, "OK" if head == eh else "MISMATCH"); bad += head != eh
print("tree", tree, "OK" if tree == et else "MISMATCH"); bad += tree != et
ls_tree = {}
for l in g("ls-tree", "-r", "-z", "HEAD").split("\0"):
    if l:
        meta, path = l.split("\t", 1); mode, typ, oid = meta.split()
        ls_tree[path] = (mode, oid)
idx = {}
for l in g("ls-files", "-s", "-z").split("\0"):
    if l:
        meta, path = l.split("\t", 1); mode, oid, st = meta.split()
        idx[path] = (mode, oid)
print("index records == HEAD tree records:", idx == ls_tree); bad += idx != ls_tree
blobs = mism = 0
for path, (mode, oid) in ls_tree.items():
    if mode == "160000":
        continue
    blobs += 1
    fp = os.path.join(c, path)
    st_ = os.lstat(fp)
    if mode == "120000":
        data = os.readlink(fp).encode(); okm = stat.S_ISLNK(st_.st_mode)
    else:
        data = open(fp, "rb").read()
        okm = stat.S_ISREG(st_.st_mode) and (bool(st_.st_mode & 0o111) == (mode == "100755"))
    h = hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()
    if h != oid or not okm:
        mism += 1; print("  MISMATCH", path)
print("tracked blobs %d, byte/mode mismatches %d" % (blobs, mism)); bad += mism
res = g("status", "--porcelain", "--ignored", "--untracked-files=all")
print("status --porcelain --ignored lines:", len(res.splitlines())); bad += bool(res.strip())
for path, (mode, oid) in ls_tree.items():
    if mode != "160000":
        continue
    sub = os.path.join(c, path)
    if not os.path.exists(os.path.join(sub, ".git")):
        print("gitlink %s %s: submodule not initialized (not required)" % (path, oid)); continue
    sh = g("rev-parse", "HEAD", cwd=sub).strip()
    dirty = g("status", "--porcelain", "--ignored", cwd=sub).strip()
    ok = sh == oid and not dirty
    print("gitlink %s mode 160000 pin %s at %s clean=%s %s" % (path, oid, sh, not dirty, "OK" if ok else "BAD"))
    bad += not ok
print("RESULT", "CLEAN" if bad == 0 else "NOT CLEAN (%d)" % bad)
sys.exit(1 if bad else 0)
