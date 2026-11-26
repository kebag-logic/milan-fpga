#!/usr/bin/env python3
"""Verify tracked blobs, modes, index and registered dependency gitlinks directly."""
import hashlib, json, os, pathlib, stat, subprocess, sys
root=pathlib.Path(sys.argv[1]).resolve()
head="5b5b0765143593f05f5a85ecd4ab1d089d23a3e4"
tree="d0508027199923e8d3464eb9d55ef185af10b6f5"
env=dict(os.environ,GIT_NO_REPLACE_OBJECTS="1")
def git(r,*args):return subprocess.check_output(["git",*args],cwd=r,env=env)
assert git(root,"rev-parse","HEAD").decode().strip()==head
assert git(root,"rev-parse","HEAD^{tree}").decode().strip()==tree
counts={};pins={}
def check(r,rev,label):
 entries=[x for x in git(r,"ls-tree","-rz",rev).split(b"\0") if x]
 expected=[];n=0
 for row in entries:
  meta,name=row.split(b"\t",1);mode,kind,oid=meta.split()
  expected.append(mode+b" "+oid+b" 0\t"+name)
  path=r/os.fsdecode(name)
  if kind==b"commit":
   if label=="root":pins[os.fsdecode(name)]=oid.decode()
   if not (path/".git").exists():
    assert name==b"external" and (not path.exists() or not any(path.iterdir()))
    continue
   assert git(path,"rev-parse","HEAD").strip()==oid
   assert pathlib.Path(git(path,"rev-parse","--show-superproject-working-tree").decode().strip()).resolve()==r
   check(path,oid.decode(),os.fsdecode(name));continue
  st=path.lstat()
  if mode==b"120000":assert stat.S_ISLNK(st.st_mode);data=os.fsencode(os.readlink(path))
  else:
   assert stat.S_ISREG(st.st_mode)
   assert bool(st.st_mode&0o111)==(mode==b"100755")
   data=path.read_bytes()
  assert hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()==oid.decode(),str(path)
  n+=1
 actual=[x for x in git(r,"ls-files","--stage","-z").split(b"\0") if x]
 assert sorted(actual)==sorted(expected),label+" index differs"
 assert not git(r,"ls-files","--others","--exclude-standard","-z"),label+" untracked sources"
 counts[label]=n
check(root,head,"root")
print(json.dumps(dict(head=head,tree=tree,tracked_blobs_verified=counts,gitlinks=pins,verdict="PASS"),indent=2))
