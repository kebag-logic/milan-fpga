#!/usr/bin/env python3
"""Verify exact commit, index, working blobs/modes, and tracked submodule links."""
import hashlib, json, os, pathlib, stat, subprocess, sys
root=pathlib.Path(sys.argv[1]).resolve()
def git(*a): return subprocess.check_output(["rtk","proxy","git","-C",str(root),*a])
head=git("rev-parse","HEAD").decode().strip()
assert head=="4029dc5de2a0a540d6a015c747319fbee7abba2e",head
detached=subprocess.run(["rtk","proxy","git","-C",str(root),"symbolic-ref","-q","HEAD"],capture_output=True)
assert detached.returncode==1,detached.stdout
tree=git("rev-parse","HEAD^{tree}").decode().strip()
assert tree=="33ec74ea7812208d7648475763816bc14a80bc8a",tree
entries=[]
for row in git("ls-tree","-rz","HEAD").split(b"\0"):
 if not row: continue
 meta,path=row.split(b"\t",1); mode,kind,oid=meta.decode().split(); entries.append((mode,kind,oid,os.fsdecode(path)))
index={}
for row in git("ls-files","-sz").split(b"\0"):
 if not row: continue
 meta,path=row.split(b"\t",1); mode,oid,stage=meta.decode().split(); assert stage=="0"; index[os.fsdecode(path)]=(mode,oid)
assert len(index)==len(entries)
links=[]
for mode,kind,oid,path in entries:
 assert index[path]==(mode,oid),("index",path)
 f=root/path
 if kind=="commit":
  actual=subprocess.check_output(["rtk","proxy","git","-C",str(f),"rev-parse","HEAD"]).decode().strip()
  assert actual==oid,(path,oid,actual); links.append({"path":path,"sha":oid}); continue
 if mode=="120000": data=os.fsencode(os.readlink(f))
 else:
  assert f.is_file() and not f.is_symlink(),path
  actual="100755" if f.stat().st_mode & stat.S_IXUSR else "100644"
  assert mode==actual,("mode",path,mode,actual); data=f.read_bytes()
 actual=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
 assert actual==oid,("blob",path,oid,actual)
status=git("status","--porcelain=v1").decode()
assert not status,status
print(json.dumps({"head":head,"tree":tree,"detached":True,"tracked_blobs_and_gitlinks":len(entries),"index_matches_tree":True,"working_bytes_and_modes_match":True,"required_submodule_gitlinks":links,"status_porcelain":status},indent=2))
