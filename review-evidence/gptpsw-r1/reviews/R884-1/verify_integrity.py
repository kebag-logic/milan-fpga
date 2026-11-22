#!/usr/bin/env python3
"""Verify tracked bytes, modes, index entries and required gitlinks without modifying them."""
from pathlib import Path
import hashlib, os, stat, subprocess, sys
root=Path(sys.argv[1]).resolve()
HEAD="f15b3a7d2bf1ba84d14140a4cda8a193d2e6b1c9"
TREE="44de68bf9dfc3534963fc1e11a6a86477c669ff1"
required={"protocol-processor","gptp-processor","third_party/verilog-axis","third_party/tsn-c-stack","third_party/lwSRP"}
def git(r,*a): return subprocess.check_output(["git","-C",str(r),*a])
def verify(r,expected,recursive=False):
 actual=git(r,"rev-parse","HEAD").decode().strip(); assert actual==expected,(r,actual,expected)
 entries={}
 for rec in git(r,"ls-tree","-rz","HEAD").split(b"\0"):
  if not rec: continue
  meta,name=rec.split(b"\t",1); mode,kind,oid=meta.decode().split(); entries[os.fsdecode(name)]=(mode,kind,oid)
 index={}
 for rec in git(r,"ls-files","--stage","-z").split(b"\0"):
  if not rec: continue
  meta,name=rec.split(b"\t",1); mode,oid,stage=meta.decode().split(); assert stage=="0";index[os.fsdecode(name)]=(mode,oid)
 assert index=={n:(m,o) for n,(m,k,o) in entries.items()},"index differs from HEAD"
 blobs=0
 for n,(mode,kind,oid) in entries.items():
  f=r/n
  if kind=="commit":
   print("gitlink",n,oid)
   if recursive and n in required: verify(f,oid)
   continue
  st=f.lstat()
  if mode=="120000": assert stat.S_ISLNK(st.st_mode);data=os.fsencode(os.readlink(f))
  else:
   assert stat.S_ISREG(st.st_mode),(n,"not regular")
   assert bool(st.st_mode&0o111)==(mode=="100755"),(n,"mode differs")
   data=f.read_bytes()
  digest=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
  assert digest==oid,(n,"blob differs",digest,oid)
  blobs+=1
 print("PASS",str(r.relative_to(root)) or ".",actual,"blobs",blobs,"index entries",len(index))
assert git(root,"rev-parse","HEAD^{tree}").decode().strip()==TREE
verify(root,HEAD,True)
print("SUPERPROJECT_STATUS",repr(git(root,"status","--porcelain=v1","--untracked-files=all").decode()))
print("PASS exact head/tree, tracked bytes, executable/symlink modes, stage-zero indexes and five required submodule gitlinks")
