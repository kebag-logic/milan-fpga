#!/usr/bin/env python3
"""Verify tracked blob bytes, executable/symlink modes, index and required gitlinks."""
import argparse,hashlib,os,stat,subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);a=p.parse_args()
root=a.root.resolve()
HEAD='095995243bc354b8a41755f3fdfae343511cc668'
TREE='843b1ede3d27b14048269ce9c3b2f9cde65bfdff'
pins={'gptp-processor':'3ce71b768a2f6f6a5274c127080146e755d02275',
 'protocol-processor':'801ef2283ec793e35a2590fc6593c90313a64041',
 'third_party/lwSRP':'73007b4807977517045e8aa485c61ebb8f5ee843',
 'third_party/tsn-c-stack':'5d03517f2ab42416654a8f2be2f71cfc51d82440',
 'third_party/verilog-axis':'48ff7a7e2ef782cf778d47910cf85835c64b1bce'}
def git(at,*args):return subprocess.check_output(['git','-C',str(at),*args])
def audit(at,label):
 entries={}
 for row in git(at,'ls-tree','-rz','HEAD').split(b'\0'):
  if not row:continue
  info,path=row.split(b'\t',1);mode,kind,oid=info.decode().split();entries[path]=(mode,oid)
 index={}
 for row in git(at,'ls-files','--stage','-z').split(b'\0'):
  if not row:continue
  info,path=row.split(b'\t',1);mode,oid,stage=info.decode().split()
  assert stage=='0',(label,path,'unmerged index')
  index[path]=(mode,oid)
 assert index==entries,(label,'index differs from HEAD')
 blobs=0;links={}
 for path,(mode,oid) in entries.items():
  name=os.fsdecode(path);f=at/name
  if mode=='160000':links[name]=oid;continue
  st=f.lstat()
  if mode=='120000':
   assert stat.S_ISLNK(st.st_mode),(label,name,'not symlink')
   data=os.fsencode(os.readlink(f))
  else:
   assert stat.S_ISREG(st.st_mode),(label,name,'not regular')
   assert bool(st.st_mode&0o111)==(mode=='100755'),(label,name,'mode')
   data=f.read_bytes()
  got=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
  assert got==oid,(label,name,'bytes')
  blobs+=1
 status=git(at,'status','--porcelain=v1','--untracked-files=all').decode()
 assert not status,(label,'status',status)
 print('PASS',label,blobs,'tracked blobs: bytes, modes, index; clean status')
 return links
assert git(root,'rev-parse','HEAD').decode().strip()==HEAD
assert git(root,'rev-parse','HEAD^{tree}').decode().strip()==TREE
print('HEAD',HEAD);print('TREE',TREE)
links=audit(root,'root')
for name,oid in pins.items():
 assert links[name]==oid,(name,'gitlink')
 assert git(root/name,'rev-parse','HEAD').decode().strip()==oid,(name,'HEAD')
 print('GITLINK',name,oid)
 audit(root/name,name)
for name,oid in links.items():
 if name not in pins:print('UNINITIALIZED/OUT-OF-SCOPE GITLINK',name,oid)
print('PASS exact published checkout preserved')
