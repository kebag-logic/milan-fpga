#!/usr/bin/env python3
"""Verify tracked bytes, kinds, modes, index and required submodule pins."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
ap = argparse.ArgumentParser()
ap.add_argument("repo", type=Path)
a = ap.parse_args()
repo = a.repo.resolve()
HEAD = "7bc7ceca6ba1dd1a268d6fa1704613bb141487fe"
TREE = "70ee92ab909f37d435caa0b94daab84bff83d60d"
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")
def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], env=env)
def verify(root, revision):
    entries = git(root, "ls-tree", "-rz", "--full-tree", revision).split(b"\0")
    index = {}
    for row in git(root, "ls-files", "--stage", "-z").split(b"\0"):
        if row:
            meta, name = row.split(b"\t", 1)
            mode, oid, stage = meta.split()
            assert stage == b"0", name
            assert name not in index, name
            index[name] = (mode, oid)
    expected = {}
    count = 0
    submodules = {}
    for row in entries:
        if not row: continue
        meta, name = row.split(b"\t", 1)
        mode, kind, oid = meta.split()
        expected[name] = (mode, oid)
        if mode == b"160000":
            submodules[os.fsdecode(name)] = oid.decode()
            continue
        path = root / os.fsdecode(name)
        st = path.lstat()
        if mode == b"120000":
            assert stat.S_ISLNK(st.st_mode), name
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(st.st_mode), name
            executable = bool(st.st_mode & 0o111)
            assert executable == (mode == b"100755"), name
            data = path.read_bytes()
        digest = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        assert digest == oid.decode(), name
        count += 1
    assert index == expected, "index differs from tree"
    return count, submodules
assert git(repo, "rev-parse", "HEAD").decode().strip() == HEAD
assert git(repo, "rev-parse", "HEAD^{tree}").decode().strip() == TREE
count, pins = verify(repo, HEAD)
print(json.dumps({"head":HEAD,"tree":TREE,"parent_blobs_verified":count,"index":"exact"}))
for name in ("protocol-processor", "gptp-processor", "third_party/verilog-axis"):
    root = repo / name
    assert not root.is_symlink()
    assert Path(git(root, "rev-parse", "--show-toplevel").decode().strip()).resolve() == root
    assert (root / ".git").is_file(), "required submodule is not registered"
    actual = git(root, "rev-parse", "HEAD").decode().strip()
    assert actual == pins[name], name
    total, _ = verify(root, actual)
    print(json.dumps({"submodule":name,"gitlink":actual,"blobs_verified":total,"index":"exact"}))
print("PASS: tracked blob bytes, modes, kinds, index and required gitlinks match the review head")
