#!/usr/bin/env python3
"""Prove tracked bytes, file types, executable modes, index and required pins."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
head = "04e1435a218908d2b12b4053e5dab2c2dcac2ebf"
expected_tree = "30980a43ee2b14afd59e25b16aafb18ea6e1df41"
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")
required = {"protocol-processor", "gptp-processor", "third_party/verilog-axis"}

def git(where, *args):
    return subprocess.check_output(["git", "-C", str(where), *args], env=env)

def verify(where, revision, label):
    assert git(where, "rev-parse", "HEAD").decode().strip() == revision
    records = {}
    for row in git(where, "ls-tree", "-rz", revision).split(b"\0"):
        if not row:
            continue
        meta, path = row.split(b"\t", 1)
        mode, kind, oid = meta.decode().split()
        records[path.decode()] = (mode, kind, oid)
    expected_index = {path: (mode, oid, "0") for path, (mode, kind, oid) in records.items()}
    index = {}
    for row in git(where, "ls-files", "--stage", "-z").split(b"\0"):
        if row:
            meta, path = row.split(b"\t", 1)
            assert path.decode() not in index, (label, "multiple index stages", path)
            index[path.decode()] = tuple(meta.decode().split())
    assert index == expected_index, (label, "index differs from commit tree")
    files = 0
    for name, (mode, kind, oid) in records.items():
        path = where / name
        if kind == "commit":
            if label == "superproject" and name in required:
                assert path.is_dir() and not path.is_symlink()
                verify(path, oid, name)
            continue
        st = path.lstat()
        if mode == "120000":
            assert stat.S_ISLNK(st.st_mode), (label, name, "not symlink")
            data = os.readlink(path).encode()
        else:
            assert stat.S_ISREG(st.st_mode), (label, name, "not regular")
            assert bool(st.st_mode & 0o111) == (mode == "100755"), (label, name, "mode")
            data = path.read_bytes()
        actual = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        assert actual == oid, (label, name, "blob mismatch")
        files += 1
    print(json.dumps({"repository": label, "head": revision, "files_proved": files,
                      "index": "exact", "bytes_and_modes": "exact"}))

assert git(root, "rev-parse", "HEAD^{tree}").decode().strip() == expected_tree
verify(root, head, "superproject")
print("External historical submodule remains uninitialized; its recorded gitlink is verified in the index.")
print("PASS: exact tree, tracked blobs/modes/index and all three required submodule populations")
