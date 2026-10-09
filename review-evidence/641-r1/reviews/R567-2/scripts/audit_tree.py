#!/usr/bin/env python3
"""Verify tracked bytes, modes, index, gitlinks, and required populations."""
import hashlib, json, os, stat, subprocess, sys
from pathlib import Path
root=Path(sys.argv[1]).resolve()
env=dict(os.environ,GIT_NO_REPLACE_OBJECTS="1")
def git(where,*args):
 return subprocess.check_output(["git","-C",str(where),*args],env=env)
def audit(where,rev):
 entries={}; files=0
 for record in git(where,"ls-tree","-rz",rev).split(b"\0"):
  if not record:continue
  meta,name=record.split(b"\t",1);mode,kind,oid=meta.decode().split();name=name.decode();entries[name]=(mode,oid)
  if kind=="commit":continue
  p=where/name;s=p.lstat()
  if mode=="120000":
   assert stat.S_ISLNK(s.st_mode),name;data=os.fsencode(os.readlink(p))
  else:
   assert stat.S_ISREG(s.st_mode),name
   assert ("100755" if s.st_mode&0o111 else "100644")==mode,name
   data=p.read_bytes()
  got=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
  assert got==oid,(name,got,oid);files+=1
 index={}
 for record in git(where,"ls-files","--stage","-z").split(b"\0"):
  if not record:continue
  meta,name=record.split(b"\t",1);mode,oid,stage=meta.decode().split()
  assert stage=="0",name;index[name.decode()]=(mode,oid)
 assert index==entries,"index differs from committed tree"
 return {"revision":git(where,"rev-parse",rev).decode().strip(),"tree":git(where,"rev-parse",rev+"^{tree}").decode().strip(),"verified_files":files,"index_entries":len(index),"bytes_modes_index":"PASS"},entries
result,entries=audit(root,"HEAD")
assert result["revision"]=="614b4aa5f408d75673b546ce6efb6ef126437be2"
result["submodules"]={}
for sub in ("protocol-processor","gptp-processor","third_party/verilog-axis"):
 mode,pin=entries[sub];assert mode=="160000"
 assert git(root/sub,"rev-parse","HEAD").decode().strip()==pin
 a,_=audit(root/sub,pin);result["submodules"][sub]=a
result["other_gitlinks"]={n:oid for n,(mode,oid) in entries.items() if mode=="160000" and n not in result["submodules"]}
result["status"]=git(root,"status","--porcelain=v1","--untracked-files=all").decode()
print(json.dumps(result,indent=2))
