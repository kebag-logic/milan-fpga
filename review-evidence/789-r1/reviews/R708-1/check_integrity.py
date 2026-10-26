#!/usr/bin/env python3
"""Verify raw tracked bytes, modes, index entries and required gitlinks."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
out = Path(__file__).resolve().parent
env = {**os.environ, 'GIT_NO_REPLACE_OBJECTS':'1'}
def git(where, *args):
    return subprocess.check_output(['git',*args],cwd=where,env=env)
def verify(where, ref, label):
    entries = git(where,'ls-tree','-rz',ref).split(b'\0')
    tree = {}
    count = 0
    links = {}
    for entry in entries:
        if not entry:
            continue
        header,raw = entry.split(b'\t',1)
        mode,kind,oid = header.decode().split()
        name = os.fsdecode(raw)
        tree[raw] = (mode,oid,'0')
        path = where / name
        if kind == 'commit':
            links[name] = oid
            continue
        info = path.lstat()
        if mode == '120000':
            assert stat.S_ISLNK(info.st_mode), (label,name,'not symlink')
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(info.st_mode), (label,name,'not regular')
            actual_mode = '100755' if info.st_mode & 0o111 else '100644'
            assert mode == actual_mode, (label,name,'mode')
            data = path.read_bytes()
        got = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert got == oid, (label,name,'blob bytes')
        count += 1
    index = {}
    for entry in git(where,'ls-files','--stage','-z').split(b'\0'):
        if entry:
            header,name = entry.split(b'\t',1)
            index[name] = tuple(header.decode().split())
    assert tree == index, (label,'index differs from committed tree')
    print(json.dumps({'repository':label,'revision':ref,'blobs_verified':count,
                      'index_and_modes':'PASS','gitlinks':links},sort_keys=True))
    return links

head = git(root,'rev-parse','HEAD').decode().strip()
assert head == 'fddf3671ebc96a953755fa1b9a3ecec5f071a350'
assert git(root,'rev-parse','HEAD^{tree}').decode().strip() == 'd758e8963591f123d3398719f0a331f9cc9bbf91'
assert subprocess.run(['git','symbolic-ref','-q','HEAD'],cwd=root,env=env,capture_output=True).returncode == 1
links = verify(root,head,'candidate')
for sub in ['protocol-processor','gptp-processor','third_party/verilog-axis','third_party/tsn-c-stack']:
    where = root/sub
    assert (where/'.git').is_file(), (sub,'not registered submodule')
    assert git(where,'rev-parse','HEAD').decode().strip() == links[sub], (sub,'pin')
    verify(where,links[sub],sub)
assert not git(root,'status','--porcelain=v1','--untracked-files=all').strip()
manifest = json.loads((out/'public/evidence-manifest.json').read_text())
checked = 0
for entry in manifest:
    path = out/'public'/entry['file']
    if path.is_file():
        assert hashlib.sha256(path.read_bytes()).hexdigest() == entry['published_sha256'], entry['file']
        checked += 1
print('Public receipt hashes matched:',checked)
print('Exact head/tree, raw tracked bytes/modes/index, required submodule pins and bytes: PASS')
