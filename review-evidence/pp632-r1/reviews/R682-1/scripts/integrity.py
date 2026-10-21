#!/usr/bin/env python3
"""Verify tracked bytes, modes, indexes and the consumer's required gitlinks."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import sys
p=Path(__file__).resolve().parents[1]
root=Path(sys.argv[1]).resolve()
def git(repo,*args):
    return subprocess.check_output(['git','-C',str(repo),*args])
def audit(repo):
    assert not git(repo,'diff','--raw')
    assert not git(repo,'diff','--cached','--raw')
    n=0; links={}
    for row in filter(None,git(repo,'ls-files','--stage','-z').split(b'\0')):
        attrs,name=row.split(b'\t',1)
        mode,oid,stage=attrs.decode().split(); assert stage=='0'
        path=repo/name.decode()
        if mode=='160000':
            links[name.decode()]=oid; continue
        raw=path.readlink().as_posix().encode() if mode=='120000' else path.read_bytes()
        assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==oid,name
        if mode!='120000': assert bool(path.stat().st_mode & 0o111)==(mode=='100755'),name
        n+=1
    return {'head':git(repo,'rev-parse','HEAD').decode().strip(),'tree':git(repo,'rev-parse','HEAD^{tree}').decode().strip(),'verified_tracked_blobs_and_modes':n,'gitlinks':links,'status':git(repo,'status','--short').decode()}
result={'time_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'processor':audit(root)}
assert result['processor']['head']=='51f88c7e14e7e2527c09ff9a23b93dd6b857fd50'
assert result['processor']['tree']=='438b7967df80fabeef960173e28bc1334de30cec'
parent=p/'scratch/parent'
result['consumer']=audit(parent)
assert result['consumer']['head']=='32fb8fc26acf7dedc507512d7a455898a26afd84'
result['required_submodules']={}
for name in ('protocol-processor','gptp-processor','third_party/verilog-axis','third_party/tsn-c-stack'):
    item=audit(parent/name)
    assert item['head']==result['consumer']['gitlinks'][name]
    assert not item['status'],item
    result['required_submodules'][name]=item
assert not result['processor']['status'] and not result['consumer']['status']
rom=(parent/'tb/verilator/milan_dp/ucode.hex').read_bytes()
assert hashlib.sha256(rom).hexdigest()=='518b900c4a5650902c3ea9125941e434857ba2f379b6c92268a67fef459d37f8'
result['consumer_runtime_ROM_restored_sha256']=hashlib.sha256(rom).hexdigest()
cg=Path('/sys/fs/cgroup')/Path('/proc/self/cgroup').read_text().strip().split(':',2)[2].lstrip('/')
result['resource_record']={name:(cg/name).read_text().strip() for name in ('memory.max','memory.peak','memory.events')}
(p/'receipts/final-integrity.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
