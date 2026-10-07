#!/usr/bin/env python3
"""Prove tracked raw bytes, executable modes, index entries and required gitlinks."""
import hashlib, os, stat, subprocess, sys
from pathlib import Path
root=Path(sys.argv[1]).resolve()
expected="8b78a8fd36864246336c71c061ac4f21d629952f"
env={**os.environ,"GIT_NO_REPLACE_OBJECTS":"1"}
def git(repo,*args):
 return subprocess.check_output(["git","-C",str(repo),*args],env=env)
def verify(repo,rev,label):
 assert git(repo,"rev-parse","HEAD").decode().strip()==rev
 records=git(repo,"ls-tree","-rz",rev).split(b"\0")
 index={}
 for row in git(repo,"ls-files","--stage","-z").split(b"\0"):
  if row:
   meta,name=row.split(b"\t",1); mode,oid,stage=meta.split(); assert stage==b"0"
   index[name]=(mode,oid)
 count=0; links={}
 for row in records:
  if not row: continue
  meta,name=row.split(b"\t",1); mode,kind,oid=meta.split()
  assert index.pop(name)==(mode,oid),name
  path=repo/os.fsdecode(name)
  if kind==b"commit": links[os.fsdecode(name)]=oid.decode(); continue
  st=path.lstat()
  if mode==b"120000":
   assert stat.S_ISLNK(st.st_mode); data=os.fsencode(os.readlink(path))
  else:
   assert stat.S_ISREG(st.st_mode),name
   assert bool(st.st_mode&0o111)==(mode==b"100755"),name
   data=path.read_bytes()
  blob=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
  assert blob==oid.decode(),name
  count+=1
 assert not index,index
 assert not git(repo,"diff","--cached","--name-only",rev).strip()
 flags=git(repo,"ls-files","-v").splitlines()
 assert not any(x[:1].islower() or x.startswith(b"S ") for x in flags)
 print(f"PASS {label}: head {rev}; {count} tracked blobs match raw bytes/modes and exact stage-0 index; {len(links)} gitlinks")
 return links
links=verify(root,expected,"candidate")
assert git(root,"rev-parse","HEAD^{tree}").decode().strip()=="ee59c5cb2b3adc55d3907eac24f9a5e27466b6c8"
for name in ("protocol-processor","gptp-processor","third_party/verilog-axis"):
 sub=root/name
 assert (sub/".git").is_file()
 verify(sub,links[name],name)
 print("PASS registered submodule",name,git(sub,"rev-parse","--show-superproject-working-tree").decode().strip()==str(root))
print("External optional submodule remains uninitialized; required gitlinks verified.")
print("PASS exact head/tree, blobs, modes and index verified")
