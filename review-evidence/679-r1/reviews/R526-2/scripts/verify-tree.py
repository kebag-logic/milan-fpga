"""Prove tracked bytes, modes and index independently of status flags.

Usage: python3 verify-tree.py CHECKOUT
"""
import hashlib
import os
from pathlib import Path
import stat
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
expected_head = "04e1435a218908d2b12b4053e5dab2c2dcac2ebf"
expected_tree = "30980a43ee2b14afd59e25b16aafb18ea6e1df41"
required = {
    "protocol-processor": "ead8036035affd53ef4b29979190f2f4f67084c0",
    "gptp-processor": "5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d",
    "third_party/verilog-axis": "48ff7a7e2ef782cf778d47910cf85835c64b1bce",
}
env = {**os.environ, "GIT_NO_REPLACE_OBJECTS": "1"}


def git(directory, *args):
    return subprocess.check_output(["git", "-C", str(directory), *args], env=env)


def verify(directory, expected, label):
    assert git(directory, "rev-parse", "HEAD").decode().strip() == expected
    tree = {}
    blobs = 0
    for record in git(directory, "ls-tree", "-rz", "--full-tree", "HEAD").split(b"\0"):
        if not record:
            continue
        meta, path = record.split(b"\t", 1)
        mode, kind, oid = meta.split()
        tree[path] = (mode, oid)
        if kind == b"commit":
            continue
        target = directory / os.fsdecode(path)
        info = target.lstat()
        if mode == b"120000":
            assert stat.S_ISLNK(info.st_mode), path
            data = os.fsencode(os.readlink(target))
        else:
            assert stat.S_ISREG(info.st_mode), path
            actual_mode = b"100755" if info.st_mode & 0o111 else b"100644"
            assert mode == actual_mode, path
            data = target.read_bytes()
        actual = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest().encode()
        assert actual == oid, path
        blobs += 1
    index = {}
    for record in git(directory, "ls-files", "--stage", "-z").split(b"\0"):
        if not record:
            continue
        meta, path = record.split(b"\t", 1)
        mode, oid, stage = meta.split()
        assert stage == b"0" and path not in index, path
        index[path] = (mode, oid)
    assert tree == index, label
    print(f"PASS {label}: HEAD {expected}; {blobs} exact tracked blobs/modes; {len(index)} exact stage-zero index entries")
    return tree


assert git(root, "rev-parse", "HEAD^{tree}").decode().strip() == expected_tree
tree = verify(root, expected_head, "parent")
for name, pin in required.items():
    sub = root / name
    assert not sub.is_symlink() and sub.is_dir()
    assert (sub / ".git").is_file()
    assert Path(git(sub, "rev-parse", "--show-superproject-working-tree").decode().strip()).resolve() == root
    assert tree[name.encode()] == (b"160000", pin.encode())
    verify(sub, pin, name)
print("PASS exact parent tree", expected_tree)
print("Optional external gitlink retained:", tree[b"external"][1].decode())
assert not git(root, "status", "--porcelain").strip()
print("PASS clean checkout; no tracked source restoration required")
