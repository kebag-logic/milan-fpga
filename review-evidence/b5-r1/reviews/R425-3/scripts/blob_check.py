#!/usr/bin/env python3
"""Hash every tracked file's on-disk bytes as a blob and compare with HEAD's tree,
including mode.  Usage: blob_check.py <repo>"""
import hashlib, os, stat, subprocess, sys
repo = sys.argv[1]
out = subprocess.run(["git", "-C", repo, "ls-tree", "-r", "-z", "HEAD"], capture_output=True, check=True).stdout
bad = n = links = 0
for rec in out.split(b"\0"):
    if not rec:
        continue
    meta, path = rec.split(b"\t", 1); mode, typ, oid = meta.decode().split()
    p = os.path.join(repo.encode(), path)
    if typ == "commit":
        links += 1; continue
    n += 1
    st = os.lstat(p)
    if mode == "120000":
        data = os.readlink(p); ok_mode = stat.S_ISLNK(st.st_mode)
    else:
        data = open(p, "rb").read(); ok_mode = stat.S_ISREG(st.st_mode) and (bool(st.st_mode & 0o100) == (mode == "100755"))
    h = hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()
    if h != oid or not ok_mode:
        bad += 1; print("MISMATCH", mode, path.decode())
print(f"tracked blobs {n}, gitlinks {links}, mismatched bytes or mode {bad}")
