#!/usr/bin/env python3
"""Verify tracked bytes, modes, index and required gitlinks without status shortcuts."""
import hashlib
import os
from pathlib import Path
import stat
import subprocess
import sys

HEAD = "a27808375427859dc357f6bfd0a88842062b20ed"
TREE = "5519813ecda9827ba2f30a15ede5aa9e66bc4bea"
REQUIRED = {"protocol-processor", "gptp-processor", "third_party/verilog-axis"}
ENV = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], env=ENV)


def verify(root, revision, label):
    entries = {}
    for record in git(root, "ls-tree", "-rz", "--full-tree", revision).split(b"\0"):
        if not record:
            continue
        meta, name = record.split(b"\t", 1)
        mode, kind, oid = meta.decode().split()
        entries[os.fsdecode(name)] = (mode, kind, oid)
    expected_index = {n: (v[0], v[2], "0") for n, v in entries.items()}
    actual_index = {}
    for record in git(root, "ls-files", "--stage", "-z").split(b"\0"):
        if record:
            meta, name = record.split(b"\t", 1)
            key = os.fsdecode(name)
            assert key not in actual_index, (label, key, "multiple stages")
            actual_index[key] = tuple(meta.decode().split())
    assert actual_index == expected_index, (label, "index mismatch")
    hidden = [r for r in git(root, "ls-files", "-v", "-z").split(b"\0") if r and r[:1] != b"H"]
    assert not hidden, (label, "index flags", hidden)
    count = 0
    for name, (mode, kind, oid) in entries.items():
        path = root / name
        if kind == "commit":
            if label == "." and name in REQUIRED:
                assert not path.is_symlink()
                assert git(path, "rev-parse", "HEAD").decode().strip() == oid
                assert git(path, "rev-parse", "--show-superproject-working-tree").strip()
                verify(path, oid, name)
            print(f"gitlink {label}/{name} {oid}" + (" required verified" if name in REQUIRED else " index/tree retained"))
            continue
        st = path.lstat()
        if mode == "120000":
            assert stat.S_ISLNK(st.st_mode), (label, name, "symlink type")
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(st.st_mode), (label, name, "regular type")
            actual_mode = "100755" if st.st_mode & 0o111 else "100644"
            assert mode == actual_mode, (label, name, "mode")
            data = path.read_bytes()
        digest = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        assert digest == oid, (label, name, "blob bytes")
        count += 1
    print(f"PASS {label}: {count} tracked blobs; modes, bytes, index and flags exact")


root = Path(sys.argv[1]).resolve()
assert git(root, "rev-parse", "HEAD").decode().strip() == HEAD
assert git(root, "rev-parse", "HEAD^{tree}").decode().strip() == TREE
print("head", HEAD)
print("tree", TREE)
verify(root, HEAD, ".")
print("untracked", git(root, "ls-files", "--others", "--exclude-standard").decode().strip() or "none")
