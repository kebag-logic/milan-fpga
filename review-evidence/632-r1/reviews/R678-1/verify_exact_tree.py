#!/usr/bin/env python3
"""Verify raw tracked bytes, file modes, the complete index, and required gitlinks."""
import argparse,hashlib,os,pathlib,subprocess
p=argparse.ArgumentParser();p.add_argument("repo",type=pathlib.Path);a=p.parse_args()
def git(root,*args):return subprocess.check_output(["git","-C",str(root),*args])
def verify(root,expected):
    actual=git(root,"rev-parse","HEAD").decode().strip();assert actual==expected,(root.name,actual,expected)
    tree=git(root,"ls-tree","-r","-z","HEAD").split(b"\0"); expect=[]; count=0; links=[]
    for entry in tree:
        if not entry:continue
        meta,path=entry.split(b"\t",1);mode,kind,oid=meta.split();expect.append(mode+b" "+oid+b" 0\t"+path)
        if kind==b"commit":links.append((os.fsdecode(path),oid.decode()));continue
        f=root/os.fsdecode(path)
        if mode==b"120000":assert f.is_symlink();body=os.fsencode(os.readlink(f))
        else:
            assert not f.is_symlink();body=f.read_bytes();actual_mode=b"100755" if f.stat().st_mode&0o111 else b"100644";assert mode==actual_mode,(str(path),mode,actual_mode)
        got=hashlib.sha1(b"blob "+str(len(body)).encode()+b"\0"+body).hexdigest();assert got==oid.decode(),str(path)
        count+=1
    index=git(root,"ls-files","--stage","-z").split(b"\0");assert sorted(e for e in index if e)==sorted(expect),"index mismatch"
    print(root.name,"HEAD",actual,"tracked blobs",count,"bytes/modes/index PASS")
    return links
head="f1fda3f1f87c64801e436e129326b5bd5952bf20";links=dict(verify(a.repo,head))
assert git(a.repo,"rev-parse","HEAD^{tree}").decode().strip()=="b5bb11d04270aeb2721f1961c4d85a11fc7debde"
for sub in ["protocol-processor","gptp-processor","third_party/verilog-axis","third_party/tsn-c-stack"]:
    assert (a.repo/sub/".git").is_file(),"submodule is not initialized at its gitlink"
    verify(a.repo/sub,links[sub]);print("gitlink",sub,links[sub],"PASS")
print("Exact published head/tree, tracked bytes/modes/index and four required submodule gitlinks verified.")
