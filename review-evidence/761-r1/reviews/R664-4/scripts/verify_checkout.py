#!/usr/bin/env python3
"""Verify raw tracked bytes, modes, index entries and required submodule pins."""
import hashlib
import os
import pathlib
import stat
import subprocess
import sys
os.environ["GIT_NO_REPLACE_OBJECTS"] = "1"
root = pathlib.Path(sys.argv[1]).resolve()
head = "f3fef856dbf7f8e559fa9066f6fc9af1ea091c9d"
required = {"protocol-processor", "gptp-processor", "third_party/verilog-axis", "third_party/tsn-c-stack", "third_party/lwSRP"}
def git(path, *args):
    return subprocess.check_output(["git", "-C", str(path), *args])
def check(path, revision, label):
    assert git(path,"rev-parse","HEAD").decode().strip()==revision
    tree={}
    links=[]
    for row in git(path,"ls-tree","-rz",revision).split(b"\0"):
        if not row: continue
        meta,name=row.split(b"\t",1)
        mode,kind,oid=meta.split()
        tree[name]=(mode,oid)
        dest=path/os.fsdecode(name)
        if kind==b"commit":
            links.append((os.fsdecode(name),oid.decode()))
            continue
        st=dest.lstat()
        if mode==b"120000":
            assert stat.S_ISLNK(st.st_mode),name
            data=os.fsencode(os.readlink(dest))
        else:
            assert stat.S_ISREG(st.st_mode),name
            actual=b"100755" if st.st_mode & 0o111 else b"100644"
            assert actual==mode,(name,actual,mode)
            data=dest.read_bytes()
        got=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest().encode()
        assert got==oid,name
    idx={}
    for row in git(path,"ls-files","--stage","-z").split(b"\0"):
        if not row: continue
        meta,name=row.split(b"\t",1)
        mode,oid,stage=meta.split()
        assert stage==b"0" and name not in idx,name
        idx[name]=(mode,oid)
    assert idx==tree,label
    print(f"{label}: {len(tree)-len(links)} blobs raw bytes/modes verified; complete index equals pinned tree; {len(links)} gitlinks")
    return links
links=check(root,head,"source")
assert git(root,"rev-parse","HEAD^{tree}").decode().strip()=="c1c7c13bd84fa4d6544783ab82bfe09fa7483c6a"
for name,pin in links:
    print(f"gitlink {name} {pin}")
    if name in required:
        assert not (root/name).is_symlink()
        check(root/name,pin,name)
assert required <= {name for name,_ in links}
print("external gitlink verified in source tree/index; its uninitialized checkout is not required for this review.")
assert not git(root,"status","--porcelain","--untracked-files=no").strip()
print("PASS: exact head/tree and all required tracked populations intact. No source mutation or restoration needed.")
