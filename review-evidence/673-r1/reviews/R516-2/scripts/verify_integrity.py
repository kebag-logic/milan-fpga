#!/usr/bin/env python3
"""Check raw tracked bytes, entry modes, index, and required submodule pins."""
import hashlib
import os
from pathlib import Path
import stat
import subprocess
import sys

repo = Path(sys.argv[1]).resolve()
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")

def git(root, *args):
    return subprocess.check_output(["git", "--no-replace-objects", "-C", str(root), *args], env=env)

def verify(root, commit):
    assert git(root, "rev-parse", "HEAD").decode().strip() == commit
    tree = git(root, "ls-tree", "-rz", commit)
    expected_index = []
    count = 0
    links = {}
    for row in tree.split(b"\0"):
        if not row:
            continue
        info, path = row.split(b"\t", 1)
        mode, kind, oid = info.split()
        expected_index.append(mode + b" " + oid + b" 0\t" + path)
        if kind == b"commit":
            links[os.fsdecode(path)] = oid.decode()
            continue
        file = root / os.fsdecode(path)
        st = file.lstat()
        if mode == b"120000":
            assert stat.S_ISLNK(st.st_mode), path
            content = os.fsencode(os.readlink(file))
        else:
            assert stat.S_ISREG(st.st_mode), path
            assert bool(st.st_mode & stat.S_IXUSR) == (mode == b"100755"), path
            content = file.read_bytes()
        actual = hashlib.sha1(b"blob " + str(len(content)).encode() + b"\0" + content).hexdigest()
        assert actual == oid.decode(), path
        count += 1
    index = git(root, "ls-files", "--stage", "-z").split(b"\0")
    assert sorted(filter(None, index)) == sorted(expected_index)
    assert not git(root, "diff", "--raw", "HEAD")
    print(f"PASS {root.name if root != repo else 'superproject'} {commit}: {count} blobs, exact modes and index")
    return links

head = "793dcd3f7867d85f8c1f5c9ef2b04dc9c2d9c5df"
links = verify(repo, head)
required = {"protocol-processor": "ead8036035affd53ef4b29979190f2f4f67084c0",
            "gptp-processor": "5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d",
            "third_party/verilog-axis": "48ff7a7e2ef782cf778d47910cf85835c64b1bce"}
for name, pin in required.items():
    assert links[name] == pin
    root = repo / name
    assert not root.is_symlink() and (root / ".git").is_file()
    assert git(root, "rev-parse", "--show-superproject-working-tree").decode().strip() == str(repo)
    verify(root, pin)
assert git(repo, "rev-parse", "HEAD^{tree}").decode().strip() == "4044003424303525864889c45788aeb8a48c8501"
print("PASS exact head tree and all three required gitlinks; no restoration needed")
