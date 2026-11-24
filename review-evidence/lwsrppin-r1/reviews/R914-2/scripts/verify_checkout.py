"""Verify exact tracked bytes, filesystem modes, index entries and initialized gitlinks.

Usage: python3 -I -B scripts/verify_checkout.py <candidate-root>
"""
import hashlib
import os
from pathlib import Path
import stat
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
head = "ed7df79c6f87a4172c885f268ad67629bd56c4eb"
tree = "9065222f25fa3e23aa73783effe26694949ceaea"

def git(where, *args):
    return subprocess.check_output(["git", "--no-replace-objects", "-C", str(where), *args])

def verify(where, revision, label):
    entries = {}
    for row in git(where, "ls-tree", "-rz", revision).split(b"\0"):
        if not row:
            continue
        meta, raw_name = row.split(b"\t", 1)
        mode, kind, oid = meta.decode().split()
        name = os.fsdecode(raw_name)
        entries[name] = (mode, oid)
        path = where / name
        if mode == "160000":
            continue
        info = path.lstat()
        if mode == "120000":
            assert stat.S_ISLNK(info.st_mode), name
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(info.st_mode), name
            assert bool(info.st_mode & stat.S_IXUSR) == (mode == "100755"), name
            data = path.read_bytes()
        digest = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        assert digest == oid, name
    index = {}
    for row in git(where, "ls-files", "--stage", "-z").split(b"\0"):
        if row:
            meta, raw_name = row.split(b"\t", 1)
            mode, oid, stage = meta.decode().split()
            assert stage == "0"
            index[os.fsdecode(raw_name)] = (mode, oid)
    assert entries == index, label + " index differs from tree"
    print(f"{label}: {len(entries)} tracked entries; blob bytes, modes and index PASS")
    return entries

assert git(root, "rev-parse", "HEAD").decode().strip() == head
assert git(root, "rev-parse", "HEAD^{tree}").decode().strip() == tree
print("HEAD", head)
print("tree", tree)
entries = verify(root, head, "candidate")
for name, (mode, oid) in entries.items():
    if mode != "160000":
        continue
    print("gitlink", name, oid)
    where = root / name
    if not (where / ".git").exists():
        assert name == "external", "required submodule not initialized: " + name
        print("external: unused import uninitialized; recorded gitlink verified")
        continue
    assert git(where, "rev-parse", "HEAD").decode().strip() == oid, name
    verify(where, oid, name)
print("tracked candidate and required submodule identity: PASS")
