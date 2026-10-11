#!/usr/bin/env python3
"""Verify exact committed/index/worktree bytes and modes, including gitlinks."""
import argparse, hashlib, json, os, stat, subprocess
from pathlib import Path
ap=argparse.ArgumentParser(); ap.add_argument("root",type=Path); a=ap.parse_args(); r=a.root.resolve()
def git(*args): return subprocess.check_output(["git","-C",str(r),*args])
head=git("rev-parse","HEAD").decode().strip(); tree=git("rev-parse","HEAD^{tree}").decode().strip()
assert head=="02063dc1b593d422406991bf0bc60e5cc47828ff"; assert tree=="2fd23c4ce9d7f23f73d6b4440b494e62d88a2682"
entries=[]; links=[]
for ent in git("ls-tree","-rz","HEAD").split(b"\0"):
 if not ent: continue
 meta,raw=ent.split(b"\t",1); mode,kind,oid=meta.decode().split(); name=os.fsdecode(raw); f=r/name
 if mode=="160000":
  links.append({"path":name,"expected":oid,"actual":subprocess.check_output(["git","-C",str(f),"rev-parse","HEAD"]).decode().strip()}); assert links[-1]["actual"]==oid; continue
 data=os.readlink(f).encode() if mode=="120000" else f.read_bytes()
 got=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
 actual="120000" if f.is_symlink() else ("100755" if f.stat().st_mode & stat.S_IXUSR else "100644")
 assert (got,actual)==(oid,mode),(name,got,oid,actual,mode)
 entries.append((mode,oid,name))
assert git("write-tree").decode().strip()==tree
assert not git("status","--porcelain=v2","--untracked-files=all"),"checkout has changes"
print(json.dumps({"head":head,"tree":tree,"tracked_files_checked":len(entries),"index_tree_matches":True,"worktree_bytes_modes_match":True,"submodule_gitlinks":links,"status":"clean","entries":entries},indent=2))
