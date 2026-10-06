#!/usr/bin/env python3
"""Verify tracked bytes, Git modes and stage-zero index against raw commit trees."""
import hashlib
import os
from pathlib import Path
import stat
import subprocess
import sys

repo = Path(sys.argv[1]).resolve()
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")
required = {"protocol-processor", "gptp-processor", "third_party/verilog-axis"}

def git(root, *args):
    return subprocess.check_output(["rtk", "proxy", "git", "-c", "core.commitGraph=false", *args], cwd=root, env=env)

def verify(root, revision, label):
    assert git(root, "rev-parse", "HEAD").decode().strip() == revision
    raw = git(root, "ls-tree", "-rz", revision)
    entries = {}
    for row in raw.split(b"\0"):
        if not row:
            continue
        meta, name = row.split(b"\t", 1)
        mode, kind, oid = meta.split()
        entries[name] = (mode, oid)
    index = {}
    for row in git(root, "ls-files", "--stage", "-z").split(b"\0"):
        if not row:
            continue
        meta, name = row.split(b"\t", 1)
        mode, oid, stage = meta.split()
        assert stage == b"0" and name not in index
        index[name] = (mode, oid)
    assert entries == index, label + " index differs from tree"
    blobs = 0
    links = []
    for name, (mode, oid) in entries.items():
        path = root / os.fsdecode(name)
        if mode == b"160000":
            links.append((path, oid.decode(), os.fsdecode(name)))
            continue
        info = path.lstat()
        if mode == b"120000":
            assert stat.S_ISLNK(info.st_mode)
            content = os.fsencode(os.readlink(path))
        else:
            assert mode in (b"100644", b"100755") and stat.S_ISREG(info.st_mode)
            assert bool(info.st_mode & 0o111) == (mode == b"100755"), os.fsdecode(name)
            content = path.read_bytes()
        digest = hashlib.sha1(b"blob " + str(len(content)).encode() + b"\0" + content).hexdigest()
        assert digest == oid.decode(), label + ":" + os.fsdecode(name)
        blobs += 1
    print("PASS", label, "head", revision, "tracked_blobs", blobs,
          "index_entries", len(index), "tree_modes_and_raw_bytes_equal")
    for path, pin, name in links:
        if (path / ".git").exists():
            verify(path, pin, label + "/" + name)
        else:
            assert label != "candidate" or name not in required
            print("PIN ONLY", label + "/" + name, pin, "uninitialized optional submodule; no execution claimed")

verify(repo, "72d3780d23a0b96362f8ae64059311b866ff5776", "candidate")
print("PASS all required initialized submodules verified, including index and raw tracked bytes")
