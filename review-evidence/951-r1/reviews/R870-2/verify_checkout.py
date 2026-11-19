#!/usr/bin/env python3
"""Prove physical tracked bytes, modes, index and required pinned checkouts."""
import hashlib, os, pathlib, stat, subprocess, sys
def git(root,*args):
    return subprocess.check_output(["git","-C",str(root),*args],env={**os.environ,"GIT_NO_REPLACE_OBJECTS":"1"})
def verify(root,rev,label):
    rows=git(root,"ls-tree","-rz","--full-tree",rev).split(b"\0")
    tree={}
    for row in rows:
        if not row: continue
        meta,path=row.split(b"\t",1)
        mode,kind,oid=meta.split()
        tree[path]=(mode,oid)
        if kind==b"commit": continue
        p=root/os.fsdecode(path)
        st=p.lstat()
        if mode==b"120000":
            assert stat.S_ISLNK(st.st_mode),(label,path,"not symlink")
            data=os.fsencode(os.readlink(p))
        else:
            assert stat.S_ISREG(st.st_mode),(label,path,"not regular")
            assert bool(st.st_mode & 0o111)==(mode==b"100755"),(label,path,"mode")
            data=p.read_bytes()
        digest=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest().encode()
        assert digest==oid,(label,path,"blob")
    index={}
    for row in git(root,"ls-files","--stage","-z").split(b"\0"):
        if not row: continue
        meta,path=row.split(b"\t",1)
        mode,oid,stage=meta.split()
        assert stage==b"0",(label,path,"stage")
        assert path not in index,(label,path,"duplicate")
        index[path]=(mode,oid)
    assert index==tree,(label,"index differs")
    assert git(root,"rev-parse","HEAD").strip()==rev.encode(),(label,"HEAD")
    print(label,rev,"PASS",len(tree),"tracked entries: physical blobs/modes and complete index")
    return tree
root=pathlib.Path(sys.argv[1] if len(sys.argv)>1 else ".").resolve()
head="f09d82e05270bdd77e07f7fc2e14d064c1123be8"
tree=verify(root,head,"candidate")
for name in ("gptp-processor","protocol-processor","third_party/lwSRP","third_party/tsn-c-stack","third_party/verilog-axis"):
    mode,oid=tree[os.fsencode(name)]
    assert mode==b"160000"
    sub=root/name
    assert not sub.is_symlink()
    assert (sub/".git").is_file(),"registered submodule gitfile required"
    superpath=git(sub,"rev-parse","--show-superproject-working-tree").decode().strip()
    assert pathlib.Path(superpath).resolve()==root
    verify(sub,oid.decode(),name)
assert git(root,"status","--porcelain","--untracked-files=all")==b""
print("Working tree status empty, including untracked files")
print("Optional external submodule uninitialized and unused; tree/index gitlink verified only")
print("RESTORE/INTEGRITY PASS; no candidate source files changed by review")

