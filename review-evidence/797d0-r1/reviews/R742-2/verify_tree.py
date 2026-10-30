#!/usr/bin/env python3
"""Verify HEAD bytes, modes and index plus required dependency gitlinks without filters."""
import argparse,hashlib,os,stat,subprocess
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument("repo",type=Path);a=ap.parse_args();root=a.repo.resolve()
required={"protocol-processor","gptp-processor","third_party/verilog-axis","third_party/tsn-c-stack"}
def git(path,*args):return subprocess.check_output(["git","-C",str(path),*args])
def check(path,expected=None):
 head=git(path,"rev-parse","HEAD").decode().strip()
 if expected:assert head==expected,(path,head,expected)
 entries={}
 for record in git(path,"ls-tree","-rz","HEAD").split(b"\0"):
  if not record:continue
  meta,name=record.split(b"\t",1);mode,kind,oid=meta.decode().split();entries[name.decode()]=(mode,kind,oid)
 index={}
 for record in git(path,"ls-files","--stage","-z").split(b"\0"):
  if not record:continue
  meta,name=record.split(b"\t",1);mode,oid,stage=meta.decode().split();assert stage=="0";index[name.decode()]=(mode,oid)
 assert index=={n:(m,o) for n,(m,k,o) in entries.items()},"index differs from HEAD"
 blobs=0;modules=[]
 for name,(mode,kind,oid) in entries.items():
  f=path/name
  if kind=="commit":modules.append((name,oid));continue
  if mode=="120000":assert f.is_symlink();raw=os.readlink(f).encode()
  else:
   assert f.is_file() and not f.is_symlink(),name
   assert bool(f.stat().st_mode&stat.S_IXUSR)==(mode=="100755"),name
   raw=f.read_bytes()
  actual=hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest();assert actual==oid,name
  blobs+=1
 print(("root" if path==root else str(path.relative_to(root))),head,"tracked blobs",blobs,"bytes/modes/index PASS")
 return modules
mods=check(root,"3e6d92c17bd1d2118e9bc3d8a0e1fae90a69e8ee")
for name,oid in mods:
 f=root/name
 if (f/".git").exists():check(f,oid)
 else:
  assert name not in required,name
  print(name,"uninitialized optional gitlink",oid)
assert required.issubset({n for n,o in mods})
print("PASS all tracked entries and required dependency pins")
