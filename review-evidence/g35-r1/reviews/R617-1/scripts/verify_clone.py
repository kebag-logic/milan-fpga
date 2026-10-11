#!/usr/bin/env python3
"""Verify HEAD, index, bytes, executable modes, and required gitlinks without writes.
Usage: verify_clone.py CLONE EXPECTED_HEAD EXPECTED_TREE
"""
import os, subprocess, sys
from pathlib import Path
c=Path(sys.argv[1]); h,t=sys.argv[2:4]
def git(*args): return subprocess.check_output(["git","-C",str(c),*args])
errors=[]
for label,args,expected in [("HEAD",["rev-parse","HEAD"],h),("tree",["rev-parse","HEAD^{tree}"],t),("index tree",["write-tree"],t)]:
 value=git(*args).decode().strip(); print(label+": "+value)
 if value!=expected: errors.append(label+" mismatch")
tree={}
for row in git("ls-tree","-rz","HEAD").split(b"\0"):
 if row:
  meta,path=row.split(b"\t",1);mode,kind,blob=meta.split();tree[path]=(mode,blob)
index={}
for row in git("ls-files","--stage","-z").split(b"\0"):
 if row:
  meta,path=row.split(b"\t",1);mode,blob,stage=meta.split();index[path]=(mode,blob)
  if stage!=b"0":errors.append("unmerged index entry")
if tree!=index:errors.append("index modes/blobs/paths differ from HEAD")
links=[]
for path,(mode,blob) in index.items():
 rel=os.fsdecode(path);f=c/rel
 if mode==b"160000":
  links.append((rel,blob.decode()))
  actual=subprocess.check_output(["git","-C",str(f),"rev-parse","HEAD"]).strip()
  if actual!=blob:errors.append("gitlink checkout mismatch: "+rel)
 elif mode==b"120000":
  data=os.fsencode(os.readlink(f)); actual=subprocess.check_output(["git","hash-object","--stdin"],input=data).strip()
  if actual!=blob:errors.append("symlink differs: "+rel)
 else:
  actual=git("hash-object","--no-filters","--",rel).strip()
  if actual!=blob:errors.append("worktree blob differs: "+rel)
  if bool(f.stat().st_mode & 0o111)!=(mode==b"100755"):errors.append("executable mode differs: "+rel)
status=git("status","--porcelain=v1","--ignored","--untracked-files=all")
if status:errors.append("nonempty status: "+status.decode())
print(f"Tracked entries: {len(index)}; required gitlinks: {len(links)}")
for path,blob in links:print(f"gitlink {path}: {blob}")
print("Errors:",len(errors)); print("\n".join(errors)); print("VERIFY FAILED" if errors else "VERIFY OK")
sys.exit(bool(errors))
