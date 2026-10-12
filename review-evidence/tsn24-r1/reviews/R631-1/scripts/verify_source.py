#!/usr/bin/env python3
"""Verify every tracked byte, executable mode, index entry and gitlink."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess

p=argparse.ArgumentParser()
p.add_argument('source',type=Path)
p.add_argument('receipt',type=Path)
a=p.parse_args()
source=a.source.resolve()
def git(*args):
    return subprocess.check_output(['git',*args],cwd=source)
head=git('rev-parse','HEAD').decode().strip()
tree=git('rev-parse','HEAD^{tree}').decode().strip()
assert head=='9ef7bd5281c0bb3f2967b11c5a5d8d74a75755d1'
assert tree=='dcf00056e872f60856d46444b9871ca598fd4e50'
rows=[]
expected={}
for entry in git('ls-tree','-rz','HEAD').split(b'\0'):
    if not entry:continue
    meta,path=entry.split(b'\t',1)
    mode,kind,blob=meta.decode().split()
    name=path.decode()
    expected[name]=(mode,blob,'0')
    f=source/name
    if kind=='commit':
        actual=subprocess.check_output(['git','rev-parse','HEAD'],cwd=f).decode().strip()
        assert actual==blob
    else:
        s=f.lstat()
        if mode=='120000':
            assert stat.S_ISLNK(s.st_mode)
            data=os.readlink(f).encode()
        else:
            assert stat.S_ISREG(s.st_mode)
            actual_mode='100755' if s.st_mode&stat.S_IXUSR else '100644'
            assert actual_mode==mode,(name,mode,actual_mode)
            data=f.read_bytes()
        actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert actual==blob,(name,blob,actual)
    rows.append({'path':name,'mode':mode,'kind':kind,'blob':blob,'verified':True})
index={}
for entry in git('ls-files','--stage','-z').split(b'\0'):
    if not entry:continue
    meta,path=entry.split(b'\t',1)
    mode,blob,stage=meta.decode().split()
    index[path.decode()]=(mode,blob,stage)
assert index==expected
status=git('status','--porcelain=v1','--untracked-files=all').decode()
assert status=='',status
result={'head':head,'tree':tree,'tracked_files':len(rows),'gitlinks':[r for r in rows if r['kind']=='commit'],
        'index_matches_tree':True,'tracked_bytes_and_modes_match':True,'status':status,'entries':rows}
a.receipt.write_text(json.dumps(result,indent=2)+'\n')
print(f'PASS {len(rows)} tracked entries; exact bytes, modes and index; clean status; {len(result["gitlinks"])} gitlinks')
