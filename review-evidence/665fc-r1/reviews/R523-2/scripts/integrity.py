#!/usr/bin/env python3
"""Verify exact tracked object bytes, modes, index and required gitlinks."""
import argparse, hashlib, json, os, pathlib, stat, subprocess
p=argparse.ArgumentParser();p.add_argument("--source",type=pathlib.Path,default=pathlib.Path.cwd());a=p.parse_args()
root=a.source.resolve();env=dict(os.environ,GIT_NO_REPLACE_OBJECTS="1")
def git(path,*args):return subprocess.check_output(["git",*args],cwd=path,env=env)
def verify(path,head):
    assert git(path,"rev-parse","HEAD").decode().strip()==head
    entries={}
    for row in git(path,"ls-tree","-rz",head).split(b"\0"):
        if not row:continue
        meta,name=row.split(b"\t",1);mode,kind,oid=meta.split();entries[name]=(mode,kind,oid)
    idx={}
    for row in git(path,"ls-files","--stage","-z").split(b"\0"):
        if not row:continue
        meta,name=row.split(b"\t",1);mode,oid,stage=meta.split();assert stage==b"0"
        assert name not in idx;idx[name]=(mode,oid)
    assert idx=={n:(m,o) for n,(m,k,o) in entries.items()},"index does not match tree"
    blobs=0;links={}
    for n,(mode,kind,oid) in entries.items():
        file=path/os.fsdecode(n)
        if kind==b"commit":links[os.fsdecode(n)]=oid.decode();continue
        s=file.lstat()
        if mode==b"120000":assert stat.S_ISLNK(s.st_mode);data=os.fsencode(os.readlink(file))
        else:
            assert stat.S_ISREG(s.st_mode),str(file)
            assert (mode==b"100755")==bool(s.st_mode & 0o111),str(file)
            data=file.read_bytes()
        actual=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
        assert actual==oid.decode(),str(file)
        blobs+=1
    return dict(head=head,tree=git(path,"rev-parse",head+"^{tree}").decode().strip(),verified_blobs=blobs,index_matches=True,gitlinks=links)
head="db9aa8c9b135b34ff3d070a979dee70440b37cc6"
out={"superproject":verify(root,head)}
for name in ("protocol-processor","gptp-processor","third_party/verilog-axis"):
    path=root/name
    assert (path/".git").is_file() and not (path/".git").is_symlink()
    assert git(path,"rev-parse","--show-superproject-working-tree").decode().strip()==str(root)
    out[name]=verify(path,out["superproject"]["gitlinks"][name])
out["optional_external"]="gitlink verified; checkout uninitialized, unused by focused checks"
print(json.dumps(out,indent=2))
