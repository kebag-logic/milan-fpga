#!/usr/bin/env python3
"""Compare raw tracked bytes, types, modes and index with committed trees."""
import argparse
import hashlib
import os
from pathlib import Path
import stat
import subprocess

p = argparse.ArgumentParser()
p.add_argument("root", type=Path)
a = p.parse_args()
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")
def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], env=env)
def audit(root, revision):
    records = git(root, "ls-tree", "-rz", revision).split(b"\0")
    wanted, counts = {}, {"blobs": 0, "gitlinks": 0}
    for record in filter(None, records):
        meta, rawname = record.split(b"\t", 1)
        mode, kind, oid = meta.split()
        wanted[rawname] = (mode, oid, b"0")
        if kind == b"commit":
            counts["gitlinks"] += 1
            continue
        path = root / os.fsdecode(rawname)
        st = path.lstat()
        if mode == b"120000":
            assert stat.S_ISLNK(st.st_mode), rawname
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(st.st_mode), rawname
            data = path.read_bytes()
            assert bool(st.st_mode & 0o111) == (mode == b"100755"), rawname
        digest = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest().encode()
        assert digest == oid, (rawname, digest, oid)
        counts["blobs"] += 1
    observed = {}
    for record in filter(None, git(root, "ls-files", "--stage", "-z").split(b"\0")):
        meta, name = record.split(b"\t", 1)
        mode, oid, stage = meta.split()
        assert name not in observed, name
        observed[name] = (mode, oid, stage)
    assert wanted == observed, "index differs from committed tree"
    print(root.name, revision, counts, "bytes/modes/index PASS")
root = a.root.resolve()
head = git(root, "rev-parse", "HEAD").decode().strip()
assert head == "7ddbbdc9be73728b239718c8976261c7e0ad0563"
tree = git(root, "rev-parse", "HEAD^{tree}").decode().strip()
assert tree == "a1813edb60d34073859f67b388a1e10d76cc86c3"
print("HEAD", head, "TREE", tree)
audit(root, head)
for name in ("protocol-processor", "gptp-processor", "third_party/verilog-axis"):
    meta = git(root, "ls-tree", "HEAD", "--", name).split(b"\t", 1)[0].split()
    assert meta[:2] == [b"160000", b"commit"]
    pin = meta[2].decode()
    sub = root / name
    assert git(sub, "rev-parse", "HEAD").decode().strip() == pin
    assert git(sub, "rev-parse", "--show-superproject-working-tree").decode().strip() == str(root)
    audit(sub, pin)
print("Required submodule gitlinks and populations PASS; optional external remains uninitialized.")
print(git(root, "status", "--porcelain=v1", "--untracked-files=normal").decode(), end="")
