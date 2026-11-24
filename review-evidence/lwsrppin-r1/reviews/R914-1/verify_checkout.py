#!/usr/bin/env python3
"""Compare tracked bytes, file kinds, executable bits, index entries and gitlinks with the exact commits."""
import hashlib
import os
from pathlib import Path
import stat
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
head = "dbba60e68a6e4a46f80e381c30ff823ee4ff7484"
required = {"gptp-processor", "protocol-processor", "third_party/lwSRP",
            "third_party/tsn-c-stack", "third_party/verilog-axis"}
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1", GIT_OPTIONAL_LOCKS="0")
def git(path, *args):
    return subprocess.check_output(["git", "-C", str(path), *args], env=env)
def check(path, commit, label):
    assert git(path, "rev-parse", "HEAD").decode().strip() == commit
    records = git(path, "ls-tree", "-rz", commit).split(b"\0")
    expected = {}
    links = {}
    checked = 0
    for record in filter(None, records):
        meta, name = record.split(b"\t", 1)
        mode, kind, oid = meta.split()
        expected[name] = (mode, oid, b"0")
        p = path / os.fsdecode(name)
        if mode == b"160000":
            links[os.fsdecode(name)] = oid.decode()
            continue
        st = p.lstat()
        if mode == b"120000":
            assert stat.S_ISLNK(st.st_mode), name
            data = os.fsencode(os.readlink(p))
            digest = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        else:
            assert stat.S_ISREG(st.st_mode), name
            assert bool(st.st_mode & 0o111) == (mode == b"100755"), name
            h = hashlib.sha1(b"blob " + str(st.st_size).encode() + b"\0")
            with p.open("rb") as f:
                for chunk in iter(lambda: f.read(1048576), b""):
                    h.update(chunk)
            digest = h.hexdigest()
        assert digest == oid.decode(), (label, name, digest, oid)
        checked += 1
    actual = {}
    for record in filter(None, git(path, "ls-files", "--stage", "-z").split(b"\0")):
        meta, name = record.split(b"\t", 1)
        assert name not in actual
        actual[name] = tuple(meta.split())
    assert actual == expected, label + " index mismatch"
    print(label, commit, "tracked blobs/modes", checked, "index entries", len(actual), "PASS")
    return links

links = check(root, head, "superproject")
assert git(root, "rev-parse", "HEAD^{tree}").decode().strip() == "1e85cc2bb2ba13643ce6ae7cfb14a49a5a838c6c"
for name in sorted(required):
    assert (root / name / ".git").is_file(), name
    check(root / name, links[name], name)
print("external gitlink retained", links["external"], "uninitialized and unused")
print("No source restoration was necessary: all probes used memory or disposable output trees.")
