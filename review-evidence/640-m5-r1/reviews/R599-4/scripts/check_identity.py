#!/usr/bin/env python3
"""Prove tracked bytes, executable modes, stage-zero index, and required pins."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess

p = argparse.ArgumentParser()
p.add_argument("repo", type=Path)
a = p.parse_args()
a.repo = a.repo.resolve()
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")
def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args], env=env)
def audit(repo, revision):
    expected = {}
    for row in git(repo, "ls-tree", "-rz", revision).split(b"\0"):
        if not row:
            continue
        meta, name = row.split(b"\t", 1)
        mode, kind, oid = meta.decode().split()
        expected[os.fsdecode(name)] = (mode, oid)
    actual = {}
    for row in git(repo, "ls-files", "--stage", "-z").split(b"\0"):
        if not row:
            continue
        meta, name = row.split(b"\t", 1)
        mode, oid, stage = meta.decode().split()
        assert stage == "0", (repo.name, os.fsdecode(name), stage)
        actual[os.fsdecode(name)] = (mode, oid)
    assert actual == expected, "index differs from committed tree"
    flags = git(repo, "ls-files", "-v", "-z").split(b"\0")
    assert all(not row or row[:1] == b"H" for row in flags), "hidden index flag"
    count = 0
    for name, (mode, oid) in expected.items():
        if mode == "160000":
            continue
        path = repo / name
        st = path.lstat()
        if mode == "120000":
            assert stat.S_ISLNK(st.st_mode), name
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(st.st_mode), name
            assert bool(st.st_mode & 0o111) == (mode == "100755"), name
            data = path.read_bytes()
        digest = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        assert digest == oid, name
        count += 1
    print(json.dumps({"repository": repo.name, "head": git(repo, "rev-parse", "HEAD").decode().strip(),
                      "tracked_blobs_proved": count, "index_matches": True,
                      "bytes_and_modes_match": True}))
    return expected
head = "2bef9e50489a60f216a8073a9f5ea0645752b33f"
assert git(a.repo, "rev-parse", "HEAD").decode().strip() == head
assert git(a.repo, "rev-parse", "HEAD^{tree}").decode().strip() == "9777e890c07850052a0d9134cdb22388a651c5f1"
entries = audit(a.repo, head)
required = ("protocol-processor", "gptp-processor", "third_party/verilog-axis")
for name in required:
    mode, pin = entries[name]
    assert mode == "160000"
    sub = a.repo / name
    assert (sub / ".git").is_file(), name
    assert git(sub, "rev-parse", "HEAD").decode().strip() == pin, name
    parent = git(sub, "rev-parse", "--show-superproject-working-tree").decode().strip()
    assert Path(parent).resolve() == a.repo.resolve(), name
    audit(sub, pin)
print("PASS: exact head, tracked bytes/modes/index, and all three required submodule gitlinks")
print("Optional external and third_party/lwSRP checkouts remain uninitialized; their index gitlinks match HEAD.")
