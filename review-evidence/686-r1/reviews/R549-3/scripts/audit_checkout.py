#!/usr/bin/env python3
"""Prove tracked bytes, modes, index and required submodule pins independently of status."""
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
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")
head = "9c601b5983acfd60fb269b9a88c27b48cab7cf65"
tree = "d2337a496fb13813beb2f4a13aefcaca0e0a94db"
required = {"protocol-processor", "gptp-processor", "third_party/verilog-axis"}

def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], env=env)

def audit(root, commit, label):
    entries = git(root, "ls-tree", "-rz", commit).split(b"\0")
    expected_index = []
    blobs = 0
    links = []
    for entry in entries:
        if not entry:
            continue
        header, name = entry.split(b"\t", 1)
        mode, kind, oid = header.split()
        expected_index.append(mode + b" " + oid + b" 0\t" + name)
        path = root / os.fsdecode(name)
        if kind == b"commit":
            links.append((os.fsdecode(name), oid.decode()))
            continue
        s = path.lstat()
        if mode == b"120000":
            assert stat.S_ISLNK(s.st_mode), (label, str(name), "kind")
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(s.st_mode), (label, str(name), "kind")
            assert bool(s.st_mode & 0o111) == (mode == b"100755"), (label, str(name), "mode")
            data = path.read_bytes()
        actual = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        assert actual == oid.decode(), (label, str(name), "bytes")
        blobs += 1
    actual_index = git(root, "ls-files", "--stage", "-z").rstrip(b"\0").split(b"\0")
    assert sorted(actual_index) == sorted(expected_index), (label, "index differs")
    assert git(root, "rev-parse", "HEAD").decode().strip() == commit
    return dict(repository=label, commit=commit, tracked_blobs=blobs,
                bytes_modes_index="PASS", gitlinks=dict(links))

repo = a.repo.resolve()
assert git(repo, "rev-parse", "HEAD^{tree}").decode().strip() == tree
results = [audit(repo, head, "root")]
for name, pin in results[0]["gitlinks"].items():
    if name in required:
        results.append(audit(repo / name, pin, name))
assert required <= set(results[0]["gitlinks"])
delta = git(repo, "diff", "--name-only", "48f12dc1", head).decode().splitlines()
assert delta == ["docs/design/MAAP_FABRIC.md"]
print(json.dumps(dict(head=head, tree=tree, results=results, round3_changed_paths=delta,
                     unused_external="uninitialized; excluded by repository's required-submodule contract"), indent=2))
