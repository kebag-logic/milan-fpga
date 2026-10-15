#!/usr/bin/env python3
"""Verify exact tracked bytes, modes and index against immutable trees.

Usage: python3 verify_checkout.py /path/to/review-clone
Does not rely on status, assume-unchanged or skip-worktree flags.
"""
import hashlib
import os
import stat
import subprocess
import sys
from pathlib import Path

HEAD = "2639eecf3f94aa1a8be5c922058a05f0a48b1933"
TREE = "c0bece4c6943bee323b9a72c4e677abdda840004"
root = Path(sys.argv[1]).resolve()


def git(repo, *args):
    return subprocess.check_output(["git", "--no-replace-objects", "-C", str(repo), *args])


def verify(repo, rev, label):
    assert git(repo,"rev-parse","HEAD").decode().strip() == rev, label
    records = git(repo, "ls-tree", "-rz", "--full-tree", rev).split(b"\0")
    expected = {}
    links = {}
    blobs = 0
    for record in filter(None, records):
        meta, rawpath = record.split(b"\t", 1)
        mode, kind, oid = meta.decode().split()
        expected[rawpath] = (mode, oid, "0")
        path = repo / os.fsdecode(rawpath)
        if kind == "commit":
            links[os.fsdecode(rawpath)] = oid
            continue
        info = path.lstat()
        if mode == "120000":
            assert stat.S_ISLNK(info.st_mode), os.fsdecode(rawpath)
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(info.st_mode), os.fsdecode(rawpath)
            assert bool(info.st_mode & 0o111) == (mode == "100755"), os.fsdecode(rawpath)
            data = path.read_bytes()
        actual = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        assert actual == oid, os.fsdecode(rawpath)
        blobs += 1
    index = {}
    for record in filter(None, git(repo,"ls-files","--stage","-z").split(b"\0")):
        meta, rawpath = record.split(b"\t",1)
        assert rawpath not in index, "unmerged index"
        index[rawpath] = tuple(meta.decode().split())
    assert expected == index, label + " index differs from commit tree"
    print(label, "HEAD", rev, "blobs", blobs, "bytes/modes/index PASS")
    return links


assert git(root,"rev-parse",HEAD+"^{tree}").decode().strip() == TREE
links = verify(root, HEAD, "superproject")
for name in ["protocol-processor","gptp-processor","third_party/verilog-axis","third_party/tsn-c-stack","third_party/lwSRP"]:
    sub = root/name
    assert (sub/".git").is_file() and not sub.is_symlink(), name
    assert git(sub,"rev-parse","--show-superproject-working-tree").decode().strip() == str(root), name
    verify(sub, links[name], name)
print("external: uninitialized, not required; gitlink",links["external"])
print("TREE",TREE,"RESTORATION PASS: no tracked byte, mode, index or required gitlink drift")
