#!/usr/bin/env python3
"""Verify raw tracked bytes, modes, complete index and initialized gitlinks."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
env = {**os.environ,"GIT_NO_REPLACE_OBJECTS":"1"}
def git(at,*args):
    return subprocess.check_output(["git",*args],cwd=at,env=env)
reports = []
def verify(at, revision, label):
    assert git(at,"rev-parse","HEAD").decode().strip() == revision
    raw = git(at,"ls-tree","-rz",revision)
    expected = {}
    submodules = []
    blobs = 0
    for entry in raw.split(b"\0"):
        if not entry: continue
        meta,name = entry.split(b"\t",1)
        mode,kind,oid = meta.split()
        expected[name]=(mode,oid,b"0")
        path = at / os.fsdecode(name)
        if kind == b"commit":
            submodules.append((path,oid.decode(),os.fsdecode(name)))
            continue
        st = path.lstat()
        if mode == b"120000":
            assert stat.S_ISLNK(st.st_mode), str(path)
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(st.st_mode), str(path)
            assert bool(st.st_mode & 0o111) == (mode == b"100755"), str(path)
            data = path.read_bytes()
        actual=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
        assert actual == oid.decode(), str(path)
        blobs += 1
    actual_index={}
    index_bytes=git(at,"ls-files","--stage","-z")
    for entry in index_bytes.split(b"\0"):
        if not entry: continue
        meta,name = entry.split(b"\t",1)
        mode,oid,stage = meta.split()
        assert name not in actual_index
        actual_index[name]=(mode,oid,stage)
    assert actual_index == expected, label+" index mismatch"
    reports.append({"path":label,"head":revision,"tree":git(at,"rev-parse",revision+"^{tree}").decode().strip(),
                    "tracked_blobs":blobs,"index_entries":len(expected),
                    "index_sha256":hashlib.sha256(index_bytes).hexdigest(),"result":"PASS"})
    for path,pin,name in submodules:
        if not (path / ".git").exists():
            assert name == "external", name
            reports.append({"path":name,"pin":pin,"result":"gitlink retained; intentionally uninitialized"})
        else:
            verify(path,pin,label+"/"+name)
verify(root,"6841c5e3be421dc59900b392b51cbc3c0a110471",".")
assert git(root,"status","--porcelain","--untracked-files=no") == b""
print(json.dumps(reports,indent=2))
