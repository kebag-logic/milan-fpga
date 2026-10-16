#!/usr/bin/env python3
"""Verify raw HEAD blobs, modes, indexes and required gitlink checkouts without status shortcuts."""
import hashlib,json,os,stat,subprocess,sys
from pathlib import Path
root=Path(sys.argv[1]).resolve()
required=['protocol-processor','gptp-processor','third_party/verilog-axis','third_party/tsn-c-stack']
env={**os.environ,'GIT_NO_REPLACE_OBJECTS':'1'}
def git(repo,*args):return subprocess.check_output(['git','-C',str(repo),*args],env=env)
def check(repo):
    tree={}
    for row in git(repo,'ls-tree','-rz','HEAD').split(b'\0'):
        if not row:continue
        header,path=row.split(b'\t',1);mode,kind,oid=header.split();tree[path]=(mode,oid)
    idx={}
    for row in git(repo,'ls-files','--stage','-z').split(b'\0'):
        if not row:continue
        header,path=row.split(b'\t',1);mode,oid,stage=header.split(); assert stage==b'0',(path,stage)
        idx[path]=(mode,oid)
    assert idx==tree,'index != HEAD tree'
    files=0;links={}
    for raw,(mode,expected) in tree.items():
        name=os.fsdecode(raw); path=repo/name
        if mode==b'160000': links[name]=expected.decode();continue
        st=path.lstat()
        if mode==b'120000':
            assert stat.S_ISLNK(st.st_mode),name
            data=os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(st.st_mode),name
            assert bool(st.st_mode & 0o111)==(mode==b'100755'),name
            data=path.read_bytes()
        actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest().encode()
        assert actual==expected,name
        files+=1
    return {'head':git(repo,'rev-parse','HEAD').decode().strip(),'tree':git(repo,'rev-parse','HEAD^{tree}').decode().strip(),
            'verified_blobs_and_modes':files,'index_equals_head':True,'gitlinks':links}
result={'superproject':check(root),'submodules':{}}
assert result['superproject']['head']=='6f86eee604729b80684526fc5b9be720d94f179a'
assert result['superproject']['tree']=='32964c6b4b2fc2422ea0f4d05532e2999820240f'
for name in required:
    path=root/name
    assert not path.is_symlink() and (path/'.git').is_file(),name
    row=check(path)
    assert row['head']==result['superproject']['gitlinks'][name],name
    result['submodules'][name]=row
result['status']=git(root,'status','--porcelain=v1','--untracked-files=all').decode()
assert not result['status']
print(json.dumps(result,indent=2))
