#!/usr/bin/env python3
"""Verify every tracked byte, executable mode, index entry and gitlink."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

root,packet=map(Path,sys.argv[1:])
head='cb8bab044d98a89d8c4eb2b56bd81835e6fc5d48'
tree='a19fe4d05c3bfcab317780fe8e57f07f77c23469'
def git(*args):return subprocess.check_output(['git',*args],cwd=root)
assert git('rev-parse','HEAD').decode().strip()==head
assert git('rev-parse','HEAD^{tree}').decode().strip()==tree
index={}
for row in git('ls-files','--stage','-z').split(b'\0'):
    if not row:continue
    meta,path=row.split(b'\t');mode,sha,stage=meta.decode().split()
    assert stage=='0'
    index[path.decode()]=(mode,sha)
entries=[];gitlinks=[]
for row in git('ls-tree','-r','-z',head).split(b'\0'):
    if not row:continue
    meta,rel=row.split(b'\t');mode,kind,sha=meta.decode().split();rel=rel.decode();path=root/rel
    assert index.pop(rel)==(mode,sha),(rel,'index mismatch')
    if mode=='160000':
        actual=subprocess.check_output(['git','rev-parse','HEAD'],cwd=path,text=True).strip()
        assert actual==sha
        gitlinks.append({'path':rel,'sha':sha});continue
    data=os.readlink(path).encode() if mode=='120000' else path.read_bytes()
    actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    assert actual==sha,(rel,'blob mismatch')
    if mode!='120000':assert bool(path.stat().st_mode&0o111)==(mode=='100755'),(rel,'mode mismatch')
    entries.append({'path':rel,'mode':mode,'blob':sha})
assert not index,index
status=git('status','--porcelain=v1').decode()
assert not status,status
result={'head':head,'tree':tree,'tracked_blobs':len(entries),'index_exact':True,
        'bytes_exact':True,'modes_exact':True,'gitlinks':gitlinks,'status':status,'entries':entries}
(packet/'receipts/final-integrity.json').write_text(json.dumps(result,indent=2)+'\n')
print(f'PASS: {len(entries)} tracked blobs, bytes/modes/index exact; {len(gitlinks)} gitlinks; clean checkout')
