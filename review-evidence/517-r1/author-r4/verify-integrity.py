import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess

out = Path(__file__).resolve().parent
root = Path.cwd()
env = dict(os.environ,GIT_NO_REPLACE_OBJECTS='1')

def git(where,*args):
    return subprocess.check_output(['git','-C',str(where),*args],env=env)

def verify(where):
    head = git(where,'rev-parse','HEAD').decode().strip()
    tree = {}
    for entry in git(where,'ls-tree','-rz','HEAD').split(b'\0'):
        if not entry: continue
        meta,path = entry.split(b'\t',1)
        mode,kind,oid = meta.decode().split()
        tree[os.fsdecode(path)] = (mode,oid)
    index = {}
    for entry in git(where,'ls-files','--stage','-z').split(b'\0'):
        if not entry: continue
        meta,path = entry.split(b'\t',1)
        mode,oid,stage = meta.decode().split()
        assert stage=='0',(where,path,stage)
        index[os.fsdecode(path)] = (mode,oid)
    assert tree==index,where
    for entry in git(where,'ls-files','-v','-z').split(b'\0'):
        if entry: assert entry[:1] not in (b'h',b'S',b's'),(where,entry)
    count = 0
    pins = {}
    for name,(mode,oid) in tree.items():
        path = where/name
        if mode=='160000':
            pins[name]=oid
            continue
        st = path.lstat()
        if mode=='120000':
            assert stat.S_ISLNK(st.st_mode),path
            data=os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(st.st_mode),path
            assert bool(st.st_mode & 0o111)==(mode=='100755'),path
            data=path.read_bytes()
        actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert actual==oid,path
        count+=1
    return dict(head=head,files_verified=count,pins=pins,index_matches=True)

report={'parent':verify(root),'submodules':{}}
for name in ('third_party/verilog-axis','protocol-processor','gptp-processor'):
    result=verify(root/name)
    assert result['head']==report['parent']['pins'][name],name
    report['submodules'][name]=result
(out/'final-integrity.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
