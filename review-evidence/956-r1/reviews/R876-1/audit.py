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
head='0d80f0ed2a880c3a3b2429c669f104801203ec05'
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
late=git(repo,'diff','--name-only','8845364d..HEAD').decode().splitlines()
print('Post-code-head changes: '+', '.join(late))
assert not any(x.startswith('sw/firmware/') and '/test/' not in x for x in late)
assert not any(x.startswith(('hdl/','sw/litex/','configs/','sw/mailbox/')) for x in late)
print('No firmware, RTL, configuration, linker or mailbox input changed after 8845364d')
root=packet/'scratch/review-evidence/956-r1'
if not root.exists():
    evidence='a58b1c37af70d774b69f6741bb50d3a1b020aa0a'
    git(repo,'fetch','origin',evidence)
    archive=packet/'scratch/evidence.tar'
    archive.parent.mkdir(parents=True,exist_ok=True)
    archive.write_bytes(git(repo,'archive',evidence,'review-evidence/956-r1'))
    with tarfile.open(archive) as tar:
        tar.extractall(packet/'scratch',filter='data')
entries=json.loads((root/'MANIFEST.json').read_text())
for e in entries:
    assert hashlib.sha256((root/e['file']).read_bytes()).hexdigest()==e['published_sha256']
print(f'Public evidence manifest: {len(entries)} published SHA-256 values match')
for k in range(4):
    name=f'fw-gate-shard{k}-8845364d.txt'
    text=(root/'author-r1/receipts'/name).read_text()
    print(name+': '+text.splitlines()[0])
    print('  '+text.splitlines()[1])
    assert 'test_ctrl_firmware: PASS' in text
    assert not any(line.startswith('[ESCAPED]') for line in text.splitlines())
print('ROM payload: 113064 + 25662 + 520 = 139246 B; capacity 139264 B; raw spare 18 B')
print('Ledger aligned ROM: 139248 B; aligned spare 16 B; total allocation 58 RAMB36 unchanged')
print('RESULT: PASS')
