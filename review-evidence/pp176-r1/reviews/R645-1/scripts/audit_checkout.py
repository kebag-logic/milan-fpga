#!/usr/bin/env python3
"""Verify raw tracked blobs, executable modes, index records and gitlinks."""
import argparse
import hashlib
import os
from pathlib import Path
import stat
import subprocess

HEAD = '29f58ad30a97327d92b50f17f49d085cd97066a5'
TREE = 'c6fbf3914e940bf129152ba341b80d686ba30247'

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', type=Path, required=True)
    a = ap.parse_args()
    def git(*args):return subprocess.check_output(['git','-C',str(a.repo),*args])
    assert git('rev-parse','HEAD').strip().decode()==HEAD
    assert git('rev-parse','HEAD^{tree}').strip().decode()==TREE
    expected={}
    for record in git('ls-tree','-rz','--full-tree',HEAD).split(b'\0'):
        if not record:continue
        meta,name=record.split(b'\t',1);mode,kind,oid=meta.split()
        expected[name]=(mode,kind,oid)
    actual={}
    for record in git('ls-files','--stage','-z').split(b'\0'):
        if not record:continue
        meta,name=record.split(b'\t',1);mode,oid,stage=meta.split()
        assert stage==b'0',name
        assert name not in actual,name
        actual[name]=(mode,oid)
    assert actual=={n:(v[0],v[2]) for n,v in expected.items()},'Index differs from HEAD'
    links=[]
    for name,(mode,kind,oid) in expected.items():
        f=a.repo/os.fsdecode(name)
        if kind==b'commit':
            links.append((name.decode(),oid.decode()))
            assert subprocess.check_output(['git','-C',str(f),'rev-parse','HEAD']).strip()==oid
            continue
        if mode==b'120000':
            assert f.is_symlink(),name
            data=os.fsencode(os.readlink(f))
        else:
            assert f.is_file() and not f.is_symlink(),name
            executable=bool(f.stat().st_mode & stat.S_IXUSR)
            assert executable==(mode==b'100755'),name
            data=f.read_bytes()
        raw=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest().encode()
        assert raw==oid,name
    assert not git('status','--porcelain=v1','--untracked-files=no').strip()
    print('HEAD',HEAD)
    print('TREE',TREE)
    print('PASS raw blob bytes, tracked modes and stage-zero index:',len(expected),'entries')
    print('Required gitlinks:',links if links else 'none in this standalone processor tree')
    print('PASS tracked checkout restored to exact head')

if __name__=='__main__':main()
