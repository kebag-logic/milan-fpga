#!/usr/bin/env python3
"""Prove tracked bytes, modes, index records, and required gitlinks."""
import argparse, hashlib, json, os, stat, subprocess
from pathlib import Path
HEAD = "3880c1eb6e2f927a07f98150d5b05a228f8f4efd"
TREE = "6bba0f2cf6c330ca1bd5cb012b571e69044b0dd7"
REQUIRED = ("protocol-processor", "gptp-processor", "third_party/verilog-axis")
ENV = {**os.environ, "GIT_NO_REPLACE_OBJECTS": "1"}
def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], env=ENV)
def verify(root, rev, label):
    entries = {}
    for row in git(root, "ls-tree", "-rz", rev).split(b"\0"):
        if row:
            meta, name = row.split(b"\t", 1)
            mode, kind, oid = meta.decode().split()
            entries[name.decode()] = (mode, kind, oid)
    index = {}
    for row in git(root, "ls-files", "--stage", "-z").split(b"\0"):
        if row:
            meta, name = row.split(b"\t", 1)
            mode, oid, stage = meta.decode().split()
            assert stage == "0", (label, name.decode(), "unmerged index")
            assert name.decode() not in index
            index[name.decode()] = (mode, oid)
    assert index == {n:(m,o) for n,(m,k,o) in entries.items()}, (label, "index differs")
    files = 0
    for name, (mode, kind, oid) in entries.items():
        if kind == "commit":
            continue
        p = root / name
        s = p.lstat()
        if mode == "120000":
            assert stat.S_ISLNK(s.st_mode), (label, name, "mode")
            data = os.fsencode(os.readlink(p))
        else:
            assert stat.S_ISREG(s.st_mode), (label, name, "not regular")
            actual = "100755" if s.st_mode & stat.S_IXUSR else "100644"
            assert actual == mode, (label, name, "mode")
            data = p.read_bytes()
        got = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        assert got == oid, (label, name, "blob bytes")
        files += 1
    return {"artifact":label, "commit":rev, "tree":git(root,"rev-parse",rev+"^{tree}").decode().strip(), "tracked_files_verified":files, "index":"exact", "bytes_and_modes":"exact"}, entries
p = argparse.ArgumentParser(); p.add_argument("source", type=Path); a=p.parse_args()
root = a.source.resolve()
assert git(root,"rev-parse","HEAD").decode().strip() == HEAD
r, entries = verify(root,HEAD,"parent"); assert r["tree"] == TREE
results=[r]
for name in REQUIRED:
    mode, kind, pin=entries[name]; assert mode=="160000" and kind=="commit"
    sub=root/name
    assert git(sub,"rev-parse","HEAD").decode().strip()==pin
    assert git(sub,"rev-parse","--show-superproject-working-tree").decode().strip()==str(root)
    r,_ = verify(sub,pin,name); results.append(r)
print(json.dumps({"result":"PASS", "repositories":results, "historical_external":"not required; gitlink verified through parent index"}, indent=2))
