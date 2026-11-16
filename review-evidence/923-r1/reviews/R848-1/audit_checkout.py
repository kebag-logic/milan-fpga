#!/usr/bin/env python3
"""Audit tracked working bytes, executable modes, index and required gitlinks."""
import hashlib
import os
from pathlib import Path
import stat
import subprocess
import sys

repo = Path(sys.argv[1]).resolve()
head = "70c100da36330bb3862d76fa6eb003091775f310"
tree = "9be8e9f218622a0e65053d6b99cf0b54dce2eae0"
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")
def git(root, *args):
    return subprocess.check_output(["git", *args], cwd=root, env=env)

def audit(root, expected):
    actual = git(root, "rev-parse", "HEAD").decode().strip()
    assert actual == expected, (root, actual, expected)
    index = {}
    for item in git(root, "ls-files", "--stage", "-z").split(b"\0"):
        if item:
            meta, name = item.split(b"\t", 1)
            mode, oid, stage = meta.split()
            assert stage == b"0", (name, stage)
            index[name] = (mode, oid)
    checked = 0
    expected_index = {}
    for item in git(root, "ls-tree", "-rz", "HEAD").split(b"\0"):
        if not item:
            continue
        meta, name = item.split(b"\t", 1)
        mode, kind, oid = meta.split()
        expected_index[name] = (mode, oid)
        path = root / os.fsdecode(name)
        if kind == b"commit":
            if name == b"external":
                print("UNINITIALIZED optional external gitlink", oid.decode(), "index verified")
                continue
            print("REQUIRED gitlink", path.relative_to(repo), oid.decode())
            audit(path, oid.decode())
            continue
        info = path.lstat()
        if mode == b"120000":
            assert stat.S_ISLNK(info.st_mode), path
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(info.st_mode), path
            actual_mode = b"100755" if info.st_mode & 0o111 else b"100644"
            assert actual_mode == mode, (path, actual_mode, mode)
            data = path.read_bytes()
        digest = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        assert digest == oid.decode(), (path, digest, oid)
        checked += 1
    assert index == expected_index, "index differs from HEAD tree: " + str(root)
    status = git(root, "status", "--porcelain=v1", "--untracked-files=all")
    assert not status, (root, status)
    print("PASS", root.name, actual, "tracked blobs", checked, "bytes/modes/index clean")

assert git(repo, "rev-parse", "HEAD^{tree}").decode().strip() == tree
audit(repo, head)
print("PASS exact published head/tree and all required submodule gitlinks")
