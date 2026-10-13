#!/usr/bin/env python3
"""Prove tracked bytes, modes, index entries and required submodule gitlinks."""
import argparse,hashlib,json,os,stat,subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("--root",type=Path,required=True);a=p.parse_args()
env=dict(os.environ,GIT_NO_REPLACE_OBJECTS="1")
def git(root,*args):return subprocess.check_output(["git","-C",str(root),*args],env=env)
head="e2cd089ce2d902c73a5f7c6ae5bcee3aa84461bd"
assert git(a.root,"rev-parse","HEAD").decode().strip()==head
assert git(a.root,"rev-parse","HEAD^{tree}").decode().strip()=="295aadcc963e941f2fcc97b27d497aa787da0d86"
required={"protocol-processor","gptp-processor","third_party/verilog-axis","third_party/tsn-c-stack"}
results=[]
def verify(root,commit,label):
    entries={}
    for entry in git(root,"ls-tree","-rz",commit).split(b"\0"):
        if not entry:continue
        meta,name=entry.split(b"\t",1);mode,kind,oid=meta.split()
        entries[name]=(mode,kind,oid)
    index={}
    for entry in git(root,"ls-files","--stage","-z").split(b"\0"):
        if not entry:continue
        meta,name=entry.split(b"\t",1);mode,oid,stage=meta.split()
        assert stage==b"0",(label,name,"unmerged index")
        assert name not in index,(label,name,"duplicate index")
        index[name]=(mode,oid)
    assert index=={n:(m,o)for n,(m,k,o)in entries.items()},(label,"index/tree mismatch")
    blobs=0;links=[]
    for name,(mode,kind,oid) in entries.items():
        path=root/os.fsdecode(name)
        if mode==b"160000":
            links.append({"path":os.fsdecode(name),"pin":oid.decode()})
            if label=="root" and os.fsdecode(name) in required:
                assert path.is_dir() and not path.is_symlink()
                assert (path/".git").is_file(),(name,"not registered submodule")
                assert git(path,"rev-parse","HEAD").strip()==oid
                verify(path,oid.decode(),os.fsdecode(name))
            continue
        st=path.lstat()
        if mode==b"120000":
            assert stat.S_ISLNK(st.st_mode);data=os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(st.st_mode),(label,name,"file kind")
            actual=b"100755" if st.st_mode&0o111 else b"100644"
            assert actual==mode,(label,name,"mode")
            data=path.read_bytes()
        hashed=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
        assert hashed==oid.decode(),(label,name,"blob bytes")
        blobs+=1
    results.append({"scope":label,"head":commit,"tracked_blobs_checked":blobs,"index_equal":True,"bytes_and_modes_equal":True,"gitlinks":links})
verify(a.root,head,"root")
print(json.dumps({"head":head,"tree":git(a.root,"rev-parse","HEAD^{tree}").decode().strip(),"checks":results,"status":git(a.root,"status","--short").decode()},indent=2))
