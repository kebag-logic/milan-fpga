#!/usr/bin/env python3
"""Verify HEAD, index, tracked blob bytes, modes and every required gitlink."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
output = Path(sys.argv[2]).resolve()
def git(*args):
    return subprocess.check_output(["git", "-C", str(root), *args])

head = git("rev-parse", "HEAD").decode().strip()
tree = git("rev-parse", "HEAD^{tree}").decode().strip()
assert head == "4bee75b2e647507a71ece50359fceb135c334757"
assert tree == "6bca4f9099adb67e6ca3758f9738975bba32d2d4"
expected = {}
for line in git("ls-tree", "-rz", "HEAD").split(b"\0"):
    if line:
        meta, path = line.split(b"\t", 1)
        mode, kind, oid = meta.decode().split()
        expected[path.decode()] = (mode, oid)
index = {}
for line in git("ls-files", "--stage", "-z").split(b"\0"):
    if line:
        meta, path = line.split(b"\t", 1)
        mode, oid, stage = meta.decode().split()
        assert stage == "0"
        index[path.decode()] = (mode, oid)
assert index == expected
checked, links = [], []
for path, (mode, oid) in expected.items():
    target = root / path
    if mode == "160000":
        actual = subprocess.check_output(["git", "-C", str(target), "rev-parse", "HEAD"]).decode().strip()
        assert actual == oid
        links.append(dict(path=path, required=oid, actual=actual))
        continue
    info = target.lstat()
    if mode == "120000":
        assert stat.S_ISLNK(info.st_mode)
        data = os.readlink(target).encode()
    else:
        assert stat.S_ISREG(info.st_mode)
        assert bool(info.st_mode & 0o111) == (mode == "100755"), path
        data = target.read_bytes()
    actual = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    assert actual == oid, path
    checked.append(dict(path=path, mode=mode, blob=actual, sha256=hashlib.sha256(data).hexdigest()))
status = git("status", "--porcelain=v1", "--untracked-files=all").decode()
assert not status, status
record = dict(head=head, tree=tree, index_matches_head=True, tracked_files=len(checked),
              tracked_bytes_and_modes_match=True, gitlinks=links, status=status, files=checked)
output.write_text(json.dumps(record, indent=2)+"\n")
print(f"PASS: {len(checked)} tracked files, exact bytes/modes/index; {len(links)} required submodule gitlinks; clean detached source head.")
