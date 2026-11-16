#!/usr/bin/env python3
"""Verify raw working files, modes and index against commit trees, recursively."""
import hashlib
import os
from pathlib import Path
import subprocess
import sys
root=Path(sys.argv[1]).resolve()
env=dict(os.environ,GIT_NO_REPLACE_OBJECTS="1")
def git(repo,*args):
    return subprocess.check_output(["git","-C",str(repo),*args],env=env)
def verify(repo, rev, label):
    entries=git(repo,"ls-tree","-rz",rev).split(b"\0")
    want=[]; count=0
    for raw in entries:
        if not raw: continue
        meta,name=raw.split(b"\t",1)
        mode,kind,oid=meta.split()
        want.append(mode+b" "+oid+b" 0\t"+name)
        p=repo/os.fsdecode(name)
        if kind==b"commit":
            if os.fsdecode(name)=="external":
                print(label+" external: intentionally uninitialized gitlink "+oid.decode()); continue
            assert p.is_dir() and not p.is_symlink(),str(p)
            assert git(p,"rev-parse","HEAD").strip()==oid,str(p)
            verify(p,oid.decode(),label+"/"+os.fsdecode(name));continue
        assert os.path.lexists(p),str(p)
        if mode==b"120000":
            assert p.is_symlink(),str(p)
            data=os.fsencode(os.readlink(p))
        else:
            assert p.is_file() and not p.is_symlink(),str(p)
            actual=b"100755" if p.stat().st_mode & 0o111 else b"100644"
            assert actual==mode,(p,actual,mode)
            data=p.read_bytes()
        digest=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest().encode()
        assert digest==oid,(p,digest,oid)
        count+=1
    actual=git(repo,"ls-files","--stage","-z").split(b"\0")
    assert sorted(x for x in actual if x)==sorted(want),label+" index differs"
    print(label+": "+rev+"; "+str(count)+" raw blobs/modes and complete index MATCH")
head=git(root,"rev-parse","HEAD").decode().strip()
assert head=="6ceed75374210935cff4f10d014b9a5ef137615e"
print("head "+head+" tree "+git(root,"rev-parse","HEAD^{tree}").decode().strip())
verify(root,head,"root")
print("PASS source bytes, modes, index and initialized submodule gitlinks")
