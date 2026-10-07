#!/usr/bin/env python3
"""Verify raw tracked bytes, modes, index and required submodule pins."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

ROOT = Path(sys.argv[1]).resolve()
ENV = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")

def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], env=ENV)

def verify(root, revision):
    records = git(root, "ls-tree", "-rz", revision).split(b"\0")
    expected = []
    blobs = 0
    links = {}
    for record in filter(None, records):
        metadata, raw_path = record.split(b"\t", 1)
        mode, kind, oid = metadata.split()
        path = os.fsdecode(raw_path)
        expected.append(mode + b" " + oid + b" 0\t" + raw_path)
        if kind == b"commit":
            links[path] = oid.decode()
            continue
        full = root / path
        st = full.lstat()
        if mode == b"120000":
            assert stat.S_ISLNK(st.st_mode), path
            data = os.fsencode(os.readlink(full))
        else:
            assert stat.S_ISREG(st.st_mode), path
            assert bool(st.st_mode & 0o111) == (mode == b"100755"), path
            data = full.read_bytes()
        digest = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        assert digest == oid.decode(), path
        blobs += 1
    actual = git(root, "ls-files", "--stage", "-z").split(b"\0")
    assert sorted(filter(None, actual)) == sorted(expected), "index differs from committed tree"
    assert git(root, "diff", "--no-ext-diff", "--no-textconv", revision) == b""
    return {"head": revision, "blobs_verified": blobs, "index": "exact", "gitlinks": links}

head = git(ROOT, "rev-parse", "HEAD").decode().strip()
assert head == "853a7357ba86d758a0e38f65db89a6187fb547bc"
result = {"superproject": verify(ROOT, head), "submodules": {}}
for path in ("third_party/verilog-axis", "protocol-processor", "gptp-processor"):
    child = ROOT / path
    assert (child / ".git").is_file() and not child.is_symlink()
    pin = result["superproject"]["gitlinks"][path]
    assert git(child, "rev-parse", "HEAD").decode().strip() == pin
    assert Path(git(child, "rev-parse", "--show-superproject-working-tree").decode().strip()) == ROOT
    result["submodules"][path] = verify(child, pin)
result["tree"] = git(ROOT, "rev-parse", "HEAD^{tree}").decode().strip()
assert result["tree"] == "78af3f0b2ca316ad2b14440ff7bd4d64ca322bd2"
result["status"] = git(ROOT, "status", "--porcelain=v1").decode()
assert not result["status"]
print(json.dumps(result, indent=2))
