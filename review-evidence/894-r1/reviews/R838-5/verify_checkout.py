#!/usr/bin/env python3
"""Verify actual tracked bytes, modes, index entries and populated gitlinks against HEAD."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

root, packet = (Path(x).resolve() for x in sys.argv[1:3])
def git(at,*args):
    return subprocess.check_output(['git','-C',str(at),*args])
def verify(at):
    tree={}
    for entry in git(at,'ls-tree','-rz','--full-tree','HEAD').split(b'\0'):
        if entry:
            meta,path=entry.split(b'\t',1)
            mode,kind,oid=meta.split()
            tree[path]=(mode,kind,oid)
    index={}
    for entry in git(at,'ls-files','--stage','-z').split(b'\0'):
        if entry:
            meta,path=entry.split(b'\t',1)
            mode,oid,stage=meta.split()
            assert stage==b'0'
            index[path]=(mode,oid)
    assert index=={k:(v[0],v[2]) for k,v in tree.items()}
    flags=git(at,'ls-files','-v','-z').split(b'\0')
    assert all(not f or f[:1]==b'H' for f in flags)
    blobs=0;subs=[]
    for path,(mode,kind,oid) in tree.items():
        p=at/os.fsdecode(path)
        if kind==b'commit':
            exists=(p/'.git').exists()
            item={'path':os.fsdecode(path),'gitlink':oid.decode(),'populated':exists}
            if exists:
                assert git(p,'rev-parse','HEAD').strip()==oid
                item['verification']=verify(p)
            subs.append(item)
            continue
        st=p.lstat()
        if mode==b'120000':
            assert stat.S_ISLNK(st.st_mode)
            data=os.fsencode(os.readlink(p))
        else:
            assert stat.S_ISREG(st.st_mode)
            expected=b'100755' if st.st_mode&stat.S_IXUSR else b'100644'
            assert expected==mode,(path,mode,expected)
            data=p.read_bytes()
        actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest().encode()
        assert actual==oid,path
        blobs+=1
    return {'head':git(at,'rev-parse','HEAD').decode().strip(),
            'tree':git(at,'rev-parse','HEAD^{tree}').decode().strip(),
            'tracked_blobs_verified':blobs,'index_equals_tree':True,'hidden_index_flags':False,
            'untracked':git(at,'ls-files','--others','--exclude-standard').decode().splitlines(),
            'submodules':subs}
result=verify(root)
assert result['head']=='7398ec0aeea468d92ff642a03a06e291a0cd58d1'
assert result['tree']=='2787f9fae40e581584d454e6cb476e68d1850487'
(packet/'checkout-integrity.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
