#!/usr/bin/env python3
"""Prove raw tracked bytes, modes, index and required gitlinks. Usage: REPO PACKET."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

repo, packet = (Path(x).resolve() for x in sys.argv[1:3])
os.environ['GIT_NO_REPLACE_OBJECTS'] = '1'
head = '66b4def34dcbc0d371ce4eb339d3d0226875befa'
tree = 'b5bba478993ff213d953aa73ca5fecc8d5476c8a'
def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args])
def prove(root, revision):
    expected = {}
    for entry in git(root, 'ls-tree', '-rz', revision).split(b'\0'):
        if entry:
            header, name = entry.split(b'\t',1)
            mode, kind, oid = header.split()
            expected[name] = (mode, kind, oid)
    actual = {}
    for entry in git(root, 'ls-files', '--stage', '-z').split(b'\0'):
        if entry:
            header,name = entry.split(b'\t',1)
            mode,oid,stage = header.split()
            assert stage == b'0' and name not in actual, (root.name, name, stage)
            actual[name] = (mode,oid)
    assert actual == {n:(m,o) for n,(m,k,o) in expected.items()}, root.name+' index mismatch'
    count = 0
    links = {}
    for name,(mode,kind,oid) in expected.items():
        path = root/os.fsdecode(name)
        if mode == b'160000':
            links[os.fsdecode(name)] = oid.decode()
            continue
        st = path.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(st.st_mode)
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(st.st_mode), str(path.relative_to(root))
            assert bool(st.st_mode & 0o111) == (mode == b'100755'), str(path.relative_to(root))
            data = path.read_bytes()
        actual_oid = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert actual_oid == oid.decode(), str(path.relative_to(root))
        count += 1
    flags = git(root,'ls-files','-v','-z').split(b'\0')
    assert all(not r or (not chr(r[0]).islower() and r[0:1] != b'S') for r in flags)
    return dict(revision=revision, blob_count=count, gitlinks=links, bytes_modes_index='exact', hidden_flags=0)
assert git(repo,'rev-parse','HEAD').decode().strip() == head
assert git(repo,'rev-parse','HEAD^{tree}').decode().strip() == tree
result = dict(head=head,tree=tree,parent=prove(repo,head),submodules={})
for name in ('protocol-processor','gptp-processor','third_party/verilog-axis','third_party/tsn-c-stack','third_party/lwSRP'):
    pin = result['parent']['gitlinks'][name]
    sub = repo/name
    assert sub.is_dir() and not sub.is_symlink() and (sub/'.git').is_file(), name
    assert git(sub,'rev-parse','HEAD').decode().strip() == pin, name
    assert Path(git(sub,'rev-parse','--show-superproject-working-tree').decode().strip()).resolve() == repo, name
    result['submodules'][name] = prove(sub,pin)
result['status'] = git(repo,'status','--porcelain=v1').decode()
assert result['status'] == ''
result['external'] = 'Unchanged gitlink, uninitialized; not a required test input.'
packet.joinpath('integrity-result.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS exact HEAD and tree; parent blobs:', result['parent']['blob_count'])
for name,rec in result['submodules'].items():
    print('PASS',name,rec['revision'],'blobs:',rec['blob_count'])
print('PASS raw bytes/modes/index; no hidden flags; tracked status clean')
