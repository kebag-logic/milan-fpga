"""Prove tracked bytes, modes, index and required submodule pins without status trust.

Usage: python3 -B check_integrity.py REPO
"""
import hashlib
import json
import os
import stat
import subprocess
import sys
from pathlib import Path

root=Path(sys.argv[1]).resolve()
env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1')
def git(repo,*args):
    return subprocess.check_output(['git','-C',str(repo),*args],env=env)
def inspect(repo, revision, label):
    entries={}
    for r in git(repo,'ls-tree','-rz',revision).split(b'\0'):
        if r:
            meta,name=r.split(b'\t',1);mode,kind,oid=meta.decode().split()
            entries[os.fsdecode(name)]=(mode,kind,oid)
    index={}
    for r in git(repo,'ls-files','--stage','-z').split(b'\0'):
        if r:
            meta,name=r.split(b'\t',1);mode,oid,stage=meta.decode().split()
            assert stage=='0'
            index[os.fsdecode(name)]=(mode,oid)
    assert index=={n:(m,o) for n,(m,k,o) in entries.items()},label+' index mismatch'
    count=0
    for name,(mode,kind,oid) in entries.items():
        if kind=='commit':continue
        f=repo/name;s=f.lstat()
        if mode=='120000':
            assert stat.S_ISLNK(s.st_mode),name
            b=os.fsencode(os.readlink(f))
        else:
            assert stat.S_ISREG(s.st_mode),name
            assert bool(s.st_mode&0o111)==(mode=='100755'),name
            b=f.read_bytes()
        assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==oid,name
        count+=1
    assert git(repo,'rev-parse','HEAD').decode().strip()==revision
    return dict(repository=label,head=revision,tree=git(repo,'rev-parse',revision+'^{tree}').decode().strip(),tracked_blobs=count,index_matches=True,bytes_and_modes_match=True),entries
head='2263c6288956a5edd841df62252326780edd4870'
first,entries=inspect(root,head,'candidate')
assert first['tree']=='04234de69a17538c76eff84e001cb4ec2c742a04'
results=[first]
for name in ('protocol-processor','gptp-processor','third_party/verilog-axis'):
    mode,kind,pin=entries[name];assert mode=='160000' and kind=='commit'
    sub=root/name
    assert (sub/'.git').is_file()
    assert Path(git(sub,'rev-parse','--show-superproject-working-tree').decode().strip()).resolve()==root
    r,_=inspect(sub,pin,name);r['registered_submodule']=True;results.append(r)
changed=git(root,'diff','--name-only','fa450d301805881ad713b67521477bf042ddadfd..'+head).decode().splitlines()
assert changed==['docs/findings/653_DISCONNECT_ORDER_BENCH.md']
print(json.dumps(dict(passed=True,repositories=results,changed_paths=changed,external='not initialized; outside required three-submodule population'),indent=2))
