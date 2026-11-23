#!/usr/bin/env python3
"""Check raw working bytes, modes, index entries and required submodule pins."""
import argparse, pathlib, subprocess, hashlib, stat, json
p=argparse.ArgumentParser();p.add_argument('source',type=pathlib.Path);a=p.parse_args()
def git(root,*args): return subprocess.check_output(['git',*args],cwd=root)
def verify(root,expected):
 head=git(root,'rev-parse','HEAD').decode().strip();assert head==expected
 entries={};count=0
 for row in git(root,'ls-tree','-rz','HEAD').split(b'\0'):
  if not row:continue
  info,name=row.split(b'\t',1);mode,typ,oid=info.split();entries[name]=(mode,oid)
  if typ!=b'blob':continue
  path=root/name.decode();s=path.lstat()
  if mode==b'120000':data=str(path.readlink()).encode();actual=b'120000'
  else:data=path.read_bytes();actual=b'100755' if s.st_mode & stat.S_IXUSR else b'100644'
  assert actual==mode,(name,'mode')
  h=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest().encode()
  assert h==oid,(name,'bytes');count+=1
 index={}
 for row in git(root,'ls-files','--stage','-z').split(b'\0'):
  if not row:continue
  info,name=row.split(b'\t',1);mode,oid,stage=info.split();assert stage==b'0';index[name]=(mode,oid)
 assert index==entries,'index mismatch'
 return dict(head=head,tree=git(root,'rev-parse','HEAD^{tree}').decode().strip(),blobs=count,bytes_modes_index='PASS')
r={'parent':verify(a.source,'2e278379c1ae9ea09063b3e3cb183d0e8a3f0929'),'submodules':{}}
for row in git(a.source,'ls-tree','-r','HEAD').decode().splitlines():
 info,name=row.split('\t',1);mode,typ,oid=info.split()
 if mode!='160000':continue
 if name=='external':r['submodules'][name]={'gitlink':oid,'status':'uninitialized; outside required gate set'};continue
 r['submodules'][name]=verify(a.source/name,oid)
r['status']='PASS'
print(json.dumps(r,indent=2))
