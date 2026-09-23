#!/usr/bin/env python3
"""Verify a review clone is byte-for-byte at the exact head: HEAD and tree,
index == HEAD, every tracked non-gitlink blob's on-disk bytes and executable
bit, the gitlink pins, and no untracked or ignored files.
Usage: restore_verify.py <clone> <expected head> <expected tree>
"""
import os, stat, subprocess, sys

repo, head, tree = sys.argv[1:4]
g = lambda *a, **k: subprocess.run(["git", "-C", repo, *a], check=True, capture_output=True, text=True, **k).stdout
print("HEAD", g("rev-parse", "HEAD").strip(), "expected", head)
print("tree", g("rev-parse", "HEAD^{tree}").strip(), "index tree", g("write-tree").strip(), "expected", tree)
idx = [l.split(None, 3) for l in g("ls-files", "-s").splitlines()]
links = [(m, o, p) for m, o, _s, p in idx if m == "160000"]
files = [(m, o, p) for m, o, _s, p in idx if m != "160000"]
for m, o, p in links:
    print("gitlink", m, o, p)
disk = g("hash-object", "--no-filters", "--stdin-paths", input="\n".join(p for _m, _o, p in files) + "\n").split()
bad = 0
for (m, o, p), h in zip(files, disk):
    st = os.lstat(os.path.join(repo, p))
    ok = stat.S_ISLNK(st.st_mode) if m == "120000" else (
        stat.S_ISREG(st.st_mode) and bool(st.st_mode & 0o111) == (m == "100755"))
    if h != o or not ok:
        bad += 1
        print("MISMATCH", m, p)
extra = g("status", "--porcelain=v1", "--ignored", "--untracked-files=all").splitlines()
print("tracked blobs", len(files), "mismatches", bad, "status lines", len(extra))
print("RESULT", "PASS" if bad == 0 and not extra and g("rev-parse", "HEAD").strip() == head
      and g("write-tree").strip() == tree else "FAIL")
