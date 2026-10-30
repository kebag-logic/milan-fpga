#!/usr/bin/env python3
"""Verify a checkout against its commit: every tracked blob's bytes and mode,
stage-0 index entries with no hidden flags, and the expected gitlinks.

Usage: python3 -I verify_tree.py <checkout> <commit> [<path>=<sha> ...]
"""
import hashlib, os, stat, subprocess, sys
from pathlib import Path

root, commit = Path(sys.argv[1]), sys.argv[2]
want_links = dict(a.split("=", 1) for a in sys.argv[3:])
git = lambda *a: subprocess.run(["git", "-C", str(root), *a], check=True, capture_output=True).stdout
fail = []
tree = {}
for rec in git("ls-tree", "-r", "-z", "--full-tree", commit).split(b"\0"):
    if rec:
        meta, path = rec.split(b"\t", 1)
        mode, kind, sha = meta.split()
        tree[path.decode()] = (mode.decode(), kind.decode(), sha.decode())
index = {}
for rec in git("ls-files", "-s", "-z").split(b"\0"):
    if rec:
        meta, path = rec.split(b"\t", 1)
        mode, sha, stage = meta.split()
        index[path.decode()] = (mode.decode(), sha.decode(), stage.decode())
flags = [l for l in git("ls-files", "-v").decode().splitlines() if not l.startswith("H ")]
if flags: fail.append(f"index entries with hidden flags: {flags[:5]}")
if set(index) != set(tree): fail.append(f"index/tree path sets differ: {sorted(set(index) ^ set(tree))[:5]}")
blobs = links = 0
for path, (mode, kind, sha) in tree.items():
    ix = index.get(path)
    if ix and (ix[0] != mode or ix[1] != sha or ix[2] != "0"):
        fail.append(f"index entry {path}: {ix} vs {mode} {sha}")
    full = root / path
    if kind == "commit":
        links += 1
        if path in want_links and want_links[path] != sha:
            fail.append(f"gitlink {path}: {sha} != expected {want_links[path]}")
        continue
    st = os.lstat(full)
    if mode == "120000":
        data = os.readlink(full).encode()
        ok_mode = stat.S_ISLNK(st.st_mode)
    else:
        data = full.read_bytes()
        ok_mode = stat.S_ISREG(st.st_mode) and bool(st.st_mode & 0o100) == (mode == "100755")
    if not ok_mode: fail.append(f"mode {path}: {oct(st.st_mode)} vs {mode}")
    h = hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()
    if h != sha: fail.append(f"bytes {path}: {h} vs {sha}")
    blobs += 1
for p in want_links:
    if p not in tree: fail.append(f"expected gitlink {p} absent")
head = git("rev-parse", "HEAD").decode().strip()
if head != git("rev-parse", commit + "^{commit}").decode().strip(): fail.append(f"HEAD {head} is not {commit}")
untracked = git("status", "--porcelain", "--ignored", "--untracked-files=all").decode().splitlines()
untracked = [u for u in untracked if not u.endswith("/")]
print(f"HEAD {head}; {blobs} blobs and {links} gitlinks checked; status lines {untracked[:10]}")
for f in fail: print("FAIL", f)
print("RESULT:", "PASS" if not fail else f"{len(fail)} FAIL")
sys.exit(1 if fail else 0)
