#!/usr/bin/env python3
"""Prove disk blob bytes/modes, index tree, HEAD, and required gitlinks."""
import hashlib
import os
from pathlib import Path
import stat
import subprocess
import sys

HEAD = "27433e47c6d7805376547a91b418cf6aa9d95d2a"
TREE = "b8eed7686df2a3a1980ac68f3667da45451e5e3b"
repo = Path(sys.argv[1]).resolve()
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")
def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], env=env)
def verify(root, rev, label):
    assert git(root, "rev-parse", "HEAD").decode().strip() == rev, label
    expected = git(root, "rev-parse", rev + "^{tree}").decode().strip()
    assert git(root, "write-tree").decode().strip() == expected, label + " index"
    count = 0
    links = {}
    for row in git(root, "ls-tree", "-rz", rev).split(b"\0"):
        if not row:
            continue
        meta, name = row.split(b"\t", 1)
        mode, kind, oid = meta.decode().split()
        path = root / os.fsdecode(name)
        if mode == "160000":
            links[os.fsdecode(name)] = oid
            continue
        st = path.lstat()
        if mode == "120000":
            assert stat.S_ISLNK(st.st_mode), name
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(st.st_mode), name
            assert bool(st.st_mode & 0o111) == (mode == "100755"), name
            data = path.read_bytes()
        digest = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        assert digest == oid, name
        count += 1
    print(f"{label}: HEAD {rev}; index {expected}; {count} disk blobs and modes verified")
    return links
assert git(repo, "rev-parse", "HEAD^{tree}").decode().strip() == TREE
links = verify(repo, HEAD, "candidate")
for name in ("protocol-processor", "gptp-processor", "third_party/verilog-axis"):
    assert git(repo / name, "rev-parse", "--show-superproject-working-tree").decode().strip() == str(repo)
    verify(repo / name, links[name], name)
print("PASS: exact candidate bytes, modes, index and required gitlinks")
