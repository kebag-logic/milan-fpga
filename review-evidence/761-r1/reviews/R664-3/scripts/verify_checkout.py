#!/usr/bin/env python3
"""Verify raw tracked bytes, modes, index and populated required gitlinks."""
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

def audit(where, rev):
    entries = git(where, "ls-tree", "-rz", rev).split(b"\0")
    expected = {}
    count = 0
    links = []
    for entry in filter(None, entries):
        meta, name = entry.split(b"\t", 1)
        mode, kind, oid = meta.split()
        expected[name] = (mode, oid, b"0")
        path = where / os.fsdecode(name)
        if kind == b"commit":
            links.append((os.fsdecode(name), oid.decode()))
            continue
        st = path.lstat()
        if mode == b"120000":
            assert stat.S_ISLNK(st.st_mode), name
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(st.st_mode), name
            assert bool(st.st_mode & 0o111) == (mode == b"100755"), name
            data = path.read_bytes()
        actual = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        assert actual == oid.decode(), f"blob mismatch: {name!r}"
        count += 1
    index = {}
    for entry in filter(None, git(where, "ls-files", "--stage", "-z").split(b"\0")):
        meta, name = entry.split(b"\t", 1)
        mode, oid, stage = meta.split()
        assert name not in index, f"unmerged: {name!r}"
        index[name] = mode, oid, stage
    assert index == expected, "index differs from commit tree"
    label = "." if where == root else str(where.relative_to(root))
    print(f"PASS {label}: {count} blobs, raw bytes/modes/index equal {rev}")
    return dict(links)

head = git(root, "rev-parse", "HEAD").decode().strip()
assert head == "d30a208d44d5868cc356e6a8b7abc89b062ca9bd"
tree = git(root, "rev-parse", "HEAD^{tree}").decode().strip()
assert tree == "d203767adbab4025cbfb3f760540783f65cc2e6c"
print(f"HEAD {head}\nTREE {tree}")
links = audit(root, head)
required = ["protocol-processor", "gptp-processor", "third_party/verilog-axis", "third_party/tsn-c-stack"]
for name in required + ["third_party/lwSRP"]:
    sub = root / name
    assert not sub.is_symlink()
    assert (sub / ".git").is_file(), f"not an initialized submodule: {name}"
    assert git(sub, "rev-parse", "HEAD").decode().strip() == links[name]
    owner = Path(git(sub, "rev-parse", "--show-superproject-working-tree").decode().strip())
    assert owner.resolve() == root
    audit(sub, links[name])
print("external gitlink retained; external remains uninitialized and is not a gate input")
assert not git(root, "status", "--porcelain", "--untracked-files=all").strip()
print("PASS parent status clean; no tracked-byte restoration needed")
