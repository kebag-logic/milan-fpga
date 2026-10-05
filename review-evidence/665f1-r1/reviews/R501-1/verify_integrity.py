#!/usr/bin/env python3
"""Prove tracked bytes, modes, index and required gitlinks directly from objects."""
import hashlib
import os
from pathlib import Path
import stat
import subprocess
import sys
root=Path(sys.argv[1]).resolve()
env=dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")
HEAD="215c3c0be5d8db6d9a1ba5aca3827dfe969c042e"
TREE="a574cf75a8d3a233ad7dc6b31ca31fbf1f214848"
def git(repo,*args):
    return subprocess.check_output(["git","-C",str(repo),*args],env=env)
def check(repo,rev,label):
    assert git(repo,"rev-parse","HEAD").decode().strip()==rev
    entries={}
    for row in git(repo,"ls-tree","-rz",rev).split(b"\0"):
        if not row: continue
        info,name=row.split(b"\t",1)
        mode,kind,oid=info.decode().split()
        entries[name]=(mode,kind,oid)
    index={}
    for row in git(repo,"ls-files","--stage","-z").split(b"\0"):
        if not row: continue
        info,name=row.split(b"\t",1)
        mode,oid,stage=info.decode().split()
        assert stage=="0", (label,"unmerged index")
        assert name not in index
        index[name]=(mode,oid)
    assert index=={n:(m,o) for n,(m,k,o) in entries.items()},(label,"index differs from tree")
    count=0
    for name,(mode,kind,oid) in entries.items():
        if kind=="commit": continue
        path=repo/os.fsdecode(name)
        st=path.lstat()
        if mode=="120000":
            assert stat.S_ISLNK(st.st_mode),(label,os.fsdecode(name),"not symlink")
            data=os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(st.st_mode),(label,os.fsdecode(name),"not regular file")
            assert bool(st.st_mode&0o111)==(mode=="100755"),(label,os.fsdecode(name),"mode mismatch")
            data=path.read_bytes()
        actual=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
        assert actual==oid,(label,os.fsdecode(name),"blob mismatch")
        count+=1
    print(label+": "+str(count)+" tracked blobs/modes and full index match "+rev)
    return entries
entries=check(root,HEAD,"superproject")
assert git(root,"rev-parse","HEAD^{tree}").decode().strip()==TREE
print("tree "+TREE)
for name in ["protocol-processor","gptp-processor","third_party/verilog-axis"]:
    mode,kind,pin=entries[name.encode()]
    assert mode=="160000" and kind=="commit"
    assert (root/name/".git").is_file(),(name,"not registered submodule checkout")
    check(root/name,pin,name)
    print("gitlink "+name+" "+pin)
status=git(root,"status","--porcelain=v1","--untracked-files=all").decode()
assert not status,status
print("working tree clean; no tracked edits or untracked probe/build files")
print("external gitlink retained; optional external checkout uninitialized and unused")
