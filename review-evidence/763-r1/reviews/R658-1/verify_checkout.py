#!/usr/bin/env python3
"""Verify raw working bytes, executable modes, staged entries and required gitlinks."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess

p = argparse.ArgumentParser()
p.add_argument("repo", type=Path)
p.add_argument("packet", type=Path)
a = p.parse_args()
repo, packet = a.repo.resolve(), a.packet.resolve()
head = "07c6c72fce79e705bcf28a70071497d0ce7040e4"
tree = "c70d7afe29d34724474bfc05053fe3cb43801026"
required = ("protocol-processor", "gptp-processor", "third_party/lwSRP",
            "third_party/tsn-c-stack", "third_party/verilog-axis")

def git(root, *args):
    return subprocess.check_output(["git", *args], cwd=root)

def verify(root, revision):
    entries = {}
    for row in git(root, "ls-tree", "-rz", revision).split(b"\0"):
        if not row:
            continue
        left, name = row.split(b"\t", 1)
        mode, kind, oid = left.decode().split()
        entries[name.decode()] = (mode, kind, oid)
    index = {}
    for row in git(root, "ls-files", "--stage", "-z").split(b"\0"):
        if not row:
            continue
        left, name = row.split(b"\t", 1)
        mode, oid, stage = left.decode().split()
        assert stage == "0", name
        index[name.decode()] = (mode, oid)
    assert index == {name: (v[0], v[2]) for name, v in entries.items()}
    checked = 0
    for name, (mode, kind, oid) in entries.items():
        if kind == "commit":
            continue
        path = root / name
        s = path.lstat()
        if mode == "120000":
            assert stat.S_ISLNK(s.st_mode), name
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(s.st_mode), name
            assert bool(s.st_mode & 0o111) == (mode == "100755"), name
            data = path.read_bytes()
        actual = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        assert actual == oid, name
        checked += 1
    return entries, checked

assert git(repo, "rev-parse", "HEAD").decode().strip() == head
assert git(repo, "rev-parse", "HEAD^{tree}").decode().strip() == tree
entries, count = verify(repo, head)
result = {"head": head, "tree": tree, "raw_parent_blobs_verified": count,
          "index_matches_head": True, "bytes_and_modes_match": True, "submodules": []}
for name in required:
    oid = entries[name][2]
    assert git(repo / name, "rev-parse", "HEAD").decode().strip() == oid
    _, subcount = verify(repo / name, oid)
    result["submodules"].append({"path": name, "gitlink": oid,
                                  "raw_blobs_verified": subcount, "index_matches_head": True})
result["unused_uninitialized_external_gitlink"] = entries["external"][2]
result["status_porcelain"] = git(repo, "status", "--porcelain=v1", "--untracked-files=all").decode()
assert not result["status_porcelain"]
(packet / "checkout-integrity.json").write_text(json.dumps(result, indent=2) + "\n")
print("PASS: raw parent blobs", count, "; required submodules", len(required), "; clean index and status")
