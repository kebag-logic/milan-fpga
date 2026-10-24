#!/usr/bin/env python3
"""Compare tracked bytes, file modes, index entries, and required gitlinks."""
import hashlib,json,os,stat,subprocess,sys
from pathlib import Path
repo,packet=map(lambda s:Path(s).resolve(),sys.argv[1:3])
def git(root,*args):return subprocess.check_output(['git',*args],cwd=root)
def inspect(root):
    head=git(root,'rev-parse','HEAD').decode().strip()
    tree=git(root,'ls-tree','-rz','HEAD')
    expected={};errors=[];blobs=0
    for row in tree.split(b'\0'):
        if not row:continue
        meta,name=row.split(b'\t',1);mode,kind,oid=meta.split();expected[name]=(mode,oid)
        if kind!=b'blob':continue
        path=root/os.fsdecode(name);blobs+=1
        if not path.exists() and not path.is_symlink():errors.append([os.fsdecode(name),'missing']);continue
        if mode==b'120000':data=os.fsencode(os.readlink(path));actualmode=b'120000'
        else:
            data=path.read_bytes();actualmode=b'100755' if path.stat().st_mode & stat.S_IXUSR else b'100644'
        digest=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest().encode()
        if (actualmode,digest)!=(mode,oid):errors.append([os.fsdecode(name),'bytes/mode mismatch'])
    index={}
    for row in git(root,'ls-files','--stage','-z').split(b'\0'):
        if not row:continue
        meta,name=row.split(b'\t',1);mode,oid,stage=meta.split()
        if stage!=b'0':errors.append([os.fsdecode(name),'unmerged index'])
        index[name]=(mode,oid)
    if index!=expected:errors.append(['index','does not equal HEAD tree'])
    return {'head':head,'tree':git(root,'rev-parse','HEAD^{tree}').decode().strip(),'blobs_checked':blobs,'errors':errors}
result={'parent':inspect(repo),'submodules':{}}
for name in ['protocol-processor','gptp-processor','third_party/verilog-axis','third_party/tsn-c-stack','third_party/lwSRP']:
    record=inspect(repo/name)
    expected=git(repo,'rev-parse','HEAD:'+name).decode().strip()
    record['expected_gitlink']=expected
    if record['head']!=expected:record['errors'].append(['HEAD','off gitlink'])
    result['submodules'][name]=record
result['status']=git(repo,'status','--short').decode()
result['diff_check_rc']=subprocess.run(['git','diff','--check','a032c6d6','HEAD'],cwd=repo,capture_output=True).returncode
(packet/'integrity.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
sys.exit(any(r['errors'] for r in [result['parent'],*result['submodules'].values()]) or bool(result['status']))
