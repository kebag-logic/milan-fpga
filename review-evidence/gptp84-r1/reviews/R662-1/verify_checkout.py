#!/usr/bin/env python3
"""Verify exact tracked content, modes, index, interfaces and gitlinks."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

root=Path(sys.argv[1]).resolve()
p=Path(__file__).resolve().parent
head='53ac2e9d75ceb381c2d2b04854e760304d9ae43f'
tree='69618d639b4019c0c27d6b03cfae8f9d36830d8b'
def git(*args):
    return subprocess.check_output(['git',*args],cwd=root)
assert git('rev-parse','HEAD').decode().strip()==head
assert git('rev-parse','HEAD^{tree}').decode().strip()==tree
rows=[]
for row in git('ls-tree','-rz',head).split(b'\0'):
    if not row: continue
    meta,name=row.split(b'\t',1)
    mode,kind,oid=meta.decode().split()
    path=name.decode()
    if mode=='160000':
        actual=subprocess.check_output(['git','-C',str(root/path),'rev-parse','HEAD']).decode().strip()
        assert actual==oid,path
    else:
        f=root/path
        if mode=='120000':
            data=os.readlink(f).encode()
            actual_mode='120000'
        else:
            data=f.read_bytes()
            actual_mode='100755' if f.stat().st_mode & 0o111 else '100644'
        actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert actual==oid and actual_mode==mode,path
    rows.append({'path':path,'mode':mode,'object':oid})
expected={x['path']:(x['mode'],x['object'],'0') for x in rows}
index={}
for row in git('ls-files','--stage','-z').split(b'\0'):
    if row:
        meta,path=row.split(b'\t',1)
        index[path.decode()]=tuple(meta.decode().split())
assert expected==index
path='hdl/top/KL_gptp_engine.sv'
def interface(rev):
    text=git('show',rev+':'+path).decode()
    text=re.sub(r'/\*.*?\*/','',text,flags=re.S)
    text=re.sub(r'//[^\n]*','',text)
    text=text[text.index('module KL_gptp_engine'):]
    return re.sub(r'\s+','',text[:text.index(');')+2])
assert interface('43acfbcc')==interface(head)
result={'head':head,'tree':tree,'tracked_entries':len(rows),
        'tracked_bytes_and_modes_match':True,'index_matches_tree':True,
        'gitlinks':[x for x in rows if x['mode']=='160000'],
        'engine_module_ports_parameters_identical_to_base':True,
        'status_porcelain':git('status','--porcelain').decode(),'entries':rows}
(p/'checkout-verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='entries'},indent=2))
