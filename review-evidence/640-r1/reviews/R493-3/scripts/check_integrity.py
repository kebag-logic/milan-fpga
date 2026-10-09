#!/usr/bin/env python3
"""Verify exact tree, index, working bytes/modes, and required submodules."""
import hashlib, os, stat, subprocess, sys
from pathlib import Path
root=Path(sys.argv[1]).resolve()
expected="173362fc21c33078b7feed42a24a3636907010f5"
env=dict(os.environ,GIT_NO_REPLACE_OBJECTS="1")
def git(at,*args):
    return subprocess.check_output(["git","-C",str(at),*args],env=env)
def verify(at,rev):
    assert git(at,"rev-parse","HEAD").decode().strip()==rev
    tree=git(at,"ls-tree","-rz",rev)
    index=git(at,"ls-files","--stage","-z")
    expected_index=[]; count=0; links={}
    for entry in tree.split(b"\0"):
        if not entry: continue
        info,name=entry.split(b"\t",1); mode,kind,oid=info.split()
        expected_index.append(mode+b" "+oid+b" 0\t"+name)
        path=at/os.fsdecode(name)
        if kind==b"commit": links[os.fsdecode(name)]=oid.decode(); continue
        s=path.lstat()
        if mode==b"120000":
            assert stat.S_ISLNK(s.st_mode),name
            data=os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(s.st_mode),name
            actual_mode=b"100755" if s.st_mode&0o111 else b"100644"
            assert actual_mode==mode,(name,mode,actual_mode)
            data=path.read_bytes()
        actual=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
        assert actual==oid.decode(),name
        count+=1
    assert sorted(index.rstrip(b"\0").split(b"\0"))==sorted(expected_index),"index differs"
    print(f"PASS {at.name}: HEAD={rev}, {count} exact blobs/modes, complete stage-0 index")
    return links
assert git(root,"rev-parse","HEAD^{tree}").decode().strip()=="fbc807d191d0c98f7fac332502e93f9c65c81138"
links=verify(root,expected)
for name in ("protocol-processor","gptp-processor","third_party/verilog-axis"):
    sub=root/name
    assert not sub.is_symlink() and (sub/".git").is_file(),name
    assert git(sub,"rev-parse","--show-superproject-working-tree").decode().strip()==str(root)
    verify(sub,links[name])
print("PASS required gitlinks and registered submodules; external and lwSRP are outside required population")
print("status:",git(root,"status","--porcelain=v1").decode().strip() or "clean")
