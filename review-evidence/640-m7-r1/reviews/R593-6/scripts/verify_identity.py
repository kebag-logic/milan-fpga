#!/usr/bin/env python3
"""Verify raw tracked bytes/modes and complete stage-zero index against HEAD."""
import hashlib
import os
from pathlib import Path
import stat
import subprocess
import sys
root=Path(sys.argv[1]).resolve()
env={**os.environ,"GIT_NO_REPLACE_OBJECTS":"1","GIT_OPTIONAL_LOCKS":"0"}
HEAD="7fb3664b9b53d0c4caa4b64415dd9cc3e850e4b0"
TREE="540ed6c59e0004185e682f28be9bb5b42e584f09"
BASE="4c5d70b50230fbd5da347852d39daf7f23b3df0b"
def git(path,*args):
    return subprocess.check_output(["git","-C",str(path),*args],env=env)
def verify(path,expected):
    assert git(path,"rev-parse","HEAD").decode().strip()==expected
    records={}
    blobs=0
    links=[]
    for row in git(path,"ls-tree","-rz","--full-tree",expected).split(b"\0"):
        if not row:continue
        meta,name=row.split(b"\t",1)
        mode,kind,oid=meta.split()
        records[name]=(mode,oid,b"0")
        f=path/os.fsdecode(name)
        if mode==b"160000":
            links.append((os.fsdecode(name),oid.decode()))
            continue
        st=f.lstat()
        if mode==b"120000":
            assert stat.S_ISLNK(st.st_mode),name
            data=os.fsencode(os.readlink(f))
        else:
            assert stat.S_ISREG(st.st_mode),name
            assert bool(st.st_mode & 0o111)==(mode==b"100755"),name
            data=f.read_bytes()
        actual=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
        assert actual==oid.decode(),(name,actual,oid.decode())
        blobs+=1
    index={}
    for row in git(path,"ls-files","--stage","-z").split(b"\0"):
        if not row:continue
        meta,name=row.split(b"\t",1)
        mode,oid,stage=meta.split()
        assert stage==b"0" and name not in index,(name,stage)
        index[name]=(mode,oid,stage)
    assert index==records,"index/tree mismatch"
    assert git(path,"write-tree").decode().strip()==git(path,"rev-parse",expected+"^{tree}").decode().strip()
    label="parent" if path==root else str(path.relative_to(root))
    print(f"{label}: {blobs} blobs: raw bytes, file modes, full index PASS; HEAD {expected}")
    return links
assert git(root,"rev-parse","HEAD^{tree}").decode().strip()==TREE
assert git(root,"rev-parse","HEAD^").decode().strip()==BASE
assert git(root,"diff","--name-only",BASE,HEAD).decode().splitlines()==["docs/testing/CI_WORKFLOWS.md"]
print("one commit / one documentation file; exact parent, HEAD and tree PASS")
for name,pin in verify(root,HEAD):
    print(f"gitlink {name} {pin}")
    if name=="external":
        print("external: unused checkout uninitialized; committed/index gitlink verified")
        continue
    assert (root/name/".git").is_file(),name
    assert git(root/name,"rev-parse","--show-toplevel").decode().strip()==str(root/name),name
    verify(root/name,pin)
assert not git(root,"status","--porcelain=v1","--untracked-files=all").strip(),"dirty worktree"
print("PASS: exact tracked bytes/modes/index, all initialized dependencies and gitlinks; worktree clean")
