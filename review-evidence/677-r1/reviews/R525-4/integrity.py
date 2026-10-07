#!/usr/bin/env python3
"""Compare tracked disk bytes, modes and index against committed trees."""
import argparse
import hashlib
import os
from pathlib import Path
import stat
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("repo", type=Path)
args = parser.parse_args()
root = args.repo.resolve()
HEAD = "708e5634f28e6e5a19236a9b0a9a543c3622e52d"
TREE = "5aab27ec48b9ac84d26e92440b6a55b59cf69298"

def git(repo, *argv):
    return subprocess.check_output(["git", "-C", str(repo), *argv])

def inspect(repo, expected, label):
    assert git(repo, "rev-parse", "HEAD").decode().strip() == expected
    entries = {}
    for row in git(repo, "ls-tree", "-rz", "--full-tree", expected).split(b"\0"):
        if row:
            meta, path = row.split(b"\t", 1)
            mode, kind, oid = meta.split()
            entries[path] = (mode, kind, oid)
    index = {}
    for row in git(repo, "ls-files", "--stage", "-z").split(b"\0"):
        if row:
            meta, path = row.split(b"\t", 1)
            mode, oid, stage = meta.split()
            assert stage == b"0", (label, path, "unmerged index")
            index[path] = (mode, oid)
    assert index == {p:(m,o) for p,(m,k,o) in entries.items()}, (label,"index differs")
    count = 0
    for name, (mode, kind, oid) in entries.items():
        if kind == b"commit":
            continue
        path = repo / os.fsdecode(name)
        st = path.lstat()
        if mode == b"120000":
            assert stat.S_ISLNK(st.st_mode), (label,name,"kind")
            raw = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(st.st_mode), (label,name,"kind")
            actual_mode = b"100755" if st.st_mode & 0o111 else b"100644"
            assert actual_mode == mode, (label,name,"mode")
            raw = path.read_bytes()
        digest = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest().encode()
        assert digest == oid, (label,name,"bytes")
        count += 1
    print(f"PASS {label}: HEAD={expected}; {count} tracked blobs and modes; full index matches")
    return entries

assert git(root,"rev-parse","HEAD^{tree}").decode().strip() == TREE
assert subprocess.run(["git","-C",str(root),"symbolic-ref","-q","HEAD"],capture_output=True).returncode == 1
entries = inspect(root, HEAD, "candidate")
for name in ("third_party/verilog-axis", "protocol-processor", "gptp-processor"):
    mode, kind, oid = entries[name.encode()]
    assert mode == b"160000" and kind == b"commit"
    assert (root/name/".git").exists() and not (root/name).is_symlink()
    inspect(root/name, oid.decode(), name)
print("PASS exact detached head, tree, raw tracked bytes/modes, indices and all three required gitlinks")
