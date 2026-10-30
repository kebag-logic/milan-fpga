#!/usr/bin/env python3
"""Verify tracked filesystem bytes, modes, index and initialized submodule pins."""
import hashlib,os,pathlib,stat,subprocess,sys
root=pathlib.Path(sys.argv[1]).resolve()
def git(cwd,*args):
 return subprocess.check_output(['git','--no-replace-objects','-C',str(cwd),*args])
def blob_hash(data):
 return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
def verify(path,head):
 assert git(path,'rev-parse','HEAD').decode().strip()==head
 tree=git(path,'ls-tree','-rz',head); entries=[];count=0;subs=[]
 for rec in tree.split(b'\0'):
  if not rec: continue
  meta,rel=rec.split(b'\t',1); mode,kind,oid=meta.split();name=os.fsdecode(rel);f=path/name
  entries.append(mode+b' '+oid+b' 0\t'+rel+b'\0')
  if kind==b'commit':
   subs.append((name,oid.decode()));continue
  st=f.lstat()
  if mode==b'120000':
   assert stat.S_ISLNK(st.st_mode),name
   data=os.fsencode(os.readlink(f))
  else:
   assert stat.S_ISREG(st.st_mode),name
   assert bool(st.st_mode & 0o111)==(mode==b'100755'),name
   data=f.read_bytes()
  assert blob_hash(data)==oid.decode(),name
  count+=1
 assert git(path,'ls-files','--stage','-z')==b''.join(entries),'index mismatch'
 flags=git(path,'ls-files','-v','-z').split(b'\0')
 assert all(not r or r[:1]==b'H' for r in flags),'hidden index flag'
 print(f'{path.name}: {head}; {count} tracked blobs, modes and stage-0 index match; no hidden index flags')
 for name,pin in subs:
  if name=='external':
   print('external: gitlink '+pin+'; deliberately uninitialized, no active consumer')
  else:
   assert (path/name/'.git').exists(),name
   verify(path/name,pin)
verify(root,'f99405af0b2caad46e84f50f8251ffbffaa80836')
print('EXACT TRACKED STATE VERIFIED')
