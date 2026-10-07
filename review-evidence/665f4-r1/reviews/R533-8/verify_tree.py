#!/usr/bin/env python3
"""Verify committed bytes, modes, index and required direct submodule pins.

Run from the isolated candidate checkout. This bypasses status/index hiding
flags for the filesystem comparison and ignores replacement objects.
"""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess

HEAD = "a6e6916826448f81de2b779ca61a87a9f8c47278"
TREE = "819d9290c443690487fbc8123765a14a5ba4535e"
REQUIRED = {"protocol-processor", "gptp-processor", "third_party/lwSRP",
            "third_party/verilog-axis"}
env = {**os.environ, "GIT_NO_REPLACE_OBJECTS": "1"}

def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], env=env)

def check(root, revision):
    assert git(root, "rev-parse", "HEAD").decode().strip() == revision
    entries = {}
    count = 0
    for record in git(root, "ls-tree", "-rz", revision).split(b"\0"):
        if not record:
            continue
        meta, raw_path = record.split(b"\t", 1)
        mode, kind, oid = meta.decode().split()
        name = os.fsdecode(raw_path)
        entries[name] = (mode, oid)
        if kind != "blob":
            continue
        path = root / name
        actual = path.lstat()
        if mode == "120000":
            assert stat.S_ISLNK(actual.st_mode), name
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(actual.st_mode), name
            expected_mode = "100755" if actual.st_mode & 0o111 else "100644"
            assert mode == expected_mode, (name, mode, expected_mode)
            data = path.read_bytes()
        measured = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        assert measured == oid, (name, measured, oid)
        count += 1
    index = {}
    for record in git(root, "ls-files", "--stage", "-z").split(b"\0"):
        if not record:
            continue
        meta, raw_path = record.split(b"\t", 1)
        mode, oid, stage = meta.decode().split()
        assert stage == "0", record
        index[os.fsdecode(raw_path)] = (mode, oid)
    assert index == entries, "index differs from committed entries"
    flags = git(root, "ls-files", "-v", "-z").split(b"\0")
    assert all(not row or row[:1] == b"H" for row in flags), "hidden index flags"
    assert not git(root, "status", "--porcelain=v1", "--untracked-files=all"), "dirty status"
    return entries, count

root = Path.cwd().resolve()
assert git(root, "rev-parse", "HEAD^{tree}").decode().strip() == TREE
entries, count = check(root, HEAD)
result = {"head": HEAD, "tree": TREE, "root_verified_blobs": count,
          "index": "exact committed entries; no hidden flags",
          "status": "clean, including untracked files", "submodules": {}}
for name in sorted(REQUIRED):
    mode, oid = entries[name]
    assert mode == "160000"
    subroot = root / name
    assert git(subroot, "rev-parse", "--show-toplevel").decode().strip() == str(subroot)
    assert git(subroot, "rev-parse", "--show-superproject-working-tree").decode().strip() == str(root)
    _, count = check(subroot, oid)
    result["submodules"][name] = {"pin": oid, "verified_blobs": count}
print(json.dumps(result, indent=2))
