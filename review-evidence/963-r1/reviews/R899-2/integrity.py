#!/usr/bin/env python3
"""Check tracked bytes, file kinds/modes, index and required gitlinks.
Usage: python3 integrity.py CHECKOUT
"""
import hashlib
import json
import os
import stat
import subprocess
import sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')
def git(path, *args):
    return subprocess.check_output(['git','-C',str(path),*args],env=env)
def check(path, rev):
    entries = git(path,'ls-tree','-rz',rev).split(b'\0')
    expected = []
    count = 0
    links = {}
    for entry in filter(None,entries):
        meta, name = entry.split(b'\t',1)
        mode, kind, oid = meta.split()
        expected.append(mode+b' '+oid+b' 0\t'+name)
        p = path / os.fsdecode(name)
        if kind == b'commit':
            links[os.fsdecode(name)] = oid.decode()
            continue
        s = p.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(s.st_mode), str(p)
            data = os.fsencode(os.readlink(p))
        else:
            assert stat.S_ISREG(s.st_mode), str(p)
            assert bool(s.st_mode & 0o111) == (mode == b'100755'), str(p)
            data = p.read_bytes()
        actual = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert actual == oid.decode(), str(p)
        count += 1
    index = list(filter(None,git(path,'ls-files','--stage','-z').split(b'\0')))
    assert sorted(index) == sorted(expected), 'index mismatch'
    assert git(path,'rev-parse','HEAD').decode().strip() == rev
    return {'head':rev, 'tracked_blobs_verified':count,'index_and_modes':'exact', 'gitlinks':links}
head='a18f0996f4b1b654a232dfe56fa64ee7ecaf697e'
r = {'superproject':check(root,head)}
assert git(root,'rev-parse','HEAD^{tree}').decode().strip() == 'a897a1e08c1cd4b63c37b0e5625b819d4649d568'
r['required_submodules'] = {}
for name in ['protocol-processor','gptp-processor','third_party/verilog-axis','third_party/tsn-c-stack','third_party/lwSRP']:
    r['required_submodules'][name] = check(root/name,r['superproject']['gitlinks'][name])
r['status'] = git(root,'status','--porcelain').decode()
print(json.dumps(r,indent=2))
