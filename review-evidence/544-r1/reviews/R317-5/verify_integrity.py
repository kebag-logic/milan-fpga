#!/usr/bin/env python3
"""Prove tracked bytes, modes, index and required submodule gitlinks."""
import argparse, hashlib, json, os, stat, subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('out',type=Path);a=p.parse_args()
HEAD='8383e929fab3ff57a768c88b8b1ff9b568afcf14'
def git(root,*args):
    return subprocess.check_output(['git','-C',str(root),*args],env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1'))
def verify(root,rev):
    assert git(root,'rev-parse','HEAD').decode().strip()==rev
    entries=git(root,'ls-tree','-rz',rev).split(b'\0'); expected=[]; errors=[]; blobs=0; links={}
    for e in entries:
        if not e:continue
        meta,name=e.split(b'\t',1);mode,kind,oid=meta.split();path=root/os.fsdecode(name)
        expected.append(mode+b' '+oid+b' 0\t'+name)
        if kind==b'commit':links[os.fsdecode(name)]=oid.decode();continue
        try:
            st=path.lstat()
            if mode==b'120000':
                assert stat.S_ISLNK(st.st_mode);data=os.fsencode(os.readlink(path))
            else:
                assert stat.S_ISREG(st.st_mode)
                assert bool(st.st_mode & 0o111)==(mode==b'100755')
                data=path.read_bytes()
            actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest().encode()
            assert actual==oid
            blobs+=1
        except (OSError,AssertionError):errors.append(os.fsdecode(name))
    index=git(root,'ls-files','--stage','-z').split(b'\0')
    assert sorted(x for x in index if x)==sorted(expected),'index differs from tree'
    assert not errors,errors
    return dict(head=rev,tree=git(root,'rev-parse',rev+'^{tree}').decode().strip(),
                tracked_blobs_verified=blobs,index_matches=True,byte_mode_errors=errors,gitlinks=links)
rows={'parent':verify(a.root,HEAD)}
for name in ('third_party/verilog-axis','protocol-processor','gptp-processor'):
    sub=a.root/name
    assert (sub/'.git').is_file() and not sub.is_symlink()
    rows[name]=verify(sub,rows['parent']['gitlinks'][name])
rows['status']=git(a.root,'status','--porcelain=v2').decode()
assert rows['status']=='',rows['status']
a.out.write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(rows,indent=2))
