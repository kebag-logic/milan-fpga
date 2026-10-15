#!/usr/bin/env python3
"""Prove tracked working bytes, modes, index entries and required gitlinks directly."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
ROOT = Path(sys.argv[1]).resolve()
EXPECTED = "c48bfe38b25f002d24898cec265520b9fc1a7111"
EXPECTED_TREE = "33e999cb842593dbbd9d2e97cfeea587d581b63a"
REQUIRED = ("protocol-processor", "gptp-processor", "third_party/verilog-axis", "third_party/tsn-c-stack")
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1", GIT_OPTIONAL_LOCKS="0")
def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], env=env)
def verify(root, commit):
    entries = {}
    for row in git(root, "ls-tree", "-rz", "--full-tree", commit).split(b"\0"):
        if not row: continue
        header, path = row.split(b"\t", 1)
        mode, kind, oid = header.split()
        entries[path] = (mode, kind, oid)
    index = {}
    for row in git(root, "ls-files", "--stage", "-z").split(b"\0"):
        if not row: continue
        header, path = row.split(b"\t", 1)
        mode, oid, stage = header.split()
        assert stage == b"0", (path, stage)
        assert path not in index, path
        index[path] = (mode, oid)
    assert index == {p:(m,o) for p,(m,k,o) in entries.items()}, "index differs from commit tree"
    blobs = 0
    for rel, (mode, kind, oid) in entries.items():
        if kind == b"commit": continue
        path = root / os.fsdecode(rel)
        st = path.lstat()
        if mode == b"120000":
            assert stat.S_ISLNK(st.st_mode), rel
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(st.st_mode), rel
            actual_mode = b"100755" if st.st_mode & 0o111 else b"100644"
            assert actual_mode == mode, rel
            data = path.read_bytes()
        digest = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest().encode()
        assert digest == oid, rel
        blobs += 1
    return entries, blobs
assert git(ROOT, "rev-parse", "HEAD").decode().strip() == EXPECTED
assert git(ROOT, "rev-parse", "HEAD^{tree}").decode().strip() == EXPECTED_TREE
entries, blobs = verify(ROOT, EXPECTED)
rows = {"head": EXPECTED, "tree": EXPECTED_TREE, "root_blob_count": blobs, "submodules": {}}
for name in REQUIRED:
    mode, kind, oid = entries[name.encode()]
    assert mode == b"160000" and kind == b"commit"
    sub = ROOT / name
    assert (sub / ".git").is_file()
    assert git(sub, "rev-parse", "HEAD").strip() == oid
    assert Path(git(sub, "rev-parse", "--show-superproject-working-tree").decode().strip()).resolve() == ROOT
    _, count = verify(sub, oid.decode())
    rows["submodules"][name] = {"gitlink": oid.decode(), "blob_count": count}
rows["status_porcelain"] = git(ROOT, "status", "--porcelain=v1").decode()
assert not rows["status_porcelain"]
rows["result"] = "PASS: exact tracked bytes, file modes, stage-zero index and required registered submodules"
print(json.dumps(rows, indent=2))
