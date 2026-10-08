#!/usr/bin/env python3
"""Verify bytes/modes/index against exact Git trees, including public dependencies."""
import argparse
import hashlib
import os
from pathlib import Path
import stat
import subprocess

p = argparse.ArgumentParser()
p.add_argument("root", type=Path)
a = p.parse_args()
env = {**os.environ, "GIT_NO_REPLACE_OBJECTS": "1", "GIT_OPTIONAL_LOCKS": "0"}

def git(root, *words):
    return subprocess.check_output(["git", "-C", str(root), *words], env=env)

def verify(root, rev, name):
    assert git(root, "rev-parse", "HEAD").decode().strip() == rev
    assert not git(root, "for-each-ref", "--format=%(refname)", "refs/replace")
    entries = []
    for row in git(root, "ls-tree", "-rz", rev).split(b"\0"):
        if not row:
            continue
        meta, path = row.split(b"\t", 1)
        mode, kind, oid = meta.split()
        entries.append((mode, kind, oid, path))
    expected_index = {path: (mode, oid, b"0") for mode, kind, oid, path in entries}
    actual_index = {}
    for row in git(root, "ls-files", "--stage", "-z").split(b"\0"):
        if not row:
            continue
        meta, path = row.split(b"\t", 1)
        assert path not in actual_index
        actual_index[path] = tuple(meta.split())
    assert actual_index == expected_index, name + " index mismatch"
    files = 0
    submodules = []
    for mode, kind, oid, path in entries:
        target = root / os.fsdecode(path)
        if mode == b"160000":
            submodules.append((target, oid.decode(), os.fsdecode(path)))
            continue
        info = target.lstat()
        if mode == b"120000":
            assert stat.S_ISLNK(info.st_mode)
            data = os.fsencode(os.readlink(target))
        else:
            assert stat.S_ISREG(info.st_mode), os.fsdecode(path)
            actual_mode = b"100755" if info.st_mode & 0o111 else b"100644"
            assert actual_mode == mode, os.fsdecode(path)
            data = target.read_bytes()
        actual = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        assert actual == oid.decode(), os.fsdecode(path)
        files += 1
    print(f"PASS {name}: {rev}; {files} tracked blob bytes/modes; index equals tree")
    for target, pin, label in submodules:
        print(f"gitlink {label} {pin}")
    return submodules

root = a.root.resolve()
assert git(root, "rev-parse", "HEAD^{tree}").decode().strip() == "1452e3d48865f09739432b92608401371257dfb1"
subs = verify(root, "fe1cd0679f5028c749af7242c903a82ca2b3d692", "superproject")
for target, pin, label in subs:
    if label == "external":
        print("LIMIT external intentionally not initialized or executed")
        continue
    if not (target / ".git").exists():
        assert target.is_dir() and not any(target.iterdir()), label + " has unregistered contents"
        print(f"LIMIT {label} uninitialized and empty; superproject tree/index gitlink verified; no dependency execution claimed")
        continue
    assert (target / ".git").is_file(), label + " is not a registered submodule"
    verify(target, pin, label)
assert not git(root, "status", "--porcelain=v1", "--untracked-files=normal", "--ignored")
print("PASS final status empty; candidate source and index unchanged")
