#!/usr/bin/env python3
"""Prove tracked bytes, modes, indexes and required gitlinks against exact objects."""
import hashlib, json, os, stat, subprocess, sys
from pathlib import Path
repo, output = map(Path, sys.argv[1:3])
HEAD = '220b51f2eb50c32f830e0b5a8ee1ce138b218bb6'
env = dict(os.environ,GIT_NO_REPLACE_OBJECTS='1')
def git(root,*args):
    return subprocess.check_output(['git','-C',str(root),*args],env=env)
def verify(root,rev):
    tree = git(root,'ls-tree','-rz',rev)
    expected_index, count, links, errors = [], 0, {}, []
    for entry in tree.split(b'\0'):
        if not entry: continue
        meta, raw_path = entry.split(b'\t',1)
        mode, kind, oid = meta.split()
        path = os.fsdecode(raw_path)
        expected_index.append(mode+b' '+oid+b' 0\t'+raw_path)
        if kind == b'commit':
            links[path] = oid.decode()
            continue
        p = root/path
        try:
            st = p.lstat()
            if mode == b'120000':
                assert stat.S_ISLNK(st.st_mode)
                data = os.fsencode(os.readlink(p))
            else:
                assert stat.S_ISREG(st.st_mode)
                assert bool(st.st_mode & 0o111) == (mode == b'100755')
                data = p.read_bytes()
            actual = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
            assert actual == oid.decode()
            count += 1
        except (AssertionError,OSError) as e:
            errors.append({'path':path,'error':str(e) or 'bytes/mode mismatch'})
    actual_index = git(root,'ls-files','-sz').split(b'\0')
    assert sorted(x for x in actual_index if x) == sorted(expected_index), 'index mismatch'
    assert not errors, errors
    return {'revision':rev,'tracked_blobs_verified':count,'index_matches':True,'errors':errors,'gitlinks':links}
assert git(repo,'rev-parse','HEAD').decode().strip() == HEAD
result = {'parent':verify(repo,HEAD),'submodules':{}}
for path in ['protocol-processor','gptp-processor','third_party/verilog-axis','third_party/tsn-c-stack','third_party/lwSRP']:
    pin = result['parent']['gitlinks'][path]
    assert (repo/path/'.git').is_file(), path
    assert git(repo/path,'rev-parse','HEAD').decode().strip() == pin
    result['submodules'][path] = verify(repo/path,pin)
result['tree'] = git(repo,'rev-parse','HEAD^{tree}').decode().strip()
assert result['tree'] == 'a4bc2ed645a1cc426a2e83d1773c3c5e2ccb5405'
result['status'] = git(repo,'status','--porcelain=v1').decode()
assert not result['status']
output.write_text(json.dumps(result,indent=2)+'\n')
print('PASS: parent and five initialized submodules match tracked bytes, modes, indexes and gitlinks')
