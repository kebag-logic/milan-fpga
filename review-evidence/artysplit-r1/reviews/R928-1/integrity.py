#!/usr/bin/env python3
"""Verify reviewed tracked bytes, file modes, index and submodule gitlinks.
Usage: integrity.py SOURCE
"""
from pathlib import Path
import hashlib, os, stat, subprocess, sys
root=Path(sys.argv[1]).resolve()
def git(*args):
 return subprocess.check_output(['git','-C',str(root),*args])
head='248d85c1453213b0f1642967a4046f395c82c56b'
tree='ad0444dbf9089b90ac3693c0bc46421894cfadeb'
assert git('rev-parse','HEAD').decode().strip()==head
assert git('rev-parse','HEAD^{tree}').decode().strip()==tree
expected={}
for rec in git('ls-tree','-rz','HEAD').split(b'\0'):
 if rec:
  meta,path=rec.split(b'\t',1);mode,kind,oid=meta.decode().split()
  expected[path.decode()]=(mode,oid)
index={}
for rec in git('ls-files','-s','-z').split(b'\0'):
 if rec:
  meta,path=rec.split(b'\t',1);mode,oid,stage=meta.decode().split()
  assert stage=='0'
  index[path.decode()]=(mode,oid)
assert index==expected, 'index differs from reviewed tree'
count=0
for path,(mode,oid) in expected.items():
 p=root/path
 if mode=='160000':
  if (p/'.git').exists():
   actual=subprocess.check_output(['git','-C',str(p),'rev-parse','HEAD']).decode().strip()
   assert actual==oid,(path,actual,oid)
   subprocess.run(['git','-C',str(p),'diff','--quiet','HEAD','--'],check=True)
   print('GITLINK',path,oid,'checkout matches; tracked diff clean')
  else: print('GITLINK',path,oid,'uninitialized; tree/index verified only')
  continue
 s=p.lstat()
 if mode=='120000':
  assert stat.S_ISLNK(s.st_mode),path
  data=os.readlink(p).encode()
 else:
  assert stat.S_ISREG(s.st_mode),path
  actual='100755' if s.st_mode & stat.S_IXUSR else '100644'
  assert actual==mode,(path,actual,mode)
  data=p.read_bytes()
 actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
 assert actual==oid,(path,actual,oid)
 count+=1
print('HEAD',head)
print('TREE',tree)
print('PASS',count,'tracked blobs: raw bytes and modes match; complete index matches tree')
print('STATUS',git('status','--porcelain=v1','--untracked-files=normal').decode().strip() or 'clean')
