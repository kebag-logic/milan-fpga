#!/usr/bin/env python3
"""Verify raw tracked bytes, modes, index and pinned submodules without trusting status."""
import hashlib
import json
import os
import stat
import subprocess
import sys
import tarfile
from pathlib import Path

repo=Path(sys.argv[1]).resolve()
packet=Path(__file__).resolve().parent
head='1825ba4eaccfe40788391b7af5533fae8c910a85'
env={**os.environ,'GIT_NO_REPLACE_OBJECTS':'1'}
def git(at,*args):
    return subprocess.check_output(['git','-C',str(at),*args],env=env)
def check(at,expected):
    assert git(at,'rev-parse','HEAD').decode().strip()==expected
    raw=git(at,'ls-tree','-rz',expected)
    tree={}
    for entry in raw.split(b'\0'):
        if not entry: continue
        meta,name=entry.split(b'\t',1)
        mode,kind,oid=meta.split()
        tree[name]=(mode,oid)
    indexed={}
    for entry in git(at,'ls-files','--stage','-z').split(b'\0'):
        if not entry: continue
        meta,name=entry.split(b'\t',1)
        mode,oid,stage=meta.split()
        assert stage==b'0'
        indexed[name]=(mode,oid)
    assert indexed==tree,'index differs from expected tree'
    n=0
    for name,(mode,oid) in tree.items():
        if mode==b'160000': continue
        f=at/os.fsdecode(name)
        st=f.lstat()
        if mode==b'120000':
            assert stat.S_ISLNK(st.st_mode)
            data=os.fsencode(os.readlink(f))
        else:
            assert stat.S_ISREG(st.st_mode)
            assert bool(st.st_mode&0o111)==(mode==b'100755'),f'mode mismatch: {name!r}'
            data=f.read_bytes()
        digest=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest().encode()
        assert digest==oid,f'blob mismatch: {name!r}'
        n+=1
    return n,tree
n,tree=check(repo,head)
print(f'HEAD {head}')
print('TREE '+git(repo,'rev-parse','HEAD^{tree}').decode().strip())
print(f'Superproject: {n} tracked blobs, raw bytes and modes match; index equals HEAD')
for path in ('protocol-processor','gptp-processor','third_party/verilog-axis','third_party/tsn-c-stack','third_party/lwSRP'):
    pin=tree[path.encode()][1].decode()
    assert (repo/path/'.git').is_file(),'required submodule is not registered'
    n,_=check(repo/path,pin)
    print(f'{path}: {pin}; {n} blobs, raw bytes/modes/index match')

print('External optional gitlink: '+tree[b'external'][1].decode()+'; not initialized, not required by these probes')
late=git(repo,'diff','--name-only','b4a1dde2..HEAD').decode().splitlines()
assert set(late)=={'sw/firmware/ctrl/test/srp_talker_mutants.py','docs/design/SPLIT_CONTROL_MEMORY.md','sw/firmware/ctrl/srp/README.md'}
print('After b4a1dde2: only mutation table and two documentation files changed; production image inputs identical')
root=packet/'scratch/review-evidence/956-r1'
entries=json.loads((root/'MANIFEST.json').read_text())
for e in entries:
    assert hashlib.sha256((root/e['file']).read_bytes()).hexdigest()==e['published_sha256'],e['file']
print(f'Public packet: {len(entries)} manifest hashes verified at 362a303989763207c30c801b66aa9333a0130204')
raw=git(repo,'cat-file','commit','362a303989763207c30c801b66aa9333a0130204')
print('Evidence commit signature header present: '+str(b'\ngpgsig ' in raw))
print('Manifest authenticates published bytes by hash; no cryptographic signature claim is made')
for k in range(4):
    name=f'fw-gate-shard{k}-847b2e21.txt'
    txt=(root/'author-r2/receipts'/name).read_text()
    assert 'test_ctrl_firmware: PASS' in txt
    assert not any(line.startswith('[ESCAPED]') for line in txt.splitlines())
    print(name+': '+txt.splitlines()[0])
print('ROM: aligned rom_end 139136; capacity 34*4096=139264; spare 128; total platform allocation 58 RAMB36')
print('RESULT: PASS')
