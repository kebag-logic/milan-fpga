#!/usr/bin/env python3
"""Verify raw tracked bytes, filesystem modes, index records and required gitlinks."""
import hashlib, os, pathlib, stat, subprocess, sys
repo=pathlib.Path(sys.argv[1]).resolve(); env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1')
def git(root,*args): return subprocess.check_output(['git',*args],cwd=root,env=env)
expected='9413958c66c0dcd632b3e0e7ac44505314fed41a'
assert git(repo,'rev-parse','HEAD').decode().strip()==expected
assert git(repo,'rev-parse','HEAD^{tree}').decode().strip()=='83b2c214071b7f3f74c0eda10048ec674e3d5fdc'
def verify(root,label):
 rows={}
 for row in git(root,'ls-tree','-rz','HEAD').split(b'\0'):
  if not row: continue
  meta,path=row.split(b'\t',1); mode,kind,sha=meta.split(); rows[path]=(mode,sha)
 index={}
 for row in git(root,'ls-files','--stage','-z').split(b'\0'):
  if not row: continue
  meta,path=row.split(b'\t',1); mode,sha,stage=meta.split(); assert stage==b'0'; assert path not in index
  index[path]=(mode,sha)
 assert index==rows,(label,'index mismatch')
 n=0; subs=[]
 for path,(mode,sha) in rows.items():
  p=root/os.fsdecode(path)
  if mode==b'160000': subs.append((p,sha)); continue
  st=p.lstat()
  if mode==b'120000': assert stat.S_ISLNK(st.st_mode); data=os.fsencode(os.readlink(p))
  else:
   assert stat.S_ISREG(st.st_mode)
   actual=b'100755' if st.st_mode&0o111 else b'100644'; assert mode==actual,(label,path,'mode')
   data=p.read_bytes()
  actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest().encode()
  assert actual==sha,(label,path,'bytes'); n+=1
 print(label,git(root,'rev-parse','HEAD').decode().strip(),'raw bytes/modes/index PASS',n,'files')
 return subs
for p,pin in verify(repo,'parent'):
 name=str(p.relative_to(repo))
 if name=='external':
  assert pin==b'efeb541ae5fe1e078332d8462dca2fc2d9cb8db5'
  print(name,pin.decode(),'gitlink verified; optional checkout absent'); continue
 assert (p/'.git').exists(),name
 assert git(p,'rev-parse','HEAD').strip()==pin,name
 verify(p,name)
print('EXACT HEAD INTEGRITY PASS')
