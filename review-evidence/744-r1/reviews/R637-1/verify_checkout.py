#!/usr/bin/env python3
"""Verify committed tree, index, tracked bytes/modes and required submodule pins."""
import argparse
import hashlib
import os
from pathlib import Path
import stat
import subprocess

ap = argparse.ArgumentParser()
ap.add_argument("repository", type=Path)
a = ap.parse_args()
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")

def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], env=env)

def verify(root, expected):
    head = git(root, "rev-parse", "HEAD").decode().strip()
    assert head == expected, (root.name, head, expected)
    entries = {}
    links = {}
    for row in git(root, "ls-tree", "-rz", "--full-tree", expected).split(b"\0"):
        if not row:
            continue
        header, path = row.split(b"\t", 1)
        mode, kind, oid = header.split()
        entries[path] = (mode, oid, b"0")
        f = root / os.fsdecode(path)
        if kind == b"commit":
            links[os.fsdecode(path)] = oid.decode()
            continue
        st = f.lstat()
        if mode == b"120000":
            assert stat.S_ISLNK(st.st_mode), path
            raw = os.fsencode(os.readlink(f))
        else:
            assert stat.S_ISREG(st.st_mode), path
            assert bool(st.st_mode & 0o111) == (mode == b"100755"), path
            raw = f.read_bytes()
        digest = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest().encode()
        assert digest == oid, (path, "working blob differs")
    index = {}
    for row in git(root, "ls-files", "--stage", "-z").split(b"\0"):
        if not row:
            continue
        header, path = row.split(b"\t", 1)
        assert path not in index, (path, "multiple index entries")
        index[path] = tuple(header.split())
    assert index == entries, "index/tree mismatch"
    print(f"PASS {root.name}: HEAD {head}; {len(entries)-len(links)} tracked blobs exact; modes and index exact; {len(links)} gitlinks")
    return links

root = a.repository.resolve()
head = "f643377f15c0d939d875ae5698672f1b0a99a644"
assert git(root, "rev-parse", "HEAD^{tree}").decode().strip() == "3e77395e26cb6216d0908fbec71cec87421d826f"
links = verify(root, head)
for name in ("protocol-processor", "gptp-processor", "third_party/verilog-axis", "third_party/tsn-c-stack", "third_party/lwSRP"):
    sub = root / name
    assert sub.is_dir() and not sub.is_symlink()
    assert (sub / ".git").is_file() and not (sub / ".git").is_symlink()
    assert git(sub, "rev-parse", "--show-superproject-working-tree").decode().strip() == str(root)
    verify(sub, links[name])
print("external is inactive and uninitialized; its superproject gitlink/index were checked.")
print("Runner SHA-256 " + hashlib.sha256((root / "scripts/act_ci.py").read_bytes()).hexdigest())
print("PASS final tracked byte/mode/index and required-submodule verification")
