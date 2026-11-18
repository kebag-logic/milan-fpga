#!/usr/bin/env python3
"""Verify tracked raw bytes, executable modes, index entries, and required gitlinks."""
import argparse,hashlib,os,stat,subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('repo',type=Path);a=p.parse_args()
env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1')
def git(root,*args):return subprocess.check_output(['git',*args],cwd=root,env=env)
def verify(root,revision,label):
 tree=git(root,'ls-tree','-rz',revision)
 expected={}; count=0
 for row in tree.split(b'\0'):
  if not row:continue
  info,name=row.split(b'\t',1); mode,kind,oid=info.split();expected[name]=(mode,oid)
  if kind==b'commit':continue
  f=root/os.fsdecode(name); s=f.lstat()
  if mode==b'120000':
   assert stat.S_ISLNK(s.st_mode),name;data=os.fsencode(os.readlink(f))
  else:
   assert stat.S_ISREG(s.st_mode),name
   actual=b'100755' if s.st_mode&0o111 else b'100644';assert actual==mode,(name,actual,mode)
   data=f.read_bytes()
  h=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest().encode();assert h==oid,name
  count+=1
 indexed={}
 for row in git(root,'ls-files','--stage','-z').split(b'\0'):
  if not row:continue
  info,name=row.split(b'\t',1);mode,oid,stage=info.split();assert stage==b'0';indexed[name]=(mode,oid)
 assert indexed==expected,label
 print(label,'raw tracked blobs/modes/index PASS',count,'blobs',len(expected),'entries')
 return expected
head=git(a.repo,'rev-parse','HEAD').decode().strip();assert head=='0297a19a056ee3d5d705bc502c4ae7808689ede7'
tree=git(a.repo,'rev-parse','HEAD^{tree}').decode().strip();assert tree=='e3e4dbefc89e29cc646fd5e2cf757338ba3877a9'
print('HEAD',head); print('TREE',tree)
entries=verify(a.repo,'HEAD','review clone')
for name in ['protocol-processor','gptp-processor','third_party/verilog-axis','third_party/tsn-c-stack']:
 mode,pin=entries[name.encode()];assert mode==b'160000'
 sub=a.repo/name;assert (sub/'.git').exists();assert git(sub,'rev-parse','HEAD').strip()==pin
 print('GITLINK',name,pin.decode());verify(sub,pin.decode(),name)
print('Uninitialized external submodule is outside the required validation set.')
print('CHECKOUT INTEGRITY PASS')
