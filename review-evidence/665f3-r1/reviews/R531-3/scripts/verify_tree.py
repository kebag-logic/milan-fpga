#!/usr/bin/env python3
"""Verify raw tracked bytes, executable modes, index records, and required submodule pins."""
import hashlib
import os
from pathlib import Path
import stat
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")
def git(where, *args):
    return subprocess.check_output(["git", "-C", str(where), *args], env=env)

def verify(where, rev):
    records = git(where, "ls-tree", "-rz", rev).split(b"\0")
    expected = []
    links = []
    count = 0
    digest = hashlib.sha256()
    for rec in filter(None, records):
        meta, path = rec.split(b"\t", 1)
        mode, kind, oid = meta.split()
        expected.append(mode + b" " + oid + b" 0\t" + path)
        target = where / os.fsdecode(path)
        if kind == b"commit":
            links.append((path, oid))
            continue
        st = target.lstat()
        if mode == b"120000":
            assert stat.S_ISLNK(st.st_mode), path
            data = os.fsencode(os.readlink(target))
        else:
            assert stat.S_ISREG(st.st_mode), path
            assert bool(st.st_mode & 0o111) == (mode == b"100755"), path
            data = target.read_bytes()
        hashed = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest().encode()
        assert hashed == oid, path
        digest.update(mode + b" " + path + b"\0" + hashed + b"\n")
        count += 1
    index = list(filter(None, git(where, "ls-files", "--stage", "-z").split(b"\0")))
    assert sorted(index) == sorted(expected), "index differs from committed tree"
    print("root" if where == root else where.relative_to(root), "blobs", count, "raw-byte-and-mode digest", digest.hexdigest(), "index PASS")
    return links

head = git(root, "rev-parse", "HEAD").decode().strip()
assert head == "abb3a78a12c29ff13ee7f71a00b387a6c91dc361"
tree = git(root, "rev-parse", "HEAD^{tree}").decode().strip()
assert tree == "d85f5361950dbf3f8deff0d45f4cb4fe7ff1e7fd"
print("HEAD", head, "TREE", tree)
links = verify(root, head)
required = {b"protocol-processor", b"gptp-processor", b"third_party/verilog-axis"}
for path, oid in links:
    print("gitlink", os.fsdecode(path), oid.decode())
    if path in required:
        sub = root / os.fsdecode(path)
        assert git(sub, "rev-parse", "HEAD").strip() == oid
        assert (sub / ".git").is_file()
        verify(sub, oid.decode())
print("PASS: exact bytes, modes, index and required gitlinks")
