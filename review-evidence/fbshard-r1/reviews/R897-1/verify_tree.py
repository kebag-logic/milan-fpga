#!/usr/bin/env python3
"""Verify tracked bytes, executable modes, index entries and required gitlinks."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
expected = "b7b351935f65416c8632c21dd13e08fb2e9c1d9c"
required = ("gptp-processor", "protocol-processor", "third_party/lwSRP", "third_party/tsn-c-stack", "third_party/verilog-axis")
def git(where, *args):
    return subprocess.check_output(["git", "-C", str(where), *args])
def check(where, rev):
    assert git(where, "rev-parse", "HEAD").decode().strip() == rev
    entries = {}
    links = {}
    for row in git(where, "ls-tree", "-rz", rev).split(b"\0"):
        if not row:
            continue
        metadata, name = row.split(b"\t", 1)
        mode, kind, oid = metadata.split()
        path = where / os.fsdecode(name)
        entries[name] = (mode, oid)
        if kind == b"commit":
            links[os.fsdecode(name)] = oid.decode()
            continue
        info = path.lstat()
        if mode == b"120000":
            assert stat.S_ISLNK(info.st_mode), name
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(info.st_mode), name
            assert bool(info.st_mode & 0o111) == (mode == b"100755"), name
            data = path.read_bytes()
        actual = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest().encode()
        assert actual == oid, os.fsdecode(name)
    index = {}
    for row in git(where, "ls-files", "--stage", "-z").split(b"\0"):
        if not row:
            continue
        metadata, name = row.split(b"\t", 1)
        mode, oid, stage = metadata.split()
        assert stage == b"0"
        index[name] = (mode, oid)
    assert index == entries, "index differs from pinned tree"
    for row in git(where, "ls-files", "-v", "-z").split(b"\0"):
        if row:
            assert row[:1] == b"H", "index skip/assume-unchanged flag"
    return {"commit": rev, "tree": git(where, "rev-parse", "HEAD^{tree}").decode().strip(), "entries": len(entries), "gitlinks": links, "bytes_modes_index": "PASS"}

result = {"root": check(root, expected)}
assert result["root"]["tree"] == "bcebbd36ca937a68b9323f962711c42f80e4ccdd"
for name in required:
    pin = result["root"]["gitlinks"][name]
    result[name] = check(root / name, pin)
print(json.dumps(result, indent=2))
