#!/usr/bin/env python3
"""Verify tracked bytes, executable modes, index entries and required gitlinks."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess

p = argparse.ArgumentParser()
p.add_argument("root", type=Path)
p.add_argument("--head", default="d40e4e9827be2516f8f34b9d65f0a483fff2194c")
a = p.parse_args()
root = a.root.resolve()
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")
def git(repo, *words):
    return subprocess.check_output(["git", "-C", str(repo), *words], env=env)

def verify(repo, head):
    actual = git(repo, "rev-parse", "HEAD").decode().strip()
    assert actual == head, (repo, actual, head)
    expected = {}
    for item in git(repo, "ls-tree", "-rz", head).split(b"\0"):
        if not item:
            continue
        meta, name = item.split(b"\t", 1)
        mode, kind, oid = meta.decode().split()
        expected[os.fsdecode(name)] = (mode, kind, oid)
    index = {}
    for item in git(repo, "ls-files", "--stage", "-z").split(b"\0"):
        if not item:
            continue
        meta, name = item.split(b"\t", 1)
        mode, oid, stage = meta.decode().split()
        assert stage == "0", (name, stage)
        key = os.fsdecode(name)
        assert key not in index
        index[key] = (mode, oid)
    assert index == {n:(m,o) for n,(m,k,o) in expected.items()}, "index does not equal head tree"
    count = 0
    links = {}
    for name, (mode, kind, oid) in expected.items():
        path = repo / name
        if kind == "commit":
            links[name] = oid
            continue
        st = path.lstat()
        if mode == "120000":
            assert stat.S_ISLNK(st.st_mode), name
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(st.st_mode), name
            assert ("100755" if st.st_mode & stat.S_IXUSR else "100644") == mode, name
            data = path.read_bytes()
        held = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        assert held == oid, (name, held, oid)
        count += 1
    return {"head":actual,"tree":git(repo,"rev-parse","HEAD^{tree}").decode().strip(),"blobs_verified":count,"gitlinks":links}

result = {"parent":verify(root,a.head)}
for name in ("protocol-processor","gptp-processor","third_party/verilog-axis","third_party/lwSRP","third_party/tsn-c-stack"):
    result[name] = verify(root/name,result["parent"]["gitlinks"][name])
print(json.dumps(result,indent=2))
print("PASS: exact tracked blob bytes, Git modes, index and five required submodule gitlinks")
