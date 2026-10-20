"""Verify tracked bytes, types, modes, index and required submodule pins."""
import hashlib
import os
from pathlib import Path
import stat
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
HEAD = "1e914414557874648ac5041aff88b96908e0e053"
TREE = "033e6bc1fb66904e7faf7b57929d6c7a28d89732"
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")

def git(path, *args):
    return subprocess.check_output(["git", "-C", str(path), *args], env=env)

def audit(path, commit, label):
    assert git(path, "rev-parse", "HEAD").decode().strip() == commit
    rows = {}
    for row in git(path, "ls-tree", "-rz", commit).split(b"\0"):
        if not row:
            continue
        meta, name = row.split(b"\t", 1)
        mode, kind, oid = meta.split()
        rows[name] = (mode, kind, oid)
    index = {}
    for row in git(path, "ls-files", "--stage", "-z").split(b"\0"):
        if not row:
            continue
        meta, name = row.split(b"\t", 1)
        mode, oid, stage = meta.split()
        assert stage == b"0"
        index[name] = (mode, oid)
    assert index == {n: (v[0], v[2]) for n, v in rows.items()}, label
    flags = git(path, "ls-files", "-v", "-z").split(b"\0")
    assert all(not row or row[:1] == b"H" for row in flags), label
    blobs = 0
    pins = []
    for name, (mode, kind, oid) in rows.items():
        f = path / os.fsdecode(name)
        if kind == b"commit":
            pins.append((os.fsdecode(name), oid.decode()))
            continue
        st = f.lstat()
        if mode == b"120000":
            assert stat.S_ISLNK(st.st_mode), str(f)
            data = os.fsencode(os.readlink(f))
        else:
            assert stat.S_ISREG(st.st_mode), str(f)
            assert bool(st.st_mode & 0o111) == (mode == b"100755"), str(f)
            data = f.read_bytes()
        actual = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        assert actual == oid.decode(), str(f)
        blobs += 1
    print(f"PASS {label}: {commit}; {blobs} tracked blobs, exact bytes/modes/index; no hidden flags")
    return pins

assert git(root, "rev-parse", "HEAD^{tree}").decode().strip() == TREE
pins = audit(root, HEAD, "parent")
for name, pin in pins:
    if name == "external":
        print(f"OPTIONAL uninitialized external gitlink retained: {pin}")
        continue
    assert (root / name / ".git").is_file(), name
    audit(root / name, pin, name)
assert git(root, "write-tree").decode().strip() == TREE
assert not git(root, "status", "--porcelain", "--untracked-files=all")
print(f"PASS HEAD tree and index tree {TREE}; source checkout clean")
