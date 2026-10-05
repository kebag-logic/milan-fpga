#!/usr/bin/env python3
"""Prove committed blob bytes, modes, index entries and required gitlinks.

Usage: python3 verify_integrity.py CHECKOUT
Read-only; does not trust status, assume-unchanged or skip-worktree flags.
"""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

HEAD='d763fce6f3e48fa9c468aaa835653befb8382d06'
TREE='554ad4cb05ffbf9d794813990a8dfb58ec44624d'
BASE='fa450d301805881ad713b67521477bf042ddadfd'
DEV='28f9666feab2b2ba287643c63ed3a16b1e0bb863'
PACKET=Path(__file__).resolve().parent
ENV=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1')
def git(root,*args):
    return subprocess.check_output(['git','-C',str(root),*args],env=ENV)
def entries(root,revision):
    out={}
    for row in git(root,'ls-tree','-r','-z',revision).split(b'\0'):
        if not row:continue
        meta,path=row.split(b'\t',1)
        mode,kind,oid=meta.decode().split()
        out[os.fsdecode(path)]=(mode,kind,oid)
    return out
def verify(root,revision,label):
    assert git(root,'rev-parse','HEAD').decode().strip()==revision,label+' HEAD'
    tree=entries(root,revision)
    index={}
    for row in git(root,'ls-files','--stage','-z').split(b'\0'):
        if not row:continue
        meta,path=row.split(b'\t',1); mode,oid,stage=meta.decode().split()
        assert stage=='0',(label,os.fsdecode(path),'unmerged')
        name=os.fsdecode(path)
        assert name not in index,(label,name,'duplicate')
        index[name]=(mode,oid)
    assert index=={p:(v[0],v[2]) for p,v in tree.items()},label+' index differs'
    count=0
    for name,(mode,kind,oid) in tree.items():
        if kind=='commit':continue
        p=root/name;s=p.lstat()
        if mode=='120000':
            assert stat.S_ISLNK(s.st_mode),(label,name,'not symlink')
            data=os.fsencode(os.readlink(p))
        else:
            assert stat.S_ISREG(s.st_mode),(label,name,'not regular')
            assert bool(s.st_mode&0o111)==(mode=='100755'),(label,name,'mode')
            data=p.read_bytes()
        actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert actual==oid,(label,name,'bytes')
        count+=1
    print(json.dumps({'repository':label,'head':revision,'blobs':count,
                      'index':'exact','bytes':'exact','modes':'exact'}))
    return tree
def main():
    root=Path(sys.argv[1]).resolve()
    assert git(root,'rev-parse','HEAD^{tree}').decode().strip()==TREE
    tree=verify(root,HEAD,'superproject')
    for sub in ['protocol-processor','gptp-processor','third_party/verilog-axis']:
        mode,kind,pin=tree[sub]
        assert mode=='160000' and kind=='commit'
        assert (root/sub/'.git').is_file(),sub+' is not a registered submodule'
        verify(root/sub,pin,sub)
    print('OPTIONAL external gitlink '+tree['external'][2]+' unchanged; uninitialized and unused')
    live=entries(root,DEV)
    owned={'docs/README.md','docs/design/SAVED_STATE_FASTCONNECT.md'}
    touched=[]
    for name in sorted(set(tree)|set(live)):
        if tree.get(name)!=live.get(name):
            assert name in owned or name.startswith('sw/firmware/ctrl_nvm/'),name+' outside lane'
            touched.append(name)
    print('SCOPE '+json.dumps({'source_base':BASE,'integrated_dev':DEV,'lane_paths':touched}))
    for rev in [BASE,DEV,HEAD]:
        print('SHIPPING_WRITER '+rev+' '+entries(root,rev)['sw/firmware/milan_baremetal/milan_baremetal.c'][2])
    for lo,label in [(BASE,'requested_diff'),('9412006bd58c002835bb06d46045c53098cc59a5','round4_diff')]:
        diff=git(root,'diff','--binary',lo+'..'+HEAD)
        print(label+' sha256='+hashlib.sha256(diff).hexdigest())
    status=git(root,'status','--porcelain=v1','--ignored').decode()
    assert not status,'checkout has residue: '+status
    print('PASS exact committed state; clean checkout; required gitlinks and their contents verified')
    return 0
if __name__=='__main__':
    sys.exit(main())
