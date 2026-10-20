#!/usr/bin/env python3
"""Verify raw working bytes, executable modes, index entries and populated gitlinks."""
import hashlib
import os
from pathlib import Path
import stat
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
env = os.environ.copy()
env["GIT_NO_REPLACE_OBJECTS"] = "1"
def git(where, *args):
    return subprocess.check_output(["git", "-C", str(where), *args], env=env)

def verify(where, rev, label):
    records = git(where, "ls-tree", "-rz", rev).split(b"\0")
    expected = {}
    links = []
    for record in filter(None, records):
        meta, name = record.split(b"\t", 1)
        mode, kind, oid = meta.split()
        expected[name] = (mode, oid, b"0")
        file = where / os.fsdecode(name)
        if kind == b"commit":
            links.append((name, oid))
            continue
        info = file.lstat()
        if mode == b"120000":
            assert stat.S_ISLNK(info.st_mode), (label, name, "not symlink")
            data = os.fsencode(os.readlink(file))
        else:
            assert stat.S_ISREG(info.st_mode), (label, name, "not regular")
            assert bool(info.st_mode & 0o111) == (mode == b"100755"), (label, name, "mode")
            data = file.read_bytes()
        actual = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest().encode()
        assert actual == oid, (label, name, "bytes")
    index = {}
    for record in filter(None, git(where, "ls-files", "-sz").split(b"\0")):
        meta, name = record.split(b"\t", 1)
        mode, oid, stage = meta.split()
        assert name not in index, (label, name, "duplicate index stage")
        index[name] = (mode, oid, stage)
    assert index == expected, (label, "index differs from tree")
    print(label, "PASS", len(expected), "entries: raw blob bytes, modes and stage-0 index")
    return links

head = git(root, "rev-parse", "HEAD").decode().strip()
assert head == "75db4b57cff47bb614d14dead084649a4c2aa2a3"
print("head", head)
print("tree", git(root, "rev-parse", "HEAD^{tree}").decode().strip())
for name, pin in verify(root, head, "superproject"):
    sub = root / os.fsdecode(name)
    if name == b"external" and not (sub / ".git").exists():
        print("external", pin.decode(), "gitlink verified; legacy optional checkout uninitialized")
        continue
    assert (sub / ".git").is_file(), (name, "not a registered submodule")
    assert git(sub, "rev-parse", "HEAD").strip() == pin, (name, "pin mismatch")
    print("gitlink", os.fsdecode(name), pin.decode())
    verify(sub, pin.decode(), os.fsdecode(name))
assert git(root, "status", "--porcelain", "--untracked-files=no") == b""
print("RESTORATION PASS: source checkout unchanged")
