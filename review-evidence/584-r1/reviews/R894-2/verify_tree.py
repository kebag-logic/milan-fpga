#!/usr/bin/env python3
"""Verify tracked bytes, file modes, stage-0 index and required gitlinks."""
import hashlib, os, stat, subprocess, sys
from pathlib import Path
root=Path(sys.argv[1]).resolve()
required={'protocol-processor','gptp-processor','third_party/verilog-axis','third_party/tsn-c-stack'}
def git(repo,*args): return subprocess.check_output(['git','-C',str(repo),*args])
def verify(repo,label,expected):
    head=git(repo,'rev-parse','HEAD').decode().strip()
    assert head==expected,(label,'HEAD',head,expected)
    entries={}
    for row in git(repo,'ls-tree','-r','-z','HEAD').split(b'\0'):
        if not row: continue
        meta,path=row.split(b'\t',1);mode,kind,sha=meta.split()
        entries[path]=(mode,sha)
    index={}
    for row in git(repo,'ls-files','--stage','-z').split(b'\0'):
        if not row: continue
        meta,path=row.split(b'\t',1);mode,sha,stage=meta.split()
        assert stage==b'0',(label,'unmerged',path)
        index[path]=(mode,sha)
    assert entries==index,(label,'index differs from HEAD')
    n=0
    for name,(mode,sha) in entries.items():
        p=repo/os.fsdecode(name)
        if mode==b'160000':
            if (p/'.git').exists(): verify(p,label+'/'+os.fsdecode(name),sha.decode())
            else:
                assert os.fsdecode(name) not in required,(label,'missing required submodule',name)
                print('Gitlink only (uninitialized):',os.fsdecode(name),sha.decode())
            continue
        st=p.lstat()
        if mode==b'120000':
            assert stat.S_ISLNK(st.st_mode),(label,name,'not symlink')
            b=os.fsencode(os.readlink(p))
        else:
            assert stat.S_ISREG(st.st_mode),(label,name,'not regular')
            gotmode=b'100755' if st.st_mode & 0o111 else b'100644'
            assert gotmode==mode,(label,name,'mode mismatch')
            b=p.read_bytes()
        got=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest().encode()
        assert got==sha,(label,name,'blob mismatch')
        n+=1
    print('PASS',label,head,'tree',git(repo,'rev-parse','HEAD^{tree}').decode().strip(),'tracked blobs',n,'index/modes/bytes exact')
verify(root,'candidate','64d539f12532b2591f734b8e756f8a9358bb742c')
assert git(root,'rev-parse','HEAD^{tree}').decode().strip()=='761862ef4b05e0284a6150036ea85709466bbeb5'
print('All required submodule gitlinks and materialized bytes verified.')
