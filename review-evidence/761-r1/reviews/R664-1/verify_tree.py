#!/usr/bin/env python3
"""Verify raw tracked bytes, modes, index entries and required submodule pins."""
import hashlib
import os
from pathlib import Path
import stat
import subprocess
import sys

source = Path(sys.argv[1]).resolve()
head = "4191b0987d1313abc86c747ad6a9c3c0963f17da"
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")

def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], env=env)

def verify(root, revision, label):
    entries = git(root, "ls-tree", "-rz", revision).split(b"\0")
    expected_index = {}
    count = 0
    links = {}
    for entry in filter(None, entries):
        meta, name = entry.split(b"\t", 1)
        mode, kind, oid = meta.split()
        expected_index[name] = (mode, oid, b"0")
        p = root / os.fsdecode(name)
        if kind == b"commit":
            links[os.fsdecode(name)] = oid.decode()
            continue
        info = p.lstat()
        if mode == b"120000":
            assert stat.S_ISLNK(info.st_mode), (label, name, "not symlink")
            data = os.fsencode(os.readlink(p))
        else:
            assert stat.S_ISREG(info.st_mode), (label, name, "not regular")
            actual_mode = b"100755" if info.st_mode & 0o111 else b"100644"
            assert actual_mode == mode, (label, name, "mode differs")
            data = p.read_bytes()
        actual = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest().encode()
        assert actual == oid, (label, name, "raw blob differs")
        count += 1
    actual_index = {}
    for entry in filter(None, git(root, "ls-files", "--stage", "-z").split(b"\0")):
        meta, name = entry.split(b"\t", 1)
        mode, oid, stage = meta.split()
        assert name not in actual_index, (label, name, "duplicate index entry")
        actual_index[name] = (mode, oid, stage)
    assert actual_index == expected_index, (label, "index differs from commit")
    assert git(root, "rev-parse", "HEAD").decode().strip() == revision
    print(label, revision, "raw_blobs", count, "modes PASS index PASS")
    return links

assert git(source, "rev-parse", "HEAD^{tree}").decode().strip() == "5c21b067fcad3e7ff7017190f088c7ae0528b807"
links = verify(source, head, "root")
for name in ("protocol-processor", "gptp-processor", "third_party/verilog-axis", "third_party/lwSRP", "third_party/tsn-c-stack"):
    p = source / name
    assert not p.is_symlink()
    assert (p / ".git").is_file(), (name, "not registered submodule checkout")
    verify(p, links[name], name)
status = git(source, "status", "--porcelain=v1", "--untracked-files=all")
assert not status, status
print("required gitlinks PASS; unused external gitlink retained; clean worktree PASS")
