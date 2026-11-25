#!/usr/bin/env python3
"""Verify exact tracked bytes, executable modes, index entries and initialized gitlinks."""
import hashlib,json,os,pathlib,stat,subprocess
ROOT=pathlib.Path.cwd()
OUT=pathlib.Path(__file__).resolve().parent
ENV=dict(os.environ,GIT_NO_REPLACE_OBJECTS="1")
def git(root,*args):return subprocess.check_output(["git","-C",str(root),*args],env=ENV)
def check(root,revision):
    tree={}
    for row in git(root,"ls-tree","-rz",revision).split(b"\0"):
        if not row:continue
        meta,path=row.split(b"\t",1); mode,kind,oid=meta.decode().split()
        tree[os.fsdecode(path)]=(mode,kind,oid)
    index={}
    for row in git(root,"ls-files","--stage","-z").split(b"\0"):
        if not row:continue
        meta,path=row.split(b"\t",1);mode,oid,stage=meta.decode().split()
        assert stage=="0",(root,path,"unmerged index")
        index[os.fsdecode(path)]=(mode,oid)
    assert index=={p:(v[0],v[2]) for p,v in tree.items()},str(root)+" index mismatch"
    count=0;links={}
    for name,(mode,kind,oid) in tree.items():
        path=root/name
        if kind=="commit":links[name]=oid;continue
        s=path.lstat()
        if mode=="120000":
            assert stat.S_ISLNK(s.st_mode),name
            b=os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(s.st_mode),name
            assert bool(s.st_mode&stat.S_IXUSR)==(mode=="100755"),name
            b=path.read_bytes()
        actual=hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
        assert actual==oid,(name,actual,oid)
        count+=1
    return dict(blobs_verified=count,index_verified=True,gitlinks=links)
head=git(ROOT,"rev-parse","HEAD").decode().strip()
assert head=="09201d35d7ea720b3ba205da185ba35c159ec24a"
result=dict(head=head,tree=git(ROOT,"rev-parse","HEAD^{tree}").decode().strip(),parent=check(ROOT,"HEAD"),submodules={})
for name,pin in result["parent"]["gitlinks"].items():
    if name=="external":
        result["submodules"][name]={"gitlink":pin,"initialized":False,"required":False}
        continue
    root=ROOT/name
    assert (root/".git").is_file(),name+" not registered"
    actual=git(root,"rev-parse","HEAD").decode().strip()
    assert actual==pin,(name,actual,pin)
    result["submodules"][name]=dict(pin=pin,**check(root,pin))
result["tracked_status"]=git(ROOT,"status","--porcelain","--untracked-files=no").decode()
assert not result["tracked_status"]
(OUT/"checkout-integrity.json").write_text(json.dumps(result,indent=2)+"\n")
print("PASS",result["parent"]["blobs_verified"],"parent blobs; initialized submodules:",{k:v.get("blobs_verified") for k,v in result["submodules"].items()})

