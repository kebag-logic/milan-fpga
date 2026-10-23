#!/usr/bin/env python3
"""Verify exact raw tracked bytes, executable modes, index and gitlinks."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

HEAD = "cf1ca87529b4c1a9d6ba7acbf691b626e15bae9e"
TREE = "e4d84bf05d153298aeec0b15dc887aa16efef744"
PREV = "24a292a0321df6f3516f25cb6e92e24fb1988e65"
PINS = {
    "third_party/lwSRP": "08ee86e812a0eb5e1dc6cd61b494d8baf3491348",
    "gptp-processor": "55680bff3b287b9a7b0c759f51471fa617c17335",
    "protocol-processor": "93fb0b2d736b36588ea7321e25fba2f8819ea41f",
    "third_party/tsn-c-stack": "70936b77dc41981e192438388cd0aced69954f18",
    "third_party/verilog-axis": "48ff7a7e2ef782cf778d47910cf85835c64b1bce",
}
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")
root = Path(sys.argv[1]).resolve()
def git(where, *args):
    return subprocess.check_output(["git", "-C", str(where), *args], env=env)
def tree(where, rev):
    out = {}
    for record in git(where, "ls-tree", "-rz", rev).split(b"\0"):
        if record:
            meta, name = record.split(b"\t", 1)
            mode, kind, oid = meta.split()
            out[name] = (mode, kind, oid)
    return out
def verify(where, rev):
    entries = tree(where, rev)
    expected_index = {}
    count = 0
    for name, (mode, kind, oid) in entries.items():
        expected_index[name] = (mode, oid, b"0")
        if kind == b"commit":
            continue
        p = where / os.fsdecode(name)
        s = p.lstat()
        if mode == b"120000":
            assert stat.S_ISLNK(s.st_mode), os.fsdecode(name)
            data = os.fsencode(os.readlink(p))
        else:
            assert stat.S_ISREG(s.st_mode), os.fsdecode(name)
            assert bool(s.st_mode & 0o111) == (mode == b"100755"), os.fsdecode(name)
            data = p.read_bytes()
        digest = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest().encode()
        assert digest == oid, os.fsdecode(name)
        count += 1
    actual_index = {}
    for record in git(where, "ls-files", "--stage", "-z").split(b"\0"):
        if record:
            meta, name = record.split(b"\t", 1)
            assert name not in actual_index
            actual_index[name] = tuple(meta.split())
    assert actual_index == expected_index, "Index does not match commit"
    return count
assert git(root, "rev-parse", "HEAD").decode().strip() == HEAD
assert git(root, "rev-parse", "HEAD^{tree}").decode().strip() == TREE
assert git(root, "rev-parse", "HEAD^").decode().strip() == PREV
before, after = tree(root, PREV), tree(root, HEAD)
changed = [os.fsdecode(n) for n in before.keys() | after.keys() if before.get(n) != after.get(n)]
assert changed == ["docs/reference/REGISTER_MAP.md"], changed
results = {"head": HEAD, "tree": TREE, "previous": PREV, "changed": changed,
           "root_verified_blobs": verify(root, HEAD), "submodules": {}}
for name, pin in PINS.items():
    assert after[name.encode()] == (b"160000", b"commit", pin.encode())
    sub = root / name
    assert (sub / ".git").is_file() and not sub.is_symlink()
    assert git(sub, "rev-parse", "HEAD").decode().strip() == pin
    assert Path(git(sub, "rev-parse", "--show-superproject-working-tree").decode().strip()).resolve() == root
    results["submodules"][name] = {"pin": pin, "verified_blobs": verify(sub, pin)}
results["result"] = "PASS: raw bytes, modes, complete stage-zero index, registered pins"
print(json.dumps(results, indent=2))
