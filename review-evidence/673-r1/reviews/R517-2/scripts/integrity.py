#!/usr/bin/env python3
"""Prove tracked disk bytes, executable modes, index and required gitlinks."""
import hashlib
import os
from pathlib import Path
import stat
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")
expected = "793dcd3f7867d85f8c1f5c9ef2b04dc9c2d9c5df"

def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args], env=env)

def verify(repo, revision, label):
    assert git(repo, "rev-parse", "HEAD").decode().strip() == revision
    entries = {}
    for record in git(repo, "ls-tree", "-rz", "--full-tree", revision).split(b"\0"):
        if record:
            meta, name = record.split(b"\t", 1)
            mode, kind, oid = meta.split()
            entries[name] = (mode, kind, oid)
    index = {}
    for record in git(repo, "ls-files", "--stage", "-z").split(b"\0"):
        if record:
            meta, name = record.split(b"\t", 1)
            mode, oid, stage = meta.split()
            assert stage == b"0", (label, name, stage)
            assert name not in index
            index[name] = (mode, oid)
    assert index == {n: (m, o) for n, (m, k, o) in entries.items()}, label
    count = 0
    for name, (mode, kind, oid) in entries.items():
        if kind == b"commit":
            continue
        path = repo / os.fsdecode(name)
        metadata = path.lstat()
        if mode == b"120000":
            assert stat.S_ISLNK(metadata.st_mode), (label, name)
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(metadata.st_mode), (label, name)
            assert bool(metadata.st_mode & stat.S_IXUSR) == (mode == b"100755"), (label, name)
            data = path.read_bytes()
        actual = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest().encode()
        assert actual == oid, (label, name, "blob mismatch")
        count += 1
    print(f"PASS {label}: head={revision}; {count} tracked blob bytes/modes; all index records match")
    return entries

entries = verify(root, expected, "root")
assert git(root, "rev-parse", "HEAD^{tree}").decode().strip() == "4044003424303525864889c45788aeb8a48c8501"
assert subprocess.run(["git", "-C", str(root), "symbolic-ref", "-q", "HEAD"],
                      stdout=subprocess.DEVNULL).returncode == 1
for name in ("protocol-processor", "gptp-processor", "third_party/verilog-axis"):
    mode, kind, oid = entries[name.encode()]
    assert (mode, kind) == (b"160000", b"commit")
    sub = root / name
    assert (sub / ".git").is_file(), name
    assert Path(git(sub, "rev-parse", "--show-superproject-working-tree").decode().strip()).resolve() == root
    verify(sub, oid.decode(), name)
print("PASS: exact detached head/tree; required registered gitlinks and checked-out bytes match")
print("external: unused gitlink retained, checkout uninitialized (not required)")
