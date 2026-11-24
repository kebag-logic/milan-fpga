#!/usr/bin/env python3
"""Verify raw tracked blob bytes, modes, stage-zero index and gitlinks.
Usage: python3 integrity.py REPO
No Git status cache, filters or replacement refs contribute to byte proof.
"""
import hashlib, os, pathlib,stat,subprocess,sys
repo=pathlib.Path(sys.argv[1]).resolve()
env=os.environ.copy();env["GIT_NO_REPLACE_OBJECTS"]="1"
expected="bbfdb6746d585e490508783dc8a88c79fbab02c0"
def git(root,*args,input=None):return subprocess.check_output(["git","-C",str(root),*args],env=env,input=input)
def inspect(root,rev):
 entries=git(root,"ls-tree","-rz",rev).split(b"\0")
 want={};links=[];n=0
 for entry in entries:
  if not entry:continue
  meta,rawpath=entry.split(b"\t",1);mode,kind,oid=meta.split();p=root/os.fsdecode(rawpath)
  want[rawpath]=(mode,oid,b"0")
  if kind==b"commit": links.append((p,oid.decode()));continue
  st=p.lstat()
  if mode==b"120000":assert stat.S_ISLNK(st.st_mode);data=os.fsencode(os.readlink(p))
  else:
   assert stat.S_ISREG(st.st_mode), str(p.relative_to(repo))
   assert bool(st.st_mode&0o111)==(mode==b"100755"),str(p.relative_to(repo))
   data=p.read_bytes()
  digest=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest().encode()
  assert digest==oid,str(p.relative_to(repo))
  n+=1
 got={}
 for entry in git(root,"ls-files","--stage","-z").split(b"\0"):
  if not entry:continue
  meta,path=entry.split(b"\t",1);mode,oid,stage=meta.split();assert path not in got
  got[path]=(mode,oid,stage)
 assert got==want,"index differs from committed tree"
 label="superproject" if root==repo else str(root.relative_to(repo))
 print(label,rev,"PASS",n,"raw blobs; modes and index equal")
 return links
assert git(repo,"rev-parse","HEAD").decode().strip()==expected
assert git(repo,"rev-parse","HEAD^{tree}").decode().strip()=="eb8282dfbfa9d8dc2e1c87bc3c09b5c010d30263"
links=inspect(repo,expected)
for root,rev in links:
 if root.name=="external":
  print("external",rev,"gitlink preserved; intentionally uninitialized, no active consumer");continue
 assert (root/".git").is_file(),"required registered submodule absent"
 assert git(root,"rev-parse","HEAD").decode().strip()==rev
 inspect(root,rev)
print("PASS exact source bytes/modes/index and all required submodule gitlinks")
