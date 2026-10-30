#!/usr/bin/env python3
"""Check tracked bytes, modes, index records and initialized submodule pins."""
import hashlib, os, pathlib, stat, subprocess, sys
root = pathlib.Path(sys.argv[1]).resolve()
HEAD = "ac105b158bb740a65e0154305377fd4a7d0f6f87"
TREE = "10a286051e8aa59003bfac98cf4f7d5973d241f9"
def git(path, *args):
    return subprocess.check_output(["git", "--no-replace-objects", "-C", str(path), *args])
def audit(path, rev, label):
    records = git(path, "ls-tree", "-rz", rev).split(b"\0")
    expected = []
    count = 0
    submodules = []
    for record in filter(None, records):
        meta, name = record.split(b"\t", 1)
        mode, kind, oid = meta.split()
        expected.append(mode + b" " + oid + b" 0\t" + name)
        file = path / os.fsdecode(name)
        if kind == b"commit":
            submodules.append((file, oid.decode(), os.fsdecode(name)))
            continue
        st = file.lstat()
        if mode == b"120000":
            assert stat.S_ISLNK(st.st_mode), name
            data = os.fsencode(os.readlink(file))
        else:
            assert stat.S_ISREG(st.st_mode), name
            assert bool(st.st_mode & 0o111) == (mode == b"100755"), name
            data = file.read_bytes()
        actual = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        assert actual == oid.decode(), (label, name, actual, oid)
        count += 1
    index = list(filter(None, git(path, "ls-files", "--stage", "-z").split(b"\0")))
    assert sorted(index) == sorted(expected), label + " index mismatch"
    print(label + ":", count, "tracked blobs match exact bytes, modes and index")
    for sub, pin, name in submodules:
        if not (sub / ".git").exists():
            assert label == "superproject" and name == "external", (name, "required submodule absent")
            print(name, pin, "gitlink verified; uninitialized and unused by focused probes")
            continue
        actual = git(sub, "rev-parse", "HEAD").decode().strip()
        assert actual == pin, (name, pin, actual)
        print(label + "/" + name, "gitlink", pin)
        audit(sub, pin, label + "/" + name)
assert git(root, "rev-parse", "HEAD").decode().strip() == HEAD
assert git(root, "rev-parse", "HEAD^{tree}").decode().strip() == TREE
print("HEAD", HEAD, "tree", TREE)
audit(root, HEAD, "superproject")
print("CHECKOUT INTEGRITY PASS")
