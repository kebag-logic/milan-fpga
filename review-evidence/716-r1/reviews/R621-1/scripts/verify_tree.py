#!/usr/bin/env python3
"""Prove tracked bytes, kinds, executable modes and index against exact trees."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

root=Path(sys.argv[1]).resolve()
head="f41e4f2dd56eaccebb30d6c1ec255624b0ae7a48"
tree="6fab4d33da2dfeb5c349911088b17d40e23b81f3"
env={**os.environ,"GIT_NO_REPLACE_OBJECTS":"1"}
required=("protocol-processor","gptp-processor","third_party/verilog-axis","third_party/lwSRP")


def git(where,*args):
    return subprocess.check_output(["git","-C",str(where),*args],env=env)


def verify(where,revision,label):
    assert git(where,"rev-parse","HEAD").decode().strip()==revision
    entries={}
    for record in git(where,"ls-tree","-rz",revision).split(b"\0"):
        if not record: continue
        meta,path=record.split(b"\t",1)
        mode,kind,oid=meta.split()
        entries[path]=(mode,kind,oid)
    indexed={}
    for record in git(where,"ls-files","--stage","-z").split(b"\0"):
        if not record: continue
        meta,path=record.split(b"\t",1)
        mode,oid,stage=meta.split()
        assert stage==b"0",(label,path,"unmerged index")
        assert path not in indexed
        indexed[path]=(mode,oid)
    assert indexed=={p:(v[0],v[2]) for p,v in entries.items()},(label,"index differs from tree")
    checked=0
    for path,(mode,kind,oid) in entries.items():
        if kind==b"commit": continue
        location=where/os.fsdecode(path)
        st=location.lstat()
        if mode==b"120000":
            assert stat.S_ISLNK(st.st_mode),(label,path,"symlink kind")
            content=os.fsencode(os.readlink(location))
        else:
            assert stat.S_ISREG(st.st_mode),(label,path,"regular kind")
            actual=b"100755" if st.st_mode&stat.S_IXUSR else b"100644"
            assert actual==mode,(label,path,"executable mode")
            content=location.read_bytes()
        digest=hashlib.sha1(b"blob "+str(len(content)).encode()+b"\0"+content).hexdigest().encode()
        assert digest==oid,(label,path,"blob bytes")
        checked+=1
    print(json.dumps({"population":label,"head":revision,"tracked_blobs_proved":checked,"index_entries_proved":len(indexed),"bytes_kinds_modes_index":"PASS"}))
    return entries


assert git(root,"rev-parse","HEAD^{tree}").decode().strip()==tree
entries=verify(root,head,"superproject")
for rel in required:
    mode,kind,oid=entries[rel.encode()]
    assert mode==b"160000" and kind==b"commit"
    sub=root/rel
    assert not sub.is_symlink() and (sub/".git").is_file()
    assert Path(git(sub,"rev-parse","--show-superproject-working-tree").decode().strip()).resolve()==root
    verify(sub,oid.decode(),rel)
print("PASS: exact head/tree, all tracked blob bytes/modes/index entries, and all four required submodule gitlinks and populations.")
print("The optional external submodule remains uninitialised; it is not used by these checks.")
