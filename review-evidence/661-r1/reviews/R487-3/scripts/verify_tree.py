#!/usr/bin/env python3
"""Prove tracked bytes, modes, index and required submodule pins."""
import hashlib
import os
from pathlib import Path
import stat
import subprocess
import sys
ROOT = Path(sys.argv[1]).resolve()
HEAD = "3048222541ea6be725417ba0cd957607f0b821cb"
TREE = "a640b146eb68632f2d9ca153639ba2683b172b0a"
ENV = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")
def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], env=ENV)
def verify(root, rev, label):
    entries = {}
    for row in git(root, "ls-tree", "-rz", rev).split(b"\0"):
        if row:
            meta, path = row.split(b"\t", 1)
            mode, kind, oid = meta.split()
            entries[path] = (mode, oid)
    index = {}
    for row in git(root, "ls-files", "--stage", "-z").split(b"\0"):
        if row:
            meta, path = row.split(b"\t", 1)
            mode, oid, stage = meta.split()
            assert stage == b"0" and path not in index, (label, path, "index stage")
            index[path] = (mode, oid)
    assert index == entries, (label, "index differs from tree")
    count = 0
    for path, (mode, oid) in entries.items():
        if mode == b"160000":
            continue
        file = root / os.fsdecode(path)
        st = file.lstat()
        if mode == b"120000":
            assert stat.S_ISLNK(st.st_mode), (label, path, "symlink mode")
            data = os.fsencode(os.readlink(file))
        else:
            assert stat.S_ISREG(st.st_mode), (label, path, "regular mode")
            actual_mode = b"100755" if st.st_mode & 0o111 else b"100644"
            assert actual_mode == mode, (label, path, "executable mode")
            data = file.read_bytes()
        digest = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest().encode()
        assert digest == oid, (label, path, "blob mismatch")
        count += 1
    print(f"PASS {label}: {count} tracked blob bytes/modes and index exactly match {rev}")
    return entries
assert git(ROOT, "rev-parse", "HEAD").decode().strip() == HEAD
assert git(ROOT, "rev-parse", "HEAD^{tree}").decode().strip() == TREE
entries = verify(ROOT, HEAD, "parent")
for sub in ("protocol-processor", "gptp-processor", "third_party/verilog-axis"):
    mode, oid = entries[os.fsencode(sub)]
    assert mode == b"160000"
    checkout = ROOT / sub
    assert checkout.is_dir() and not checkout.is_symlink()
    assert (checkout / ".git").is_file(), (sub, "not registered submodule")
    assert git(checkout, "rev-parse", "--show-superproject-working-tree").decode().strip() == str(ROOT)
    pin = oid.decode()
    assert git(checkout, "rev-parse", "HEAD").decode().strip() == pin
    verify(checkout, pin, sub)
print("PASS exact head, tree and all three required gitlinks")
