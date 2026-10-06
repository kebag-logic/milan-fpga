#!/usr/bin/env python3
"""Prove tracked bytes, modes and index against HEAD, recursively at required pins."""
import os,sys,hashlib,stat,subprocess
from pathlib import Path
root=Path(sys.argv[1]).resolve()
os.environ['GIT_NO_REPLACE_OBJECTS']='1'
def git(r,*args): return subprocess.check_output(['git','-C',str(r),*args])
def prove(r,rev,label):
 rows=git(r,'ls-tree','-rz',rev).split(b'\0'); expected=[]; count=0
 for row in rows:
  if not row: continue
  meta,name=row.split(b'\t',1); mode,typ,oid=meta.split(); rel=os.fsdecode(name); f=r/rel
  expected.append(mode+b' '+oid+b' 0\t'+name)
  if typ==b'commit':
   print(f'{label}/{rel}: gitlink {oid.decode()}')
   if label=='.' and rel=='external':
    print('external: uninitialized optional submodule; index gitlink checked, contents not claimed')
    continue
   assert git(f,'rev-parse','HEAD').strip()==oid,(label,rel,'HEAD')
   prove(f,oid.decode(),label+'/'+rel)
   continue
  st=f.lstat()
  if mode==b'120000':
   assert stat.S_ISLNK(st.st_mode),(label,rel,'symlink mode')
   data=os.fsencode(os.readlink(f))
  else:
   assert stat.S_ISREG(st.st_mode),(label,rel,'file mode')
   assert bool(st.st_mode&0o111)==(mode==b'100755'),(label,rel,'exec mode')
   data=f.read_bytes()
  actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest().encode()
  assert actual==oid,(label,rel,'bytes')
  count+=1
 index=git(r,'ls-files','--stage','-z').split(b'\0')
 assert sorted(x for x in index if x)==sorted(expected),(label,'index entries')
 print(f'{label}: {count} tracked blobs byte/mode exact; index exact')
head=git(root,'rev-parse','HEAD').decode().strip()
assert head=='021b9c1fb966e9a1a4acef6b5233edd3518f32a0',head
assert git(root,'rev-parse','HEAD^{tree}').decode().strip()=='b7c103aaffff9a48f7c05436372875c5d94331c7'
print('head '+head)
prove(root,head,'.')
print('PASS exact head, tree, tracked blobs, modes, index and required submodule pins')
