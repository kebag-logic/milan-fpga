#!/usr/bin/env python3
"""Check raw working bytes, executable modes, index entries and populated gitlinks."""
import hashlib,os,stat,subprocess,sys
from pathlib import Path
repo=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1')
def git(root,*args): return subprocess.check_output(['git','-C',str(root),*args],env=env)
def verify(root,revision):
    head=git(root,'rev-parse','HEAD').decode().strip(); assert head==revision,(root.name,head,revision)
    entries={}
    for row in git(root,'ls-tree','-rz',revision).split(b'\0'):
        if not row: continue
        meta,path=row.split(b'\t',1);mode,kind,oid=meta.decode().split();entries[os.fsdecode(path)]=(mode,kind,oid)
    index={}
    for row in git(root,'ls-files','--stage','-z').split(b'\0'):
        if not row: continue
        meta,path=row.split(b'\t',1); mode,oid,stage=meta.decode().split();assert stage=='0'
        index[os.fsdecode(path)]=(mode,oid)
    assert index=={k:(v[0],v[2]) for k,v in entries.items()},root.name
    blobs=0
    for name,(mode,kind,oid) in entries.items():
        f=root/name
        if kind=='commit': continue
        st=f.lstat()
        if mode=='120000':
            assert stat.S_ISLNK(st.st_mode),name
            data=os.fsencode(os.readlink(f))
        else:
            assert stat.S_ISREG(st.st_mode),name
            actual='100755' if st.st_mode&0o111 else '100644'
            assert actual==mode,(name,actual,mode)
            data=f.read_bytes()
        actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert actual==oid,name
        blobs+=1
    print(root.name,head,'raw blobs/modes/index PASS',blobs)
    return entries
head='87a2b77d1ed49f634c616f2d27b6aa9b9f5d786d'
assert git(repo,'rev-parse','HEAD^{tree}').decode().strip()=='95076a30447b31a37d02298bf87b4fdd6a809d89'
entries=verify(repo,head)
required={'protocol-processor','gptp-processor','third_party/verilog-axis','third_party/tsn-c-stack'}
for name,(mode,kind,oid) in entries.items():
    if kind!='commit': continue
    assert mode=='160000'
    if (repo/name/'.git').exists():
        verify(repo/name,oid)
        print('gitlink',name,oid,'PASS')
        required.discard(name)
    else: print('gitlink',name,oid,'uninitialized; tree/index intact')
assert not required,required
assert not git(repo,'status','--porcelain','--untracked-files=no').strip()
print('PASS: exact tracked source, modes, stage-zero index, required submodules')
