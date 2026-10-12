#!/usr/bin/env python3
"""Prove tracked bytes, modes, index entries and initialized required pins."""
import hashlib, json, os, stat, subprocess, sys
from pathlib import Path
root=Path(sys.argv[1]).resolve()
expected="acadfacd52c6daabf892d6ebe99da11ca06748cb"
env=dict(os.environ,GIT_NO_REPLACE_OBJECTS="1")
def git(repo,*args):
    return subprocess.check_output(["git","-C",str(repo),*args],env=env)
def check(repo,head):
    assert git(repo,"rev-parse","HEAD").decode().strip()==head
    tree=git(repo,"ls-tree","-rz",head)
    expected_index=[]; n=0; links={}
    for rec in tree.split(b"\0"):
        if not rec: continue
        meta,path=rec.split(b"\t",1);mode,kind,oid=meta.split()
        expected_index.append(mode+b" "+oid+b" 0\t"+path+b"\0")
        if kind==b"commit":
            links[os.fsdecode(path)]=oid.decode();continue
        f=repo/os.fsdecode(path);st=f.lstat()
        if mode==b"120000":
            assert stat.S_ISLNK(st.st_mode),str(f)
            data=os.fsencode(os.readlink(f))
        else:
            assert stat.S_ISREG(st.st_mode),str(f)
            assert bool(st.st_mode&0o111)==(mode==b"100755"),str(f)
            data=f.read_bytes()
        actual=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
        assert actual==oid.decode(),str(f)
        n+=1
    assert git(repo,"ls-files","--stage","-z")==b"".join(expected_index),"index differs"
    return {"head":head,"tree":git(repo,"rev-parse",head+"^{tree}").decode().strip(),"verified_blobs":n,"gitlinks":links}
a={"parent":check(root,expected)}
for name in ("protocol-processor","gptp-processor","third_party/verilog-axis"):
    pin=a["parent"]["gitlinks"][name]
    assert (root/name/".git").is_file(),"required registered submodule missing"
    a[name]=check(root/name,pin)
print(json.dumps(a,indent=2))
