#!/usr/bin/env python3
"""Read-only canonical HEAD, index, disk bytes/modes and initialized gitlink verification."""
import argparse, hashlib, os, stat, subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("checkout",type=Path);a=p.parse_args();root=a.checkout.resolve()
env={**os.environ,"GIT_NO_REPLACE_OBJECTS":"1","GIT_GRAFT_FILE":"/dev/null/no-grafts"}
def git(repo,*args):return subprocess.check_output(["git","-C",str(repo),*args],env=env)
def inspect(repo,expected,label):
 head=git(repo,"rev-parse","HEAD").decode().strip();assert head==expected,(label,head)
 tree=git(repo,"rev-parse","HEAD^{tree}").decode().strip()
 print(label,"HEAD",head,"tree",tree)
 want={}
 for row in git(repo,"ls-tree","-rz","HEAD").split(b"\0"):
  if not row:continue
  meta,name=row.split(b"\t",1);mode,kind,oid=meta.split();want[name]=(mode,oid)
 index={}
 for row in git(repo,"ls-files","--stage","-z").split(b"\0"):
  if not row:continue
  meta,name=row.split(b"\t",1);mode,oid,stage=meta.split();assert stage==b"0",(label,name,stage);index[name]=(mode,oid)
 assert want==index,(label,"index differs")
 flagged=[r for r in git(repo,"ls-files","-v","-z").split(b"\0") if r and (r[:1].islower() or r[:1]==b"S")];assert not flagged,(label,flagged)
 algo=git(repo,"rev-parse","--show-object-format").decode().strip();count=0;links=[]
 for name,(mode,oid) in want.items():
  path=repo/os.fsdecode(name)
  if mode==b"160000":links.append((os.fsdecode(name),oid.decode()));continue
  st=path.lstat()
  if mode==b"120000":assert stat.S_ISLNK(st.st_mode),(label,name);data=os.fsencode(os.readlink(path))
  else:
   assert stat.S_ISREG(st.st_mode),(label,name)
   actual=b"100755" if st.st_mode & stat.S_IXUSR else b"100644";assert mode==actual,(label,name,mode,actual);data=path.read_bytes()
  digest=hashlib.new(algo,b"blob %d\0"%len(data)+data).hexdigest().encode();assert digest==oid,(label,name,"bytes")
  count+=1
 assert not git(repo,"for-each-ref","refs/replace"),(label,"replace refs")
 print(label,"PASS",count,"tracked blobs/modes; exact stage-0 index; no hidden-index flags or replacement refs")
 return tree,links
head="feed95bbb6429e5af0ee3f0a24c531777279e9de";tree,links=inspect(root,head,"parent")
assert tree=="434e9291e6ceb5bd32bcd63fd13f257ed6d82bed"
required={"third_party/tsn-c-stack","third_party/lwSRP","protocol-processor","gptp-processor","third_party/verilog-axis"}
for rel,pin in links:
 if rel in required:inspect(root/rel,pin,rel)
 else:print(rel,"gitlink",pin,"not required or executed")
print("parent status",repr(git(root,"status","--porcelain=v1","--untracked-files=all").decode()))
print("PASS: exact head bytes, modes, index and required gitlinks")
