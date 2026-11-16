#!/usr/bin/env python3
"""Verify raw tracked blobs, executable/symlink modes, index and required gitlinks."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess

ap=argparse.ArgumentParser()
ap.add_argument('--repo',type=Path,required=True)
args=ap.parse_args()
root=args.repo.resolve()
expected='09a948d46413ef3b3ab0fa11bf97c06323f9051f'
required=['protocol-processor','gptp-processor','third_party/verilog-axis',
          'third_party/lwSRP','third_party/tsn-c-stack']
errors=[]
def git(path,*argv):
    return subprocess.check_output(['git','-C',str(path),*argv])
def verify(path,rev,label):
    entries={}
    raw=git(path,'ls-tree','-r','-z',rev)
    for line in raw.split(b'\0'):
        if not line: continue
        metadata,name=line.split(b'\t',1)
        mode,kind,oid=metadata.decode().split()
        entries[name]=(mode,oid)
        if kind!='blob': continue
        f=path/os.fsdecode(name)
        st=f.lstat()
        actual_mode='120000' if stat.S_ISLNK(st.st_mode) else '100755' if st.st_mode&0o111 else '100644'
        data=os.fsencode(os.readlink(f)) if stat.S_ISLNK(st.st_mode) else f.read_bytes()
        digest=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        if (actual_mode,digest)!=(mode,oid): errors.append(f'{label}/{os.fsdecode(name)}: bytes or mode differ')
    index_raw=git(path,'ls-files','--stage','-z')
    index={}
    for line in index_raw.split(b'\0'):
        if not line: continue
        metadata,name=line.split(b'\t',1)
        mode,oid,stage=metadata.decode().split()
        if stage!='0': errors.append(f'{label}: index stage {stage}')
        index[name]=(mode,oid)
    if entries!=index: errors.append(f'{label}: index differs from committed tree')
    actual=git(path,'rev-parse','HEAD').decode().strip()
    if actual!=rev: errors.append(f'{label}: HEAD differs')
    return {'label':label,'head':actual,'tree':git(path,'rev-parse','HEAD^{tree}').decode().strip(),
            'tracked_entries':len(entries),'index_sha256':hashlib.sha256(index_raw).hexdigest(),
            'raw_blobs_modes_and_index':'PASS' if not errors else 'see errors'},entries

records=[]
rec,entries=verify(root,expected,'superproject'); records.append(rec)
for name in required:
    mode,pin=entries[os.fsencode(name)]
    if mode!='160000': errors.append(f'{name}: not a gitlink')
    if (root/name).is_symlink() or not (root/name/'.git').is_file():
        errors.append(f'{name}: not an initialized submodule')
    rec,_=verify(root/name,pin,name); records.append(rec)
result={'expected_head':expected,'records':records,'errors':errors,'result':'FAIL' if errors else 'PASS'}
print(json.dumps(result,indent=2))
raise SystemExit(bool(errors))
