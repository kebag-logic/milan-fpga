#!/usr/bin/env python3
"""Prove tracked bytes, executable modes, index entries and required gitlinks."""
import argparse, hashlib, json, os, pathlib, stat, subprocess
p=argparse.ArgumentParser();p.add_argument("source",type=pathlib.Path);a=p.parse_args()
env=os.environ.copy();env["GIT_NO_REPLACE_OBJECTS"]="1"
def git(root,*args): return subprocess.check_output(["git","-C",str(root),*args],env=env)
def prove(root,rev):
    entries={}; links={}; count=0
    assert git(root,"rev-parse","HEAD").decode().strip()==rev
    for item in git(root,"ls-tree","-rz",rev).split(b"\0"):
        if not item: continue
        meta,name=item.split(b"\t",1);mode,kind,oid=meta.decode().split();name=os.fsdecode(name)
        entries[name]=(mode,oid)
        path=root/name
        if kind=="commit": links[name]=oid;continue
        s=path.lstat()
        if mode=="120000":
            assert stat.S_ISLNK(s.st_mode),name
            data=os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(s.st_mode),name
            assert bool(s.st_mode & 0o111)==(mode=="100755"),name
            data=path.read_bytes()
        digest=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
        assert digest==oid,name
        count+=1
    index={}
    for item in git(root,"ls-files","--stage","-z").split(b"\0"):
        if not item:continue
        meta,name=item.split(b"\t",1);mode,oid,stage=meta.decode().split()
        assert stage=="0",os.fsdecode(name)
        index[os.fsdecode(name)]=(mode,oid)
    assert index==entries,"index differs from head tree"
    return {"head":rev,"tree":git(root,"rev-parse",rev+"^{tree}").decode().strip(),"blobs_verified":count,"index_matches_tree":True,"gitlinks":links}
head="62c261c2d1b899a9cf90c901b25b5a85846dfef6"
result={"root":prove(a.source,head)}
required=("protocol-processor","gptp-processor","third_party/verilog-axis")
for name in required:
    result[name]=prove(a.source/name,result["root"]["gitlinks"][name])
for name in result["root"]["gitlinks"]:
    if name not in required:
        result[name]={"required_for_focused_render":False,"initialized":(a.source/name/".git").exists(),"pin":result["root"]["gitlinks"][name]}
print(json.dumps(result,indent=2))
