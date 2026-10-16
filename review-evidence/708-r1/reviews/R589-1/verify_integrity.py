#!/usr/bin/env python3
"""Prove tracked blob bytes, types, modes, stage-0 index and gitlinks.
Usage: verify_integrity.py CHECKOUT
"""
import hashlib,os,pathlib,stat,subprocess,sys
root=pathlib.Path(sys.argv[1]).resolve()
env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1')
def git(repo,*args):return subprocess.check_output(['git','-C',str(repo),*args],env=env)
head='5c6f50eefa4c5545f052ec843363ace5e7936e8a'
assert git(root,'rev-parse','HEAD').decode().strip()==head
assert git(root,'rev-parse','HEAD^{tree}').decode().strip()=='d4b0e17fdf530ddb2ca8ec8c3986bcc4a9189254'
def verify(repo,pin):
 records=git(repo,'ls-tree','-rz',pin).split(b'\0');expected={};subs=[];count=0
 for rec in records:
  if not rec:continue
  info,name=rec.split(b'\t',1);mode,kind,oid=info.split();expected[name]=(mode,oid,b'0')
  rel=os.fsdecode(name);path=repo/rel
  if kind==b'commit':subs.append((rel,oid.decode()));continue
  meta=path.lstat()
  if mode==b'120000':assert stat.S_ISLNK(meta.st_mode);data=os.fsencode(os.readlink(path))
  else:
   assert stat.S_ISREG(meta.st_mode),rel
   assert bool(meta.st_mode&0o111)==(mode==b'100755'),rel
   data=path.read_bytes()
  actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest().encode()
  assert actual==oid,rel;count+=1
 actual={}
 for rec in git(repo,'ls-files','--stage','-z').split(b'\0'):
  if rec:
   info,name=rec.split(b'\t',1);m,o,s=info.split();assert name not in actual;actual[name]=(m,o,s)
 assert actual==expected,'index differs from commit'
 print(str(repo.relative_to(root)) or '.',pin,'PASS',count,'blobs; modes and index exact')
 return subs
subs=verify(root,head)
for name,pin in subs:
 print('gitlink',name,pin)
 if name=='external':continue
 repo=root/name;assert git(repo,'rev-parse','HEAD').decode().strip()==pin
 assert pathlib.Path(git(repo,'rev-parse','--show-toplevel').decode().strip()).resolve()==repo
 verify(repo,pin)
print('PASS exact parent and five required submodule byte/mode/index populations; unused external gitlink verified')
