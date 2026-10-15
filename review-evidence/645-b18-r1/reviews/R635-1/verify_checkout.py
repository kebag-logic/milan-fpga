#!/usr/bin/env python3
"""Usage: verify_checkout.py REPO HEAD. Verify exact bytes, modes, index and gitlinks."""
import hashlib, os, stat, subprocess, sys
from pathlib import Path
repo=Path(sys.argv[1]); head=sys.argv[2]
env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1')
def git(*args): return subprocess.check_output(['git','-C',str(repo),*args],env=env)
assert git('rev-parse','HEAD').decode().strip()==head
entries={}
for record in git('ls-tree','-r','-z',head).split(b'\0'):
    if not record: continue
    meta,path=record.split(b'\t',1); mode,typ,oid=meta.decode().split(); entries[path.decode()]=(mode,oid)
idx={}
for record in git('ls-files','--stage','-z').split(b'\0'):
    if not record: continue
    meta,path=record.split(b'\t',1); mode,oid,stage=meta.decode().split(); assert stage=='0'
    idx[path.decode()]=(mode,oid)
assert idx==entries,'index differs from exact HEAD tree'
files=0; links=[]
for name,(mode,oid) in entries.items():
    path=repo/name
    if mode=='160000':
        links.append((name,oid)); continue
    st=path.lstat()
    if mode=='120000':
        assert stat.S_ISLNK(st.st_mode); data=os.readlink(path).encode()
    else:
        assert stat.S_ISREG(st.st_mode)
        assert ('100755' if st.st_mode & 0o111 else '100644')==mode,(name,'mode')
        data=path.read_bytes()
    got=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    assert got==oid,(name,'bytes'); files+=1
print('HEAD',head)
print('TREE',git('rev-parse',head+'^{tree}').decode().strip())
print('Exact tracked blob bytes and modes:',files,'PASS')
print('Index equals HEAD tree: PASS')
for name,oid in links: print('GITLINK',name,oid)
print('Submodule checkout status (uninitialized is not a simulated execution):')
print(git('submodule','status').decode(),end='')
print('Working tree status:',git('status','--porcelain').decode().strip() or 'clean')
