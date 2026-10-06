#!/usr/bin/env python3
"""Compare tracked bytes, filesystem modes, index entries and required gitlinks."""
import hashlib, json, os, pathlib, stat, subprocess, sys
repo=pathlib.Path(sys.argv[1]).resolve()
head="6c94e9f5f496ac25f8c4e31f9e3685c725de29f3"
env=dict(os.environ,GIT_NO_REPLACE_OBJECTS="1")
def git(root,*args): return subprocess.check_output(["git","-C",str(root),*args],env=env)
def check(root, rev):
    assert git(root,"rev-parse","HEAD").decode().strip()==rev
    entries={}
    for row in git(root,"ls-tree","-rz",rev).split(b"\0"):
        if not row: continue
        desc,path=row.split(b"\t",1);mode,kind,oid=desc.decode().split(); name=path.decode()
        entries[name]=(mode,oid)
    idx={}
    for row in git(root,"ls-files","--stage","-z").split(b"\0"):
        if not row: continue
        desc,path=row.split(b"\t",1);mode,oid,stage=desc.decode().split()
        assert stage=="0", (str(root),path,stage)
        idx[path.decode()]=(mode,oid)
    assert idx==entries, "index differs from pinned tree"
    count=0; submodules={}
    for name,(mode,oid) in entries.items():
        path=root/name
        if mode=="160000": submodules[name]=oid; continue
        st=path.lstat()
        if mode=="120000":
            assert stat.S_ISLNK(st.st_mode),name
            data=os.readlink(path).encode()
        else:
            assert stat.S_ISREG(st.st_mode),name
            assert bool(st.st_mode&0o111)==(mode=="100755"),name
            data=path.read_bytes()
        actual=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
        assert actual==oid,name
        count+=1
    return {"head":rev,"tree":git(root,"rev-parse",rev+"^{tree}").decode().strip(),"tracked_blobs_verified":count,"index":"exact","gitlinks":submodules}
result={"superproject":check(repo,head)}
for name in ("protocol-processor","gptp-processor","third_party/verilog-axis"):
    assert (repo/name/".git").is_file(),name
    result[name]=check(repo/name,result["superproject"]["gitlinks"][name])
result["external"]="gitlink checked; optional checkout not initialized"
print(json.dumps(result,indent=2))
