#!/usr/bin/env python3
"""Compare tracked bytes, executable modes, index entries and submodule pins.
Usage: python3 verify_checkout.py REPOSITORY
"""
import hashlib, os, stat, subprocess, sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args])
def verify(repo, head, label):
    assert git(repo, "rev-parse", "HEAD").decode().strip() == head
    tree = {}
    for row in git(repo, "ls-tree", "-rz", head).split(b"\0"):
        if not row: continue
        meta, name = row.split(b"\t", 1)
        mode, kind, oid = meta.split()
        tree[name] = (mode, oid)
    index = {}
    for row in git(repo, "ls-files", "--stage", "-z").split(b"\0"):
        if not row: continue
        meta, name = row.split(b"\t", 1)
        mode, oid, stage = meta.split()
        assert stage == b"0", name
        index[name] = (mode, oid)
    assert index == tree, label + " index differs"
    links = []
    count = 0
    for name, (mode, oid) in tree.items():
        path = repo / os.fsdecode(name)
        if mode == b"160000":
            links.append((path, oid.decode(), os.fsdecode(name)))
            continue
        st = path.lstat()
        if mode == b"120000":
            assert stat.S_ISLNK(st.st_mode), name
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(st.st_mode), name
            assert bool(st.st_mode & 0o111) == (mode == b"100755"), name
            data = path.read_bytes()
        digest = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        assert digest == oid.decode(), name
        count += 1
    print(f"PASS {label}: {count} tracked blobs, modes and full index match {head}; {len(links)} gitlinks")
    for path, pin, name in links:
        if (path/".git").exists():
            print(f"PIN {label}/{name}: {pin}")
            verify(path, pin, label + "/" + name)
        else:
            assert name == "external", "required submodule absent: " + name
            print(f"OPTIONAL {label}/{name}: {pin}, uninitialized")
verify(root, "01fc54756f1ffb0a3aa836681215e8321ee7e86c", "candidate")
assert not git(root, "status", "--porcelain", "--untracked-files=all").strip()
print("PASS: clean checkout; no tracked or untracked source changes")
