#!/usr/bin/env python3
"""Verify actual tracked bytes, modes, index and required submodule gitlinks."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess

HEAD = '154722e14781c7373f3229420b6e007f9bcf9835'
TREE = '1928df9c4d94eadc68e864b219a68270227e9f41'
BASELINE = 'efea74858dffc482820d4f19c26c38796a57ff75'
REQUIRED = ('protocol-processor','gptp-processor','third_party/verilog-axis','third_party/lwSRP')
ENV = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')

def git(root,*args):
    return subprocess.check_output(['git','-C',str(root),*args],env=ENV)

def audit(root,rev):
    rows = git(root,'ls-tree','-rz',rev).split(b'\0')
    expected = {}; blobs=0; links={}; errors=[]
    for row in rows:
        if not row: continue
        meta,rawpath=row.split(b'\t',1)
        mode,kind,oid=meta.decode().split()
        path=os.fsdecode(rawpath); expected[path]=(mode,oid)
        if kind == 'commit':
            links[path]=oid
            continue
        file=root/path
        try:
            s=file.lstat()
            if stat.S_ISLNK(s.st_mode):
                actual_mode='120000'; data=os.fsencode(os.readlink(file))
            elif stat.S_ISREG(s.st_mode):
                actual_mode='100755' if s.st_mode & 0o111 else '100644'; data=file.read_bytes()
            else:
                errors.append(path+': not regular blob or symlink'); continue
            actual_oid=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
            if (actual_mode,actual_oid)!=(mode,oid): errors.append(path+': actual bytes/mode differ')
        except OSError:
            errors.append(path+': missing/unreadable')
        blobs+=1
    index={}
    for row in git(root,'ls-files','--stage','-z').split(b'\0'):
        if not row: continue
        meta,rawpath=row.split(b'\t',1); mode,oid,stage=meta.decode().split()
        path=os.fsdecode(rawpath)
        if stage!='0' or path in index: errors.append(path+': nonzero/duplicate index stage')
        index[path]=(mode,oid)
    if expected!=index: errors.append('index differs from exact commit tree')
    return {'revision':rev,'verified_blobs':blobs,'gitlinks':links,'index_exact':expected==index,'errors':errors}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--source',type=Path,required=True); ap.add_argument('--output',type=Path,required=True)
    a=ap.parse_args(); root=a.source.resolve()
    assert git(root,'rev-parse','HEAD').decode().strip()==HEAD
    assert git(root,'rev-parse','HEAD^{tree}').decode().strip()==TREE
    result={'head':HEAD,'tree':TREE,'source':audit(root,HEAD),'submodules':{},'delta_baseline':BASELINE}
    result['delta_paths']=git(root,'diff','--name-only',BASELINE,HEAD).decode().splitlines()
    assert result['delta_paths']==['docs/design/MAILBOX_SPLIT.md','sw/firmware/ctrl/test/srp_feedback.hpp','sw/firmware/ctrl/test/srp_mutants.py']
    for path in REQUIRED:
        sub=root/path; pin=result['source']['gitlinks'][path]
        assert git(sub,'rev-parse','HEAD').decode().strip()==pin
        assert (sub/'.git').is_file() and not sub.is_symlink()
        item=audit(sub,pin)
        item['registered_submodule']=bool(git(sub,'rev-parse','--show-superproject-working-tree').strip())
        assert item['registered_submodule']
        result['submodules'][path]=item
    result['pass']=not result['source']['errors'] and not any(x['errors'] for x in result['submodules'].values())
    a.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    return int(not result['pass'])

if __name__=='__main__': raise SystemExit(main())
