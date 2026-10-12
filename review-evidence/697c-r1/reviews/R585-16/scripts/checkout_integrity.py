"""Verify a checkout equals its HEAD: every tracked file's bytes hash to its index blob, modes match, index == HEAD,
gitlinks equal HEAD's and (where initialised) the submodule checkout's HEAD.

Usage: python3 -I checkout_integrity.py <checkout>
"""
import hashlib
import os
import stat
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()


def git(*a, cwd=root):
    return subprocess.run(["git", *a], cwd=cwd, capture_output=True, check=True).stdout


head = git("rev-parse", "HEAD").decode().strip()
tree = git("rev-parse", "HEAD^{tree}").decode().strip()
print(f"HEAD {head} tree {tree}")
print(f"status porcelain lines (submodules included): {len(git('status', '--porcelain', '--ignore-submodules=none').splitlines())}")
print(f"index tree == HEAD tree: {git('write-tree').decode().strip() == tree}")
files = bad = 0
links = []
for entry in filter(None, git("ls-files", "-s", "-z").split(b"\0")):
    meta, path = entry.split(b"\t", 1)
    mode, oid, stage = meta.decode().split()
    p = root / os.fsdecode(path)
    if mode == "160000":
        links.append((os.fsdecode(path), oid))
        continue
    files += 1
    st = os.lstat(p)
    data = os.readlink(p).encode() if stat.S_ISLNK(st.st_mode) else p.read_bytes()
    got = hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()
    want_mode = "120000" if stat.S_ISLNK(st.st_mode) else ("100755" if st.st_mode & stat.S_IXUSR else "100644")
    if got != oid or want_mode != mode or stage != "0":
        bad += 1
        print(f"MISMATCH {os.fsdecode(path)}: index {mode} {oid} stage {stage}, disk {want_mode} {got}")
print(f"tracked files hashed from their bytes: {files}, mismatches (bytes, mode or stage): {bad}")
for path, oid in links:
    in_head = git("rev-parse", f"HEAD:{path}").decode().strip()
    try:
        out = git("rev-parse", "HEAD", cwd=root / path).decode().strip()
        top = git("rev-parse", "--show-toplevel", cwd=root / path).decode().strip()
        checkout = out if Path(top).resolve() == (root / path).resolve() else "uninitialised"
    except subprocess.CalledProcessError:
        checkout = "uninitialised"
    print(f"gitlink {path}: index {oid} HEAD {in_head} checkout {checkout} "
          f"{'OK' if oid == in_head and checkout in (oid, 'uninitialised') else 'MISMATCH'}")
sys.exit(1 if bad else 0)
